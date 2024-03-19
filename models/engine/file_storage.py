#!/usr/bin/python3
"""Module for FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for serializing and deserializing
    instances to JSON file and vice-versa.
    """

    __file_path = "file.json"
    __objects = {}
    class_dict = {"BaseModel": BaseModel, "User": User, "Place": Place,
                  "Amenity": Amenity, "City": City, "Review": Review,
                  "State": State}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    @classmethod
    def new(cls, obj):
        """Sets in __objects the obj with key <obj class name>.id."""
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    @classmethod
    def save(cls):
        """Serializes __objects to the JSON file (path: __file_path)."""
        serialized_objects = {}
        for key, value in FileStorage.__objects.items():
            serialized_objects[key] = value.to_dict()
        with open(cls.__file_path, "w", encoding="utf-8") as json_file:
            json.dump(serialized_objects, json_file)

    @classmethod
    def reload(cls):
        """Deserializes the JSON file to __objects."""
        try:
            with open(cls.__file_path, "r", encoding="utf-8") as json_file:
                loaded_objects = json.load(json_file)
            for key, value in loaded_objects.items():
                class_name = value['__class__']
                if class_name in cls.class_dict:
                    obj_class = cls.class_dict[class_name]
                    obj = obj_class(**value)
                    FileStorage.__objects[key] = obj
                else:
                    print(f"Class {class_name} not found in class_dict")
        except FileNotFoundError:
            pass
