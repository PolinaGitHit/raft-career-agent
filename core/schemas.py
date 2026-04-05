from pydantic import BaseModel, Field
from typing import Literal, List, Dict, Any
from datetime import datetime


class SkillItem(BaseModel):
    name: str
    demand: Literal["critical", "important", "nice-to-have"]
    trend: Literal["growing", "stable", "declining"]


class SkillMap(BaseModel):
    languages: List[SkillItem]
    frameworks: List[SkillItem]
    infrastructure: List[SkillItem]
    soft_skills: List[SkillItem]


class SalaryCell(BaseModel):
    min: int
    median: int
    max: int


class SalaryTable(BaseModel):
    Junior: Dict[Literal["Moscow", "Regions_RF", "Remote_USD"], SalaryCell]
    Middle: Dict[Literal["Moscow", "Regions_RF", "Remote_USD"], SalaryCell]
    Senior: Dict[Literal["Moscow", "Regions_RF", "Remote_USD"], SalaryCell]
    Lead: Dict[Literal["Moscow", "Regions_RF", "Remote_USD"], SalaryCell]


class MarketTrend(BaseModel):
    trend: Literal["growing", "stable", "declining"]
    reason: str = Field(..., min_length=10)


class LearningPhase(BaseModel):
    phase: Literal["Foundation", "Practice", "Portfolio"]
    topics: List[str]
    resources: List[Dict[str, str]]  # {"name": "...", "type": "course|book|documentation|video"}
    milestone: str


class LearningPath(BaseModel):
    phases: List[LearningPhase]


class GapAnalysis(BaseModel):
    quick_wins: List[str]
    long_term: List[str]


class PortfolioProject(BaseModel):
    title: str
    description: str
    skills_demonstrated: List[str]


class Report(BaseModel):
    role: str
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    skill_map: SkillMap
    salary_table: SalaryTable
    market_trend: MarketTrend
    top_employers: List[str]
    learning_path: LearningPath
    gap_analysis: GapAnalysis
    portfolio_project: PortfolioProject
    quality_score: int = Field(..., ge=0, le=100)
    warnings: List[str]
    is_consistent: bool

# ====================== ДОПОЛНИТЕЛЬНЫЕ СХЕМЫ ДЛЯ АГЕНТОВ ======================

class Agent2Output(BaseModel):
    """Выход Агента 2 — всё, что он добавляет в отчёт"""
    salary_table: SalaryTable
    market_trend: MarketTrend
    top_employers: List[str]

class Agent3Output(BaseModel):
    """Выход Агента 3 — всё, что он добавляет в отчёт"""
    learning_path: LearningPath
    gap_analysis: GapAnalysis
    portfolio_project: PortfolioProject

class PortfolioProjectFixed(BaseModel):
    """Вспомогательная модель для исправления portfolio_project"""
    title: str
    description: str
    skills_demonstrated: List[str]

class Agent4Output(BaseModel):
    """Выход Агента 4 — финальные проверки"""
    quality_score: int = Field(..., ge=0, le=100)
    warnings: List[str]
    is_consistent: bool