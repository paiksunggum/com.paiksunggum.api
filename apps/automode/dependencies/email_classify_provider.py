from apps.automode.adapter.outbound.clients.exaone_slm_adapter import ExaoneSLMAdapter
from apps.automode.app.ports.input.i_email_classify_use_case import (
    IEmailClassifyUseCase,
)
from apps.automode.app.use_cases.classify_spam_interactor import ClassifySpamInteractor


def get_email_classify_use_case() -> IEmailClassifyUseCase:
    return ClassifySpamInteractor(slm=ExaoneSLMAdapter())
