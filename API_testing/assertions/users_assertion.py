from http import HTTPStatus

from api.users_api import get_user
from assertions.assertion_base import assert_response_body_fields, assert_status_code, assert_response_body_value
from utilities.files_utils import read_json_test_data


def should_be_valid_users_response(request, response, param):
    # убеждаемся, что в ответе столько объектов, сколько мы ожидаем
    exp = read_json_test_data(request)[param['index']]
    exp_len, act_len = len(exp), len(response.json())
    assert_response_body_value(response, exp_len, act_len,
                               text="ОЖИДАЕМОЕ КОЛИЧЕСТВО ОБЪЕКТОВ НЕ СОВПАЛО С ФАКТИЧЕСКИМ")

    # убеждаемся в корректности значений полей полученных объектов
    assert_response_body_fields(request, response, exp)


def should_be_posted_success(request, client, response, exp_usr):
    # убеждаемся в корректности значений полей тела ответа
    assert_response_body_fields(request, response, exp_usr)


def should_be_updated_success(request, client, response, exp_usr):
    # убеждаемся в корректности значений полей тела ответа
    assert_response_body_fields(request, response, exp_usr, rmv_ids=False)

    # убеждаемся, что объект корректно обновлен на сервере
    response = get_user(client, exp_usr['id'])
    assert_status_code(response, HTTPStatus.OK)
    assert exp_usr == response.json()


def should_be_deleted_success(request, response, usr_id):
    assert_response_body_fields(request, response, rmv_ids=False)
