""" Abstract base class for all models """

from datetime import datetime
from typing import Any, Optional, List
from src import repo, db
import uuid
from abc import abstractmethod


class Base(db.Model):
    """
    Base Interface for all models
    """
    __abstract__ = True
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    @classmethod
    def get(cls, id) -> Optional[Any]:
        """
        This is a common method to get an specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        return repo.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls) -> List[Any]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        return repo.get_all(cls.__name__.lower())

    @classmethod
    def delete(cls, id) -> bool:
        """
        This is a common method to delete an specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Optional[Any]:
        """Updates an object of the class"""
