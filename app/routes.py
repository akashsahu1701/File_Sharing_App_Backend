def registered_routes(app):
    routes = get_all_routes()
    for route in routes:
        app.register_blueprint(route)


def get_all_routes():
    from app.api.users.handler import users_api
    from app.api.files.handler import files_api
    from app.api.auth.handler import auth_api

    return [users_api, files_api, auth_api]
