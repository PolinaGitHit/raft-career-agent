<div align="center">

# raft-career-agent

Мультиагентная система анализа карьерного рынка IT

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063)](https://docs.pydantic.dev/)
[![LM Studio](https://img.shields.io/badge/LLM-LM%20Studio-orange)](https://lmstudio.ai/)
[![Status](https://img.shields.io/badge/status-test_assignment-blue)](#)

Тестовое задание на стажировку в **Raft**

</div>

---

## Содержание

- [Описание](#описание)
- [Требования](#требования)
- [Архитектура проекта](#архитектура-проекта)
- [Агенты](#агенты)
- [Запуск](#подробная-инструкция-запуска-и-установки)
- [Проверка агентов](#проверка-работы-агентов-по-отдельности)

## Описание

Система принимает название IT-специальности и генерирует структурированный карьерный отчёт с помощью 4 независимых агентов.

## Требования
- Python 3.11+
- LM Studio с поднятым OpenAI-compatible API
- Локально доступный endpoint, например `http://127.0.0.1:1234/v1`

**Что делает программа:**  
1. На вход программа принимает название роли, например:
    ```bash
    python main.py "Backend Python Developer"
    ```
2. Строит карту навыков по роли.
3. Оценивает зарплатные вилки и рыночный тренд.
4. Генерирует learning path, gap analysis и идею portfolio-проекта.  
5. Проверяет итоговый отчёт на согласованность.  
6. Сохраняет результат в examples/ в двух форматах:  
    - ROLE_NAME.json  
    - ROLE_NAME.md

## Архитектура проекта
```txt
raft-career-agent/
├── main.py                  # Точка входа CLI
├── requirements.txt         # Зависимости проекта
├── test_llm.py              # Проверка подключения к модели
├── core/
│   ├── llm.py               # Обёртка над LLM: вызов, retry, JSON parsing
│   └── schemas.py           # Pydantic-схемы всех сущностей
├── agents/
│   ├── agent_1_analyst.py   # Агент 1: карта навыков
│   ├── agent_2_salary.py    # Агент 2: зарплаты и рынок
│   ├── agent_3_advisor.py   # Агент 3: learning path и portfolio
│   ├── agent_4_critic.py    # Агент 4: верификация результата
│   └── fix_portfolio.py     # Дополнительная коррекция portfolio_project
└── examples/                # Сгенерированные примеры отчётов
```

## Агенты
- **Агент 1** — Аналитик рынка (skill_map)
- **Агент 2** — Оценщик зарплат (salary_table, market_trend, top_employers)
- **Агент 3** — Карьерный советник (learning_path, gap_analysis, portfolio_project)
- **Агент 4** — Критик и верификатор (quality_score, warnings, is_consistent)  

Агенты вызываются строго последовательно с явной передачей JSON-контекста.

1. **Агент 1 — Аналитик рынка**
    - Вход: role: str
    - Выход: SkillMap (languages, frameworks, infrastructure, soft_skills)

2. **Агент 2 — Оценщик зарплат**
    - Вход: SkillMap
    - Выход: Agent2Output (salary_table, market_trend, top_employers)

3. **Агент 3 — Карьерный советник**
    - Вход: SkillMap (Agent2Output)
    - Выход: Agent3Output (learning_path, gap_analysis, portfolio_project)  

    **Fix step — корректировка portfolio**  
    После Агента 3 выполняется дополнительный шаг fix_portfolio, который улучшает описание portfolio-проекта и приводит его к ожидаемой структуре.

4. **Агент 4 — Критик и верификатор**
    - Вход: SkillMap, Agent2Output, Agent3Output
    - Выход: Agent4Output (quality_scoreб, warnings is_consistent)

## Формат отчёта
- role  
- generated_at
- skill_map
- salary_table
- market_trend
- top_employers
- learning_path
- gap_analysis
- portfolio_project
- quality_score
- warnings
- is_consistent

## Особенности реализации
1. Используется строгая валидация через Pydantic.
2. Для LLM-ответов включён режим JSON Schema.
3. Есть повторные попытки (retry) при невалидном ответе модели.
4. Перед парсингом JSON выполняется очистка типичных артефактов локальной модели.

## Ограничения
1. Для работы нужен запущенный локальный сервер модели.
2. Качество результата зависит от выбранной модели в LM Studio.
3. Проект ориентирован на генерацию структурированных данных, а не на веб-интерфейс.
4. Некоторые промпты агентов сейчас лучше всего адаптированы под роль Backend Python Developer и могут требовать доработки для полностью универсальной поддержки любых IT-ролей.

## Подробная инструкция запуска и установки

- **Установка зависимостей**
    ```bash
    pip install -r requirements.txt
    ```

- **Быстрая проверка окружения**
    ```bash
    python test_llm.py
    ```
    Скрипт делает:
    - простой текстовый запрос к модели;
    - запрос со структурированным JSON-ответом.  

- **Настройка окружения**
    ```bash
    copy .env.example .env
    ```

- **Запуск анализа ролей**
    ```bash
    python main.py "Backend Python Developer"
    ```
    ```bash
    python main.py "ML Engineer"
    ```
    ```bash
    python main.py "iOS Developer (Swift)"
    ```
- **Проверка работы агентов по отдельности**  
    **Агент 1** — Аналитик рынка
    ```bash
    python -m agents.agent_1_analyst
    ```
    **Агент 2** — Оценщик зарплат  
    ```bash
    python -m agents.agent_2_salary
    ```
    **Агент 3** — Карьерный советник
    ```bash
    python -m agents.agent_3_advisor
    ```
    **Агент 4** — Критик и верификатор
    ```bash
    python -m agents.agent_4_critic
    ```

---

<div align="center">

### raft-career-agent

Автор: **Полина Червина**   
Python • Pydantic • Typer • LM Studio  
Учебный мультиагентный проект для генерации карьерных IT-отчётов

</div>