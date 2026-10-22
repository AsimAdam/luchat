from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from luchat.config import get_settings
from luchat.prompts import SYSTEM_PROMPT
from luchat.schemas import ChatMessage

_settings = get_settings()
_client = OpenAI(api_key=_settings.openai_api_key)


def complete(messages: list[ChatMessage]) -> str:
    api_messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]
    for message in messages:
        if message.role == "user":
            api_messages.append({"role": "user", "content": message.content})
        else:
            api_messages.append({"role": "assistant", "content": message.content})

    response = _client.chat.completions.create(
        model=_settings.openai_model,
        messages=api_messages,
    )
    reply = response.choices[0].message.content
    if not reply:
        raise RuntimeError("The model returned an empty reply")
    return reply
