import random
from datetime import datetime

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.database.models import Base, Vehicle
from utils.fetch_vehicles_data import search_vehicles


class DatabaseSession:
    _instance = None
    _engine = None
    _Session = None
    _fake = None
    _fuel_options = None
    _gearbox_options = None
    _category_options = None

    def __new__(cls, db_path: str = "vehicles.db"):
        if cls._instance is None:
            cls._instance = super(DatabaseSession, cls).__new__(cls)
            cls._engine = create_engine(f"sqlite:///{db_path}")
            Base.metadata.create_all(cls._engine)
            cls._Session = sessionmaker(bind=cls._engine)
            cls._fake = Faker("pt_BR")
            cls._fuel_options = [
                "Gasolina",
                "Etanol",
                "Diesel",
                "Flex",
                "Elétrico",
            ]
            cls._gearbox_options = ["Automática", "Manual"]
            cls._category_options = [
                "hatch",
                "sedan",
                "SUV",
                "picape",
                "minivans",
                "esportivos",
                "utilitários",
            ]

        return cls._instance

    @classmethod
    def get_session(cls):
        return cls._Session()

    @classmethod
    def create_vehicles(cls, brand: str, model: str) -> Vehicle:
        """Create a vehicles.

        Args:
            brand: Vehicles brand
            model: Vehicles model

        Returns:
            Vehicles: The Vehicles object
        """
        return Vehicle(
            marca=brand,
            modelo=model,
            ano=random.randint(2000, 2025),
            motor=cls._fake.bothify(text="#.# ?"),
            combustivel=random.choice(cls._fuel_options),
            cor=cls._fake.color_name(),
            quilometragem=random.randint(0, 500000),
            portas=random.choice([2, 4]),
            cambio=random.choice(cls._gearbox_options),
            categoria=random.choice(cls._category_options),
            preco=round(random.uniform(50000, 400000), 2),
            data_fabricacao=cls._fake.date_between(
                start_date=datetime(2000, 1, 1), end_date="today"
            ),
        )

    @classmethod
    def seed_database(cls) -> None:
        """Seed  database data with fictitious vehicles based on real data."""
        session = cls.get_session()
        try:
            vehicles = search_vehicles()

            for vehicles_data in vehicles:
                vehicles = cls.create_vehicles(
                    vehicles_data["Make"], vehicles_data["Model"]
                )
                session.add(vehicles)
                session.commit()

            print("Database populated successfully!")

        except Exception as e:
            print(f"Database populated error: {e}")
            session.rollback()
            raise
        finally:
            session.close()

    @classmethod
    def clean_database(cls) -> None:
        """Remove all data in database."""
        session = cls.get_session()
        try:
            session.query(Vehicle).delete()
            session.commit()
            print("Database cleaned successfully!")
        except Exception as e:
            print(f"Database cleaned error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


# Create a global session manager
db_session = DatabaseSession()
