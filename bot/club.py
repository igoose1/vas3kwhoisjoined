import dataclasses
import datetime
import logging
import typing
from urllib.parse import urljoin

import httpx

from .database import User

CLUB_URL = "https://vas3k.club"

logger = logging.getLogger("bot")


def build_profile_url(slug: str) -> str:
    return urljoin(CLUB_URL, f"/user/{slug}")


def build_by_telegram_endpoint_url(uid: int) -> str:
    return urljoin(
        CLUB_URL,
        f"/user/by_telegram_id/{uid}.json",
    )


class NetClubException(Exception):
    pass


class MemberNotFound(Exception):
    pass


@dataclasses.dataclass
class ClubMember:
    full_name: str
    slug: str
    profile_url: str = dataclasses.field(init=False)

    def __post_init__(self):
        self.profile_url = build_profile_url(self.slug)


@dataclasses.dataclass
class Club:
    token: str
    client: httpx.Client = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        headers = {"Cookie": f"token={self.token}"}
        self.client = httpx.Client(headers=headers)

    def fetch(self, telegram_id: int) -> User | typing.NoReturn:
        try:
            logger.info("do a fetch (tid=%s).", telegram_id)
            response = self.client.get(
                build_by_telegram_endpoint_url(telegram_id),
            )
        except httpx.RequestError:
            logger.exception("couldn't get data from club.")
            raise NetClubException
        if response.status_code == 400:
            User.create(
                telegram_id=telegram_id,
                is_in_club=False,
            )
            raise MemberNotFound
        try:
            user = response.json()["user"]
            User.delete().where(User.telegram_id == telegram_id).execute()
            return User.create(
                telegram_id=telegram_id,
                is_in_club=True,
                full_name=user["full_name"],
                club_slug=user["slug"],
            )
        except KeyError:
            logger.exception("couldn't parse data from club.")
            raise NetClubException

    def is_data_too_old(self, user: User) -> bool:
        delta = datetime.datetime.now() - user.last_checked
        return (
            not user.is_in_club and delta > datetime.timedelta(hours=1)
        ) or (user.is_in_club and delta > datetime.timedelta(days=1))

    def get_or_fetch(self, telegram_id: int) -> User | typing.NoReturn:
        try:
            user = User.get(User.telegram_id == telegram_id)
        except User.DoesNotExist:
            return self.fetch(telegram_id)
        if self.is_data_too_old(user):
            user = self.fetch(telegram_id)
        return user

    def whois(self, telegram_id: int) -> ClubMember | typing.NoReturn:
        user = self.get_or_fetch(telegram_id)
        if user.is_in_club:
            return ClubMember(user.full_name, user.club_slug)
        else:
            raise MemberNotFound
