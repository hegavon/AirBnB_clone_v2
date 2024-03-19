#!/usr/bin/python3

from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
import os
import pep8
import unittest
from datetime import datetime, timezone
from models.base_model import BaseModel
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class test_Amenity(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Amenity"
        self.value = Amenity

    def test_name2(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)

class TestAmenity(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    @classmethod
    def setUpClass(cls):
        """Amenity testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage and Amenity instances for testing.
        """
        cls.backup_file = "file.json"
        cls.temp_file = "tmp"
        cls.setup_file_storage()
        cls.amenity = Amenity(name="The Andrew Lindburg treatment")

    @classmethod
    def tearDownClass(cls):
        """Amenity testing teardown.
        Restore original file.json.
        Delete the FileStorage, DBStorage and Amenity test instances.
        """
        cls.cleanup_file_storage()
        del cls.amenity
        if isinstance(models.storage, DBStorage):
            cls.cleanup_db_storage()

    @classmethod
    def setup_file_storage(cls):
        """Set up FileStorage for testing."""
        try:
            os.rename(cls.backup_file, cls.temp_file)
        except FileNotFoundError:
            pass

    @classmethod
    def cleanup_file_storage(cls):
        """Clean up FileStorage after testing."""
        try:
            os.remove(cls.backup_file)
        except FileNotFoundError:
            pass
        try:
            os.rename(cls.temp_file, cls.backup_file)
        except FileNotFoundError:
            pass

    @classmethod
    def cleanup_db_storage(cls):
        """Clean up DBStorage after testing."""
        cls.dbstorage._DBStorage__session.close()
        del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        result = style.check_files(["models/amenity.py"])
        self.assertEqual(result.total_errors, 0, "Fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        amenity = Amenity(email="a", password="a")
        self.assertEqual(str, type(amenity.id))
        self.assertEqual(datetime, type(amenity.created_at))
        self.assertEqual(datetime, type(amenity.updated_at))
        self.assertTrue(hasattr(amenity, "__tablename__"))
        self.assertTrue(hasattr(amenity, "name"))
        self.assertTrue(hasattr(amenity, "place_amenities"))

    @unittest.skipIf(isinstance(models.storage, DBStorage), "Testing FileStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_updated_at, self.amenity.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Amenity." + self.amenity.id, f.read())

    @unittest.skipIf(not isinstance(models.storage, DBStorage), "Testing DBStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertLess(old_updated_at, self.amenity.updated_at)
        db = MySQLdb.connect(user="hbnb_test", passwd="hbnb_test_pwd", db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM `amenities` WHERE BINARY name = '{}'".
                format(self.amenity.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.amenity.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(dict, type(amenity_dict))
        self.assertEqual(self.amenity.id, amenity_dict["id"])
        self.assertEqual("Amenity", amenity_dict["__class__"])
        self.assertEqual(self.amenity.created_at.isoformat(), amenity_dict["created_at"])
        self.assertEqual(self.amenity.updated_at.isoformat(), amenity_dict["updated_at"])
        self.assertEqual(self.amenity.name, amenity_dict["name"])

    def test_is_subclass(self):
        """Check that Amenity is a subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.amenity, Amenity)

    def test_two_models_are_unique(self):
        """Test that different Amenity instances are unique."""
        other_amenity = Amenity(email="a", password="a")
        self.assertNotEqual(self.amenity.id, other_amenity.id)
        self.assertLess(self.amenity.created_at, other_amenity.created_at)
        self.assertLess(self.amenity.updated_at, other_amenity.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.now(timezone.utc)
        new_amenity = Amenity("1", id="5", created_at=dt.isoformat())
        self.assertEqual(new_amenity.id, "5")
        self.assertEqual(new_amenity.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.amenity.__str__()
        self.assertIn("[Amenity] ({})".format(self.amenity.id), s)
        self.assertIn("'id': '{}'".format(self.amenity.id), s)
        self.assertIn("'created_at': {}".format(repr(self.amenity.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.amenity.updated_at)), s)


if __name__ == "__main__":
    unittest.main()
