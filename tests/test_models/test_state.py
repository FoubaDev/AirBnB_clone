#!/usr/bin/python3
"""Defines unittests for models/state.py.
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation"""

    def no_args_instantiates_test(self):
        self.assertEqual(State, type(State()))

    def new_instance_stored_in_objects_test(self):
        self.assertIn(State(), models.storage.all().values())

    def id_is_public_str_test(self):
        self.assertEqual(str, type(State().id))

    def created_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(State().created_at))

    def updated_at_is_public_datetime_test(self):
        self.assertEqual(datetime, type(State().updated_at))

    def name_is_public_class_attribute_test(self):
        st = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(st))
        self.assertNotIn("name", st.__dict__)

    def two_states_unique_ids_test(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def two_states_different_created_at_test(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def two_states_different_updated_at_test(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def str_representation_test(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        ststr = st.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    def args_unused_test(self):
        st = State(None)
        self.assertNotIn(None, st.__dict__.values())

    def instantiation_with_kwargs_test(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        st = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(st.id, "345")
        self.assertEqual(st.created_at, dt)
        self.assertEqual(st.updated_at, dt)

    def instantiation_with_None_kwargs_test(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method"""

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
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        self.assertLess(first_updated_at, st.updated_at)

    def two_saves_test(self):
        st = State()
        sleep(0.05)
        first_updated_at = st.updated_at
        st.save()
        second_updated_at = st.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        st.save()
        self.assertLess(second_updated_at, st.updated_at)

    def save_with_arg_test(self):
        st = State()
        with self.assertRaises(TypeError):
            st.save(None)

    def save_updates_file_test(self):
        st = State()
        st.save()
        stid = "State." + st.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method"""

    def to_dict_type_test(self):
        self.assertTrue(dict, type(State().to_dict()))

    def to_dict_contains_correct_keys_test(self):
        st = State()
        self.assertIn("id", st.to_dict())
        self.assertIn("created_at", st.to_dict())
        self.assertIn("updated_at", st.to_dict())
        self.assertIn("__class__", st.to_dict())

    def to_dict_contains_added_attributes_test(self):
        st = State()
        st.middle_name = "Holberton"
        st.my_number = 98
        self.assertEqual("Holberton", st.middle_name)
        self.assertIn("my_number", st.to_dict())

    def to_dict_datetime_attributes_are_strs_test(self):
        st = State()
        st_dict = st.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def to_dict_output_test(self):
        dt = datetime.today()
        st = State()
        st.id = "123456"
        st.created_at = st.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(st.to_dict(), tdict)

    def contrast_to_dict_dunder_dict_test(self):
        st = State()
        self.assertNotEqual(st.to_dict(), st.__dict__)

    def to_dict_with_arg_test(self):
        st = State()
        with self.assertRaises(TypeError):
            st.to_dict(None)


if __name__ == "__main__":
    unittest.main()
