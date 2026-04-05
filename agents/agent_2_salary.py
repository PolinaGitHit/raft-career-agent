from core.llm import call_llm
from core.schemas import SkillMap, Agent2Output

def agent_2_salary(skill_map: SkillMap) -> Agent2Output:
    """
    Агент 2: Оценщик зарплат
    Вход: skill_map от Агента 1
    Выход: salary_table + market_trend + top_employers
    """
    system_prompt = """
Ты — ведущий специалист по заработным платам в IT-рынке России и Remote (2025–2026 год).
Ты точно знаешь актуальные вилки по грейдам и регионам.

Правила:
- Грейды: Junior / Middle / Senior / Lead
- Регионы: Moscow / Regions_RF / Remote_USD
- Для каждой ячейки указывай min / median / max (целые числа)
- market_trend: "growing" | "stable" | "declining" + короткое обоснование (1-2 предложения)
- top_employers: 3–5 реальных компаний, которые активно нанимают на эту роль
- Будь реалистичным по цифрам (учитывай текущий рынок)
- Ответ — ТОЛЬКО чистый JSON по схеме Agent2Output
"""

    # Превращаем skill_map в читаемый текст для промпта
    skill_text = skill_map.model_dump_json(indent=2)

    user_message = f"""
Роль: Backend Python Developer

Навыки (skill_map):
{skill_text}

Верни JSON строго по схеме Agent2Output.
"""

    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=Agent2Output
    )


# ====================== ТЕСТ АГЕНТА 2 ======================
if __name__ == "__main__":
    # Для теста берём готовый skill_map из Агента 1
    from agents.agent_1_analyst import agent_1_analyst
    
    test_role = "Backend Python Developer"
    skill_map = agent_1_analyst(test_role)
    
    print(f"Запуск Агента 2 для роли: {test_role}\n")
    
    result = agent_2_salary(skill_map)
    
    print("Агент 2 успешно завершён!\n")
    print(result.model_dump_json(indent=2))