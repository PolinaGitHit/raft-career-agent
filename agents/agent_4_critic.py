from core.llm import call_llm
from core.schemas import SkillMap, Agent2Output, Agent3Output, Agent4Output

def agent_4_critic(
    skill_map: SkillMap,
    agent2: Agent2Output,
    agent3: Agent3Output
) -> Agent4Output:
    """
    Агент 4: Критик и верификатор (адаптирован под слабую локальную модель)
    """
    system_prompt = """
Ты — строгий, но справедливый технический ревьюер.
Проверяй отчёт на реальные противоречия, а не на мелкие обрезанные строки.

Проверяемые критерии:
- Зарплаты соответствуют уровню навыков? (да → хорошо)
- Portfolio использует технологии из skill_map? (да → хорошо)
- Learning path логичен?
- Нет ли явных противоречий (declining навык в приоритете learning_path)?

Если всё в целом связано и полезно — ставь quality_score 75-90.
Warnings — только реальные проблемы.
is_consistent = True, если нет критических ошибок.

Ответь ТОЛЬКО JSON по схеме Agent4Output.
"""

    context = f"""
=== SKILL MAP ===
{skill_map.model_dump_json(indent=2)}

=== SALARY & MARKET ===
{agent2.model_dump_json(indent=2)}

=== LEARNING + PORTFOLIO ===
{agent3.model_dump_json(indent=2)}
"""

    user_message = f"""
Роль: Backend Python Developer

Полный контекст:
{context}

Оцени отчёт реалистично для 2025-2026 года.
"""

    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=Agent4Output
    )


# ====================== ТЕСТ АГЕНТА 4 ======================
if __name__ == "__main__":
    # Для теста запускаем полную цепочку 1 → 2 → 3 → 4
    from agents.agent_1_analyst import agent_1_analyst
    from agents.agent_2_salary import agent_2_salary
    from agents.agent_3_advisor import agent_3_advisor
    
    test_role = "Backend Python Developer"
    
    print(f"Запуск Агента 4 для роли: {test_role}\n")
    
    skill_map = agent_1_analyst(test_role)
    agent2 = agent_2_salary(skill_map)
    agent3 = agent_3_advisor(skill_map, agent2)
    
    result = agent_4_critic(skill_map, agent2, agent3)
    
    print("Агент 4 успешно завершён!\n")
    print(result.model_dump_json(indent=2))