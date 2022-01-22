# Тестовое приложение-блог для практики в обучении автоматизации тестирования

## Необоходимое для запуска
В контейнере:
 - Docker
 - docker-compose

В виртуальном окружении Python:
- Python 3.5+
- pipenv

## Запуск API в контейнере.

```bash
pipenv run pip freeze > requirements.txt

docker-compose up --build
или через суперюзера
sudo docker-compose up --build

```

## Запуск API через pipenv.
```bash
pipenv shell
pipenv install
python api/run.py
```


## Запуск тестов

### Через unittest
- python -m unittest tests.unittests.test_validation_unittest

### Через pytest
- cd tests/pytest
- pytest -v