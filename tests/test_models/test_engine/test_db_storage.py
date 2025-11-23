#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_get(self):
        """Test that get method retrieves specific objects from database"""
        # Create test object
        state = State()
        state.name = "California"
        models.storage.new(state)
        models.storage.save()
        
        # Test get with class object and valid id
        retrieved_state = models.storage.get(State, state.id)
        self.assertEqual(retrieved_state, state)
        self.assertEqual(retrieved_state.name, "California")
        
        # Test get with class name string and valid id
        retrieved_state_str = models.storage.get("State", state.id)
        self.assertEqual(retrieved_state_str, state)
        
        # Test get with invalid id
        self.assertIsNone(models.storage.get(State, "invalid_id"))
        self.assertIsNone(models.storage.get("State", "invalid_id"))
        
        # Test get with None parameters
        self.assertIsNone(models.storage.get(None, state.id))
        self.assertIsNone(models.storage.get(State, None))
        self.assertIsNone(models.storage.get(None, None))
        
        # Test get with invalid class
        self.assertIsNone(models.storage.get("InvalidClass", state.id))
        
        # Clean up
        models.storage.delete(state)
        models.storage.save()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count(self):
        """Test that count method returns correct number of objects"""
        # Get initial counts
        initial_total = models.storage.count()
        initial_states = models.storage.count(State)
        initial_cities = models.storage.count(City)
        
        # Create and add some objects
        state1 = State()
        state1.name = "Florida"
        state2 = State()
        state2.name = "Texas"
        
        models.storage.new(state1)
        models.storage.new(state2)
        models.storage.save()
        
        # Test count all objects (should increase by 2)
        self.assertEqual(models.storage.count(), initial_total + 2)
        
        # Test count by class object
        self.assertEqual(models.storage.count(State), initial_states + 2)
        
        # Test count by class name string
        self.assertEqual(models.storage.count("State"), initial_states + 2)
        
        # Test count with class that has no instances
        self.assertEqual(models.storage.count(City), initial_cities)
        
        # Add a city
        city = City()
        city.name = "Miami"
        city.state_id = state1.id
        models.storage.new(city)
        models.storage.save()
        
        # Test updated counts
        self.assertEqual(models.storage.count(), initial_total + 3)
        self.assertEqual(models.storage.count(State), initial_states + 2)
        self.assertEqual(models.storage.count(City), initial_cities + 1)
        self.assertEqual(models.storage.count("City"), initial_cities + 1)
        
        # Clean up
        models.storage.delete(city)
        models.storage.delete(state1)
        models.storage.delete(state2)
        models.storage.save()
