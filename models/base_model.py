#!/usr/bin/python3

"""Defines the BaseModel class."""
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    """Base class for all our classes"""
    def __init__(self, *args, **kwargs):
        """
        Deserialize and serialize a class.
        """
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = self.updated_at = datetime.utcnow()
            models.storage.new(self)
            return

        self.id = kwargs.get('id', str(uuid4()))

        for key, val in kwargs.items():
            if key == "__class__":
                continue

        if "created_at" in kwargs:
            self.created_at = datetime.strptime(
                kwargs['created_at'], '%Y-%m-%dT%H:%M:%S'
                )

        if "updated_at" in kwargs:
            self.updated_at = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S'
            )

    def __str__(self):
        """string representation"""
        formated = "[{}] ({}) {}"
        return formated.format(
                type(self).__name__,
                self.id,
                self.__dict__)

    def save(self):
        """updating"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):
        """dictionary representation"""
        data = {**self.__dict__}
        data["__class__"] = type(self).__name__
        data["created_at"] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        data["updated_at"] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        return data

    @classmethod
    def all(cls):
        """Return all instance of class"""
        return models.storage.find_all(cls.__name__)

    @classmethod
    def count(cls):
        """Retrieve the number of all  instances of classe"""
        return len(models.storage.find_all(cls.__name__))

    @classmethod
    def create(cls, *args, **kwargs):
        """Creates an Instance"""
        new_instance = cls(*args, **kwargs)
        return new_instance.id

    @classmethod
    def show(cls, instance_id):
        """Retrieve an instance"""
        return models.storage.find_by_id(
            cls.__name__,
            instance_id
        )

    @classmethod
    def destroy(cls, instance_id):
        """Deletes an instance"""
        return models.storage.delete_by_id(
            cls.__name__,
            instance_id
        )

    @classmethod
    def update(cls, instance_id, *args):
        """Updates an instance with provided attribute(s).

        Args:
            instance_id (str): ID of the instance to update.
            *args: Pairs of attribute name and value for update.

        Raises:
            ValueError: If no attribute name is provided.
        """

        if not args:
            raise ValueError("Missing attribute name")

        if len(args) == 1 and isinstance(args[0], dict):
            updates = args[0].items()
        else:
            updates = [args[:2]]

        for attr, value in updates:
            models.storage.update_one(cls.__name__, instance_id, attr, value)
