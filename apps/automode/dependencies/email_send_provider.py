from apps.automode.adapter.outbound.n8n_email_gateway import N8nEmailGateway
from apps.automode.app.ports.input.i_email_send_use_case import IEmailSendUseCase
from apps.automode.app.use_cases.email_send_interactor import EmailSendInteractor
from core.lol.faker_orchestrator import FakerOrchestrator


def get_email_send_use_case() -> IEmailSendUseCase:
    return EmailSendInteractor(
        orchestrator=FakerOrchestrator(),
        gateway=N8nEmailGateway(),
    )
