# Пример FastAPI приложения для лабораторной работы 9

## Создание и настройка окружения
### Установите необходимые пакеты:    
`poetry add fastapi sqlalchemy psycopg2 python-dotenv alembic uvicorn`  


### Настройте алембик:  

Инициализируйте алембик внутри директории проекта:   
`alembic init migrations`    

Отредактируйте файл env.py внутри папки migrations:  
Импортируйте в него ваши модели, добавьте базовую модель алхимии и импортируйте строку подключения к базе.  
```commandline
config.set_section_option(
    config.config_ini_section, "sqlalchemy.url", settings.database_url
)
from app.models import *  # noqa
target_metadata = Base.metadata
```
Вы можете взять файл env.py из данного репозитория и заменить им созданный (только проследите за импортом моделей).

### Команды алмебика:
`alembic revision --autogenerate --message="add user tbl"` - создать файл миграции  
`alembic upgrade head` - запуск миграции

### Запуск приложения через uvicorn:  
`uvicorn app.main:app --host 127.0.0.1 --port 8000`  

## О проекте
Для начала советую ознакомиться с логикой `users`, а затем изучить `computers`. Я разместил эти модули в соответствующей директории, 
рекомендую вам использовать такую же структуру приложение.  
Единственным неудобным моментом является то, что файл `models` не разделен, я очень рекомендую в каждом модуле держать свой файл `models`.
Главное не забыть импортировать все модели в `env.py` алембика.

# Не импортируйте ваш .env в github репозиторий, я загрузил его только для примера!