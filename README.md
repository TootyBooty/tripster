# tripster

для запуска приложения в docker необходимо из корневой директории использовать команду:

    make up

Воспользоваться приложением можно через документацию по url:

    http://127.0.0.1:8000/docs

Авторизация в Swagger:

-  <img width="580" alt="image" src="https://github.com/TootyBooty/tripster/assets/96263024/5ab25b5e-7fe1-4831-aad2-f47dc4da3817">


Основные возможности:
  - Создание пользователя:
    
        curl -X 'POST' \
        'http://127.0.0.1:8000/api/v1/auth/register' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "name": "kirill",
        "email": "e@mail.com",
        "password": "qwerty"
        }'

  - Получение токена авторизации:
   
          curl -X 'POST' \
          'http://127.0.0.1:8000/api/v1/auth/token' \
          -H 'accept: application/json' \
          -H 'Content-Type: application/x-www-form-urlencoded' \
          -d 'grant_type=&username=e%40mail.com&password=qwerty&scope=&client_id=&client_secret='

  - Получение списка публикаций по заданным фильтрам:
   
            curl -X 'GET' \
          'http://127.0.0.1:8000/api/v1/publication/?order_by=created_at&ascending=false' \
          -H 'accept: application/json'

  - Создание публикации:
   
            curl -X 'POST' \
            'http://127.0.0.1:8000/api/v1/publication/' \
            -H 'accept: application/json' \
            -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzA2ODk0MTA3fQ.pMxmHBcOFBXzDNmbrcS5SLZhHYBry9OQV8hfkmU7TuM' \
            -H 'Content-Type: application/json' \
            -d '{
            "text": "Hello world!"
          }'

  - Добавить оценку публикации (like | dislike):
   
          curl -X 'POST' \
          'http://127.0.0.1:8000/api/v1/publication/4/rate' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzA2ODk0MTA3fQ.pMxmHBcOFBXzDNmbrcS5SLZhHYBry9OQV8hfkmU7TuM' \
          -H 'Content-Type: application/json' \
          -d '"like"'


  - Убрать оценку с публикации:
   
          curl -X 'DELETE' \
          'http://127.0.0.1:8000/api/v1/publication/4/rate' \
          -H 'accept: application/json' \
          -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzA2ODk0MTA3fQ.pMxmHBcOFBXzDNmbrcS5SLZhHYBry9OQV8hfkmU7TuM'
      
