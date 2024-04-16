from enum import Enum


class Routes(str, Enum):
    USERS = '/users'
    USERS_ITEM = '/users/{}'
    USERS_PAG = '/users/?page={}'

    def __str__(self) -> str:
        return self.value
