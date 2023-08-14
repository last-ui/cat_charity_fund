from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationBase, DonationCreate, DonationDB
from app.services.investment import run_investment

router = APIRouter()


@router.post(
    '/',
    response_model=DonationCreate,
    response_model_exclude_none=True
)
async def create_new_donation(
        donation_in: DonationBase,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_not_fully_invested(
        session
    )
    if charity_projects:
        return await run_investment(
            donation_in, charity_projects, session, user
        )
    return await donation_crud.create(
        obj_in=donation_in,
        user=user,
        session=session
    )


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationCreate],
    response_model_exclude_none=True,
)
async def get_user_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_by_user(user.id, session)
