def test_post_v1_account_password(account_helper, prepare_user):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = "987654321"
    account_helper.register_user_and_activate(login=login, password=password, email=email)
    account_helper.user_login(login=login, password=password)
    account_helper.change_password(login=login, email=email, old_password=password, new_password=new_password)
    account_helper.user_login(login=login, password=new_password)