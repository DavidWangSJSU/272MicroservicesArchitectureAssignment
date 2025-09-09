from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

orders = {
    1: {"user_id": 1, "product": "Laptop"},
    2: {"user_id": 2, "product": "Smartphone"}
}

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Enrich with user info from User Service
    try:
        resp = requests.get(f"http://localhost:5001/users/{order['user_id']}", timeout=2)
        if resp.status_code == 200:
            order = {**order, "user": resp.json()}
    except requests.RequestException:
        pass
    return jsonify(order)

@app.route("/orders", methods=["POST"])
def create_order():
    new_order = request.json or {}
    order_id = (max(orders.keys()) + 1) if orders else 1
    orders[order_id] = new_order
    return jsonify({"order_id": order_id}), 201

if __name__ == "__main__":
    app.run(port=5002)
