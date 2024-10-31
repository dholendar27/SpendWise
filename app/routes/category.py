from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, current_user

from app.models import Expense, Category
from app.extensions import db

category = Blueprint('category', __name__, url_prefix='/category')


@category.route('/add', methods=['POST'])
@jwt_required()
def add_expense():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    category = Category(user_id=current_user.id, name = data['name'], budget=data['budget'])
    db.session.add(category)
    db.session.commit()
    return jsonify({'success': 'Category Created Successfully'}), 201


@category.route('/delete/<string:category_id>', methods=['DELETE'])
@jwt_required()
def delete_expense(category_id):
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({'success': 'Category Deleted Successfully'}), 201


@category.route('/update/<string:category_id>', methods=['PUT'])
@jwt_required()
def update_expense(category_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400
    category = Category.query.filter(Category.id == category_id).first()
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    category.name = data['name']
    category.budget = data['budget']
    db.session.commit()
    return jsonify({'success': 'Category Updated Successfully'}), 201

@category.route('/list', methods=['GET'])
@jwt_required()
def list_category():
    categories = Category.query.all()
    category = [category.to_dict() for category in categories]
    return jsonify({'categories': category})



