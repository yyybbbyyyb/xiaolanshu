"""
用户收藏、吃过等行为
"""

import re
from django.views.decorators.http import require_POST, require_http_methods, require_GET

from ..models import User, CafeteriaCollection, CounterCollection, PostCollection, EatCollection
from ...post.models import Post
from ...cafeteria.models import Counter, Cafeteria, Dish
from .user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
@jwt_auth()
def get_user_action_info(request: HttpRequest):
    """
    获取用户收藏、吃过等行为
    """
    user = User.objects.filter(id=request.user.id).first()

    cafeterias = CafeteriaCollection.objects.filter(collector=user)
    counters = CounterCollection.objects.filter(collector=user)
    posts = PostCollection.objects.filter(collector=user)
    eats = EatCollection.objects.filter(collector=user)
    posts_upload = Post.objects.filter(author=user)

    return success_api_response({
        'collectDishesId': [post.post.id for post in posts],
        'collectCountersId': [counter.counter.id for counter in counters],
        'collectCafeteriasId': [cafeteria.cafeteria.id for cafeteria in cafeterias],
        'ateId': [eat.post.id for eat in eats],
        'uploadPostId': [post.id for post in posts_upload],
    })


@response_wrapper
@require_GET
@jwt_auth()
def get_collect_dishes_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    posts = PostCollection.objects.filter(collector=user)

    post_list = []
    for post in posts[offset:offset + 5]:
        post_list.append({
            'id': post.post.id,
            'name': post.post.title,
            'img': re.split(r'[\s\n\r]+', post.post.images)[0],
            'collectCount': PostCollection.objects.filter(post=post.post).count(),
            'ateCount': EatCollection.objects.filter(post=post.post).count(),
            'user': {
                'id': post.collector.id,
                'username': post.collector.username,
                'avatar': post.collector.avatar.url,
            },
        })

    return success_api_response({'info': post_list})


@response_wrapper
@require_GET
@jwt_auth()
def get_collect_counters_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    counters = CounterCollection.objects.filter(collector=user)

    counter_list = []
    for counter in counters[offset:offset + 5]:
        counter_list.append({
            'id': counter.counter.id,
            'name': counter.counter.name,
            'img': counter.counter.image.url,
            'collectCount': CounterCollection.objects.filter(counter=counter.counter).count(),
            'floor': counter.counter.floor,
        })

    return success_api_response({'info': counter_list})


@response_wrapper
@require_GET
@jwt_auth()
def get_collect_cafeterias_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    cafeterias = CafeteriaCollection.objects.filter(collector=user)

    cafeteria_list = []
    for cafeteria in cafeterias[offset:offset + 5]:
        cafeteria_list.append({
            'id': cafeteria.cafeteria.id,
            'name': cafeteria.cafeteria.name,
            'img': cafeteria.cafeteria.image.url,
            'collectCount': CafeteriaCollection.objects.filter(cafeteria=cafeteria.cafeteria).count(),
        })

    return success_api_response({'info': cafeteria_list})


@response_wrapper
@require_GET
@jwt_auth()
def get_ate_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    eats = EatCollection.objects.filter(collector=user)

    post_list = []
    for eat in eats[offset:offset + 5]:
        post_list.append({
            'id': eat.post.id,
            'name': eat.post.title,
            'img': re.split(r'[\s\n\r]+', eat.post.images)[0],
            'collectCount': PostCollection.objects.filter(post=eat.post).count(),
            'ateCount': EatCollection.objects.filter(post=eat.post).count(),
            'user': {
                'id': eat.collector.id,
                'username': eat.collector.username,
                'avatar': eat.collector.avatar.url,
            },
        })

    return success_api_response({'info': post_list})


@response_wrapper
@require_GET
@jwt_auth()
def get_post_list(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    posts = Post.objects.filter(author=user)

    post_list = []
    for post in posts[offset:offset + 5]:
        post_list.append({
            'id': post.id,
            'name': post.title,
            'img': re.split(r'[\s\n\r]+', post.images)[0],
            'collectCount': PostCollection.objects.filter(post=post).count(),
            'ateCount': EatCollection.objects.filter(post=post).count(),
            'user': {
                'id': post.author.id,
                'username': post.author.username,
                'avatar': post.author.avatar.url,
            },
        })

    return success_api_response({'info': post_list})


@response_wrapper
@require_POST
@jwt_auth()
def collect_post(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    post_id = data.get('post_id')
    if not post_id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '帖子不存在')

    post = Post.objects.get(id=post_id)

    if PostCollection.objects.filter(collector=user, post=post).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '已收藏过该帖子')

    PostCollection.objects.create(collector=user, post=post)

    return success_api_response({'info': '帖子收藏成功'})


@response_wrapper
@require_POST
@jwt_auth()
def collect_counter(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    counter_id = data.get('id')
    if not counter_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    counter = Counter.objects.get(id=counter_id)

    if CounterCollection.objects.filter(collector=user, counter=counter).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '已收藏过该窗口')

    CounterCollection.objects.create(collector=user, counter=counter)

    return success_api_response({'info': '窗口收藏成功'})


@response_wrapper
@require_POST
@jwt_auth()
def collect_cafeteria(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    cafeteria_id = data.get('id')
    if not cafeteria_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    cafeteria = Cafeteria.objects.get(id=cafeteria_id)

    if CafeteriaCollection.objects.filter(collector=user, cafeteria=cafeteria).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '已收藏过该食堂')

    CafeteriaCollection.objects.create(collector=user, cafeteria=cafeteria)

    return success_api_response({'info': '食堂收藏成功'})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth()
def cancel_collect_post(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)
    print(data)

    post_id = data.get('post_id')
    if not post_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    post = Post.objects.get(id=post_id)

    if not PostCollection.objects.filter(collector=user, post=post).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '未收藏过该帖子')

    PostCollection.objects.filter(collector=user, post=post).delete()

    return success_api_response({'info': '帖子取消收藏成功'})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth()
def cancel_collect_counter(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    counter_id = data.get('id')
    if not counter_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    counter = Counter.objects.get(id=counter_id)

    if not CounterCollection.objects.filter(collector=user, counter=counter).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '未收藏过该窗口')

    CounterCollection.objects.filter(collector=user, counter=counter).delete()

    return success_api_response({'info': '窗口取消收藏成功'})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth()
def cancel_collect_cafeteria(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    cafeteria_id = data.get('id')
    if not cafeteria_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    cafeteria = Cafeteria.objects.get(id=cafeteria_id)

    if not CafeteriaCollection.objects.filter(collector=user, cafeteria=cafeteria).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '未收藏过该食堂')

    CafeteriaCollection.objects.filter(collector=user, cafeteria=cafeteria).delete()

    return success_api_response({'info': '食堂取消收藏成功'})


@response_wrapper
@require_POST
@jwt_auth()
def eat(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    post_id = data.get('post_id')

    if not post_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    post = Post.objects.get(id=post_id)

    if EatCollection.objects.filter(collector=user, post=post).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '已吃过该菜品')

    EatCollection.objects.create(collector=user, post=post)

    return success_api_response({'info': '菜品吃过成功'})


@response_wrapper
@require_http_methods(['DELETE'])
@jwt_auth()
def cancel_eat(request: HttpRequest):
    user = User.objects.filter(id=request.user.id).first()

    data = parse_request_data(request)

    post_id = data.get('post_id')
    if not post_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传递参数')

    post = Post.objects.get(id=post_id)

    if not EatCollection.objects.filter(collector=user, post=post).exists():
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '未吃过该菜品')

    EatCollection.objects.filter(collector=user, post=post).delete()

    return success_api_response({'info': '菜品取消吃过成功'})
