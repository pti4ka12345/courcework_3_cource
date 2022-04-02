from flask import request
from flask_restx import Resource, Namespace, reqparse, abort

from project.exceptions import ItemNotFound

from project.services.user_service import UserService
from project.setup_db import db
from project.tools.security import auth_required, get_id_from_token

user_ns = Namespace('user')
parser = reqparse.RequestParser()
parser.add_argument('username', type=str)
parser.add_argument('role', type=str)


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    @user_ns.response(200, "OK")
    @user_ns.response(400, "User not found")
    def get(self):
        user_id = get_id_from_token()
        try:
            return UserService(db.session).get_item_by_id(user_id)
        except ItemNotFound:
            abort(404, message="User not found")
    #
    # def patch(self, user_id: int):
    #     req_json = request.json
    #     if not req_json:
    #         abort(404, message="Bad Request")
    #     if not req_json.get('id'):
    #         req_json['id'] = user_id
    #     try:
    #         return UserService(db.session).update(req_json)
    #     except ItemNotFound:
    #         abort(404, message="User not found")

# @user_ns.route('/password/')
# class UserPatchView(Resource):
#     @auth_required
#     @user_ns.response(200, "OK")
#     @user_ns.response(400, "User not found")
#     def put(self):
#         req_json = request.json
#         if not req_json:
#             abort(404, message="Bad Request")
#         if not req_json.get('password_1') or not req_json.get('password_2'):
#             abort(404, message="Bad Request")
#         if not req_json.get('id'):
#             req_json['id'] = user_id
#         try:
#             return UserService(db.session).update_pass(req_json)
#         except ItemNotFound:
#             abort(404, message="User not found")