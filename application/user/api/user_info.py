"""
注册
登陆
登出
注销
修改头像
修改密码
修改用户名、邮箱、性别、简介、学号等信息
获取当前登陆用户信息
根据用户id获取用户信息
"""
import re


from django.contrib.auth import authenticate, logout
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.utils import timezone

from .user_auth import create_access_token, create_refresh_token, jwt_auth
from ..models import User, Auth
from ...utils import *


@response_wrapper
@require_POST
def user_register(request: HttpRequest):
    data = parse_request_data(request)

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if not username or not password or not email:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '内容未填写完整')

    # 检测数据合法性
    if User.objects.filter(username=username).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
    pattern = r'^[0-9a-zA-Z_]{5,15}$'
    if not re.match(pattern, username):
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名需为5-15位字母、数字或下划线')
    if User.objects.filter(email=email).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '邮箱已存在')

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
            return failed_api_response(ErrorCode.CANNOT_LOGIN_ERROR, '用户已注销, 请联系管理员')
        else:
            token = create_access_token(user)
            refresh_token = create_refresh_token(user)
            return success_api_response({'message': '登录成功',
                                         'username': user.username,
                                         'token': token,
                                         'refresh_token': refresh_token})


@response_wrapper
@jwt_auth()
@require_POST
def user_logout(request: HttpRequest):
    Auth.objects.filter(user=request.user).delete()
    return success_api_response({'message': '登出成功'})


@response_wrapper
@jwt_auth()
@require_http_methods(['DELETE'])
def user_delete(request: HttpRequest):
    user = User(request.user)
    if user.avatar != 'media/avatar/default.png':
        user.avatar.delete()
    logout(request)
    user.avatar = 'media/avatar/default.png'
    user.isDelete = True
    user.intorduction = '用户已注销'
    user.save()
    Auth.objects.filter(user=user).delete()
    return success_api_response({'message': '注销成功'})


@response_wrapper
@jwt_auth()
@require_POST
def user_change_avatar(request: HttpRequest):
    user = User(request.user)
    avatar = request.FILES.get('avatar')

    if avatar:
        if avatar.size > 2 * 1024 * 1024:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '头像图片大小不能超过2MB')
        if user.avatar != 'avatar/default.png':
            user.avatar.delete()
        avatar.name = user.username + str(timezone.now()) + '.png'
        user.avatar = avatar
    else:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '头像未上传')

    user.save()
    return success_api_response({'message': '头像修改成功', 'url': user.avatar.url})


@response_wrapper
@jwt_auth()
@require_POST
def user_change_password(request: HttpRequest):
    data = parse_request_data(request)

    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '内容未填写完整')

    user = authenticate(username=request.user.username, password=old_password)
    if user is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '原密码错误')
    else:
        user.set_password(new_password)
        user.save()
        return success_api_response({'message': '密码修改成功'})


@response_wrapper
@jwt_auth()
@require_http_methods(['PUT'])
def user_change_info(request: HttpRequest):
    user = User(request.user)
    data = parse_request_data(request)

    username = data.get('username')
    email = data.get('email')
    gender = data.get('gender')
    introduction = data.get('introduction')
    student_id = data.get('student_id')

    if username:
        if User.objects.filter(username=username).exists():
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名已存在')
        else:
            pattern = r'^[0-9a-zA-Z_]{5,15}$'
            if not re.match(pattern, username):
                return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户名需为5-15位字母、数字或下划线')
            user.username = username

    if email:
        if User.objects.filter(email=email).exists():
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '邮箱已存在')
        user.email = email

    if gender:
        user.gender = gender

    if introduction:
        user.introduction = introduction

    if student_id:
        if User.objects.filter(student_id=student_id).exists():
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '学号已存在')
        user.student_id = student_id

    user.save()
    return success_api_response({'message': '信息修改成功'})


@response_wrapper
@jwt_auth()
@require_GET
def user_get_info(request: HttpRequest):
    user = User(request.user)
    return success_api_response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'student_id': user.student_id,
        'gender': user.gender,
        'introduction': user.introduction,
        'avatar': user.avatar.url,
    })


@response_wrapper
@require_GET
def user_get_info_by_id(request: HttpRequest, user_id: int):
    target_user = User.objects.filter(id=user_id)
    if not target_user.exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '用户不存在')
    return success_api_response({
        'id': target_user[0].id,
        'username': target_user[0].username,
        'email': target_user[0].email,
        'student_id': target_user[0].student_id,
        'gender': target_user[0].gender,
        'introduction': target_user[0].introduction,
        'avatar': target_user[0].avatar.url,
    })
