from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import json
import re
import time
from typing import Optional

load_dotenv()

client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL"),
)

MODEL = os.getenv("LLM_MODEL")
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
MAX_RETRIES = 3


def clean_json_string(content: str) -> str:
    """Очищает типичные ошибки локальной модели"""
    content = re.sub(r'[\u200b\u200c\u200d\ufeff]', '', content)          # невидимые символы
    content = re.sub(r'Remote\s*US[D$]?', 'Remote_USD', content)          # частые опечатки
    content = re.sub(r'Regions_RF\s*\{?', 'Regions_RF', content)
    content = content.replace('"Remote US$"', '"Remote_USD"')
    content = content.replace("'Remote US$'", '"Remote_USD"')
    return content.strip()


def call_llm(
    system_prompt: str,
    user_message: str,
    response_model: type[BaseModel] | None = None,
) -> BaseModel | str:
    """
    Вызов LLM с retry + очисткой JSON.
    Пытается до MAX_RETRIES раз при ошибках валидации или парсинга.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ]

            if response_model:
                schema = response_model.model_json_schema()
                json_instruction = (
                    "Ответь **ТОЛЬКО** чистым валидным JSON без какого-либо дополнительного текста, "
                    "markdown или объяснений. Не используй ```json."
                )
                full_system = f"{system_prompt}\n\n{json_instruction}\n\nJSON Schema:\n{json.dumps(schema, indent=2)}"
                messages[0]["content"] = full_system

                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=TEMPERATURE,
                    response_format={
                        "type": "json_schema",
                        "json_schema": {
                            "name": response_model.__name__,
                            "schema": schema,
                            "strict": True
                        }
                    }
                )

                content = completion.choices[0].message.content.strip()
                content = clean_json_string(content)

                data = json.loads(content)
                return response_model.model_validate(data)

            else:
                # Текстовый режим (не используется в агентах)
                completion = client.chat.completions.create(
                    model=MODEL,
                    messages=messages,
                    temperature=TEMPERATURE,
                )
                return completion.choices[0].message.content

        except Exception as e:
            print(f"Попытка {attempt}/{MAX_RETRIES} не удалась: {type(e).__name__}")
            if attempt == MAX_RETRIES:
                raise ValueError(
                    f"Не удалось получить валидный JSON после {MAX_RETRIES} попыток.\n"
                    f"Последняя ошибка: {e}"
                )
            time.sleep(1.5)  # небольшая пауза между попытками

    raise ValueError("Неизвестная ошибка в call_llm")