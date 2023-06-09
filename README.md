# REST API для key-value хранилища

# Основные технологии
- Python 3.9
- Flask 2.2.3
- Redis 4.5.4

# Запуск сервиса
#### Запуск приложения и Redis в докере
```
$ make run
```

#### Остановка контейнеров
```
$ make stop
```

#### Запуск тестов
```
$ make test
```

#### Запуск линтеров
```
$ make lint
```

# Описание работы сервиса
Основные моменты реализации:
- В `src/app/api` хранятся ручки и pydantic-модели
- Валидация данных осуществляется при помощи пакетов `pydantic` и `flask_pydantic`
- В `src/app/key_value_storage` хранится redis-клиент
- Для коннекта с Redis используется пул соединений. Реализовано в классе `RedisClient`
- Абстрактный базовый класс `BaseKeyValueStorage` описывает поведение клиентов для key-value хранилищ, если потребуется расширять логику
- Данные пользователя хранятся в хэше Redis под ключом вида `user:<user_id>`, id пользователя в формате `uuid`
- Состояние Redis сохраняется при помощи RDB
- В `src/app/logic` хранится логика взаимодействия с key-value хранилищем
- Использован менеджер пакетов `poetry`
- Добавлены юнит-тесты, покрывающее базовую логику сервиса
- Добавлен `Dockerfile`
- Добавлен минимальный ci для запуска юнит-тестов и линтеров (flake8, bandit)
