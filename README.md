# raft-career-agent
Тестовое задание мультиагентной системы для Raft
# Мультиагентная система анализа карьерного рынка IT

Тестовое задание на стажировку в **Raft**

## Описание

Система принимает название IT-специальности и генерирует структурированный карьерный отчёт с помощью 4 независимых агентов.

## Архитектура

- **Агент 1** — Аналитик рынка (skill_map)
- **Агент 2** — Оценщик зарплат (salary_table, market_trend, top_employers)
- **Агент 3** — Карьерный советник (learning_path, gap_analysis, portfolio_project)
- **Агент 4** — Критик и верификатор (quality_score, warnings, is_consistent)

Агенты вызываются строго последовательно с явной передачей JSON-контекста.

## Как запустить

- **Установка зависимостей**
```bash
pip install -r requirements.txt
```

- **Настройка окружения**
```bash
copy .env.example .env
```

**LM Studio должнг быть запущен на http://127.0.0.1:1234**

- **Запуск анализа**
```bash
python main.py "Backend Python Developer"
```
```bash
python main.py "ML Engineer"
```
```bash
python main.py "iOS Developer (Swift)"
```

## Проверка работы агентов по отдельности

**Каждого агента можно протестировать самостоятельно:**

- **Агент 1 — Аналитик рынка**
```bash
python -m agents.agent_1_analyst
```

- **Агент 2 — Оценщик зарплат**
```bash
python -m agents.agent_2_salary
```

- **Агент 3 — Карьерный советник**
```bash
python -m agents.agent_3_advisor
```

- **Агент 4 — Критик и верификатор**
```bash
python -m agents.agent_4_critic
```

## Архитектура проекта

## Логика работы программы