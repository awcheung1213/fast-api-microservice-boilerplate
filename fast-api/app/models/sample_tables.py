from sqlalchemy import Boolean, Column, DateTime, Integer, func, MetaData, Numeric, String, Table
from sqlalchemy.dialects.postgresql import JSONB, UUID


#TODO: Replace placeholder
sample_table_1 = Table(
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('updated', DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column('is_available', Boolean, default=False),
    Column('metadata', JSONB),
    Column('name', String, nullable=False),
    name='product_table', metadata=MetaData()
)


#TODO: Replace placeholder
sample_table_2 = Table(
    Column('id', UUID(as_uuid=True), primary_key=True),
    Column('created', DateTime(timezone=True), nullable=False, server_default=func.now()),
    Column('quantity', Integer, nullable=False),
    Column('price', Numeric(10, 2), nullable=False),
    name='order_table', metadata=MetaData()
)
