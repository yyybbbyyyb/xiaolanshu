from django.views.decorators.http import require_POST, require_http_methods, require_GET

from ..models import Cafeteria, Counter
from ...user.api.user_auth import jwt_auth
from ...utils import *


@response_wrapper
@require_GET
@jwt_auth(allow_anonymous=True)
def get_counters(request: HttpRequest):
    """
    获取食堂的窗口信息
    """
    date = parse_request_data(request)

    cafeteria_name = date.get('name')
    if not cafeteria_name:
        return failed_api_response(ErrorCode.REQUIRED_ARG_IS_NULL_ERROR, '为传入食堂名')

    cafeteria = Cafeteria.objects.get(name=cafeteria_name)
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
            'collectCount': 10,
        })