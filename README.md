# task3

Работает через Celery + Redis для запуска scrapy через api  
p.s Так-же, из каталога проекта rocketdata/rocketdata/spiders можно все так-же вручную запустить паука  
scrapy crawl git_spider  
После текста "Введите название аккаунта:" нужно ввести название аккаунта  



@База данных PostgreSql + Redis для Celery  
Создать каталог mkdir rockertdata_django  
Перейти в каталог cd rockertdata_django  
Клонировать каталог проекта с github  
git clone URL  
Устанавливаем виртуальное окружение  
python -m venv .venv  
Активировать виртуальное окружение  
source .venv/bin/activate  
Перейти в каталог проекта который склонировали  
cd parse_github  
Устанавливаем зависимости  
pip install -r requirements.txt  
Создать файл для подключения скрытых настроек из settings.py  
Добавляем в файл такие параметры и сохраняем:  

# Ваш хост  
ALLOWED_HOSTS=127.0.0.1  
# Дебаг режим True/ False  
DEBUG=True  
# Ваш секретный ключ  
SECRET_KEY=django-insecure-t9ao17z9oura90)q)9lm92m6(yra6+bz&x4^_9k85n$w-l5(8f  
# Ваш db engine  
DATABASES_ENGINE=django.db.backends.postgresql_psycopg2  
# Ваше название db  
DATABASES_NAME=postgres  
# User db  
DATABASES_USER=postgres  
# password db  
DATABASES_PASSWORD=  
# Хост db  
DATABASES_HOST=localhost  
# Порт db  
DATABASES_PORT=5432  

Делаем миграции  
./manage.py makemigrations  
./manage.py migrate  
Создаем супер-юзера  
./manage.py createsuperuser  

Выйти из этого каталога и зайти в каталог паука  
cd ..  
cd rocketdata/rocketdata  
Открываем settings.py и прописываем в настройках базы данных то, что прописали и django  
host, port, username, database  
Если есть пароль, то и его - password  
DATABASE = {  
    "drivername": 'postgresql',  
    "host": 'localhost',  
    "port": '5432',  
    "username": 'postgres',  
    # "password": '12345',  
    "database": 'postgres',  
}  
Сохраняем файл и переходим в каталог spiders  
cd spiders  
Запускаем проект  
scrapy crawl git_spider  
Он попросит ввести Логин профиля, допустим scrapy или MariyaSha  

В зависимости от того проект это или юзер, будут работать разные сценарии.  
У проект url выглядит так https://github.com/orgs/NAMEORG  
У юзеров url выглядит так https://github.com/MariyaSha  



Теперь возвращаемся в каталог Django parse_github  
Запускаем Django  
./manage.py runserver  

1)Апи получения ссылок на страницы пользователей (или проектов)  
http://127.0.0.1:8000/gitlink/  
2)Апи получения общей статистики  
http://127.0.0.1:8000/gitoveral/  
3)Сделать апи получения репозиториев пользователя (или проекта)  
Где в конце , вместо - 1 , это айди владельца по pk  
http://127.0.0.1:8000/gitgetrep/1/  
4)Апи получения статистики по одному пользователю (или проекту)  
Где в конце , вместо - 1 , это айди владельца по pk  
http://127.0.0.1:8000/gitindividualstats/1/  

Добавил еще просто список всех-всех репозиториев  
http://127.0.0.1:8000/gitgetall/  


Третья часть!!  

Запустить Redis в докере  
docker run -d -p 6379:6379 redis  

В корне проекта django запустить Celery  
celery -A parse_github worker -l info --max-tasks-per-child 1  

p.s в pipelines.py осталась и старая версия, с сохранением напрямую в БД  
Она в конце, закомментированная  

Запустить тесты, их 3 штуки.Они вплоть до аутентификации по токену  
./manage.py test api.tests  

Что-бы заиспользовать апи для сохранения собранных данных  
Для этого нужно сгенерировать API_TOKEN в django.  
Находясь в корневой папке Django проекта parse_github зайти в shell  
./manage.py shell  
Сделать импорт модели  
from rest_framework_api_key.models import APIKey  
Сгенерировать Токен  
api_key, key = APIKey.objects.create_key(name="my-remote-service")  
Чтобы посмотреть токен который сгенерировали, тут же, в shell ввести key  
Этот токен нужно прописать в settings.py паука.  
Переходим в каталог с settings.py  
rocketdata/rocketdata  
Изменить Константу API_TOKEN  
API_TOKEN = 'Api-Key GzMJnncw.8dN9RH0TKXLKue2fDMW4t75phdyEUmus'  
После Api-Key должен быть ваш Токен, который сгенерировали  
После этого запускаем паука и он сохраняет данные через Апи  

Апи для по сохранению данных о репозиториях пользователя (или проекта)  

Добавлять через это апи для запуска scrapy  
Нужно вставить ссылку и имя профиля.Парсит по имени  
http://127.0.0.1:8000/scrapycreate/  

А через это апи scrapy сохраняет данные из pipelines.py  
http://127.0.0.1:8000/gitcreateuser/  
 




