"""SQLModel database models for MCP Control Center."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import Column, Field, JSON, SQLModel


class FeatureStatus(str, Enum):
    """Feature status values."""

    DRAFT = "DRAFT"
    PLANNED = "PLANNED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class SpecificationKind(str, Enum):
    """Specification type values."""

    API = "API"
    UI = "UI"
    DATA = "DATA"
    SECURITY = "SECURITY"


class RefactorScope(str, Enum):
    """Refactor scope values."""

    FILE = "FILE"
    PACKAGE = "PACKAGE"
    SERVICE = "SERVICE"


class RiskLevel(str, Enum):
    """Risk level values."""

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class RuleCategory(str, Enum):
    """Rule category values."""

    STYLE = "STYLE"
    SECURITY = "SECURITY"
    SOC = "SOC"
    TESTING = "TESTING"
    PERF = "PERF"


class RuleGate(str, Enum):
    """Rule gate values."""

    WARN = "WARN"
    FAIL = "FAIL"


class UpdateSource(str, Enum):
    """Agent update source values."""

    AGENT = "AGENT"
    MCP = "MCP"


class Project(SQLModel, table=True):
    """Project entity."""

    __tablename__ = "projects"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    repo_url: Optional[str] = None
    language_matrix: dict = Field(default_factory=dict, sa_column=Column(JSON))
    tags: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Feature(SQLModel, table=True):
    """Feature entity."""

    __tablename__ = "features"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    title: str = Field(index=True)
    description_md: str = ""
    status: FeatureStatus = Field(default=FeatureStatus.DRAFT)
    priority: int = Field(default=3)
    labels: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    mcp_ids: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Specification(SQLModel, table=True):
    """Specification entity."""

    __tablename__ = "specifications"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    kind: SpecificationKind = Field(default=SpecificationKind.API)
    version: str = "1.0"
    doc_md: str = ""
    links: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class RefactorPlan(SQLModel, table=True):
    """Refactor plan entity."""

    __tablename__ = "refactor_plans"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    scope: RefactorScope = Field(default=RefactorScope.FILE)
    rationale_md: str = ""
    soc_findings: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    risk_level: RiskLevel = Field(default=RiskLevel.LOW)
    status: str = "Proposed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ADR(SQLModel, table=True):
    """Architecture Decision Record entity."""

    __tablename__ = "adrs"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    title: str
    context_md: str = ""
    decision_md: str = ""
    consequences_md: str = ""
    status: str = "Proposed"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Rule(SQLModel, table=True):
    """Rule entity for quality gates."""

    __tablename__ = "rules"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    name: str
    category: RuleCategory = Field(default=RuleCategory.STYLE)
    policy_md: str = ""
    gate: RuleGate = Field(default=RuleGate.WARN)
    enabled: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class AgentUpdate(SQLModel, table=True):
    """Agent update entity."""

    __tablename__ = "agent_updates"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    source: UpdateSource = Field(default=UpdateSource.AGENT)
    payload_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Proposal(SQLModel, table=True):
    """Proposal entity."""

    __tablename__ = "proposals"

    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="projects.id", index=True)
    summary_md: str = ""
    patch_manifest_json: dict = Field(default_factory=dict, sa_column=Column(JSON))
    linked_features: list[int] = Field(default_factory=list, sa_column=Column(JSON))
    status: str = "Draft"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
