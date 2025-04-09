from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.model import Base


class GroupUser(Base):
    __tablename__ = "groups_users"

    user_id = mapped_column(ForeignKey("users.id", ondelete="Cascade"), primary_key=True)
    group_id = mapped_column(ForeignKey("groups.id", ondelete="Cascade"), primary_key=True)