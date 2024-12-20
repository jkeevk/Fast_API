from models import ORM_OBJ, ORM_CLS, USER_OBJ, USER_CLS


from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException



async def add_advert(session: AsyncSession, advert: ORM_OBJ):
    session.add(advert)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Advert already exists")


async def get_advert_by_id(session: AsyncSession, orm_cls: ORM_CLS, advert_id: int) -> ORM_OBJ:
    orm_obj = await session.get(orm_cls, advert_id)
    if orm_obj is None:
        raise HTTPException(status_code=404, detail="Advert not found")
    return orm_obj


async def delete_advert(advert: ORM_OBJ, session: AsyncSession):
    await session.delete(advert)
    await session.commit()



async def add_user(session: AsyncSession, user: USER_OBJ):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(status_code=409, detail="User already exists")