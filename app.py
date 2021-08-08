from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(35))
    email = db.Column(db.String(120))
    current_balance = db.Column(db.Float, default=5000)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return "<Customer %r>" % self.id


class Transfers(db.Model):
    __tablename__ = "transfers"
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    amount = db.Column(db.Float, default=0)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return "<Transaction %r>" % self.id


@app.route("/")
def index():
    # if request.method == "POST":
    #     name = request.form["name"]
    #     email = request.form["email"]
    #     balance = request.form["balance"]
    #     new_customer = Customer(name=name, email=email, current_balance=balance)
    #     try:
    #         db.session.add(new_customer)
    #         db.session.commit()
    #         return redirect(url_for("index"))
    #     except:
    #         return "There was an issue adding that customer"
    # else:
    #     customers = Customer.query.order_by(Customer.date_created).all()
    return render_template("index.html")


@app.route("/view_all")
def view_all():
    customers = Customer.query.order_by(Customer.date_created).all()
    return render_template("view_all.html", customers=customers)


@app.route("/payment/<int:cust_id>", methods=["POST", "GET"])
def payment(cust_id):
    user = Customer.query.get_or_404(cust_id)
    customers = Customer.query.filter(Customer.id != cust_id)
    if request.method == "POST":

        customer_id = request.form["customer"]
        customer = Customer.query.get_or_404(customer_id)
        amount = float(request.form["amount"])
        balance = user.current_balance
        if amount >= balance or balance < 500:
            return render_template(
                "payment.html",
                user=user,
                context="Enter a valid amount",
            )
        customer.current_balance = customer.current_balance + amount
        user.current_balance = user.current_balance - amount
        new_transaction = Transfers(
            sender_id=user.id, receiver_id=customer_id, amount=amount
        )
        try:
            db.session.add(new_transaction)
            db.session.commit()
            return redirect(url_for("view_all"))
        except:
            return "There was an issue with tranfersing that amount"

    return render_template("payment.html", user=user, customers=customers)


@app.route("/transactions")
def transactions():
    all_transactions = Transfers.query.order_by(Transfers.transaction_date.desc()).all()

    return render_template("transactions.html", transactions=all_transactions)


if __name__ == "__main__":
    app.run(debug=True)
