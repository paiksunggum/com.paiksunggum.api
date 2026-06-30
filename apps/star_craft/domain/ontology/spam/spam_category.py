from enum import Enum


class SpamCategory(str, Enum):
    PHISHING = "phishing"
    PROMOTIONAL = "promotional"
    MALWARE = "malware"
    SCAM = "scam"
    LEGITIMATE = "legitimate"
