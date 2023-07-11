"""Custom context processor"""

def dashboard_paths(request):
    """
    Function returns available urls that are conditioning the rendering of user_dashboard_navbar.html

    """
    return {
            'DASHBOARD_PATHS': ['/cars_observed', '/cars_history', '/car_advert_add', '/car_advert_data']
    }
