from datetime import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User
from app.schemas.charity_project import CharityProjectCreate


async def run_investment(
        obj_in,
        db_objects,
        session: AsyncSession,
        user: Optional[User] = None,
):
    data_in = obj_in.dict(exclude_unset=True)
    full_amount = data_in['full_amount']
    data_in['invested_amount'] = 0
    updated_objects = await get_updated_objects(
        db_objects=db_objects, data_in=data_in, full_amount=full_amount
    )
    session.add_all(updated_objects)
    db_object = await get_db_object(obj_in, data_in, user)
    session.add(db_object)
    await session.commit()
    await session.refresh(db_object)
    return db_object


async def get_updated_objects(db_objects, data_in: dict, full_amount: int):
    updated_objects = []
    for db_obj in db_objects:
        diff_amount = db_obj.full_amount - db_obj.invested_amount
        if full_amount < diff_amount:
            db_obj.invested_amount += full_amount
            data_in['invested_amount'] += full_amount
            updated_objects.append(db_obj)
            return updated_objects
        db_obj.invested_amount += diff_amount
        db_obj.fully_invested = True
        db_obj.close_date = datetime.now()
        data_in['invested_amount'] += diff_amount
        updated_objects.append(db_obj)
        full_amount -= diff_amount
        if full_amount == 0:
            return updated_objects


async def get_db_object(obj_in, data_in: dict, user: Optional[User] = None):
    if data_in['invested_amount'] == data_in['full_amount']:
        data_in['fully_invested'] = True
        data_in['close_date'] = datetime.now()
        if user:
            data_in['user_id'] = user.id
    if isinstance(obj_in, CharityProjectCreate):
        db_object = CharityProject(**data_in)
    else:
        db_object = Donation(**data_in)
    return db_object
