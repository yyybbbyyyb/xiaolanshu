"""
注册
登陆
修改密码
修改头像
获取用户信息
"""
import re


from django.contrib.auth import authenticate, logout
from django.views.decorators.http import require_POST

from .user_auth import create_access_token, create_refresh_token
from ..models import User
from ...utils import *


@response_wrapper
@require_POST
def user_register(request: HttpRequest):
    data = parse_request_data(request)

    username = data.get('username')
    password = data.get('password')
    password_again = data.get('password_again')
    email = data.get('email')

    if not username or not password or not password_again or not email:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '内容未填写完整')

    # 检测数据合法性
    if User.objects.filter(username=username).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
    pattern = r'^[0-9a-zA-Z_]{5,15}$'
    if not re.match(pattern, username):
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名需为5-15位字母、数字或下划线')
    if User.objects.filter(email=email).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '邮箱已存在')
    if password != password_again:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '两次密码不一致')

    # 创建用户
    User.objects.create_user(username=username, password=password, email=email)

    return success_api_response({'message': '注册成功'})


@response_wrapper
@require_POST
def user_login(request: HttpRequest):
    data = parse_request_data(request)

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '内容未填写完整')

    user = authenticate(username=username, password=password)
    if user is None:
        if User.objects.filter(username=username).exists():
            return failed_api_response(ErrorCode.CANNOT_LOGIN_ERROR, '密码错误')
        else:
            return failed_api_response(ErrorCode.CANNOT_LOGIN_ERROR, '用户不存在')
    else:
        if user.isDelete:
            return failed_api_response(ErrorCode.CANNOT_LOGIN_ERROR, '用户已注销')
        else:
            token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return success_api_response({'message': '登录成功',
                                         'username': user.username,
                                         'token': token,
                                         'refresh_token': refresh_token})

