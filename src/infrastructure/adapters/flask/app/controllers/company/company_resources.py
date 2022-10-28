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
from flask import _request_ctx_stack
from flask_cors import cross_origin
from flask_restx import Resource, Namespace
from flask_restx.reqparse import request

from src.application.company.company_uc import GetCompany, GetAllCompanies, CreateCompany
from src.domain.entities.common_entity import JwtEntity
from src.domain.entities.company_entity import CompanyNewEntity
from src.infrastructure.adapters.auth0.auth0_service import requires_auth

#
# This file contains the company endpoints Api-rest
# @author David Córdoba
#

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
    def get(self, *args, **kwargs):
        limit = request.json['limit']
        offset = request.json['offset']
        result = self.get_all_companies.execute(limit, offset)
        return json.loads(result.json()), 200

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def post(self, *args, **kwargs):
        jwt_entity = JwtEntity.parse_obj(_request_ctx_stack.top.current_user)
        role = kwargs['role']
        entity = CompanyNewEntity.parse_obj(json.loads(request.form['body']))
        files = request.files.getlist('files[]')
        result = self.create_company.execute(role, entity, files)
        return json.loads(result.json()), 201


@api.route("/<string:company_uuid>")
class CompanyResource(Resource):

    @inject.autoparams('get_company')
    def __init__(self, api: None, get_company: GetCompany):
        self.api = api
        self.get_company = get_company

    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth
    def get(self, company_uuid, *args, **kwargs):
        result = self.get_company.execute(company_uuid)
        return json.loads(result.json()), 200

