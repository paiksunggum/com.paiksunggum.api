from apps.star_craft.domain.ontology.spam.spam_category import SpamCategory

SPAM_TAXONOMY: dict[SpamCategory, list[str]] = {
    SpamCategory.PHISHING: ["계정 탈취", "링크 위장", "긴급 문구"],
    SpamCategory.PROMOTIONAL: ["할인", "이벤트", "구독"],
    SpamCategory.MALWARE: ["첨부파일", "실행파일", "매크로"],
    SpamCategory.SCAM: ["금전 요구", "당첨 알림", "투자 유도"],
    SpamCategory.LEGITIMATE: [],
}
