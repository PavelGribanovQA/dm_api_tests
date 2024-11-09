import allure

from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from dm_api_account.models.user_details_envelope import UserRole

@allure.suite('Тесты на проверку метода get_v1_account')
class TestsGetV1Account:
    @allure.sub_suite('Позитивные тесты')
    @allure.title("Проверка получения данных авторизованного пользователя")
    def test_get_v1_account_auth(
            self,
            auth_account_helper
    ):
        with check_status_code_http():
            response = auth_account_helper.dm_account_api.account_api.get_v1_account()
            GetV1Account.check_response_values(response)

    @allure.sub_suite('Негативные тесты')
    @allure.title("Проверка получения данных не авторизованного пользователя")
    def test_get_v1_account_no_auth(
            self,
            account_helper
    ):
        with check_status_code_http(401, 'User must be authenticated'):
            account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
