#  Bookstagram
Я изучаю fastAPI и Pytest, работая над этим проектом

---
## О проекте

Bookstagram - дает возможность зарегистрироваться и постить свои заметки о книгах, собирать лайки и комментарии.
Искать любые посты об интересных тебе книгах.


Используя этот проект, ты можешь потренироваться в использовании и тестировании api.
Позже я добавлю интересные задания.



---
## Описание методов
### User
---
### Create User - Метод регистрации пользователя

**Request**

POST
{url}/users

Параметры запроса (raw json)
| Параметр | Описание | Обязательность |
| --- | --- | --- |
| email | email пользователя | Да |
| password | Пароль пользователя | Да |
|  |  |  |

**Response**

- Успешная обработка запроса:    
    Код ответа - 201 Created    
    И  объект в формате json     
    ```json
    {
    "id": id, 
    "email": "email"
    }
    ```
    
- Неуспешная обработка запроса:
    - Данный пользователь уже зарегистрирован в системе        
        Код ответа - 409        
        И  объект в формате json         
        ```json
        {
        "detail": "User with this email is already registered"
        }
        ```
        
    - Не переданы обязательные параметры или переданы некорректные значения        
        Код ответа - 422        
        И  объект в формате json с указанием на ошибку

---
### Get User - Метод поиска пользователя

**Request**

GET

{{url}}/users/{{id}}

| Параметр | Описание | Обязательность | Тип |
| --- | --- | --- | --- |
| id | Уникальный идентификатор пользователя | Да | Integer |

**Response**

- Успешная обработка запроса:
    
    Код ответа - 200 Ok
    
    И  объект в формате json 
    
    ```json
    {
        "id": id,
        "email": "email"
    }
    ```
    
- Неуспешная обработка запроса:
    - Данный пользователь Не зарегистрирован в системе
        
        Код ответа - 404 Not Found
        
        И  объект в формате json 
        
        ```json
        {
        "detail": "User with id {{id}} was not found"
        }
        ```
        
    - Не переданы обязательные параметры
        
        Код ответа - 405 Method Not Allowed
        
        И  объект в формате json
        
        ```json
         {
        "detail": "Method Not Allowed"
        }
        ```
        

    - В параметре передано невалидное значение
    
        Код ответа - 422 Unprocessable Entity
    
        И  объект в формате json с указанием на ошибку

---





### Authentication

### Login User - Метод авторизации пользователя

**Request**

POST

{url}/login 

Параметры запроса (form-data)

| Параметр | Описание | Обязательность |
| --- | --- | --- |
| username  | email пользователя | Да |
| password | Пароль пользователя | Да |

**Response**

- Успешная обработка запроса:
    
    Код ответа - 200 Ок
    
    И  объект в формате json 
    
    ```json
    {
    "access_token": access_token, 
    "token_type": "bearer"
    }
    ```
    
- Неуспешная обработка запроса:
    - Данные пользователя не зарегистрированы в системе
        
        Код ответа - 404
        
        И  объект в формате json 
        
        ```json
        {
        "detail": "Invalid credentials"
        }
        ```
        
    - Не переданы обязательные параметры
        
        Код ответа - 422
        
        И  объект в формате json с указанием на отсутствующий параметр


