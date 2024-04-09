from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/flaskApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Transaction model
class TransactionData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    sender = db.Column(db.String(50), nullable=False)
    receiver = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'date': self.date,
            'amount': self.amount,
            'sender': self.sender,
            'receiver': self.receiver
        }

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'balance': self.balance
        }

# Resource classes
class TransactionList(Resource):
    def get(self):
        transactions = TransactionData.query.all()
        transaction_list = [trans.serialize() for trans in transactions]
        return jsonify(transaction_list)

    def post(self):
        data = request.json
        new_transaction = TransactionData(date=data['date'], amount=data['amount'],
                                          sender=data['sender'], receiver=data['receiver'])
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify(new_transaction.serialize()), 201

class Transaction(Resource):
    def get(self, transaction_id):
        transaction = TransactionData.query.get_or_404(transaction_id)
        return jsonify(transaction.serialize())

    def put(self, transaction_id):
        transaction = TransactionData.query.get_or_404(transaction_id)
        data = request.json
        for key, value in data.items():
            setattr(transaction, key, value)
        db.session.commit()
        return jsonify(transaction.serialize())

    def delete(self, transaction_id):
        transaction = TransactionData.query.get_or_404(transaction_id)
        db.session.delete(transaction)
        db.session.commit()
        return '', 204

class SendMoney(Resource):
    def post(self):
        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')
        amount = data.get('amount')
        if not sender or not receiver or not amount:
            return {'error': 'Missing required fields'}, 400
        
        # Fetch sender's and receiver's balances from the database
        sender_account = User.query.filter_by(username=sender).first()
        receiver_account = User.query.filter_by(username=receiver).first()
        
        # Checking if sender or receiver does not exist
        if not sender_account or not receiver_account:
            return {'error': 'Sender or receiver does not exist'}, 400
        
        sender_balance = sender_account.balance
        receiver_balance = receiver_account.balance
        
        # Checking if sender has sufficient balance
        if sender_balance < amount:
            return {'error': 'Insufficient balance'}, 400

        # Updating sender's and receiver's balances in the database
        sender_account.balance -= amount
        receiver_account.balance += amount
        db.session.commit()

        # Creating a new transaction
        new_transaction = TransactionData(date=data['date'], amount=amount,
                                          sender=sender, receiver=receiver)
        db.session.add(new_transaction)
        db.session.commit()
        return new_transaction.serialize(), 201

api.add_resource(TransactionList, '/transactions')
api.add_resource(Transaction, '/transactions/<int:transaction_id>')
api.add_resource(SendMoney, '/send-money')

if __name__ == '__main__':
    app.run(debug=True)
