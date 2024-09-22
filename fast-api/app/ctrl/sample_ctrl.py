from sqlalchemy import Connection, select
from models.sample_model import SampleModel
from models.sample_table import sample_table_1, sample_table_2
from util.sql_helpers import execute_sql

def get_order_data(
        conn: Connection,
        order_number: int
) -> SampleModel:
    
    statement = select(
        sample_table_2.c.id,
        sample_table_1.c.name,
        sample_table_2.c.quantity,
        sample_table_2.c.price,
    ).where(sample_table_2.c.id == order_number)

    print(statement)

    result = execute_sql(statement, 'fetchone')

    data = SampleModel(
        id=result[0],
        name=result[1],
        quantity=result[2],
        price=result[3]
    )

    return data