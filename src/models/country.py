"""
Country related functionality
"""

from src import repo, db
from typing import List

class Country(db.Model):
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """

    __tablename__ = 'countries'

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cities = db.relationship('City', backref='country', lazy=True)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> List["Country"]:
        """Get all countries"""
        countries: list["Country"] = repo.get_all("country")

        return countries

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        for country in Country.get_all():
            if country.code == code:
                return country
        return None

    @staticmethod
    def create(name: str, code: str) -> "Country":
        """Create a new country"""
        country = Country(name, code)

        repo.save(country)

        return country
