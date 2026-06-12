import pytest


@pytest.mark.ollama
def test_korean_ai_integration():
    ollama = pytest.importorskip("ollama", reason="ollama 미설치")
    Kiwi = pytest.importorskip("kiwipiepy", reason="kiwipiepy 미설치").Kiwi

    kiwi = Kiwi()
    kiwi.space_tolerance = 2

    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."

    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    print(f"입력 문장: {question}")

    tokens = kiwi.tokenize(question)
    nouns = [t.form for t in tokens if t.tag.startswith('NN')]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] 야놀자 EEVE-Korean 모델 추론 중... ---")

    response = ollama.chat(
        model='anpigon/eeve-korean-10.8b:latest',
        messages=[{'role': 'user', 'content': question}]
    )
    answer = response['message']['content']

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)

    assert answer, "모델 응답이 비어 있습니다."


if __name__ == "__main__":
    import ollama
    from kiwipiepy import Kiwi as _Kiwi

    kiwi = _Kiwi()
    kiwi.space_tolerance = 2
    question = "자연어처리는 넘흐 재밌어요. 올라마와 키위 라이브러리의 장점을 짧게 요약해줘."

    print("\n--- [1단계] 입력 문장 전처리 중... ---")
    print(f"입력 문장: {question}")
    tokens = kiwi.tokenize(question)
    nouns = [t.form for t in tokens if t.tag.startswith('NN')]
    print(f"추출된 핵심 명사: {nouns}")

    print("\n--- [2단계] 야놀자 EEVE-Korean 모델 추론 중... ---")
    response = ollama.chat(
        model='anpigon/eeve-korean-10.8b:latest',
        messages=[{'role': 'user', 'content': question}]
    )
    answer = response['message']['content']

    print("\n--- [3단계] AI 최종 답변 ---")
    print(answer)
