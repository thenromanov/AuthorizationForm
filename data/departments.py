import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from .dbSession import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Department(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    chief = Column(Integer, ForeignKey('users.id'))
    members = Column(String, nullable=True)
    email = Column(String, nullable=True)
    user = orm.relationship('User')

    def __repr__(self):
        return f'<Department> {self.id} {self.title} {self.chief}'
