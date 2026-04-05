import typer
from rich.console import Console
from rich.panel import Panel
from datetime import datetime
from pathlib import Path

from core.schemas import Report, PortfolioProject
from agents.agent_1_analyst import agent_1_analyst
from agents.agent_2_salary import agent_2_salary
from agents.agent_3_advisor import agent_3_advisor
from agents.agent_4_critic import agent_4_critic
from agents.fix_portfolio import fix_portfolio

app = typer.Typer()
console = Console()


def save_report(report: Report, role: str):
    safe_name = "".join(c if c.isalnum() else "_" for c in role)
    examples_dir = Path("examples")
    examples_dir.mkdir(exist_ok=True)
    
    json_path = examples_dir / f"{safe_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(report.model_dump_json(indent=2))
    
    md_path = examples_dir / f"{safe_name}.md"
    md_content = f"""# Карьерный отчёт: {role}

**Сгенерировано:** {report.generated_at}  
**Quality Score:** {report.quality_score}/100

## 1. Карта навыков
{report.skill_map.model_dump_json(indent=2)}

## 2. Зарплаты и рынок
{{
  "salary_table": {report.salary_table.model_dump_json(indent=2)},
  "market_trend": {report.market_trend.model_dump_json(indent=2)},
  "top_employers": {report.top_employers}
}}

## 3. План развития
{report.learning_path.model_dump_json(indent=2)}

## 4. Gap-анализ и портфолио
{{
  "gap_analysis": {report.gap_analysis.model_dump_json(indent=2)},
  "portfolio_project": {report.portfolio_project.model_dump_json(indent=2)}
}}

## 5. Верификация
- **Quality Score**: {report.quality_score}
- **Warnings**: {report.warnings or "Нет"}
- **Consistent**: {report.is_consistent}
"""

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    return json_path, md_path


@app.command()
def main(role: str = typer.Argument(..., help="Название специальности")):
    console.print(Panel(f"[bold cyan]Запуск анализа для роли:[/bold cyan] [yellow]{role}[/yellow]", expand=False))
    
    start_time = datetime.now()
    
    skill_map = agent_1_analyst(role)
    agent2 = agent_2_salary(skill_map)
    agent3 = agent_3_advisor(skill_map, agent2)
    
    # Простой фикс только portfolio_project
    try:
        fixed = fix_portfolio(skill_map, agent3.portfolio_project.model_dump())
        agent3.portfolio_project = PortfolioProject(
            title=fixed.title,
            description=fixed.description,
            skills_demonstrated=fixed.skills_demonstrated
        )
        print("Portfolio project успешно исправлен")
    except Exception as e:
        print(f"Фикс portfolio не сработал: {e}")

    agent4 = agent_4_critic(skill_map, agent2, agent3)
    
    full_report = Report(
        role=role,
        skill_map=skill_map,
        salary_table=agent2.salary_table,
        market_trend=agent2.market_trend,
        top_employers=agent2.top_employers,
        learning_path=agent3.learning_path,
        gap_analysis=agent3.gap_analysis,
        portfolio_project=agent3.portfolio_project,
        quality_score=agent4.quality_score,
        warnings=agent4.warnings,
        is_consistent=agent4.is_consistent,
    )
    
    json_path, md_path = save_report(full_report, role)
    
    elapsed = (datetime.now() - start_time).seconds
    
    console.print(Panel(
        f"[bold green]Анализ завершён за {elapsed} сек![/bold green]\n"
        f"JSON: [cyan]{json_path}[/cyan]\n"
        f"MD:  [cyan]{md_path}[/cyan]\n\n"
        f"Quality Score: [bold]{full_report.quality_score}/100[/bold] | "
        f"Consistent: [bold]{full_report.is_consistent}[/bold]",
        title="Результат",
        expand=False
    ))


if __name__ == "__main__":
    app()