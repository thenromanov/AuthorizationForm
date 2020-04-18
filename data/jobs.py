import datetime
import sqlalchemy
from sqlalchemy import orm, Integer, String, Boolean, DateTime, Column, ForeignKey
from .dbSession import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Jobs(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    teamLeader = Column(Integer, ForeignKey('users.id'))
    job = Column(String, nullable=True)
    workSize = Column(Integer, nullable=True)
    collaborators = Column(String, nullable=True)
    startDate = Column(DateTime, default=datetime.datetime.now)
    endDate = Column(DateTime, default=None)
    isFinished = sqlalchemy.Column(Boolean, default=True)
    user = orm.relation('User')

    def __repr__(self):
        return f'<Job> {self.id} {self.teamLeader} {self.job}'
