from apps.star_craft.domain.ontology.email.email_template import EMAIL_TEMPLATES
from apps.star_craft.domain.ontology.email.email_type import EmailType


class EmailOntology:
    @staticmethod
    def get_template_rule(email_type: EmailType) -> str:
        return EMAIL_TEMPLATES[email_type]
