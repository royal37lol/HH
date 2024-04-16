from api import routes


def get_users(client, *ids):
    return client.get(routes.Routes.USERS, params={'id': ids} if ids else None)


def get_user(client, obj_id):
    return client.get(routes.Routes.USERS_ITEM.format(obj_id))

def get_users_page(client, page):
    return client.get(routes.Routes.USERS_PAG.format(page))


def post_user(client, **kwargs):
    return client.post(routes.Routes.USERS, **kwargs)


def put_user(client, obj_id, **kwargs):
    return client.put(routes.Routes.USERS_ITEM.format(obj_id), **kwargs)


def delete_user(client, obj_id):
    return client.delete(routes.Routes.USERS_ITEM.format(obj_id))
