

DASHBOARD_PATHS = ['/cars_observed', '/cars_history', '/car_advert_add']


def dashboard_paths(request):
    return {'DASHBOARD_PATHS': DASHBOARD_PATHS}