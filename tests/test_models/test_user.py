#!/usr/bin/python3
"""Defines unittests for models/user.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.user import User


class TestUser_instantiation(unittest.TestCase):
    """Unittests for  instantiation"""

    def no_args_instantiates_test(self):
        self.assertEqual(User, type(User()))

    def new_instance_stored_in_objects_test(self):
        self.assertIn(User(), models.storage.all().values())

    def id_is_public_str_test(self):
        self.assertEqual(str, type(User().id))

    def created_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(User().created_at))

    def updated_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(User().updated_at))

    def email_is_public_str_test(self):
        self.assertEqual(str, type(User.email))

    def password_is_public_str_test(self):
        self.assertEqual(str, type(User.password))

    def first_name_is_public_str_test(self):
        self.assertEqual(str, type(User.first_name))

    def last_name_is_public_str_test(self):
        self.assertEqual(str, type(User.last_name))

    def two_users_unique_ids_test(self):
        us1 = User()
        us2 = User()
        self.assertNotEqual(us1.id, us2.id)

    def two_users_different_created_at_test(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.created_at, us2.created_at)

    def two_users_different_updated_at_test(self):
        us1 = User()
        sleep(0.05)
        us2 = User()
        self.assertLess(us1.updated_at, us2.updated_at)

    def str_representation_test(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        usstr = us.__str__()
        self.assertIn("[User] (123456)", usstr)
        self.assertIn("'id': '123456'", usstr)
        self.assertIn("'created_at': " + dt_repr, usstr)
        self.assertIn("'updated_at': " + dt_repr, usstr)

    def args_unused_test(self):
        us = User(None)
        self.assertNotIn(None, us.__dict__.values())

    def instantiation_with_kwargs_test(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        us = User(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(us.id, "345")
        self.assertEqual(us.created_at, dt)
        self.assertEqual(us.updated_at, dt)

    def instantiation_with_None_kwargs_test(self):
        with self.assertRaises(TypeError):
            User(id=None, created_at=None, updated_at=None)


class TestUser_save(unittest.TestCase):
    """Unittests for  save method"""

    @classmethod
    def setUp_test(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown_test(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def one_save_test(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        self.assertLess(first_updated_at, us.updated_at)

    def two_saves_test(self):
        us = User()
        sleep(0.05)
        first_updated_at = us.updated_at
        us.save()
        second_updated_at = us.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        us.save()
        self.assertLess(second_updated_at, us.updated_at)

    def save_with_arg_test(self):
        us = User()
        with self.assertRaises(TypeError):
            us.save(None)

    def save_updates_file_test(self):
        us = User()
        us.save()
        usid = "User." + us.id
        with open("file.json", "r") as f:
            self.assertIn(usid, f.read())


class TestUser_to_dict(unittest.TestCase):
    """Unittests for  to_dict method"""

    def to_dict_type_test(self):
        self.assertTrue(dict, type(User().to_dict()))

    def to_dict_contains_correct_keys_test(self):
        us = User()
        self.assertIn("id", us.to_dict())
        self.assertIn("created_at", us.to_dict())
        self.assertIn("updated_at", us.to_dict())
        self.assertIn("__class__", us.to_dict())

    def to_dict_contains_added_attributes_test(self):
        us = User()
        us.middle_name = "Holberton"
        us.my_number = 98
        self.assertEqual("Holberton", us.middle_name)
        self.assertIn("my_number", us.to_dict())

    def to_dict_datetime_attributes_are_strs_test(self):
        us = User()
        us_dict = us.to_dict()
        self.assertEqual(str, type(us_dict["id"]))
        self.assertEqual(str, type(us_dict["created_at"]))
        self.assertEqual(str, type(us_dict["updated_at"]))

    def to_dict_output_test(self):
        dt = datetime.today()
        us = User()
        us.id = "123456"
        us.created_at = us.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'User',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(us.to_dict(), tdict)

    def contrast_to_dict_dunder_dict_test(self):
        us = User()
        self.assertNotEqual(us.to_dict(), us.__dict__)

    def to_dict_with_arg_test(self):
        us = User()
        with self.assertRaises(TypeError):
            us.to_dict(None)


if __name__ == "__main__":
    unittest.main()
