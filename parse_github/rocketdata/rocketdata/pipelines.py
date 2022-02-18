import json
from sqlalchemy.orm import sessionmaker
from .models import Item, Owner, create_owner_table, create_items_table, db_connect
import re
import requests
from .settings import API_TOKEN


class RocketdataPipeline:
    def __init__(self):
        """
        Инициализируем подключение к базе данных
        Создаем таблицу элементов
        """
        engine = db_connect()
        create_owner_table(engine)
        create_items_table(engine)
        self.Session = sessionmaker(bind=engine)

    def funk_item(self, rep):
        request_body = json.dumps(rep)
        url = "http://127.0.0.1:8000/gitcreate/"
        headers = {
            'Authorization': API_TOKEN,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
            'Host': '127.0.0.1:8080', 'Content-Type': 'application/json', 'Accept': '*/*'}
        requests.post(url, data=request_body, headers=headers)

    def funk_owner(self, own):
        """
            Проверяем наличие в БД данных
            Если их там нет, то добавляем
        """
        session = self.Session()
        instance = session.query(Owner).filter_by(**own).one_or_none()
        if instance:
            return instance, False
        else:
            try:
                request_body = json.dumps(own)
                url = "http://127.0.0.1:8000/gitcreateuser/"
                headers = {
                    'Authorization': API_TOKEN,
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
                    'Host': '127.0.0.1:8080', 'Content-Type': 'application/json', 'Accept': '*/*'}
                requests.post(url, data=request_body, headers=headers)
            except Exception:
                raise

    def process_item(self, item, spider):
        """
            Отдает данные в виде словаря
            Регулярными выражениями исправляем тысячные значения
            Пример:
                1.2k = 1200
        """
        own = dict(
            owner_name=item['owner_name'],
            owner_link=item['owner_link']
        )
        RocketdataPipeline.funk_owner(self, own)
        session = self.Session()
        name = session.query(Owner.id).filter_by(owner_name=item['owner_name']).first()
        if not item['stars'].isdigit():
            stars = re.sub("[^0-9]", '', str(item['stars'])) + '00'
        else:
            stars = item['stars']
        if not item['watching'].isdigit():
            watching = re.sub("[^0-9]", '', str(item['watching'])) + '00'
        else:
            watching = item['watching']
        if not item['forks'].isdigit():
            forks = re.sub("[^0-9]", '', str(item['forks'])) + '00'
        else:
            forks = item['forks']
        if not item['commit_count'].isdigit():
            commit_count = re.sub("[^0-9]", "", item['commit_count'])
        else:
            commit_count = item['commit_count']
        rep = dict(
            link_rep=item['link_rep'],
            name_rep=item['name_rep'],
            about=item['about'],
            link_site=item['link_site'],
            stars=stars,
            watching=watching,
            forks=forks,
            commit_count=commit_count,
            commit_author=item['commit_author'],
            commit_name=item['commit_name'],
            commit_datetime=item['commit_datetime'],
            release_count=item['release_count'],
            release_version=item['release_version'],
            release_datetime=item['release_datetime'],
            owner=name[0]

        )
        RocketdataPipeline.funk_item(self, rep)

# class RocketdataPipeline:
#     def __init__(self):
#         """
#         Инициализируем подключение к базе данных
#         Создаем таблицу элементов
#         """
#         engine = db_connect()
#         create_owner_table(engine)
#         create_items_table(engine)
#         self.Session = sessionmaker(bind=engine)
#
#     def funk_item(self, rep):
#         """
#             Проверяем наличие в БД данных
#             Если их там нет, то добавляем
#         """
#         session = self.Session()
#         instance = session.query(Item).filter_by(**rep).one_or_none()
#         if instance:
#             return instance, False
#         else:
#             try:
#                 session.add(Item(**rep))
#                 session.commit()
#
#             except Exception:
#                 session.rollback()
#                 raise
#             finally:
#                 session.close()
#
#     def funk_owner(self, own):
#         """
#             Проверяем наличие в БД данных
#             Если их там нет, то добавляем
#         """
#         session = self.Session()
#         instance = session.query(Owner).filter_by(**own).one_or_none()
#         if instance:
#             return instance, False
#         else:
#             try:
#                 session.add(Owner(**own))
#                 session.commit()
#             except Exception:
#                 session.rollback()
#                 raise
#             finally:
#                 session.close()
#
#     def process_item(self, item, spider):
#         """
#             Отдает данные в модели в виде словаря
#             Регулярными выражениями исправляем тысячные значения
#             Пример:
#                 1.2k = 1200
#         """
#         own = dict(
#             owner_name=item['owner_name'],
#             owner_link=item['owner_link']
#         )
#         RocketdataPipeline.funk_owner(self, own)
#         name = select(Owner.id).filter_by(owner_name=item['owner_name'])
#         if not item['stars'].isdigit():
#             stars = re.sub("[^0-9]", '', str(item['stars'])) + '00'
#         else:
#             stars = item['stars']
#         if not item['watching'].isdigit():
#             watching = re.sub("[^0-9]", '', str(item['watching'])) + '00'
#         else:
#             watching = item['watching']
#         if not item['forks'].isdigit():
#             forks = re.sub("[^0-9]", '', str(item['forks'])) + '00'
#         else:
#             forks = item['forks']
#         if not item['commit_count'].isdigit():
#             commit_count = re.sub("[^0-9]", "", item['commit_count'])
#         else:
#             commit_count = item['commit_count']
#         rep = dict(
#             link_rep=item['link_rep'],
#             name_rep=item['name_rep'],
#             about=item['about'],
#             link_site=item['link_site'],
#             stars=stars,
#             watching=watching,
#             forks=forks,
#             commit_count=commit_count,
#             commit_author=item['commit_author'],
#             commit_name=item['commit_name'],
#             commit_datetime=item['commit_datetime'],
#             release_count=item['release_count'],
#             release_version=item['release_version'],
#             release_datetime=item['release_datetime'],
#             owner_id=name
#
#         )
#         RocketdataPipeline.funk_item(self, rep)
