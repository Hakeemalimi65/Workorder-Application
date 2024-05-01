from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    work_orders = db.relationship('WorkOrder', backref='user', passive_deletes=True)


class WorkOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.Text, nullable=False)
    department = db.Column(db.Text, nullable=False)
    work_requested = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)