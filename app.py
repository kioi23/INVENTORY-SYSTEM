# Import Flask and helper functions
from flask import Flask, jsonify, request

# Import functions from inventory.py
from inventory import (
    get_all_items,
    get_item_by_id,
    add_item,
    update_item,
    delete_item
)

# Create the Flask application
app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API is running!"
    })

# Returns every product in the inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():

    return jsonify(get_all_items())

# Returns a single product in the inventory by its ID
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):

    item = get_item_by_id(item_id)

    if item:
        return jsonify(item)

    return jsonify({"error": "Item not found"}), 404

# create new products in the inventory
@app.route("/inventory", methods=["POST"])
def create_item():

    data = request.get_json()

    new_item = {
        "id": len(get_all_items()) + 1,
        "name": data["name"],
        "brand": data["brand"],
        "price": data["price"],
        "stock": data["stock"],
        "barcode": data["barcode"]
    }

    add_item(new_item)

    return jsonify(new_item), 201

# update a product in the inventory
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def edit_item(item_id):

    updates = request.get_json()

    updated = update_item(item_id, updates)

    if updated:
        return jsonify(updated)

    return jsonify({"error": "Item not found"}), 404

# delete a product in the inventory
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):

    deleted = delete_item(item_id)

    if deleted:
        return jsonify({
            "message": "Item deleted successfully."
        })

    return jsonify({
        "error": "Item not found"
    }), 404

if __name__ == "__main__":
    app.run(debug=True)