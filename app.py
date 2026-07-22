"""
Flask REST API for Inventory Management System.
"""

from flask import Flask, jsonify, request

import inventory

print("Inventory module loaded from:")
print(inventory.__file__)

from inventory import (
    get_all_items,
    get_item_by_id,
    add_item,
    update_item,
    delete_item
)

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({
        "message": "Inventory Management API is running!"
    })


# GET all inventory
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(get_all_items()), 200


# GET one item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):

    item = get_item_by_id(item_id)

    if item:
        return jsonify(item), 200

    return jsonify({
        "error": "Item not found"
    }), 404


# POST new item
@app.route("/inventory", methods=["POST"])
def create_item():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received."
        }), 400

    required_fields = [
        "name",
        "brand",
        "price",
        "stock",
        "barcode"
    ]

    for field in required_fields:
        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

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


# PATCH item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def edit_item(item_id):

    updates = request.get_json()

    if not updates:
        return jsonify({
            "error": "No update data provided."
        }), 400

    updated = update_item(item_id, updates)

    if updated:
        return jsonify(updated), 200

    return jsonify({
        "error": "Item not found"
    }), 404


# DELETE item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def remove_item(item_id):

    deleted = delete_item(item_id)

    if deleted:
        return jsonify({
            "message": "Item deleted successfully."
        }), 200

    return jsonify({
        "error": "Item not found"
    }), 404


if __name__ == "__main__":
    app.run(debug=True)