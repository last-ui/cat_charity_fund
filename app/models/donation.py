from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.mixin import ColumnMixin


class Donation(ColumnMixin, Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
