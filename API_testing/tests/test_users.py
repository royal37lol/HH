from http import HTTPStatus

import pytest
from assertions.users_assertion import should_be_posted_success, should_be_updated_success, should_be_deleted_success, \
    should_be_valid_users_response

from api.api_client import ApiClient
from api.users_api import get_users, get_user, get_users_page, post_user, put_user, delete_user
from assertions.assertion_base import assert_status_code, assert_response_body_fields, assert_bad_request, \
    assert_not_found, assert_empty_list, assert_schema, assert_not_exist
from models.user_models import UserOutSchema, UserCreateOutSchema, CustomUsrCreateOutSchema, \
    UserUpdateOutSchema, CustomUsrUpdateOutSchema, UserPageOutSchema
from utilities.files_utils import read_json_test_data, read_json_common_request_data


class Testusers:
    """
    Тесты /users
    """

    @pytest.fixture(scope='class')
    def client(self):
        return ApiClient()

    def test_get_users(self, client, request):
        """
        получение заранее заготовленных юзеров из базы с параметрами по-умолчанию,
        GET /users
        """
        # получаем объекты из базы
        response = get_users(client)

        # убеждаемся, что в ответ пришли объекты, которые мы ожидаем
        assert_status_code(response, HTTPStatus.OK)
        assert_response_body_fields(request, response)


    def test_get_users_not_exist_id(self, client):
        """
        попытка получить из базы объект с несуществующим id,
        GET /users
        """
        # пытаемся получить объект, несуществующий в системе
        response = get_users(client, 8523697415)

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_empty_list(response)

    def test_get_users_invalid_id(self, client):
        """
        попытка получить из базы объект с невалидным по типу id,
        GET /users
        """
        # пытаемся получить объект, отправив невалидный по типу параметр ids
        response = get_users(client, "kjdsf23321")

        # убеждаемся, что в ответ пришел пустой список
        assert_status_code(response, HTTPStatus.NOT_FOUND)
        assert_empty_list(response)

    def test_get_user(self, client, request):
        """
        получение заранее заготовленного объекта из базы,
        GET /users/{id}
        """
        # получаем единичный объект с сервера
        response = get_user(client, 2)

        # убеждаемся, что получен именно тот объект, который мы запросили
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, UserOutSchema)
        assert_response_body_fields(request, response)

    def test_get_users_page(self, client, request):
        """
        получение заранее заготовленного объекта из базы,
        GET /users/?page={id}
        """
        # получаем единичный объект с сервера
        response = get_users_page(client, 2)

        # убеждаемся, что получен именно тот объект, который мы запросили
        assert_status_code(response, HTTPStatus.OK)
        assert_schema(response, UserPageOutSchema)
        assert_response_body_fields(request, response)

    
    def test_post_user_empty_body(self, client, request):
        """
        запись объекта в базу с пустым телом,
        POST /users
        """
        # записываем объект в базу с пустым телом
        response = post_user(client, json={})

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.CREATED)
        assert_schema(response, UserCreateOutSchema)
        should_be_posted_success(request, client, response, exp_usr={})

    def test_post_user_with_full_body(self, client, request):
        """
        запись объекта в базу полностью заполненным телом,
        POST /users
        """
        # записываем объект в базу со всеми заполненными полями
        exp_usr = read_json_common_request_data("valid_post_user")
        response = post_user(client, json=exp_usr)

        # убеждаемся, что объект успешно записан в базу
        assert_status_code(response, HTTPStatus.CREATED)
        assert_schema(response, CustomUsrCreateOutSchema)
        should_be_posted_success(request, client, response, exp_usr)

    def test_put_user_with_full_body(self, client, request):
        """
        обновление всех полей объекта в базе,
        PUT /users/{id}
        """
        # записываем объект в базу со всеми заполненными полями
        post_usr = read_json_common_request_data("valid_post_user")
        response = post_user(client, json=post_usr)
        assert_status_code(response, HTTPStatus.CREATED)

        # обновляем значения всех полей этого объекта на новые
        put_usr = read_json_test_data(request)
        put_usr_id = response.json()['id']
        response = put_user(client, put_usr_id, json=put_usr)

    def test_delete_exist_user(self, client, request):
        """
        удаление сущестующего объекта,
        DELETE /users/{id}
        """
        # записываем объект в базу со всеми заполненными полями
        response = post_user(client, json=read_json_common_request_data("valid_post_user"))
        assert_status_code(response, HTTPStatus.CREATED)

        # удаляем этот объект
        usr_id = response.json()['id']
        response = delete_user(client, usr_id)