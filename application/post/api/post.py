from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.db.models import Count

from ...user.models import User, CafeteriaCollection, CounterCollection, PostCollection, EatCollection
from ..models import Post, Comment
from ...user.api.user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
@jwt_auth()
def get_detail(request: HttpRequest):
    data = parse_request_data(request)

    post_id = data.get('id')
    post = Post.objects.get(id=post_id)
    return success_api_response({
        'title': post.title,
        'content': post.content,
        'id': post.id,
        'img': post.images.split(' '),
        'user': {
            'id': post.author.id,
            'username': post.author.username,
            'avatar': post.author.avatar.url,
        },
        'created_time': post.created_time,
        'collectCount': PostCollection.objects.filter(post=post).count(),
        'ateCount': EatCollection.objects.filter(post=post).count(),
        'commentCount': Comment.objects.filter(refer_post=post).count(),
    })


def get_recommended_posts(user, offset=0, limit=10):
    # 基于用户的收藏和吃过的帖子来推荐
    collected_posts = Post.objects.filter(collected_by=user)
    eaten_posts = Post.objects.filter(eaten_by=user)

    # 获取推荐的帖子
    recommended_posts = Post.objects \
                            .annotate(collect_count=Count('collected_by'), eat_count=Count('eaten_by')) \
                            .exclude(id__in=collected_posts) \
                            .exclude(id__in=eaten_posts) \
                            .order_by('-collect_count', '-eat_count')[offset:offset + limit]

    return recommended_posts


@response_wrapper
@require_GET
@jwt_auth()
def get_recommend(request: HttpRequest):
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    user = User.objects.get(id=request.user.id)
    limit = 10

    recommended_posts = get_recommended_posts(user, offset, limit)
    return success_api_response({
        'posts': [{
            'id': post.id,
            'name': post.title,
            'img': post.images.split(' ')[0],
            'collectCount': PostCollection.objects.filter(post=post).count(),
            'ateCount': EatCollection.objects.filter(post=post).count(),
        } for post in recommended_posts]
    })


