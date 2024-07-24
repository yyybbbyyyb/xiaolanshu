"""
用户收藏、吃过等行为
"""

from django.views.decorators.http import require_POST, require_http_methods, require_GET

from ..models import User, CafeteriaCollection, CounterCollection, PostCollection, EatCollection
from .user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
@jwt_auth()
def get_user_action_info(request: HttpRequest):
    """
    获取用户收藏、吃过等行为
    """
    user = request.user

    cafeterias = CafeteriaCollection.objects.filter(collector=user)
    counters = CounterCollection.objects.filter(collector=user)
    posts = PostCollection.objects.filter(collector=user)
    eats = EatCollection.objects.filter(collector=user)

    return success_api_response({
        'collectDishesId': [post.post.id for post in posts],
        'collectCountersId': [counter.counter.id for counter in counters],
        'collectCafeteriasId': [cafeteria.cafeteria.id for cafeteria in cafeterias],
        'ateId': [eat.post.id for eat in eats],
    })

