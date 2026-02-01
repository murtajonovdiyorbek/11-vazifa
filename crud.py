import  shutil
from pathlib import Path
from fastapi import UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import MEDIA_DIR
from schemas import BuildingCreate, BuildingResponse, CompanyCreate, CompanyResponse
from models import Company, Building

async def company_create(company: CompanyCreate, db: AsyncSession) -> CompanyResponse:
    db_company = Company(**company.model_dump())
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return CompanyResponse.model_validate(db_company)



async def building_create(building: BuildingCreate, db: AsyncSession, image: UploadFile = None, sertificate: UploadFile = None) -> BuildingResponse:

    if image:
        image_extension = image.filename.lower().split(".")[-1]
        if image_extension not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="faqat jpg, jpeg, png formatdagi rasm qabul qilinadi!")

    if sertificate:
        sertificate_extension = sertificate.filename.lower().split(".")[-1]
        if sertificate_extension not in ["pdf"]:
            raise HTTPException(status_code=400, detail="faqat pdf formatdagi sertificate qabul qilinadi!")


    db_building = Building(**building.model_dump())
    db.add(db_building)
    await db.commit()
    await db.refresh(db_building)



    if image:
        image_path = Path(MEDIA_DIR) / f"building_{db_building.id}_image.{image_extension}"
        with image_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_building.image = str(image_path)


    if sertificate:
        sertificate_path = Path(MEDIA_DIR) / f"building_{db_building.id}_document.{sertificate_extension}"
        with sertificate_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        db_building.image = str(sertificate_path)



    return BuildingResponse.model_validate(db_building)