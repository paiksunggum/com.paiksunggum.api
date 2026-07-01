from apps.automode.adapter.outbound.clients.exaone_slm_client import ExaoneSLMClient
from apps.automode.adapter.outbound.clients.telegram_client import TelegramClient
from apps.automode.adapter.outbound.gateways.n8n_email_gateway import N8nEmailGateway
from apps.automode.app.ports.input.email_send_use_case import EmailSendUseCase
from apps.automode.app.use_cases.email_send_interactor import EmailSendInteractor


def get_email_send_use_case() -> EmailSendUseCase:
    return EmailSendInteractor(
        slm=ExaoneSLMClient(),
        gateway=N8nEmailGateway(),
        telegram=TelegramClient(),
    )
