from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base,BaseModel
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.place import Place
from models.user import User
from models.state import State

classes = {"User": User, "State": State, "City": City,
           "Amenity": Amenity, "Place": Place, "Review": Review}


class DBStorage:
    """Database Storage Engine"""
    __engine = None
    __session = None

    def __init__(self):
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        
        """Creates the engine instances"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format
                                      (user, password, host,db),
                                      pool_pre_ping=True)
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the current database session  depending on the class"""
        dic = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()

                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dic[key]  = obj
        
        else:
            objs = self.__session.query(c).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dic[key] = obj
        return dic
    
    def new(self, obj):
        """ADD the object to the current database session"""
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)

            except Exception as e:
                self.__session.rollback()

    def save(self):
        """Commit the session"""
        self.__session.commit()

    def delete(self,obj=None):
        """Delete an object from the database session"""
        if obj is not None:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id).delete()

    def reload(self):
        """Creates the tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,expire_on_commit=False)
        self.__session = scoped_session(session_factory)()

    def close(self):
        """Closes the session"""
        self.__session.close()
    
