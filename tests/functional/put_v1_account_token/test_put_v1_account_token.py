from json import loads

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as MailhogConfiguration
from restclient.configuration import Configuration as DMApiConfiguration
from services.dm_api_account import DMApiAccount
from services.api_mailhog import MailHogApi

import structlog

structlog.configure(
    processors={
        structlog.processors.JSONRenderer(
            indent=6,
            ensure_ascii=True,
            sort_keys=True
        )
    }
)


# 3. сценарий для метода put_v1_account_token - Activate registered user
def test_put_v1_account_token():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DMApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'pt162'
    password = '123456789'
    email = f'{login}@mail.com'

    # Регистрация нового пользователя
    account_helper.register_user_without_activate(login=login, password=password, email=email)

    # Проверить, что пользователь не может залогиниться без активации
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, "Пользователь смог авторизоваться без активации!"

    account_helper.activate_new_user(login=login, password=password, email=email)

    # Авторизоваться
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
