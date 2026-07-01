from apps.automode.adapter.outbound.clients.exaone_slm_client import ExaoneSLMClient
from apps.automode.app.ports.input.email_classify_use_case import EmailClassifyUseCase
from apps.automode.app.use_cases.classify_spam_interactor import ClassifySpamInteractor


def get_email_classify_use_case() -> EmailClassifyUseCase:
    return ClassifySpamInteractor(slm=ExaoneSLMClient())
