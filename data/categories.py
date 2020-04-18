import sqlalchemy
from sqlalchemy import orm, Column, Integer, String, ForeignKey, Table
from .dbSession import SqlAlchemyBase


jobsToCategory = Table('association', SqlAlchemyBase.metadata,
                       Column('job', Integer, ForeignKey('jobs.id')),
                       Column('category', Integer, ForeignKey('category.id')))


class Category(SqlAlchemyBase):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    level = Column(Integer, nullable=True, unique=True)

    def __repr__(self):
        return f'<Category> {self.id} {self.level}'
