from flask import jsonify, request,Blueprint
from flask_jwt_extended import jwt_required, current_user

from app.extensions import db
from app.models import Expense, Category


expense = Blueprint('expenses', __name__, url_prefix='/expenses')


@expense.route('/add', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    expense = Expense(user_id=current_user.id, category_id=data['category_id'], amount=data['amount'], description=data['description'], date=data['date'] or "")
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': "Record has added Successfully" }), 201

@expense.route('/list', methods=['GET'])
@jwt_required()
def get_expenses():
    expeneses = Expense.query.all()
    expenses_data = [expenses.to_dict() for expenses in expeneses]
    return jsonify(expenses_data), 200

@expense.route('/count/<string:category_id>', methods=['GET'])
@jwt_required()
def get_expenses_count(category_id):
    expense = Expense.query.filter_by(category_id=category_id).filter_by(user_id=current_user.id).all()

    if not expense:
        return jsonify({'error': 'No expenses found'}), 404

    total_expenses = sum([expense.amount for expense in expense])
    return jsonify({'total_expenses': total_expenses}), 200

@expense.route('/delete/<string:expense_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id).first()
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Deleted Successfully'}), 200

@expense.route('/update/<string:expense_id>', methods=['PUT'])
@jwt_required()
def update_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id).first()
    if not expense:
        return jsonify({'error': 'No expenses found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    expense.amount = data['amount']
    expense.description = data['description']
    expense.category_id = data['category_id']
    expense.date = data['date']
    db.session.commit()
    return jsonify({'message': 'Updated Successfully'}), 200


