from uuid import UUID
from flask import Flask, request

from app.services.company_service import CompanyService

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.post("/companies")
def create_company():
    cnpj: str = request.form["cnpj"]
    nome_razao: str = request.form["nome_razao"]
    nome_fantasia: str = request.form["nome_fantasia"]
    cnae: str = request.form["cnae"]

    CompanyService.add_company(
        cnpj=cnpj,
        nome_razao=nome_razao,
        nome_fantasia=nome_fantasia,
        cnae=cnae,
    )

    return "success", 201


@app.patch("/companies/<company_id>")
def update_company(company_id: str):
    nome_fantasia: str = request.form["nome_fantasia"]
    cnae: str = request.form["cnae"]

    CompanyService.update_company(
        company_id=UUID(company_id), nome_fantasia=nome_fantasia, cnae=cnae
    )

    return "success", 200


@app.get("/companies/<company_id>")
def get_company(company_id: str):
    CompanyService.get_company(company_id=UUID(company_id))
    return "success", 200


@app.get("/companies")
def get_companies():
    companies = CompanyService.get_companies()
    return companies


@app.delete("/companies/<cnpj>")
def delete_company(cnpj: str):
    CompanyService.delete_company(cnpj=cnpj)
    return "deleted", 200
