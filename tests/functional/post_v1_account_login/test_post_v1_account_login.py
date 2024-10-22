from json import loads
from pprint import pprint

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


# 4. сценарий для метода post_v1_account_login - Authenticate via credentials
def test_post_v1_account_login():
    # Объявляем креды

    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DMApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'pt132'
    password = '123456789'
    email = f'{login}@mail.com'

    # Проверить что не созданный пользователь не может войти
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 400, "Не зарегистрированный пользователь  смог авторизоваться"
    # Регистрация и кстивация
    account_helper.register_user_and_activate(login=login, password=password, email=email)
    # Логинемся
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
