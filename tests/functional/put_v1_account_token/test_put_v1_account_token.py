def test_put_v1_account_token(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_user_without_activate(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, "Пользователь смог авторизоваться без активации!"

    account_helper.activate_new_user(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
