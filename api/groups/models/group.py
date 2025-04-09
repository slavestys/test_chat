import typing

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey

from db.model import Base
from users.models import User


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255))
    creator_id = mapped_column(ForeignKey("users.id"), nullable=False)
    creator: Mapped[User] = relationship(back_populates="created_groups")
    group_type: Mapped[int]
    chat: Mapped["Chat"] = relationship(back_populates="group")
    groups_users: Mapped[typing.List["GroupUser"]] = relationship()
    users: Mapped[typing.List[User]] = relationship(
        back_populates="groups",
        secondary="groups_users",
    )

    def is_member(self, checking_user):
        found = next((user for user in self.users if user.id == checking_user.id), None)
        return bool(found)
