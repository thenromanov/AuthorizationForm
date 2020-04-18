import datetime
import sqlalchemy
from sqlalchemy import orm, Integer, String, DateTime, Column
from .dbSession import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    surname = Column(String, nullable=True)
    name = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    position = Column(String, nullable=True)
    speciality = Column(String, nullable=True)
    address = Column(String, nullable=True)
    email = Column(String, index=True, unique=True, nullable=True)
    hashedPassword = Column(String, nullable=True)
    modifiedDate = Column(DateTime, default=datetime.datetime.now)
    jobs = orm.relation('Jobs', back_populates='user', lazy='subquery')
    departments = orm.relation('Department', back_populates='user')

    def __repr__(self):
        return f'<Colonist> {self.id} {self.name} {self.surname}'

    def setPassword(self, password):
        self.hashedPassword = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.hashedPassword, password)
