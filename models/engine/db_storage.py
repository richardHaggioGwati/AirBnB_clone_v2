#!/usr/bin/python3
""" Database storage module for HBNB project """
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """ Database storage class """
    __engine = None
    __session = None

    def __init__(self):
        """ Initialize the database connection """
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV', 'development')

        self.__engine = create_engine(f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)

    def all(self, cls=None):
        """ Query on the current database session """
        classes = [User, State, City, Amenity, Place, Review]
        objs = {}

        if cls:
            if cls in classes:
                for obj in self.__session.query(cls).all():
                    key = f"{cls.__name__}.{obj.id}"
                    objs[key] = obj
        else:
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    key = f"{cls.__name__}.{obj.id}"
                    objs[key] = obj

        return objs

    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Create all tables in the database and create the current session """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))

    def close(self):
        """ Close the session """
        self.__session.remove()
