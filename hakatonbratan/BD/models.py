import sqlalchemy

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass

class Support(Base):
    __tablename__ = "support"

    telegram_id = sqlalchemy.Column(
        sqlalchemy.String(32),
        primary_key=True,
        unique=True
    )
    
    username = sqlalchemy.Column(
        sqlalchemy.String(128)
    )

    question = sqlalchemy.Column(
        sqlalchemy.String(4096)
    )

    def __repr__(self) -> str:
        return f"Запрос от пользователя: {self.telegram_id}"
