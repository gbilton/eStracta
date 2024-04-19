from uuid import UUID
from flask import Flask, Response, request

from app.models.company import Company
from app.services.company_service import CompanyService
from app.db import db
from app import models  # noqa

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:eStractaPassword@localhost:5432/eStracta"
)

# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post("/companies")
def create_company():
    cnpj: str = request.form["cnpj"]
    nome_razao: str = request.form["nome_razao"]
    nome_fantasia: str = request.form["nome_fantasia"]
    cnae: str = request.form["cnae"]

    created_company: Company = CompanyService.add_company(
        cnpj=cnpj,
        nome_razao=nome_razao,
        nome_fantasia=nome_fantasia,
        cnae=cnae,
    )

    return created_company.dict(), 201


@app.patch("/companies/<company_id>")
def update_company(company_id: str):
    nome_fantasia: str = request.form["nome_fantasia"]
    cnae: str = request.form["cnae"]

    updated_company: Company = CompanyService.update_company(
        company_id=UUID(company_id), nome_fantasia=nome_fantasia, cnae=cnae
    )

    return updated_company.dict(), 200


@app.get("/companies/<company_id>")
def get_company(company_id: str):
    company = CompanyService.get_company(company_id=UUID(company_id))
    if not company:
        raise Exception("Company not found")
    return company.dict(), 200


@app.get("/companies")
def get_companies():
    companies = CompanyService.get_companies()
    return [company.dict() for company in companies], 200


@app.delete("/companies/<cnpj>")
def delete_company(cnpj: str):
    CompanyService.delete_company(cnpj=cnpj)
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
