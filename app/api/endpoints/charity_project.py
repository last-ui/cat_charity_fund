from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_invested_project,
                                check_name_duplicate,
                                check_project_before_edit)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.investment import run_investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Создание проекта доступно только суперюзеру."""
    await check_name_duplicate(charity_project.name, session)
    donations = await donation_crud.get_not_fully_invested(session)
    if not donations:
        new_project = await charity_project_crud.create(
            charity_project,
            session=session
        )
        return new_project
    new_project = await run_investment(
        obj_in=charity_project,
        db_objects=donations,
        session=session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_crud.get_multi(session)
    return charity_projects


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Удаление проекта доступно только суперюзеру."""
    project = await check_invested_project(project_id, session)
    await charity_project_crud.remove(project, session)
    return project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Редактирование проекта доступно только суперюзеру."""
    project = await check_project_before_edit(project_id, obj_in, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    project = await charity_project_crud.update(
        db_obj=project,
        obj_in=obj_in,
        session=session
    )
    return project
