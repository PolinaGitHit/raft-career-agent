from core.llm import call_llm
from core.schemas import SkillMap

def agent_1_analyst(role: str) -> SkillMap:
    """
    Агент 1: Аналитик рынка
    Вход: название роли (строка)
    Выход: SkillMap — структурированная карта навыков
    """
    system_prompt = """
Ты — ведущий аналитик российского и международного IT-рынка (2025–2026 год).
Твоя задача — составить максимально точную и актуальную карту востребованных навыков для указанной роли.

Правила:
- Только реальные навыки, которые встречаются в вакансиях прямо сейчас.
- Категории строго четыре: languages, frameworks, infrastructure, soft_skills.
- Для каждого навыка обязательно укажи:
  • demand: "critical" / "important" / "nice-to-have"
  • trend: "growing" / "stable" / "declining"
- Не придумывай навыки, которых нет на рынке.
- Ответ должен быть ТОЛЬКО чистым JSON по схеме SkillMap. Без объяснений.
"""

    user_message = f"""
Роль: {role}

Верни JSON строго по схеме SkillMap.
"""

    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=SkillMap
    )


# ====================== ТЕСТ АГЕНТА 1 ======================
if __name__ == "__main__":
    test_role = "Backend Python Developer"
    print(f"Запуск Агента 1 для роли: {test_role}\n")
    
    result = agent_1_analyst(test_role)
    
    print("Агент 1 успешно завершён!\n")
    print(result.model_dump_json(indent=2))