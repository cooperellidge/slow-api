import pytest
import slow_api


def test_app() -> None:
    _ = slow_api.SlowAPI()
    assert True


def test_enums() -> None:
    status_code = slow_api.enums.HttpStatusCode.HTTP_200_GOOD
    assert status_code == 200


def test_exceptions() -> None:
    with pytest.raises(slow_api.exceptions.HttpError):
        raise slow_api.exceptions.UnhandledProtocolError
