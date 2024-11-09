import allure


@allure.suite('Тесты на проверку метода логаута всех юзеров delete_v1_account_login_all')
@allure.sub_suite('Позитивные тесты')
class TestsDeleteV1AccountLoginAll:
    @allure.title("Разлогин всех пользователей")
    def test_delete_v1_account_login_all(self, auth_account_helper):
        auth_account_helper.dm_account_api.login_api.delete_v1_account_login_all()