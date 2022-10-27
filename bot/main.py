# Copyright 2022 Oskar Sharipov
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import string

import pyrogram

from . import (
    API_HASH,
    API_ID,
    BOT_TOKEN,
    CLUB_TOKEN,
    CONFIGURED_MESSAGE,
    DEFAULT_NOT_FOUND_MESSAGE,
    HELP_MESSAGE,
)
from .club import Club, MemberNotFound, NetClubException
from .database import Chat, User

__all__ = ("app",)

logger = logging.getLogger("bot")
app = pyrogram.Client("bot", API_ID, API_HASH, bot_token=BOT_TOKEN)
club = Club(CLUB_TOKEN)


def is_enabled_chat(
    filter_,
    client: pyrogram.Client,
    update: pyrogram.types.Message,
) -> bool:
    try:
        _ = Chat.get(Chat.telegram_id == update.chat.id)
        return True
    except Chat.DoesNotExist:
        return False


IsEnabledFilter = pyrogram.filters.create(is_enabled_chat, "IsEnabledFilter")


@app.on_message(pyrogram.filters.new_chat_members & IsEnabledFilter)
def welcome_new_chat_member(client, message: pyrogram.types.Message):
    logger.info("new chat member (uid=%d).", message.from_user.id)

    chat = Chat.get(Chat.telegram_id == message.chat.id)
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()

    try:
        member = club.whois(message.from_user.id)
    except MemberNotFound:
        message.reply(
            string.Template(DEFAULT_NOT_FOUND_MESSAGE).safe_substitute(
                fullname=full_name,
            ),
            quote=True,
        )
        return
    except NetClubException:
        return
    message.reply(
        string.Template(chat.found_message).safe_substitute(
            fullname=full_name,
            url=member.profile_url,
        ),
        quote=True,
    )


@app.on_message(pyrogram.filters.command("start") & pyrogram.filters.private)
def start(client, message: pyrogram.types.Message):
    message.reply(HELP_MESSAGE, quote=True, disable_web_page_preview=True)


@app.on_message(pyrogram.filters.command("start") & pyrogram.filters.group)
def enable_group(client, message: pyrogram.types.Message):
    try:
        club.whois(message.from_user.id)
    except (MemberNotFound, NetClubException):
        return
    Chat.create(
        telegram_id=message.chat.id,
        configured_by=User.get(User.telegram_id == message.from_user.id),
    )
    message.reply(
        CONFIGURED_MESSAGE,
        quote=True,
    )
