from checkers.http_checkers import check_status_code_http


def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    with check_status_code_http(400, "One or more validation errors occurred."):
        account_helper.user_login(login=login, password=password)

    account_helper.register_user_and_activate(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
