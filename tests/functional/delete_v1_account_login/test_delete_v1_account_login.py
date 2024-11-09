import allure


@allure.suite('Тесты на проверку метода delete_v1_account_login')
@allure.sub_suite('Позитивные тесты')
class TestsDeleteV1AccountLogin:
    @allure.title("Разлогин выбранного пользователя")
    def test_delete_v1_account_login(self, auth_account_helper):
        auth_account_helper.dm_account_api.login_api.delete_v1_account_login()

