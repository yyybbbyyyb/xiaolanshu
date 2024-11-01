import re
from django.views.decorators.http import require_POST, require_http_methods, require_GET

from ...user.models import User, CafeteriaCollection, CounterCollection, PostCollection, EatCollection
from ..models import Cafeteria, Counter, Dish
from ...post.models import Post
from ...user.api.user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
def get_all_cafeterias(request: HttpRequest):
    """
    获取所有食堂信息
    """
    cafeterias = Cafeteria.objects.all()
    cafeterias_info = []
    for cafeteria in cafeterias:
        cafeterias_info.append({
            'id': cafeteria.id,
            'name': cafeteria.name,
            'img': cafeteria.image.url,
            'collectCount': CafeteriaCollection.objects.filter(cafeteria=cafeteria).count(),
        })

    return success_api_response({
        'info': cafeterias_info
    })


@response_wrapper
@require_GET
def get_counters(request: HttpRequest):
    """
    获取食堂的窗口信息
    """
    data = parse_request_data(request)

    cafeteria_id = data.get('cafeteriaId')
    if not cafeteria_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '为传入食堂名')

    cafeteria = Cafeteria.objects.get(id=cafeteria_id)
    if not cafeteria:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '食堂不存在')

    counters = Counter.objects.filter(cafeteria=cafeteria)
    counters_info = []
    for counter in counters:
        counters_info.append({
            'id': counter.id,
            'name': counter.name,
            'img': counter.image.url,
            'floor': counter.floor,
            'collectCount': CounterCollection.objects.filter(counter=counter).count(),
        })

    return success_api_response({
        "info": counters_info
    })


@response_wrapper
@require_GET
def get_dishes(request: HttpRequest):
    """
    获取窗口的菜品信息, 以帖子的形式返回
    """
    data = parse_request_data(request)

    counter_id = data.get('counterId')
    if not counter_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传入窗口id')

    counter = Counter.objects.get(id=counter_id)
    if not counter:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '窗口不存在')

    dishes = Dish.objects.filter(counter=counter)

    post_info = []

    for dish in dishes:
        posts = Post.objects.filter(dish=dish)
        for post in posts:
            post_info.append({
                'id': post.id,
                'name': post.title,
                'img': re.split(r'[\s\n\r]+', post.images)[0],
                'collectCount': PostCollection.objects.filter(post=post).count(),
                'ateCount': EatCollection.objects.filter(post=post).count(),
                'user': {
                    'id': post.author.id,
                    'username': post.author.username,
                    'avatar': post.author.avatar.url,
                }
            })

    return success_api_response({
        'info': post_info
    })


@response_wrapper
def get_cafeteria(request: HttpRequest):
    """
    获取食堂信息
    """
    data = parse_request_data(request)

    cafeteria_id = data.get('cafeteriaId')
    if not cafeteria_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传入食堂id')

    cafeteria = Cafeteria.objects.get(id=cafeteria_id)
    if not cafeteria:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '食堂不存在')

    return success_api_response({
        'id': cafeteria.id,
        'name': cafeteria.name,
        'img': cafeteria.image.url,
        'collectCount': CafeteriaCollection.objects.filter(cafeteria=cafeteria).count(),
    })


@response_wrapper
@require_GET
def get_counter(request: HttpRequest):
    """
    获取窗口信息
    """
    data = parse_request_data(request)

    counter_id = data.get('counterId')
    if not counter_id:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '未传入窗口id')

    counter = Counter.objects.get(id=counter_id)
    if not counter:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '窗口不存在')

    return success_api_response({
        'id': counter.id,
        'name': counter.name,
        'img': counter.image.url,
        'floor': counter.floor,
        'collectCount': CounterCollection.objects.filter(counter=counter).count(),
    })



