from core.llm import call_llm
from core.schemas import SkillMap, Agent3Output

def fix_agent3(skill_map: SkillMap, agent3_output: Agent3Output) -> Agent3Output:
    """
    Исправляет gap_analysis и portfolio_project в выводе Агента 3.
    """
    system_prompt = """
Ты — редактор карьерных отчётов. Исправь gap_analysis и portfolio_project, сделав их чистыми и профессиональными.

Требования:
- gap_analysis.quick_wins: 3–5 конкретных пунктов
- gap_analysis.long_term: 3–5 конкретных пунктов (без "...")
- portfolio_project:
  - title: конкретное название проекта
  - description: 2–4 полных предложения на русском
  - skills_demonstrated: 5+ технологий из skill_map

Верни ТОЛЬКО чистый JSON по схеме Agent3Output (только исправленные поля).
"""

    user_message = f"""
Skill Map:
{skill_map.model_dump_json(indent=2)}

Текущий (плохой) вывод Агента 3:
{agent3_output.model_dump_json(indent=2)}

Исправь gap_analysis и portfolio_project.
"""

    fixed = call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=Agent3Output
    )
    return fixed