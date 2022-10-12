# Проектное задание четвертого спринта

Спроектируйте и реализуйте сервис для создания сокращенной формы передаваемых URL и анализа активности их использования.

Кроме этого, выберите из списка дополнительные требования и тоже реализуйте их. У каждого задания есть определённая сложность, от которой зависит количество баллов. Вам необходимо выбрать такое количество заданий, чтобы общая сумма баллов была больше 4. Выбор заданий никак не ограничен: можно выбрать все простые или одно среднее и два простых, или одно продвинутое, или решить все.

## Описание задания

Реализовать **http**-сервис, который обрабатывает поступающие запросы. Сервер стартует по адресу `http://127.0.0.1:8080`.


<details>
<summary> Список необходимых эндпойнтов (можно изменять) </summary>

1. Получить сокращенный вариант переданного URL
```python
POST /
```
Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.


2. Вернуть оригинальный URL
```python
GET /<url_id>
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL
```python
GET /<url_id>/status
```
Метод принимает в качестве параметра идентификатор сокращенного URL и возвращает информацию о количестве переходов, совершенных по ссылке.

</details>



### Дополнительные требования (отметить [Х] выбранные пункты):

- [ ] (1 балл) Реализуйте метод `GET /ping`, который возвращает информацию о статусе БД.
- [ ] (1 балл) Реализуйте возможность "удаления" сохраненного URL. Запись должна оставаться, но помечаться как удаленная. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.

- [ ] (2 балла) Реализуйте **middlware**, блокирующий доступ к сервису запросов из запрещенных подсетей (black list).
- [ ] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).

<details>
<summary> Описание изменений </summary>

- Метод `POST /shorten` принимает в теле запроса список URL в формате:
```python
[
    {
        "url_id": "<text-id>",
        "original_url": "URL for shorten"
    },
    ...
]

```
и возвращает данные в формате:
```python
[
    {
        "url_id": "<text-id>",
         "short_url": "http://...",
    },
    ...
]
```
</details>



- [ ] (3 балла) Реализуйте взаимодействие с сервисом авторизованного пользователя. Пользователь может создавать как приватные, так и публичные ссылки или изменять видимость ссылок. Вызов метода `GET /user/status` возвращает все созданные ранее ссылки в формате:

```
[
    {
        "short_id": "<text-id>",
        "short_url": "http://...",
        "original_url": "http://...",
        "type": "<public|private>"
    },
    ...
]
```

- [ ] **(5 баллов) Реализовать кастомную реализацию взаимодействия с БД. Учесть возможность работы с транзакциями.


## Требования к решению

1. Используйте фреймворк FastAPI. В качестве СУБД используйте PostgreSQL (не ниже 10).
2. Используйте концепции ООП.
3. Предусмотрите обработку исключительных ситуаций. 
4. Приведите стиль кода в соответствие pep8, flake8, mypy. 
5. Логируйте результаты действий. 
6. Покройте написанный код тестами. 
