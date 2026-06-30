from apps.automode.adapter.outbound.clients.exaone_slm_adapter import ExaoneSLMAdapter
from apps.automode.adapter.outbound.gateways.n8n_email_gateway import N8nEmailGateway
from apps.automode.app.ports.input.i_email_send_use_case import IEmailSendUseCase
from apps.automode.app.use_cases.email_send_interactor import EmailSendInteractor


def get_email_send_use_case() -> IEmailSendUseCase:
    return EmailSendInteractor(
        slm=ExaoneSLMAdapter(),
        gateway=N8nEmailGateway(),
    )
