from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"


db=SQLAlchemy(app)

class Home(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    category = db.Column(db.String(80))
    subject = db.Column(db.String(80))
    


@app.route("/" , methods=["GET","POST"])
def index():
    #print(request.method)
    if request.method == "POST":
        name = request.form["name"]
        category = request.form["category"]
        subject = request.form["subject"]
        
       

        form = Home(
        name=name,
        category=category,
        subject=subject
        )

        db.session.add(form)
        db.session.commit()

        return "Data inserted successfully"

    return "Use POST to insert data"



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug= True, port =5002)