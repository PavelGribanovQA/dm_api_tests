def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 400, "Не зарегистрированный пользователь  смог авторизоваться"

    account_helper.register_user_and_activate(login=login, password=password, email=email)

    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
