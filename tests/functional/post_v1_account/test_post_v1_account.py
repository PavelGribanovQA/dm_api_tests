import datetime
import pytest
from hamcrest import (
    assert_that,
    has_property,
    starts_with,
    all_of,
    instance_of,
    has_properties,
    equal_to,
)

from checkers.http_checkers import check_status_code_http


def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user_and_activate(login=login, password=password, email=email)
    response = account_helper.user_login(login=login, password=password, validate_response=True)
    assert_that(
        response, all_of(
            has_property("resource", has_property("login", starts_with("paveltest"))),
            has_property("resource", has_property("registration", instance_of(datetime.datetime))),
            has_property(
                "resource", has_properties(
                    {
                        "rating": has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    }
                )
            )
        )
    )
    print(response)


@pytest.mark.parametrize(
    "login, email, password, error_message, expected_status_code",
    [
        # 1. Короткий пароль (менее 6 символов)
        ("valid_login", "validemail@example.com", "12345", "Validation failed", 400),

        # 2. Невалидный email (без символа '@')
        ("valid_login", "invalidemail.com", "valid_password123", "Validation failed", 400),

        # 3. Невалидный логин (1 символ)
        ("l", "validemail@example.com", "valid_password123", "Validation failed", 400),
    ]
)
def test_post_v1_account_invalid_credentials(
        account_helper,
        login,
        email,
        password,
        error_message,
        expected_status_code
):
    # Используем контекстный менеджер для проверки ожидаемого статуса и сообщения об ошибке
    with check_status_code_http(expected_status_code=expected_status_code, expected_massage=error_message):
        response = account_helper.register_user_without_activate(login=login, password=password, email=email)
