alembic init [директория с миграциями] - инициация конфигурии
alembic revision -m [название миграции] - создать шаблон миграции
alembic revision --autogenerate -m [название миграции] - создать миграцию на основе моделей
alembic upgrade head - применить последнюю миграцию
alembic downgrade [номер ревизии] - откатить миграцию (base в самое начало)
