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

import dataclasses

__all__ = "VersionInfo"


@dataclasses.dataclass
class VersionInfo:
    major: int
    minor: int
    micro: int
    suffix: str = dataclasses.field(default="", init=False)

    def set_debug(self) -> None:
        self.suffix = "-dbg"

    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.micro}{self.suffix}"
