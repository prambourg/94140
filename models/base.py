from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True

    def row2dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
