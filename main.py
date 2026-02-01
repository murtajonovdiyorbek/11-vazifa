from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uvicorn
from database import Base, engine, get_db
from models import Company, Building
from schemas import CompanyResponse, CompanyCreate, BuildingCreate, BuildingResponse
from crud import company_create, building_create

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/company/", response_model=CompanyResponse)
async def add_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    return await company_create(company, db)


@app.get("/company/", response_model=List[CompanyResponse])
async def get_all_companies(db: AsyncSession = Depends(get_db)):
    data = await db.execute(select(Company))
    companies = data.scalars().all()
    return companies


@app.get("/company/{id}", response_model=CompanyResponse)
async def get_one_company(id: int, db: AsyncSession = Depends(get_db)):
    company = await db.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company topilmadi")
    return company


@app.put("/company/{id}", response_model=CompanyResponse)
async def update_company(id: int, new_company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    company = await db.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company topilmadi")

    for keys, value in new_company.model_dump(exclude_unset=True).items():
        setattr(company, keys, value)

    await db.commit()
    await db.refresh(company)
    return company


@app.delete("/company/{id}")
async def delete_company(id: int, db: AsyncSession = Depends(get_db)):
    company = await db.get(Company, id)
    if not company:
        raise HTTPException(status_code=404, detail="Company topilmadi")

    await db.delete(company)
    await db.commit()
    return company

@app.post("/building/", response_model=BuildingResponse)
async def add_building(building: BuildingCreate, db: AsyncSession = Depends(get_db)):
    return await building_create(building, db)


@app.get("/building/", response_model=List[BuildingResponse])
async def get_all_buildings(db: AsyncSession = Depends(get_db)):
    data = await db.execute(select(Building))
    buildings = data.scalars().all()
    return buildings


@app.get("/building/{id}", response_model=BuildingResponse)
async def get_one_building(id: int, db: AsyncSession = Depends(get_db)):
    building = await db.get(Building, id)
    if not building:
        raise HTTPException(status_code=404, detail="Building topilmadi")
    return building


@app.put("/building/{id}", response_model=BuildingResponse)
async def update_building(id: int, new_building: BuildingCreate, db: AsyncSession = Depends(get_db)):
    building = await db.get(Building, id)
    if not building:
        raise HTTPException(status_code=404, detail="Building topilmadi")

    for keys, value in new_building.model_dump(exclude_unset=True).items():
        setattr(building, keys, value)

    await db.commit()
    await db.refresh(building)
    return building


@app.delete("/building/{id}")
async def delete_building(id: int, db: AsyncSession = Depends(get_db)):
    building = await db.get(Building, id)
    if not building:
        raise HTTPException(status_code=404, detail="Buildingg topilmadi")

    await db.delete(building)
    await db.commit()
    return building


if __name__ == "__main__":
    uvicorn.run(app)