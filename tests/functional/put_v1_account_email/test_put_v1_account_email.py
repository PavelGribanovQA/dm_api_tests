import allure

from checkers.http_checkers import check_status_code_http

@allure.suite('Тесты на проверку метода put_v1_account_email')
@allure.sub_suite('Позитивные тесты')
class TestsPutV1AccountEmail:
    @allure.title("Смена почты пользователя")
    def test_put_v1_account_email(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_user_and_activate(login=login, password=password, email=email)

        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"

        account_helper.change_user_email(login=login, password=password, email=email)

        with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
            account_helper.user_login(login=login, password=password, validate_response=False)

        account_helper.activate_new_user(login=login, password=password, email=email)

        response = account_helper.user_login(login=login, password=password)
        assert response.status_code == 200, "Пользователь не смог авторизоваться"
