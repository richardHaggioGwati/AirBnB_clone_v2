#!/usr/bin/python3
'''Database storage engine'''

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv

if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

classes = {
    "User": User, "State": State, "City": City,
    "Amenity": Amenity, "Place": Place, "Review": Review
}


class DBStorage:
    '''Database storage engine for MySQL storage'''

    __engine = None
    __session = None

    def __init__(self):
        '''Instantiate a new DBStorage instance'''
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                HBNB_MYSQL_USER,
                HBNB_MYSQL_PWD,
                HBNB_MYSQL_HOST,
                HBNB_MYSQL_DB
            ),
            pool_pre_ping=True
        )

        if HBNB_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)()

    def all(self, cls=None):
        '''Query on the current DB session all cls objects'''
        dct = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    dct[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                dct[key] = obj
        return dct

    def new(self, obj):
        '''Add the obj to the current DB session'''
        if obj:
            self.__session.add(obj)

    def save(self):
        '''Commit all changes of the current DB session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Delete from the current DB session the obj if it's not None'''
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''Reload the database'''
        Base.metadata.create_all(self.__engine)

    def close(self):
        '''Close the working SQLAlchemy session'''
        self.__session.close()
