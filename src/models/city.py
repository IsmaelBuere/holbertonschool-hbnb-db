"""
City related functionality
"""

from src.models.base import Base
from src import repo, db
from src.models.country import Country


class City(Base):
    """City representation"""

    __tablename__ = 'cities'

    name = db.Column(db.String(100), nullable=False)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.code'), nullable=False)

    def __repr__(self) -> str:
        """Dummy repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        country = Country.get(data["country_code"])

        if not country:
            raise ValueError("Country not found")

        cities: list[City] = City.get_all()

        for city in cities:
            if city.name == data["name"]:
                if city.country_code == data["country_code"]:
                    raise ValueError("City already exists")

        city = City(**data)

        repo.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city
