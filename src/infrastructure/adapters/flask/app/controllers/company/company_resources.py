# -*- coding: utf-8 -*-
#
# This source code is the confidential, proprietary information of
# Bazar Network S.A.S., you may not disclose such Information,
# and may only use it in accordance with the terms of the license
# agreement you entered into with Bazar Network S.A.S.
#
# 2022: Bazar Network S.A.S.
# All Rights Reserved.
#

import json

import inject
from flask_cors import cross_origin
from flask_restx import Resource, Namespace, reqparse, abort
from flask_restx.reqparse import request
from werkzeug.datastructures import FileStorage

from src.application.company.company_uc import GetCompany, GetAllCompanies, CreateCompany
from src.domain.entities.common_entity import  InputPaginationEntity
from src.domain.entities.company_entity import CompanyNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth
from src.infrastructure.adapters.flask.app.utils.error_handling import api_error
from src.infrastructure.adapters.flask.app.utils.ultils import get_schema_and_type

#
# This file contains the company endpoints Api-rest
# @author David Córdoba
#

api = Namespace("companies", description="Company controller", path='/api/v1/companies')


@api.route("/")
class CompaniesResource(Resource):
    schema = InputPaginationEntity.schema()

    schema_company = CompanyNewEntity.schema()
    model = api.schema_model("CompanyNewEntity", schema_company)
    help_new_company = json.dumps(get_schema_and_type(schema_company), indent=2)

    # Object to upload file and json body in form data
    upload_parser = reqparse.RequestParser()
    upload_parser.add_argument('files[]', location='files',
                               type=FileStorage, action='append', help='Company Files')

    upload_parser.add_argument('body', location='form',
                               type=dict, required=False, help='Company Information \n'+help_new_company)

    @inject.autoparams('get_all_companies', 'create_company')
    def __init__(self, api: None, get_all_companies: GetAllCompanies, create_company: CreateCompany):
        self.api = api
        self.get_all_companies = get_all_companies
        self.create_company = create_company

    @api.doc(params=schema['properties'], security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, *args, **kwargs):
        limit = request.args.get('limit', 10)
        offset = request.args.get('offset', 0)
        result = self.get_all_companies.execute(limit, offset)
        return json.loads(result.json()), 200

    @api.expect(upload_parser)
    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        jwt = dict(request.headers).get('Authorization', None)
        role = kwargs.get('role', None)
        if role is None:
            e = api_error('RoleNotFound')
            abort(code=e.status_code, message=e.message, error=e.error)

        entity = CompanyNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        result = self.create_company.execute(jwt, role, entity, files)
        return json.loads(result.json()), 201


@api.route("/<string:company_uuid>")
class CompanyResource(Resource):

    @inject.autoparams('get_company')
    def __init__(self, api: None, get_company: GetCompany):
        self.api = api
        self.get_company = get_company

    @api.doc(security='Private JWT')
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, company_uuid, *args, **kwargs):
        result = self.get_company.execute(company_uuid)
        return json.loads(result.json()), 200