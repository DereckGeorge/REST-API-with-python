from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

transactions = [
    {"id": 1, "date": "2024-04-06", "amount": 100.0, "sender": "Dereck", "receiver": "Ashirafu"},
    {"id": 2, "date": "2024-04-06", "amount": 50.0, "sender": "Ashirafu", "receiver": "Dereck"},
]

class TransactionList(Resource):
    def get(self):
        return jsonify(transactions)

    def post(self):
        new_transaction = request.json
        transactions.append(new_transaction)
        return jsonify(new_transaction), 201

class Transaction(Resource):
    def get(self, transaction_id):
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                return jsonify(transaction)
        return jsonify({'error': 'Transaction not found'}), 404

    def put(self, transaction_id):
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction.update(request.json)
                return jsonify(transaction)
        return jsonify({'error': 'Transaction not found'}), 404

    def delete(self, transaction_id):
        for index, transaction in enumerate(transactions):
            if transaction['id'] == transaction_id:
                del transactions[index]
                return jsonify({'message': 'Transaction deleted'})
        return jsonify({'error': 'Transaction not found'}), 404

class SendMoney(Resource):
    def post(self):
        data = request.json
        sender = data.get('sender')
        receiver = data.get('receiver')
        amount = data.get('amount')
        if not sender or not receiver or not amount:
            return {'error': 'Missing required fields'}, 400

        # Create a new transaction
        new_transaction = {
            "id": len(transactions) + 1,
            "date": "2024-04-08",
            "amount": amount,
            "sender": sender,
            "receiver": receiver
        }
        transactions.append(new_transaction)
        return new_transaction, 201

api.add_resource(TransactionList, '/transactions')
api.add_resource(Transaction, '/transactions/<int:transaction_id>')
api.add_resource(SendMoney, '/send-money')

if __name__ == '__main__':
    app.run(debug=True)
