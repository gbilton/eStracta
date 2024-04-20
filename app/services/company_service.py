from datetime import datetime
from typing import Optional
from uuid import UUID

from psycopg2 import IntegrityError
from app.exceptions import DuplicateEntry
from app.models.company import Company
from app.models.company import Company
from app.db import db
from app.models.enums import CompanySortField, SortOrder


class CompanyService:
    @classmethod
    def add_company(
        cls, cnpj: str, nome_razao: str, nome_fantasia: str, cnae: str
    ) -> Company:
        new_company = Company(
            cnpj=cnpj,
            nome_razao=nome_razao,
            nome_fantasia=nome_fantasia,
            cnae=cnae,
        )
        # existing_company = Company.query.filter_by(cnpj=cnpj).first()
        # if existing_company:
        #     raise DuplicateEntry("Empresa já cadastrada.")

        db.session.add(new_company)
        db.session.commit()

        return new_company

    @classmethod
    def get_company(cls, company_id: UUID) -> Optional[Company]:
        company = db.get_or_404(Company, company_id)
        return company

    @classmethod
    def get_companies(
        cls,
        start: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[CompanySortField] = None,
        dir: Optional[SortOrder] = None,
    ) -> list[Company]:
        stmt = db.select(Company)
        if start is not None:
            stmt = stmt.offset(start)
        if limit is not None:
            stmt = stmt.limit(limit)

        if sort is not None:
            if dir is None or dir == SortOrder.ASCENDING:
                stmt = stmt.order_by(getattr(Company, sort.value))
            elif dir == SortOrder.DESCENDING:
                stmt = stmt.order_by(getattr(Company, sort.value).desc())

        companies = db.session.execute(stmt).scalars().all()

        return companies

    @classmethod
    def update_company(
        cls,
        company_id: UUID,
        nome_fantasia: Optional[str],
        cnae: Optional[str],
    ) -> Optional[Company]:

        company = db.get_or_404(Company, company_id)
        modified: bool = False
        if nome_fantasia:
            company.nome_fantasia = nome_fantasia
            modified = True
        if cnae:
            company.cnae = cnae
            modified = True
        if modified:
            company.updated_at = datetime.now()
            db.session.commit()
            return company
        return

    @classmethod
    def delete_company(cls, cnpj: str) -> None:
        stmt = db.select(Company).where(Company.cnpj == cnpj)
        company = db.one_or_404(stmt)
        db.session.delete(company)
        db.session.commit()
        return
