from uuid import UUID
from flask import Flask, Response, jsonify, request
from flask_migrate import Migrate


from app.exceptions import InvalidParameters
from app.models.company import Company
from app.services.company_service import CompanyService
from app.db import db
from app import models  # noqa
from app.utils import validate_parameters

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:eStractaPassword@localhost:5432/eStracta"
)
migrate = Migrate(app, db)

# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/")
def check_health():
    return "ok"


@app.post("/companies")
def create_company():
    try:
        cnpj: str = request.form["cnpj"]
        nome_razao: str = request.form["nome_razao"]
        nome_fantasia: str = request.form["nome_fantasia"]
        cnae: str = request.form["cnae"]
    except KeyError:
        return (
            "Os seguintes campos são obrigatórios: cnpj, nome_razao, nome_fantasia, cnae.",
            400,
        )

    try:
        validate_parameters(
            cnpj=cnpj,
            nome_razao=nome_razao,
            nome_fantasia=nome_fantasia,
            cnae=cnae,
        )
    except InvalidParameters as e:
        return jsonify(error=str(e)), 400

    created_company: Company = CompanyService.add_company(
        cnpj=cnpj,
        nome_razao=nome_razao,
        nome_fantasia=nome_fantasia,
        cnae=cnae,
    )

    return jsonify(created_company), 201


@app.patch("/companies/<company_id>")
def update_company(company_id: str):
    nome_fantasia: str = request.form["nome_fantasia"]
    cnae: str = request.form["cnae"]
    updated_company: Company = CompanyService.update_company(
        company_id=UUID(company_id), nome_fantasia=nome_fantasia, cnae=cnae
    )
    return jsonify(updated_company), 200


@app.get("/companies/<company_id>")
def get_company(company_id: str):
    company = CompanyService.get_company(company_id=UUID(company_id))
    if not company:
        raise Exception("Company not found")
    return jsonify(company), 200


@app.get("/companies")
def get_companies():
    query_params = {}
    query_params["sort"] = request.args.get("sort")
    query_params["limit"] = request.args.get("limit")
    query_params["start"] = request.args.get("start")
    query_params["dir"] = request.args.get("dir")
    companies: list[Company] = CompanyService.get_companies(**query_params)
    return [company for company in companies], 200


@app.delete("/companies/<cnpj>")
def delete_company(cnpj: str):
    CompanyService.delete_company(cnpj=cnpj)
    return Response(status=204)


if __name__ == "__main__":
    app.run(debug=True)
