from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db


@dataclass
class Company(db.Model):
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    cnpj: Mapped[str] = mapped_column(unique=True, nullable=False)
    nome_razao: Mapped[str] = mapped_column(unique=True, nullable=False)
    nome_fantasia: Mapped[str] = mapped_column(nullable=False)
    cnae: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[Optional[datetime]] = None
