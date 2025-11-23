#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get(self):
        """Test that get method retrieves specific objects"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        
        # Create test objects
        state = State()
        city = City()
        user = User()
        
        # Add them to storage
        storage.new(state)
        storage.new(city)
        storage.new(user)
        
        # Test get with class object and valid id
        self.assertEqual(storage.get(State, state.id), state)
        self.assertEqual(storage.get(City, city.id), city)
        self.assertEqual(storage.get(User, user.id), user)
        
        # Test get with class name string and valid id
        self.assertEqual(storage.get("State", state.id), state)
        self.assertEqual(storage.get("City", city.id), city)
        self.assertEqual(storage.get("User", user.id), user)
        
        # Test get with invalid id
        self.assertIsNone(storage.get(State, "invalid_id"))
        self.assertIsNone(storage.get("State", "invalid_id"))
        
        # Test get with None parameters
        self.assertIsNone(storage.get(None, state.id))
        self.assertIsNone(storage.get(State, None))
        self.assertIsNone(storage.get(None, None))
        
        # Test get with invalid class
        self.assertIsNone(storage.get("InvalidClass", state.id))
        
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test that count method returns correct number of objects"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        
        # Initially should be 0
        self.assertEqual(storage.count(), 0)
        self.assertEqual(storage.count(State), 0)
        self.assertEqual(storage.count("State"), 0)
        
        # Create and add some objects
        state1 = State()
        state2 = State()
        city1 = City()
        user1 = User()
        
        storage.new(state1)
        storage.new(state2)
        storage.new(city1)
        storage.new(user1)
        
        # Test count all objects
        self.assertEqual(storage.count(), 4)
        
        # Test count by class object
        self.assertEqual(storage.count(State), 2)
        self.assertEqual(storage.count(City), 1)
        self.assertEqual(storage.count(User), 1)
        self.assertEqual(storage.count(Amenity), 0)
        
        # Test count by class name string
        self.assertEqual(storage.count("State"), 2)
        self.assertEqual(storage.count("City"), 1)
        self.assertEqual(storage.count("User"), 1)
        self.assertEqual(storage.count("Amenity"), 0)
        
        # Add more objects
        amenity1 = Amenity()
        storage.new(amenity1)
        
        self.assertEqual(storage.count(), 5)
        self.assertEqual(storage.count(Amenity), 1)
        self.assertEqual(storage.count("Amenity"), 1)
        
        FileStorage._FileStorage__objects = save
