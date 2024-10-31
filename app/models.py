from datetime import timezone, datetime
from hmac import compare_digest
import uuid
from app.extensions import db
from sqlalchemy import Column, String, ForeignKey, Integer, DateTime

class User(db.Model):
    __tablename__ = 'users'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firstname = Column(String(120), nullable=False)
    lastname = Column(String(120), nullable=True)
    password = Column(String(1024), nullable=False)  # Increased for hashed password storage
    email = Column(String(120), nullable=False, unique=True)
    expenses = db.relationship('Expense', backref='user', cascade='all, delete-orphan')
    category = db.relationship('Category', backref='user', cascade='all, delete-orphan')

    def check_password(self, password):
        return compare_digest(self.password, password)

class Category(db.Model):
    __tablename__ = 'categories'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    name = Column(String(120), nullable=False, unique=True)
    budget = Column(Integer, nullable=False)
    expenses = db.relationship('Expense', backref='category', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'budget': self.budget,
        }

class Expense(db.Model):
    __tablename__ = 'expenses'
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey('users.id'), nullable=False)
    category_id = Column(String(36), ForeignKey('categories.id'), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String(120), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date,
        }
