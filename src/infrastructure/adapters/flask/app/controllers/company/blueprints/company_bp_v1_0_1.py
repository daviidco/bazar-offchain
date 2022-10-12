from flask import Blueprint
from flask_restx import Api

from src.infrastructure.adapters.flask.app.controllers.company.company_resources import api as company_ns

companies_v1_01_bp = Blueprint('companies_v1_01_bp', __name__)

api = Api(companies_v1_01_bp, version="0.1.0", title="Company")
api.add_namespace(company_ns, path='/v1/companies')
