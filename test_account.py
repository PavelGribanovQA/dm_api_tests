import requests
import json
import pytest
from faker import Faker
from client import Client


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def generate_user():
    fake = Faker("ru_RU")

    return {
        "login": fake.user_name(),
        "email": fake.email(),
        "password": fake.password()
    }


# @pytest.fixture()
# def set_url():
#     return "http://5.63.153.31:5051/v1/account"
#
#
# @pytest.fixture()
# def headers():
#     return {
#         'accept': '*/*',
#         'Content-Type': 'application/json'
#     }
#

data = [
    # короткий логин
    {
        "login": "l",
        "email": "email_12345@mail.ru",
        "password": "12345678"
    },
    # невалидный имейл
    {
        "login": "login_12345678902",
        "email": "e",
        "password": "12345678"
    },
    # короткий пароль
    {
        "login": "login_12345678902",
        "email": "email_12345@mail.ru",
        "password": "1"
    }
]

@pytest.mark.parametrize('data', data)
def test_post_v1_account(data, client):
    response = client.register_users(data)
    assert response.status_code == 200, "Статус код ответа должен быть 200"
