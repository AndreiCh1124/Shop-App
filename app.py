from flask import Flask, request, jsonify, render_template
from random import choice

app = Flask(__name__)

inventory_mixed = list()
inventory_general = ["Milk", "Orange juice", "Water", "Lemonade", "Coffee"]
inventory_food = ["Bread", "Beef", "Apples", "Oats", "Pork"]
inventory_alcohol = ["Beer", "Whiskey", "Wine", "Vodka", "Champagne"]
inventory_vegetables = ["Carrot", "Tomato", "Horseraddish", "Ginger", "Garlic"]

def pick_items(inv_list, inventory_mixed):
    pick = choice(inv_list)
    while pick in inventory_mixed:
        pick = choice(inv_list)
    inventory_mixed.append(pick)
    return inventory_mixed

for idx in range(3):
    pick_items(inventory_general, inventory_mixed)
    pick_items(inventory_alcohol, inventory_mixed)
    pick_items(inventory_food, inventory_mixed)
    pick_items(inventory_vegetables, inventory_mixed)

inventory = {
    "items1": [inventory_mixed[0], inventory_mixed[1], inventory_mixed[2], inventory_mixed[3]],
    "items2": [inventory_mixed[4], inventory_mixed[5], inventory_mixed[6], inventory_mixed[7]],
    "items3": [inventory_mixed[8], inventory_mixed[9], inventory_mixed[10], inventory_mixed[11]]
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/inventory")
def inventory_items():
    return jsonify({"items": f"Here is a list of all the available products: {', '.join(inventory['items1'])}, \
        {', '.join(inventory['items2'])}, {', '.join(inventory['items3'])}."})
            


@app.route("/shop", methods=["POST"])
def shop():
    invalid_items = list()
    shopping_list = request.form["shoppingList"]
    shopping_list = shopping_list.split(", ")
    if str(shopping_list[0]) == "":
        message_text = "Please insert an item !!!"
        return jsonify({"time": message_text})
    for item in shopping_list:
        if str(item).capitalize() not in inventory_mixed:
            invalid_items.append(item)
    if len(invalid_items) != 0:
        items = ", ".join(invalid_items)
        message_text = f"The following items are not avalibale: {items}"
        return jsonify({"time": message_text})
    else:
        message_text = f"Great choice, you will have to wait {len(shopping_list)} minutes for your product."
        return jsonify({"time": message_text})

@app.route("/echo-page", methods=["POST"])
def echo_page():
    data = request.form["message"]
    return render_template("echo_template.html", foo = str(data).upper())


@app.route("/echo", methods=["POST"])
def echo():
    return str(request.form["message"]).upper()


@app.route("/items")
def items():
    response = inventory["items1"] + inventory["items2"] + inventory["items3"]
    print(response)
    if response is None:
        return render_template("items.html")
    else:
        return render_template("items.html", items1=response[0:4], items2=response[4:8], items3=response[8:12])


@app.route("/math", methods=["POST"])
def math():
    data = request.form
    response = {
        "sum": int(data["foo"]) + int(data["bar"]),
        "mul": int(data["foo"]) * int(data["bar"])
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)