from core.llm import call_llm
from core.schemas import SkillItem, BaseModel   # ← добавили BaseModel

print("Тестируем подключение к LM Studio...")

# Простой тест (текстовый)
result = call_llm(
    system_prompt="Ты полезный ассистент.",
    user_message="Привет! Напиши одно предложение о Python-разработке.",
    response_model=None
)

print("LLM ответил:")
print(result)
print("\n" + "="*60)

# Тест структурированного ответа
class TestModel(BaseModel):
    greeting: str
    language: str

structured = call_llm(
    system_prompt="Ты полезный ассистент.",
    user_message="Ответь на приветствие и укажи язык.",
    response_model=TestModel
)

print("Структурированный ответ:")
print(structured.model_dump_json(indent=2))