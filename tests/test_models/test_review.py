#!/usr/bin/python3
"""Defines unittests for models/review.py."""
import os
import unittest
import pep8
from datetime import datetime
import models
from models.review import Review
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.engine.db_storage import DBStorage
from sqlalchemy.exc import OperationalError


class TestReview(unittest.TestCase):
    """Unittests for the Review class."""

    @classmethod
    def setUpClass(cls):
        """Review testing setup."""
        cls.file_backup = "file.json"
        try:
            os.rename(cls.file_backup, "tmp")
        except FileNotFoundError:
            pass
        models.storage._FileStorage__objects.clear()
        cls.file_storage = models.storage

        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id, name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id, user_id=cls.user.id)

        if type(models.storage) == DBStorage:
            models.storage.reload()

    @classmethod
    def tearDownClass(cls):
        """Review testing teardown."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        try:
            os.rename("tmp", cls.file_backup)
        except FileNotFoundError:
            pass
        del cls.state
        del cls.city
        del cls.user
        del cls.place
        del cls.review

    def test_pep8(self):
        """Test PEP8 styling."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["models/review.py"])
        self.assertEqual(result.total_errors, 0, "Fix PEP8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Review.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        review = Review()
        self.assertIsInstance(review.id, str)
        self.assertIsInstance(review.created_at, datetime)
        self.assertIsInstance(review.updated_at, datetime)
        self.assertTrue(hasattr(review, "__tablename__"))
        self.assertTrue(hasattr(review, "text"))
        self.assertTrue(hasattr(review, "place_id"))
        self.assertTrue(hasattr(review, "user_id"))

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing FileStorage")
    def test_nullable_attributes(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises(OperationalError):
            models.storage.save()

    def test_is_subclass(self):
        """Check that Review is a subclass of BaseModel."""
        self.assertTrue(issubclass(Review, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.review, Review)

    def test_two_models_are_unique(self):
        """Test that different Review instances are unique."""
        review = Review()
        self.assertNotEqual(self.review.id, review.id)
        self.assertLess(self.review.created_at, review.created_at)
        self.assertLess(self.review.updated_at, review.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        review = Review("1", id="5", created_at=dt.isoformat())
        self.assertEqual(review.id, "5")
        self.assertEqual(review.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = str(self.review)
        self.assertIn("[Review] ({})".format(self.review.id), s)
        self.assertIn("'id': '{}'".format(self.review.id), s)
        self.assertIn("'created_at': {}".format(repr(self.review.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.review.updated_at)), s)
        self.assertIn("'text': '{}'".format(self.review.text), s)
        self.assertIn("'place_id': '{}'".format(self.review.place_id), s)
        self.assertIn("'user_id': '{}'".format(self.review.user_id), s)

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(old_updated_at, self.review.updated_at)

    @unittest.skipIf(type(models.storage) == FileStorage, "Testing DBStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old_updated_at = self.review.updated_at
        models.storage.reload()
        self.review.save()
        self.assertNotEqual(old_updated_at, self.review.updated_at)

    def test_to_dict(self):
        """Test to_dict method."""
        review_dict = self.review.to_dict()
        self.assertEqual(dict, type(review_dict))
        self.assertEqual(self.review.id, review_dict["id"])
        self.assertEqual("Review", review_dict["__class__"])
        self.assertEqual(self.review.created_at.isoformat(), review_dict["created_at"])
        self.assertEqual(self.review.updated_at.isoformat(), review_dict["updated_at"])
        self.assertEqual(self.review.text, review_dict["text"])
        self.assertEqual(self.review.place_id, review_dict["place_id"])
        self.assertEqual(self.review.user_id, review_dict["user_id"])


if __name__ == "__main__":
    unittest.main()
