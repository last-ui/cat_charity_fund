from sqlalchemy import Column, String, Text

from app.core.config import settings
from app.core.db import Base
from app.models.mixin import ColumnMixin


class CharityProject(ColumnMixin, Base):
    name = Column(
        String(settings.max_project_name_length),
        unique=True,
        nullable=False
    )
    description = Column(Text)
