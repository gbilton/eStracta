from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import db


class CompanyModel(db.Model):
    id: Mapped[UUID] = mapped_column(primary_key=True)
    cnpj: Mapped[str]
    nome_razao: Mapped[str]
    nome_fantasia: Mapped[str]
    cnae: Mapped[str]
