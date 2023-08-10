from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
