from typing import List
from sqlalchemy import text

from src.database.db_session import db_session
from src.models.vehicle_model import VehicleModel


def execute_raw_sql(query: str) -> List[VehicleModel] | None:
    """
    Execute a raw query SQL.

    Args:
        query (str): A raw query to execute.

    Returns:
        List[VehicleModel]: return a list of VehicleModel
    """
    session = db_session.get_session()

    try:
        result = session.execute(text(query)).fetchall()

        if len(result) > 0:
            return [VehicleModel(**dict(row._mapping)) for row in result]

    except Exception as e:
        session.rollback()
        raise RuntimeError(f"Erro na execução da query: {str(e)}")
    finally:
        session.close()
