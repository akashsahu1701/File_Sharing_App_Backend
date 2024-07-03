def registered_routes(app):
    routes = get_all_routes()
    for route in routes:
        app.register_blueprint(route)


def get_all_routes():
    from app.api.users.routes import users_api
    from app.api.auth.routes import auth_api

    return [users_api, auth_api]
