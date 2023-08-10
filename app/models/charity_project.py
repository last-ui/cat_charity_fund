from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.mixin import ColumnMixin


class CharityProject(ColumnMixin, Base):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
