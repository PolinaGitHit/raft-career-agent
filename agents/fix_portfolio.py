from core.llm import call_llm
from core.schemas import SkillMap, PortfolioProject

def fix_portfolio(skill_map: SkillMap, bad_project: dict) -> PortfolioProject:
    """Исправляет portfolio_project"""
    system_prompt = """
Ты — редактор карьерных отчётов. Сделай portfolio_project профессиональным.

Требования:
- title: привлекательное название проекта
- description: 2–4 полных предложения на русском языке
- skills_demonstrated: минимум 5 технологий из skill_map

Верни ТОЛЬКО чистый JSON.
"""

    user_message = f"""
Skill Map:
{skill_map.model_dump_json(indent=2)}

Плохой проект:
{bad_project}

Исправь его.
"""

    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=PortfolioProject
    )