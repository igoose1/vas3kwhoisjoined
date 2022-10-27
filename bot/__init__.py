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

from envparse import Env

from .utils import VersionInfo

__all__ = (
    "API_ID",
    "API_HASH",
    "BOT_TOKEN",
    "CLUB_TOKEN",
    "__version__",
)

__version__ = VersionInfo(0, 0, 1)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
    ],
)

env = Env()
API_ID = env.int("API_ID")
API_HASH = env("API_HASH")
BOT_TOKEN = env("BOT_TOKEN")
CLUB_TOKEN = env("CLUB_TOKEN")
IS_DEBUG = env.bool("DEBUG", default=False)

if IS_DEBUG:
    __version__.set_debug()

HELP_MESSAGE = f"bot: {__version__}"
DEFAULT_FOUND_MESSAGE = '$fullname в <a href="$url">клубе</a>!'
DEFAULT_NOT_FOUND_MESSAGE = "$fullname не найден в клубе!"
CONFIGURED_MESSAGE = "Бот работает в этом чате!"
