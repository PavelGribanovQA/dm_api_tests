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


# 4. сценарий для метода put_v1_account_email - Смена емейла
def test_put_v1_account_email():
    # Объявляем креды
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    dm_api_configuration = DMApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)

    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    login = 'pt140'
    password = '123456789'
    email = f'{login}@mail.com'

    # Регистрация нового пользователя с активацией
    account_helper.register_user_and_activate(login=login, password=password, email=email)

    # Авторизоваться
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Меняем емейл
    account_helper.change_user_email(login=login, password=password, email=email)

    # Пытаемся войти, получаем 403
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, "Пользователь СМОГ авторизоваться!!!"

    # На почте находим токен по новому емейлу для подтверждения смены емейла
    account_helper.activate_new_user(login=login, password=password, email=email)

    # Логинимся
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"
