import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, ForeignKey
from .dbSession import SqlAlchemyBase


class Department(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=True)
    chief = Column(Integer, ForeignKey('users.id'))
    members = Column(String, nullable=True)
    email = Column(String, nullable=True)
    user = orm.relation('User')

    def __repr__(self):
        return f'<Department> {self.id} {self.title} {self.chief}'
