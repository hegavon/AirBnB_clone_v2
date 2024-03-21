#!/usr/bin/python3
""" New class for SQLAlchemy """
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects or filtered by class"""
        if cls:
            return {key: obj for key, obj in self.__objects.items()
                    if isinstance(obj, cls)}
        return self.__objects

    def new(self, obj):
        """Adds a new object to the storage"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serializes objects to JSON file"""
        serialized = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(serialized, f)

    def reload(self):
        """Deserializes JSON file to objects"""
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                data = json.load(f)
                for key, obj_data in data.items():
                    class_name = obj_data['__class__']
                    obj = eval(class_name)(**obj_data)
                    self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage"""
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects.pop(key, None)

    def close(self):
        """Reloads the storage"""
        self.reload()
