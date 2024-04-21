from datetime import datetime
from typing import Optional
from uuid import UUID

from psycopg2 import IntegrityError
from app.exceptions import DuplicateEntry
from app.models.company import Company
from app.models.company import Company
from app.db import db
from app.models.enums import CompanySortField, SortOrder
from app.utils import format_cnae, format_cnpj


class CompanyService:
    @classmethod
    def add_company(
        cls, cnpj: str, nome_razao: str, nome_fantasia: str, cnae: str
    ) -> Company:
        cnpj = format_cnpj(cnpj)
        cnae = format_cnae(cnae)

        new_company = Company(
            cnpj=cnpj,
            nome_razao=nome_razao,
            nome_fantasia=nome_fantasia,
            cnae=cnae,
        )

        db.session.add(new_company)
        db.session.commit()

        return new_company

    @classmethod
    def get_company(cls, company_id: UUID) -> Optional[Company]:
        company = db.get_or_404(
            Company, company_id, description="Company not found."
        )
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

        if any(sort == item.value for item in CompanySortField):
            if dir is None or dir == SortOrder.ASCENDING.value:
                stmt = stmt.order_by(getattr(Company, sort))
            elif dir == SortOrder.DESCENDING.value:
                stmt = stmt.order_by(getattr(Company, sort).desc())

        companies = db.session.execute(stmt).scalars().all()

        return companies

    @classmethod
    def update_company(
        cls,
        company_id: UUID,
        nome_fantasia: Optional[str],
        cnae: Optional[str],
    ) -> Optional[Company]:

        company = db.get_or_404(
            Company,
            company_id,
            description=f"Company with ID {company_id} not found.",
        )
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
        company = db.one_or_404(
            stmt, description=f"Company with CNPJ {cnpj} not found."
        )
        db.session.delete(company)
        db.session.commit()
        return
