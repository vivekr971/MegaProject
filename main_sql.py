from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:vivek%40123@localhost:3306/serviceapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    email = db.Column(db.String(100))
    unique_id = db.Column(db.Integer, unique=True, nullable=False)

@app.route("/create-customer" , methods=["POST"])
def index():
        
        name = request.json["name"]
        category = request.json["category"]
        email = request.json["email"]
        unique_id = request.json["unique_id"]
        
            # Check mandatory field
        if not unique_id:
            return "unique_id is required", 400
        
        try:
             unique_id = int(unique_id)
        except:
             return "unique_id must be an integer", 400

        # Check duplicate
        existing = Customer.query.filter_by(unique_id=unique_id).first()
        if existing:
            return "unique_id already exists", 400
        
        cust= Customer(
        name=name,
        category=category,
        email=email,
        unique_id=unique_id,
        )

        db.session.add(cust)
        db.session.commit()

        return "Data inserted successfully"

@app.route("/all_customer", methods=["GET"])
def get_all():
    data = Customer.query.all()

    result =[]

    for item in data:
        result.append({
            "id": item.id,
            "unique_id": item.unique_id,
            "name": item.name,
            "category": item.category,
            "email": item.email
        })

    return jsonify (result)

@app.route("/unique_id/<int:unique_id>", methods=["GET"])
def get_customer(unique_id):

    customer2 = Customer.query.filter_by(unique_id=unique_id).first()

    # If not found
    if not customer2:
        return {"error": "Customer not found"}, 404

    # If found
    result = {
        "name": customer2.name
    }

    return jsonify(result)



@app.route("/delete_id/<int:unique_id>", methods=["DELETE"])
def del_customer(unique_id):
     customer3 = Customer.query.filter_by(unique_id=unique_id).first()
     
     if customer3:
         db.session.delete(customer3)
         db.session.commit()
         
         return jsonify({"message": "Customer deleted successfully"})
         
     else:
          return jsonify({"message": "Customer not found"}), 404
     

     
@app.route("/update_id/<int:unique_id>", methods=["PUT"])
def update_customer(unique_id):
     customer4 = Customer.query.filter_by(unique_id=unique_id).first()
     
     if not customer4:
        return {"message": "Not found"}, 404

     data = request.get_json()

     customer4.name = data.get('name', customer4.name)

     db.session.commit()

     return {"message": "Updated"}, 200
         
         
         
       



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug= True, port =6001)
