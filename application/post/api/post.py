import random
import re
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.db.models import Count
from django.utils.dateformat import DateFormat

from ...user.models import User, CafeteriaCollection, CounterCollection, PostCollection, EatCollection
from ..models import Post, Comment
from ...cafeteria.models import Counter, Dish, Cafeteria
from ...user.api.user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
def get_detail(request: HttpRequest):
    data = parse_request_data(request)

    post_id = data.get('id')
    post = Post.objects.get(id=post_id)
    return success_api_response({
        'title': post.title,
        'content': post.content,
        'id': post.id,
        'imgs': re.split(r'[\s\n\r]+', post.images),
        'user': {
            'id': post.author.id,
            'username': post.author.username,
            'avatar': post.author.avatar.url,
        },
        'createTime': post.created_time.strftime('%Y-%m-%d %H:%M:%S'),
        'collectCount': PostCollection.objects.filter(post=post).count(),
        'ateCount': EatCollection.objects.filter(post=post).count(),
        'commentCount': Comment.objects.filter(refer_post=post).count(),
    })


def get_recommended_posts(offset=0, limit=10):
    offset = int(offset)
    limit = int(limit)

    # 获取推荐的帖子
    recommended_posts = Post.objects \
        .annotate(collect_count=Count('collected_by'), eat_count=Count('eaten_by')) \
        .order_by('-collect_count', '-eat_count')

    # 将结果转换为列表并打乱顺序
    recommended_posts_list = list(recommended_posts)
    random.shuffle(recommended_posts_list)

    # 保证高点赞和高收藏的帖子优先显示
    sorted_recommended_posts = sorted(recommended_posts_list, key=lambda post: (post.collect_count, post.eat_count),
                                      reverse=True)

    # 返回指定范围内的推荐帖子
    return sorted_recommended_posts[offset:offset + limit]


@response_wrapper
@require_GET
def get_recommend(request: HttpRequest):
    data = parse_request_data(request)
    offset = data.get('offset', 0)

    limit = 10

    recommended_posts = get_recommended_posts(offset, limit)

    return success_api_response({
        'posts': [{
            'id': post.id,
            'name': post.title,
            'img': re.split(r'[\s\n\r]+', post.images)[0],
            'user': {
                'id': post.author.id,
                'username': post.author.username,
                'avatar': post.author.avatar.url,
            },
            'collectCount': PostCollection.objects.filter(post=post).count(),
            'ateCount': EatCollection.objects.filter(post=post).count(),
        } for post in recommended_posts]
    })


@response_wrapper
@require_POST
@jwt_auth()
def upload_info(request: HttpRequest):
    user = User.objects.get(id=request.user.id)
    data = parse_request_data(request)

    counter_id = data.get('counter_id')
    dish_name = data.get('dish_name')
    dish_price = data.get('dish_price')

    post_title = data.get('post_title')
    post_content = data.get('post_content')

    if not counter_id or not dish_name or not dish_price or not post_title or not post_content:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '缺少必要的参数')

    counter = Counter.objects.get(id=counter_id)
    if not counter:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '窗口不存在')

    dish = Dish.objects.create(name=dish_name, price=dish_price, counter=counter)
    post = Post.objects.create(dish=dish, title=post_title, content=post_content, author=user)

    return success_api_response({
        'info': '上传成功',
        'id': post.id
    })


@response_wrapper
@require_POST
@jwt_auth()
def upload_image(request: HttpRequest):
    user = User.objects.get(id=request.user.id)
    data = parse_request_data(request)

    post_id = data.get('id')
    images = request.FILES.getlist('images')

    if post_id is None or not images:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '缺少必要的参数')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '帖子不存在')

    if post.author != user:
        return failed_api_response(ErrorCode.REFUSE_ACCESS_ERROR, '无权操作')

    image_urls = []
    for image in images:
        img_url = upload_img_file(image, folder='post')
        if img_url:
            image_urls.append(img_url)

    if not image_urls:
        return failed_api_response(ErrorCode.SERVER_ERROR, '图片上传失败')

    if not post.images:
        post.images = ' '.join(image_urls)
    else:
        post.images += ' ' + ' '.join(image_urls)

    post.save()

    return success_api_response({
        'info': '上传成功',
        'id': post.id,
        'image_urls': image_urls
    })


@response_wrapper
@require_POST
@jwt_auth()
def delete_post(request: HttpRequest):
    user = User.objects.get(id=request.user.id)
    data = parse_request_data(request)

    post_id = data.get('id')
    if post_id is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '缺少必要的参数')

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGUMENT_ERROR, '帖子不存在')

    if post.author != user:
        return failed_api_response(ErrorCode.REFUSE_ACCESS_ERROR, '无权操作')

    post.delete()

    return success_api_response({'info': '删除成功'})