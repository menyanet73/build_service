# Build System Microservice

Этот микросервис разработан для автоматизации процесса сборки игр с помощью задач и билдов.

#### Запуск приложения
Для запуска приложения скопируйте репозиторий 
```
git clone https://github.com/menyanet73/build_service/
```
Перейдите в репозиторий
```
cd builds_service
```
Запустите docker-compose
https://docs.docker.com/compose/install/ - инструкция установки docker-compose

```bash
docker-compose up -d
```

Приложение будет доступно по адресу http://localhost

#### Использование

Этот микросервис имеет один эндпоинт, который принимает JSON-запрос, содержащий имя билда, и возвращает список задач, отсортированных с учетом их зависимостей.
http://localhost/get_tasks/ - POST

##### Пример запроса:

```
curl --location --request POST 'http://localhost/get_tasks/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "build": "front_arm"
}'
```
##### Пример ответа:
```
["compile_exe",    "pack_build"]
```
#### Тестирование

Юнит тесты запускается автоматически при сборке контейнеров
