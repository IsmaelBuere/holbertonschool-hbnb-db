"""
  Now is easy to implement the database repository. The DBRepository
  should implement the Repository (Storage) interface and the methods defined
  in the abstract class Storage.

  The methods to implement are:
    - get_all
    - get
    - save
    - update
    - delete
    - reload (which can be empty)
"""
# Archivo que implementa el metodo de persistencia de tipo database (SQLAlchemy)

from src import db
from src.models.base import Base
from src.persistence.repository import Repository


class DBRepository(Repository):
    """Dummy DB repository"""

    def __init__(self) -> None:
        """Initialize the DBRepository"""

    def get_all(self, model_name: str) -> list:
        """Get all objects of the wanted model"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.all()
        return []

    def get(self, model_name: str, obj_id: str) -> Base | None:
        """Get an object by ID"""
        model_class = Base._decl_class_registry.get(model_name.capitalize())
        if model_class:
            return model_class.query.get(obj_id)
        return None

    def reload(self) -> None:
        """Reload data to the repository"""
        pass

    def save(self, obj: Base) -> None:
        """Save an object"""
        db.session.add(obj)
        db.session.commit()

    def update(self, obj: Base) -> Base | None:
        """Update an object"""
        db.session.commit()
        return obj

    def delete(self, obj: Base) -> bool:
        """Delete an object"""
        db.session.delete(obj)
        db.session.commit()
        return True
