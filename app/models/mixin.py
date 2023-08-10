from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer


class ColumnMixin(object):
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0, nullable=False)
    fully_invested = Column(Boolean, default=False, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
