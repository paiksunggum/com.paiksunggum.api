from apps.star_craft.domain.ontology.email.email_type import EmailType

EMAIL_TEMPLATES: dict[EmailType, str] = {
    EmailType.FORMAL: "정중하고 격식 있는 문체. 존댓말 사용. 서론-본론-결론 구조.",
    EmailType.CASUAL: "친근하고 자연스러운 문체. 편안한 표현 사용.",
    EmailType.COMPLAINT: "불만 사항을 명확하고 논리적으로 전달. 감정적이지 않게.",
    EmailType.INQUIRY: "궁금한 사항을 명확하게 질문. 필요한 정보를 구체적으로 요청.",
}
