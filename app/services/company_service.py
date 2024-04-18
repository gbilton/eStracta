from typing import Optional
from uuid import UUID
from app.models.company import Company


class CompanyService:
    companies = []

    @classmethod
    def add_company(
        cls, cnpj: str, nome_razao: str, nome_fantasia: str, cnae: str
    ):
        new_company = Company(
            cnpj=cnpj,
            nome_razao=nome_razao,
            nome_fantasia=nome_fantasia,
            cnae=cnae,
        )
        cls.companies.append(new_company)

    @classmethod
    def get_company(cls, company_id: UUID):
        for company in cls.companies:
            if company.id == company_id:
                print(company)
                return
        return

    @classmethod
    def get_companies(
        cls,
        start: Optional[int] = None,
        limit: Optional[int] = None,
        sort: Optional[str] = None,
        dir: Optional[str] = None,
    ):
        return cls.companies

    @classmethod
    def update_company(
        cls,
        company_id: UUID,
        nome_fantasia: Optional[str],
        cnae: Optional[str],
    ):
        for company in cls.companies:
            if company.id == company_id:
                if nome_fantasia:
                    company.nome_fantasia = nome_fantasia
                if cnae:
                    company.cnae = cnae
        return

    @classmethod
    def delete_company(cls, cnpj: str):
        for i, company in enumerate(cls.companies):
            if company.cnpj == cnpj:
                cls.companies.pop(i)
                return
