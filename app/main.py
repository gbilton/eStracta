from uuid import UUID
from flask import Flask, request
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from werkzeug.exceptions import BadRequest

from app.exceptions import InvalidParameters
from app.mock_data import create_mock_data
from app.models.company import Company
from app.services.company_service import CompanyService
from app.db import db
from app import models  # noqa
from app.utils import format_cnae, format_cnpj, validate_parameters

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://postgres:eStractaPassword@localhost:5432/eStracta"
)
CORS(app)

api = Api(app, doc="/docs")

company_update_model = api.model(
    "CompanyUpdate",
    {
        "nome_fantasia": fields.String(
            required=False, description="The Company's Nome Fantasia."
        ),
        "cnae": fields.String(
            required=False, description="The Company's CNAE."
        ),
    },
)
company_model = api.model(
    "Company",
    {
        "id": fields.String(readonly=True, description="Unique identifier."),
        "created_at": fields.DateTime(
            readonly=True, description="Date and time of creation."
        ),
        "updated_at": fields.DateTime(
            readonly=True, description="Last date and time of update."
        ),
        "cnpj": fields.String(
            required=True, description="The Company's CNPJ."
        ),
        "nome_razao": fields.String(
            required=True, description="The Company's Nome Razão."
        ),
        "nome_fantasia": fields.String(
            required=True, description="The Company's Nome Fantasia."
        ),
        "cnae": fields.String(
            required=True, description="The Company's CNAE."
        ),
    },
)

# initialize the app with the extension
db.init_app(app)
with app.app_context():
    db.create_all()

migrate = Migrate(app, db)


@app.route("/")
def check_health():
    return "ok"


@api.route("/companies")
class CompanyListRoutes(Resource):
    @api.expect(company_model)
    @api.marshal_with(company_model, code=201)
    def post(self):
        data = api.payload
        try:
            cnpj: str = data["cnpj"]
            nome_razao: str = data["nome_razao"]
            nome_fantasia: str = data["nome_fantasia"]
            cnae: str = data["cnae"]
        except KeyError:
            raise BadRequest(
                "The following body parameters are required: cnpj, nome_razao, nome_fantasia, cnae."
            )

        try:
            validate_parameters(
                cnpj=cnpj,
                nome_razao=nome_razao,
                nome_fantasia=nome_fantasia,
                cnae=cnae,
            )
        except InvalidParameters as error:
            raise BadRequest(str(error))

        try:
            created_company: Company = CompanyService.add_company(
                cnpj=cnpj,
                nome_razao=nome_razao,
                nome_fantasia=nome_fantasia,
                cnae=cnae,
            )
        except IntegrityError as error:
            assert isinstance(error.orig, UniqueViolation)
            raise BadRequest(str("Company already registered"))

        return created_company, 201

    @api.doc(
        params={
            "sort": "Sort order for companies",
            "limit": "Limit number of companies to retrieve",
            "start": "Start index for retrieving companies",
            "dir": "Direction for sorting companies",
        },
    )
    @api.marshal_list_with(company_model)
    def get(self):
        query_params = {}
        query_params["sort"] = request.args.get("sort")
        query_params["limit"] = request.args.get("limit")
        query_params["start"] = request.args.get("start")
        query_params["dir"] = request.args.get("dir")
        companies: list[Company] = CompanyService.get_companies(**query_params)
        return companies, 200


@api.route("/companies/<company_id>")
class CompanyRoutes(Resource):
    @api.doc(params={"company_id": "The company's unique identifier."})
    @api.marshal_with(company_model)
    def get(self, company_id: str):
        try:
            company_uuid = UUID(company_id)
        except ValueError:
            raise BadRequest("Invalid ID.")

        company = CompanyService.get_company(company_id=company_uuid)
        return company, 200

    @api.expect(company_update_model)
    @api.marshal_with(company_model)
    def patch(self, company_id: str):
        nome_fantasia: str = api.payload.get("nome_fantasia")
        cnae: str = api.payload.get("cnae")
        try:
            validate_parameters(cnae=cnae)
        except InvalidParameters as error:
            raise BadRequest(str(error))
        cnae = format_cnae(cnae)
        try:
            company_uuid = UUID(company_id)
        except ValueError:
            raise BadRequest("Invalid ID.")
        updated_company: Company = CompanyService.update_company(
            company_id=company_uuid, nome_fantasia=nome_fantasia, cnae=cnae
        )
        return updated_company, 200


@api.route("/companies/<cnpj>")
class CompanyDelete(Resource):
    @api.doc(
        params={
            "cnpj": "The Company's CNPJ (only numbers). Example: 00623904000173"
        }
    )
    @api.response(204, "Company deleted.")
    def delete(self, cnpj: str):
        cnpj = format_cnpj(cnpj=cnpj)
        CompanyService.delete_company(cnpj=cnpj)
        return "", 204


@app.post("/mock")
def create_mock():
    create_mock_data()
    return "success", 201


if __name__ == "__main__":
    app.run(debug=True)
