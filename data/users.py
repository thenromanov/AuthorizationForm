import datetime
import sqlalchemy
from sqlalchemy import orm, Integer, String, DateTime, Column
from .dbSession import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    position = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    speciality = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=True)
    hashedPassword = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    modifiedDate = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f'<Colonist> {str(self.id)} {str(self.name)} {str(self.surname)}'

    def setPassword(self, password):
        self.hashedPassword = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.hashedPassword, password)
