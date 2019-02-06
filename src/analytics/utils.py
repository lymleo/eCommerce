
def get_client_ip(request):
    x_forwarted_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarted_for:
        print(x_forwarted_for)
        ip = x_forwarted_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', None)
    return ip