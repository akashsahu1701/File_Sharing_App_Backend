def validate_users_permissions(claims: dict, permissions: list[str]) -> bool:
    for permission in claims["permissions"]:
        if permission in permissions:
            return True

    return False


# def validate_users_permissions(user_id: int, user_ids: list[int]) -> bool:
#     return user_id in user_ids
