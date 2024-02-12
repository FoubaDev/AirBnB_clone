#!/usr/bin/python3
"""Defines unittests for models/city.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation """

    def no_args_instantiates_test(self):
        self.assertEqual(City, type(City()))

    def new_instance_stored_in_objects_test(self):
        self.assertIn(City(), models.storage.all().values())

    def id_is_public_str_test(self):
        self.assertEqual(str, type(City().id))

    def created_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(City().created_at))

    def updated_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(City().updated_at))

    def state_id_is_public_class_attribute_test(self):
        cy = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(cy))
        self.assertNotIn("state_id", cy.__dict__)

    def name_is_public_class_attribute_test(self):
        cy = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(cy))
        self.assertNotIn("name", cy.__dict__)

    def two_cities_unique_ids_test(self):
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def two_cities_different_created_at_test(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def two_cities_different_updated_at_test(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def str_representation_test(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        cystr = cy.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    def args_unused_test(self):
        cy = City(None)
        self.assertNotIn(None, cy.__dict__.values())

    def instantiation_with_kwargs_test(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        cy = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(cy.id, "345")
        self.assertEqual(cy.created_at, dt)
        self.assertEqual(cy.updated_at, dt)

    def instantiation_with_None_kwargs_test(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method """

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
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        self.assertLess(first_updated_at, cy.updated_at)

    def two_saves_test(self):
        cy = City()
        sleep(0.05)
        first_updated_at = cy.updated_at
        cy.save()
        second_updated_at = cy.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        cy.save()
        self.assertLess(second_updated_at, cy.updated_at)

    def save_with_arg_test(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.save(None)

    def save_updates_file_test(self):
        cy = City()
        cy.save()
        cyid = "City." + cy.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method """

    def to_dict_type_test(self):
        self.assertTrue(dict, type(City().to_dict()))

    def to_dict_contains_correct_keys_test(self):
        cy = City()
        self.assertIn("id", cy.to_dict())
        self.assertIn("created_at", cy.to_dict())
        self.assertIn("updated_at", cy.to_dict())
        self.assertIn("__class__", cy.to_dict())

    def to_dict_contains_added_attributes_test(self):
        cy = City()
        cy.middle_name = "Holberton"
        cy.my_number = 98
        self.assertEqual("Holberton", cy.middle_name)
        self.assertIn("my_number", cy.to_dict())

    def to_dict_datetime_attributes_are_strs_test(self):
        cy = City()
        cy_dict = cy.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def to_dict_output_test(self):
        dt = datetime.today()
        cy = City()
        cy.id = "123456"
        cy.created_at = cy.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(cy.to_dict(), tdict)

    def contrast_to_dict_dunder_dict_test(self):
        cy = City()
        self.assertNotEqual(cy.to_dict(), cy.__dict__)

    def to_dict_with_arg_test(self):
        cy = City()
        with self.assertRaises(TypeError):
            cy.to_dict(None)


if __name__ == "__main__":
    unittest.main()
