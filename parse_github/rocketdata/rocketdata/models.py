from sqlalchemy import Column, Integer, String, create_engine, ForeignKey
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from . import settings


DeclarativeBase = declarative_base()


def db_connect() -> Engine:
    """
    Создаем соединение с базой данных, используя настройки базы данных из файла settings.py
    Возвращаем экземпляр sqlalchemy
    """
    return create_engine(URL(**settings.DATABASE))


def create_owner_table(engine: Engine):
    """
    Создание таблицы для владельцев
    """
    DeclarativeBase.metadata.create_all(engine)


class Owner(DeclarativeBase):
    """
    Создание модели для сохранения владельцев
    """
    __tablename__ = "api_gituser"

    id = Column('id', Integer, primary_key=True)
    owner_name = Column(String)
    owner_link = Column(String)


def create_items_table(engine: Engine):
    """
    Создание таблицы для  репозиториев
    """
    DeclarativeBase.metadata.create_all(engine)


class Item(DeclarativeBase):
    """
    Создание модели для сохранения репозиториев
    """
    __tablename__ = "api_gititem"

    id = Column('id', Integer, primary_key=True)
    link_rep = Column('link_rep', String, nullable=True)
    name_rep = Column('name_rep', String, nullable=True)
    about = Column('about', String, nullable=True)
    link_site = Column('link_site', String, nullable=True)
    stars = Column('stars', Integer, nullable=True)
    watching = Column('watching', Integer, nullable=True)
    forks = Column('forks', Integer, nullable=True)
    commit_count = Column('commit_count', Integer, nullable=True)
    commit_author = Column('commit_author', String, nullable=True)
    commit_name = Column('commit_name', String, nullable=True)
    commit_datetime = Column('commit_datetime', String, nullable=True)
    release_count = Column('release_count', String, nullable=True)
    release_version = Column('release_version', String, nullable=True)
    release_datetime = Column('release_datetime', String, nullable=True)
    owner_id = Column(Integer, ForeignKey(Owner.id))

