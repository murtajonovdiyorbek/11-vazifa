from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from typing import Optional

from database import Base



class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    info: Mapped[Optional[str]] = mapped_column(nullable=True)
    address: Mapped[str] = mapped_column(nullable=True)
    phone: Mapped[str] = mapped_column(nullable=True)

class Building(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(nullable=True)

    image: Mapped[Optional[str]] = mapped_column(nullable=True)
    sertificate: Mapped[Optional[str]] = mapped_column(nullable=True)

    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id"))