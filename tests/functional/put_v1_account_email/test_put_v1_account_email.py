from json import loads

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


# 4. сценарий для метода put_v1_account_email - Смена емейла
def test_post_v1_account():
    # Объявляем креды

    account_api = AccountApi(host='http://5.63.153.31:5051')
    login_api = LoginApi(host='http://5.63.153.31:5051')
    mailhog_api = MailhogApi(host='http://5.63.153.31:5025')

    login = 'pt44'
    password = '123456789'
    email = f'{login}@mail.com'
    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }
    # Регистрация нового пользователя
    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"Пользователь не был создан {response.json()}"

    # Получить письма из почтового сервера
    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены"

    # Получить активационный токен

    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен"

    # Активация пользователя
    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован"

    # Авторизоваться

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться"

    # Меняем емейл

    response = account_api.put_v1_account_email(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Email не был заменен"

    # Пытаемся войти, получаем 403

    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 403, "Пользователь СМОГ авторизоваться!!!"

    # На почте находим токен по новому емейлу для подтверждения смены емейла

    response = mailhog_api.get_api_v2_messages()
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Письма не были получены СМЕНА ЕМАИЛ"

    token = get_activation_token_by_login(login, response)

    assert token is not None, f"Токен для пользователя {login}, не был получен СМЕНА ЕМАИЛ"

    # Активируем этот токен

    response = account_api.put_v1_account_token(token=token)

    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не был активирован СМЕНА ЕМАИЛ"

    # Логинимся
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, "Пользователь не смог авторизоваться СМЕНА ЕМАИЛ"


def get_activation_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
    return token
