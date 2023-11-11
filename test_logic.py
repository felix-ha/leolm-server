from logic import LLM, LLMResponse, Chat, Message

expected_llm_response_1 = LLMResponse(
    answer="No Transformer loaded!",
    chat=Chat(
        messages=[
            Message(role="user", content="How are you?"),
            Message(role="assistant", content="No Transformer loaded!"),
        ]
    ),
)
expected_llm_response_2 = LLMResponse(
    answer="No Transformer loaded!",
    chat=Chat(
        messages=[
            Message(role="user", content="How are you?"),
            Message(role="assistant", content="No Transformer loaded!"),
            Message(role="user", content="Fine"),
            Message(role="assistant", content="No Transformer loaded!"),
        ]
    ),
)


def test_llm():
    llm = LLM("offline")

    result = llm("How are you?")
    result_2 = llm("Fine", result.chat)

    assert result == expected_llm_response_1
    assert result_2 == expected_llm_response_2
