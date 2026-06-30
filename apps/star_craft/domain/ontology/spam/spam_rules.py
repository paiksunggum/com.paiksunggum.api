from apps.star_craft.domain.ontology.spam.spam_category import SpamCategory

SPAM_KEYWORDS: dict[SpamCategory, list[str]] = {
    SpamCategory.PHISHING: ["비밀번호 변경", "계정 잠금", "즉시 클릭"],
    SpamCategory.PROMOTIONAL: ["무료", "특가", "지금 구매"],
    SpamCategory.MALWARE: ["파일 실행", "업데이트 필요", "보안 경고"],
    SpamCategory.SCAM: ["당첨", "송금", "수익 보장"],
}
