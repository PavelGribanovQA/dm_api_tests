
from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from checkers.post_v1_account import PostV1Account
from dm_api_account.models.user_details_envelope import UserRole


def test_get_v1_account_auth(
        auth_account_helper
):
    with check_status_code_http():
        response = auth_account_helper.dm_account_api.account_api.get_v1_account()
        GetV1Account.check_response_values(response)
    # with soft_assertions():
    #     assert_that(response.resource.login).is_equal_to("paveltest")
    #     print("Прошла проверка логина")
    #     assert_that(response.resource.online).is_instance_of(datetime)
    #     print("Прошла проверка даты")
    #     assert_that(response.resource.roles).contains(UserRole.GUEST, UserRole.PLAYER)
    #     print("Прошла проверка ролей пользователя")



def test_get_v1_account_no_auth(
        account_helper
):
    with check_status_code_http(401, 'User must be authenticated'):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)
