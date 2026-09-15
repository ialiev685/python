from fastapi import APIRouter, status, Body, HTTPException, Query

from src.schemas.conveniences import ConvenienceAddRequestSchema
from src.api.dependencies import DBDep

router = APIRouter(prefix="/conveniences", tags=["Удобства"])


@router.get('')
async def get_conveniences(db: DBDep):
    return await db.conveniences.get_all()


@router.post('')
async def add_conveniences(data: ConvenienceAddRequestSchema, db: DBDep):
    convenience = await db.conveniences.add(data)
    await db.commit()
    return {"status": status.HTTP_200_OK, 'data': convenience}
