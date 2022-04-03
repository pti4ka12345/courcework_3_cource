from flask import request
from flask_restx import Namespace, Resource, abort

from project.exceptions import ItemNotFound
from project.services.user_service import UserService
from project.setup_db import db
from project.tools.security import login_user, refresh_user_token

auth_ns = Namespace('auth')


@auth_ns.route('/login/')
class AuthView(Resource):
    def post(self):
        """User authorizations"""
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        try:
            user = UserService(db.session).get_item_by_email(email=req_json.get("email"))
            tokens = login_user(req_json, user)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")

    def put(self):
        """Refresh user token"""
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        try:
            tokens = refresh_user_token(req_json)
            return tokens, 200
        except ItemNotFound:
            abort(401, message="Authorization Error")


@auth_ns.route('/register/')
class AuthRegisterView(Resource):
    def post(self):
        """Create new user"""
        req_json = request.json
        if not req_json:
            abort(400, message='Bad Request')
        return UserService(db.session).create(req_json)