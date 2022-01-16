### Запуск


## Необоходимое для работы
Docker
docker-compose

## Запуск API в контейнере.

```bash
pipenv run pip freeze > requirements.txt

docker-compose up --build
или через суперюзера
sudo docker-compose up --build

```

## Запуск API в pipenv.
```bash
pipenv shell
pipenv install
python api/run.py
```