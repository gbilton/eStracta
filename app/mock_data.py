from app.models.company import Company
from app.db import db
from app.utils import format_cnae, format_cnpj


def create_mock_data():
    companies = [
        Company(
            cnpj="02828446000134",
            nome_razao="LITORAL LOCADORA LTDA - ME",
            nome_fantasia="Locadora Litoral",
            cnae=7711010,
        ),
        Company(
            cnpj="72610132000146",
            nome_razao="ASSESSORIA E SERVICOS LTDA - ME",
            nome_fantasia="Serviços 1A",
            cnae=7020400,
        ),
        Company(
            cnpj="01874354000128",
            nome_razao="RESTAURANTE E LANCHONETE LTDA",
            nome_fantasia="Lanchonete Express",
            cnae=5611201,
        ),
        Company(
            cnpj="04220692000134",
            nome_razao="CHURRASCARIA E RESTAURANTE LTDA - ME",
            nome_fantasia="Churrascaria do Zé",
            cnae=5611201,
        ),
        Company(
            cnpj="26159125000152",
            nome_razao="AUTO CAR LTDA - EPP",
            nome_fantasia="Auto Car",
            cnae=4520001,
        ),
        Company(
            cnpj="12146377000132",
            nome_razao="A & W PIZZARIA LTDA - ME",
            nome_fantasia="A & W Pizzaria",
            cnae=5611201,
        ),
        Company(
            cnpj="06034513000108",
            nome_razao="M & C SERVICOS DE XEROX E ENCADERNACOES LTDA - ME",
            nome_fantasia="M&C Xerox",
            cnae=8219999,
        ),
        Company(
            cnpj="02006030000130",
            nome_razao="MELHOR GESTAO EMPRESARIAL LTDA - EPP",
            nome_fantasia="Melhor Gestão",
            cnae=7020400,
        ),
        Company(
            cnpj="13080788000135",
            nome_razao="PERFUMES E INFORMATICA LTDA - ME",
            nome_fantasia="Perfumes & Informática",
            cnae=4771701,
        ),
        Company(
            cnpj="15358677000173",
            nome_razao="SHOP DESENVOLVIMENTO DE LOJAS VIRTUAIS LTDA - EPP",
            nome_fantasia="Shop Lojas Virtuais",
            cnae=6202300,
        ),
    ]

    for company in companies:
        company.cnpj = format_cnpj(str(company.cnpj))
        company.cnae = format_cnae(str(company.cnae))

    db.session.add_all(companies)
    db.session.commit()
