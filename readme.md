# Чат сервер

## Состоит из 3 компонентов 

- Сервер api, который ответчает за обработку запросов от пользователей
- Серевер веб-сокетов (pusher), который отвечает за обновление в реальном времени данныз у пользоваетелей
- Брокер сообщений kafka, который используется для передачи сообщений от api к пушеру. Например когда приходит новое сообщение

## Запуск

- Создайте 2 файла api.env и pusher.env. Можно оставить их пустыми.
- Выполнить docker compose -f deploy/docker-compose-full-dev.yml -p chat up


## Документация

http://localhost:8203/docs