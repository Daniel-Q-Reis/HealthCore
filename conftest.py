import pytest
from typing import Any


@pytest.fixture
def user() -> Any:
    from apps.users.factories import UserFactory

    return UserFactory()
