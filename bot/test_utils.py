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

import pytest

from .utils import VersionInfo


@pytest.mark.parametrize(
    ("version", "result"),
    [
        (VersionInfo(1, 2, 3), "v1.2.3"),
        (VersionInfo(10, 0, 10), "v10.0.10"),
    ],
)
def test_version_info_str(version, result):
    assert str(version) == result
