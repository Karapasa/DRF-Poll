def get_user_ip(request):
    """Определить ip пользователя"""
    x_forward_for = request.Meta.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.Meta.get('REMOTE_ADDR')
    return ip