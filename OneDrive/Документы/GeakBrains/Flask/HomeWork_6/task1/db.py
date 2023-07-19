import databases
import sqlalchemy
from settings import settings
from enum import StrEnum

DATABASE_URL = settings.DATABASE_URL
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("firstname", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("lastname", sqlalchemy.String(32), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String(128), nullable=False, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(128), nullable=False)
)

goods = sqlalchemy.Table(
    "goods",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(100), nullable=False, unique=True),
    sqlalchemy.Column("description", sqlalchemy.Text(), nullable=False),
    sqlalchemy.Column("price", sqlalchemy.DECIMAL(10, 2), default=0)
)


class OrderStatus(StrEnum):
    OPEN = "открыт"
    FORMED = "формируется"
    CONFIRMED = "подтвержден"
    IN_DELIVERY = "в доставке"
    DELIVERED = "доставлен"
    CLOSED = "закрыт"


orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("datetime_create", sqlalchemy.DateTime()),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("good_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("goods.id")),
    sqlalchemy.Column("status", sqlalchemy.String(100), nullable=False, default=OrderStatus.OPEN)
)


def init_db():
    engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    metadata.drop_all(engine)
    metadata.create_all(engine)