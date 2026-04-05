from core.llm import call_llm
from core.schemas import SkillMap, Agent2Output, Agent3Output

def agent_3_advisor(skill_map: SkillMap, agent2_output: Agent2Output) -> Agent3Output:
    """
    Агент 3 — максимально строгая версия под ТЗ Raft
    """
    system_prompt = """
Ты — очень строгий и внимательный карьерный ментор. 
Твоя задача — вернуть **идеально чистый, полный и профессиональный** JSON без единого артефакта.

СТРОГИЕ ПРАВИЛА (обязательно выполнять):

1. learning_path.phases — ровно 3 фазы:
   - "Foundation", "Practice", "Portfolio"
   - Каждая фаза должна иметь:
     * topics: минимум 4 конкретные темы
     * resources: ровно минимум 2 объекта, каждый с "name" и "type" (book / course / documentation / video)
     * milestone: одно чёткое, измеримое предложение

2. gap_analysis:
   - quick_wins: минимум 3 пункта (можно закрыть за 2–4 недели)
   - long_term: минимум 3 пункта (3+ месяца)

3. portfolio_project (КРИТИЧНО ВАЖНО):
   - title: красивое и конкретное название проекта
   - description: 2–4 полных осмысленных предложения (что делает проект, зачем он нужен)
   - skills_demonstrated: список минимум из 4–6 технологий, **точно** взятых из skill_map (без выдумок)

Запрещено:
- Любые "..." , "Текст...", "OK?", "Вход в формат...", placeholder
- Неполные объекты в resources
- Пустые списки
- Обрезанные слова

Вот хороший пример структуры:

{
  "learning_path": {
    "phases": [
      {
        "phase": "Foundation",
        "topics": ["Python advanced", "OOP", "SQL + PostgreSQL", "Django basics"],
        "resources": [
          {"name": "Automate the Boring Stuff with Python", "type": "book"},
          {"name": "Official Django Tutorial", "type": "documentation"}
        ],
        "milestone": "Создать CRUD-приложение на Django с PostgreSQL и Docker"
      },
      {
        "phase": "Practice",
        "topics": ["FastAPI", "Docker Compose", "REST API", "Testing"],
        "resources": [
          {"name": "FastAPI Official Tutorial", "type": "documentation"},
          {"name": "Test-Driven Development with FastAPI", "type": "course"}
        ],
        "milestone": "Построить два микросервиса и развернуть их через Docker Compose"
      },
      {
        "phase": "Portfolio",
        "topics": ["Kubernetes", "CI/CD", "Security", "Monitoring"],
        "resources": [
          {"name": "Kubernetes in Action", "type": "book"},
          {"name": "GitHub Actions Documentation", "type": "documentation"}
        ],
        "milestone": "Деплоить проект на Kubernetes с CI/CD"
      }
    ]
  },
  "gap_analysis": {
    "quick_wins": ["Освоить Docker", "Настроить CI/CD", "Добавить тесты"],
    "long_term": ["Изучить Kubernetes deeply", "Освоить микросервисную архитектуру"]
  },
  "portfolio_project": {
    "title": "TaskFlow — Корпоративная система управления задачами",
    "description": "Полноценный бэкенд для системы управления проектами и задачами с поддержкой команд, уведомлений и аналитики. Проект демонстрирует навыки работы с Django, FastAPI, контейнеризацией и оркестрацией.",
    "skills_demonstrated": ["Python", "Django", "FastAPI", "Docker", "PostgreSQL", "Redis"]
  }
}

Создай такой же качественный план для Backend Python Developer.
Ответь **ТОЛЬКО** чистым JSON.
"""

    skills_text = skill_map.model_dump_json(indent=2)
    salary_text = agent2_output.model_dump_json(indent=2)

    user_message = f"Роль: Backend Python Developer\n\nSkill Map:\n{skills_text}\n\nSalary & Market:\n{salary_text}"

    return call_llm(
        system_prompt=system_prompt,
        user_message=user_message,
        response_model=Agent3Output
    )


# ====================== ТЕСТ АГЕНТА 3 ======================
if __name__ == "__main__":
    # Для теста берём готовые данные от Агентов 1 и 2
    from agents.agent_1_analyst import agent_1_analyst
    from agents.agent_2_salary import agent_2_salary
    
    test_role = "Backend Python Developer"
    
    print(f"Запуск Агента 3 для роли: {test_role}\n")
    
    # Получаем входные данные
    skill_map = agent_1_analyst(test_role)
    agent2 = agent_2_salary(skill_map)
    
    # Запускаем только Агента 3
    result = agent_3_advisor(skill_map, agent2)
    
    print("Агент 3 успешно завершён!\n")
    print(result.model_dump_json(indent=2))