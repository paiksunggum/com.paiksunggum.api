import pytest
from unittest.mock import AsyncMock, MagicMock

from apps.titanic.app.use_cases.crew_james_command_interactor import JamesCommandInteractor
from apps.titanic.app.dtos.crew_james_command_dto import JamesCommandQuery, JamesCommandResponse
from apps.titanic.adapter.inbound.api.schemas.crew_james_command_schema import (
    JamesCommandFileUploadSchema,
    JamesCommandSchema,
)


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.introduce_myself = AsyncMock(
        return_value=JamesCommandResponse(id=4, name="James Cameron")
    )
    repo.upload_passengers = AsyncMock(return_value=3)
    return repo


@pytest.fixture
def interactor(mock_repository):
    return JamesCommandInteractor(repository=mock_repository)


def _schema(**overrides) -> JamesCommandFileUploadSchema:
    defaults = dict(
        passenger_id="1",
        survived="0",
        pclass="3",
        name="Braund, Mr. Owen Harris",
        gender="male",
        age="22",
        sib_sp="1",
        parch="0",
        ticket="A/5 21171",
        fare="7.25",
        cabin=None,
        embarked="S",
    )
    defaults.update(overrides)
    return JamesCommandFileUploadSchema(**defaults)


class TestIntroduceMyself:
    async def test_calls_repository_with_correct_query(self, interactor, mock_repository):
        schema = JamesCommandSchema(id=4, name="James Cameron")

        await interactor.introduce_myself(schema)

        mock_repository.introduce_myself.assert_called_once_with(
            JamesCommandQuery(id=4, name="James Cameron")
        )

    async def test_returns_repository_response(self, interactor):
        response = await interactor.introduce_myself(JamesCommandSchema(id=4, name="James Cameron"))

        assert response.id == 4
        assert response.name == "James Cameron"


class TestUploadPassengers:
    async def test_creates_one_passenger_command_per_record(self, interactor, mock_repository):
        await interactor.upload_passengers([_schema(passenger_id="1"), _schema(passenger_id="2")])

        person_commands, _ = mock_repository.upload_passengers.call_args.args
        assert len(person_commands) == 2

    async def test_passenger_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_passengers([_schema(passenger_id="7", gender="female", age="28")])

        person_commands, _ = mock_repository.upload_passengers.call_args.args
        cmd = person_commands[0]
        assert cmd.passenger_id == "7"
        assert cmd.gender == "female"
        assert cmd.age == "28"

    async def test_booking_command_contains_correct_fields(self, interactor, mock_repository):
        await interactor.upload_passengers([_schema(pclass="1", fare="100.0", embarked="C")])

        _, booking_commands = mock_repository.upload_passengers.call_args.args
        cmd = booking_commands[0]
        assert cmd.pclass == "1"
        assert cmd.fare == "100.0"
        assert cmd.embarked == "C"

    async def test_none_fields_become_empty_string(self, interactor, mock_repository):
        # None 값은 빈 문자열로 변환돼야 DB 커맨드가 일관성 유지
        await interactor.upload_passengers([_schema(survived=None, cabin=None)])

        person_commands, booking_commands = mock_repository.upload_passengers.call_args.args
        assert person_commands[0].survived == ""
        assert booking_commands[0].cabin == ""

    async def test_returns_inserted_count_from_repository(self, interactor):
        result = await interactor.upload_passengers([_schema()])

        assert result == {"inserted": 3}
