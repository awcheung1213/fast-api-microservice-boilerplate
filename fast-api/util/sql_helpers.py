import logging
from sqlalchemy import Connection, Executable
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, IntegrityError
from typing import Any, Optional
from util.custom_exceptions import DatabaseException

logger = logging.getLogger(__name__)


def execute_sql(
        conn: Connection,
        sql: Executable,
        method: Optional[str] = None
) -> Any:
    """ Helper function for executing sql """
    try:
        if method == 'fetchall':
            results = conn.execute(sql).fetchall()
        elif method == 'fetchone':
            results = conn.execute(sql).fetchone()
        elif method == 'first':
            results = conn.execute(sql).first()
        else:
            results = conn.execute(sql)
        conn.commit()
    except IntegrityError as err:
        conn.rollback()
        raise DatabaseException(str(err), status_code=409, logger=logger)
    except (SQLAlchemyError, DBAPIError) as err:
        conn.rollback()
        raise DatabaseException(str(err), logger=logger)

    return results