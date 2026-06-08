"""Titanic 인바운드 HTTP 라우터 조립."""

from fastapi import APIRouter

from apps.titanic.adapter.inbound.api.v1.crew_a_architect_router import a_architect_router
from apps.titanic.adapter.inbound.api.v1.crew_andrew_blueprint_router import andrew_blueprint_router
from apps.titanic.adapter.inbound.api.v1.crew_hartley_violin_router import hartley_violin_router
from apps.titanic.adapter.inbound.api.v1.crew_james_command_router import james_router
from apps.titanic.adapter.inbound.api.v1.crew_lowe_boat_router import lowe_boat_router
from apps.titanic.adapter.inbound.api.v1.crew_smith_captain_router import smith_captain_router
from apps.titanic.adapter.inbound.api.v1.passenger_cal_tester_router import cal_tester_router
from apps.titanic.adapter.inbound.api.v1.passenger_isidor_couple_router import isidor_couple_router
from apps.titanic.adapter.inbound.api.v1.passenger_jack_trainer_router import jack_trainer_router
from apps.titanic.adapter.inbound.api.v1.passenger_molly_scaler_router import molly_scaler_router
from apps.titanic.adapter.inbound.api.v1.passenger_rose_model_router import rose_model_router
from apps.titanic.adapter.inbound.api.v1.passenger_ruth_validation_router import ruth_validation_router

titanic_router = APIRouter()
titanic_router.include_router(james_router)
titanic_router.include_router(andrew_blueprint_router)
titanic_router.include_router(a_architect_router)
titanic_router.include_router(lowe_boat_router)
titanic_router.include_router(hartley_violin_router)
titanic_router.include_router(smith_captain_router)
titanic_router.include_router(rose_model_router)
titanic_router.include_router(jack_trainer_router)
titanic_router.include_router(molly_scaler_router)
titanic_router.include_router(cal_tester_router)
titanic_router.include_router(isidor_couple_router)
titanic_router.include_router(ruth_validation_router)

__all__ = [
    "a_architect_router",
    "andrew_blueprint_router",
    "cal_tester_router",
    "hartley_violin_router",
    "isidor_couple_router",
    "jack_trainer_router",
    "james_router",
    "lowe_boat_router",
    "molly_scaler_router",
    "rose_model_router",
    "ruth_validation_router",
    "smith_captain_router",
    "titanic_router",
]
