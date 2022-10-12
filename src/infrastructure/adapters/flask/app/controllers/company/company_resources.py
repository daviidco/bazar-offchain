import json
from typing import List

import inject
from flask import _request_ctx_stack
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request


from src.application.company.company_uc import GetCompany, GetAllCompanies, CreateCompany
from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.error_handling import AppErrorBaseClass
# from app.third_parties.auth0.aurh0_service import requires_auth
# from app.third_parties.storage.s3_service.py import upload_file_to_s3


api = Namespace("/companies", description="Company controller")


@api.route("/")
class CompaniesResource(Resource):
    @inject.autoparams('get_all_companies', 'create_company')
    def __init__(self, api:None, get_all_companies: GetAllCompanies, create_company: CreateCompany):
        self.api = api
        self.get_all_companies = get_all_companies
        self.create_company = create_company

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self):
        limit = request.json['limit']
        offset = request.json['offset']
        result = self.get_all_companies.execute(limit, offset)
        return json.loads(result.json()), 200

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self):
        jwt_entity = JwtEntity.parse_obj(_request_ctx_stack.top.current_user)
        entity = CompanyNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        result = self.create_company.execute(jwt_entity, entity, files)
        return json.loads(result.json()), 201


@api.route("/<string:company_uuid>")
class CompanyResource(Resource):

    @inject.autoparams('get_company')
    def __init__(self, api: None, get_company: GetCompany):
        self.api = api
        self.get_company = get_company

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, company_uuid):
        result = self.get_company.execute(company_uuid)
        return json.loads(result.json()), 200

