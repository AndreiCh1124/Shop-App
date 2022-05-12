from flask import Flask, request, jsonify, render_template
from random import choice, randint

app = Flask(__name__)

inventory_mixed = list()
inventory_general = ["Milk", "Orange juice", "Water", "Limonade", "Coffe"]
inventory_food = ["Bread", "Beef", "Apples", "Oats", "Pork"]
inventory_alcohol = ["Beer", "Whiskey", "Wine", "Vodka", "Champagne"]
inventory_vegetables = ["Carrot", "Tomato", "Horseradish", "Ginger", "Garlic"]

def pick_items(inv_list, inventory_mixed):
    pick = choice(inv_list)
    while pick in inventory_mixed:
        pick = choice(inv_list)
    inventory_mixed.append(pick)
    return inventory_mixed

for idx in range(randint(2, 3)):
    pick_items(inventory_general, inventory_mixed)
    pick_items(inventory_alcohol, inventory_mixed)
    pick_items(inventory_food, inventory_mixed)
    pick_items(inventory_vegetables, inventory_mixed)

inventory = {
    "items": inventory_mixed
}

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/inventory")
def inventory_items():
    return jsonify({"items": f"Here is a list of all the available products: {', '.join(inventory['items'])}."})


@app.route("/shop", methods=["POST"])
def shop():
    shopping_list = request.form["shoppingList"]
    shopping_list = shopping_list.split(", ")
    waiting_time = f"Great choice, you will have to wait {len(shopping_list)} minutes for your product."
    return jsonify({"time": waiting_time})

@app.route("/echo-page", methods=["POST"])
def echo_page():
    data = request.form["message"]
    return render_template("echo_template.html", foo = str(data).upper())


@app.route("/echo", methods=["POST"])
def echo():
    return str(request.form["message"]).upper()


@app.route("/items")
def items():
    response = inventory["items"]
    if response is None:
        return render_template("items.html")
    else:
        return render_template("items.html", items=response)


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