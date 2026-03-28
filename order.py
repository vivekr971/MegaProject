from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:vivek%40123@localhost:3306/serviceapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

getcust_url = "http://127.0.0.1:6001/all_customer"
# get_unique_url = "http://127.0.0.1:6001/all_customer"

db=SQLAlchemy(app)

class Orders(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    unique_id = db.Column(db.Integer, nullable=False)
    total_order = db.Column(db.Integer)
    amount_spent = db.Column(db.Integer)
    discount = db.Column(db.Integer)


    items = db.relationship('OrderItems', backref='order', lazy=True)


class OrderItems(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)

@app.route("/order-customer" , methods=["POST"])
def index():
        data = request.get_json()

        if not data:
            return {"error": "Invalid JSON"}, 400

        unique_id = data.get("unique_id")
        total_order = data.get("total_order")
        amount_spent = data.get("amount_spent")
        discount = data.get("discount")

        if not all([unique_id, total_order, amount_spent]):
             return {"error": "Missing required fields"}, 400

        
        response= requests.get(getcust_url)
        
        customers = response.json()

        if not any(c["unique_id"] == unique_id for c in customers):
            return {"error": "Customer not found"}, 404
        

        
        if not (1000 <= amount_spent <= 10000):
             return {"error": "amount_spent must be between 1000 and 10000"}, 400

        ord1= Orders(
        unique_id = unique_id,
        total_order = total_order,
        amount_spent = amount_spent,
        discount = discount
)


        db.session.add(ord1)
        db.session.commit()

        return {"message": "Order created successfully"}, 201



@app.route("/create_order", methods=["GET"])
def get_cust():
    response2= requests.get(getcust_url)
    data= response2.json()
    return jsonify(data)






if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug= True, port =6002)