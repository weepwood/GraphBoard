from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any

import strawberry
from sqlalchemy import select
from strawberry.dataloader import DataLoader
from strawberry.types import Info

from .context import GraphQLContext
from .models import (
    Project,
    Task,
    Workspace,
)
from .models import (
    TaskPriority as ModelTaskPriority,
)
from .models import (
    TaskStatus as ModelTaskStatus,
)


@strawberry.enum(name="TaskStatus")
class TaskStatusType(StrEnum):
    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


@strawberry.enum(name="TaskPriority")
class TaskPriorityType(StrEnum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


GraphQLInfo = Info[GraphQLContext, None]


def clear_loader(loader: DataLoader[Any, Any], key: Any) -> None:
    try:
        loader.clear(key)
    except KeyError:
        # Strawberry currently raises when clearing an uncached key.
        pass


@strawberry.type
class TaskType:
    id: strawberry.ID
    title: str
    description: str | None
    status: TaskStatusType
    priority: TaskPriorityType
    created_at: datetime
    updated_at: datetime
    project_id: strawberry.Private[str]

    @strawberry.field
    async def project(self, info: GraphQLInfo) -> ProjectType:
        project = await info.context.project_loader.load(self.project_id)
        if project is None:
            raise ValueError("Task project no longer exists")
        return project_to_type(project)


@strawberry.type
class ProjectType:
    id: strawberry.ID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    async def tasks(self, info: GraphQLInfo) -> list[TaskType]:
        tasks = await info.context.tasks_by_project_loader.load(str(self.id))
        return [task_to_type(task) for task in tasks]


@strawberry.type
class WorkspaceType:
    id: strawberry.ID
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    @strawberry.field
    async def projects(self, info: GraphQLInfo) -> list[ProjectType]:
        projects = await info.context.projects_by_workspace_loader.load(str(self.id))
        return [project_to_type(project) for project in projects]


@strawberry.input
class CreateWorkspaceInput:
    name: str
    description: str | None = None


@strawberry.input
class CreateProjectInput:
    workspace_id: strawberry.ID
    name: str
    description: str | None = None


@strawberry.input
class CreateTaskInput:
    project_id: strawberry.ID
    title: str
    description: str | None = None
    priority: TaskPriorityType = TaskPriorityType.MEDIUM


@strawberry.input
class UpdateTaskStatusInput:
    task_id: strawberry.ID
    status: TaskStatusType


def workspace_to_type(workspace: Workspace) -> WorkspaceType:
    return WorkspaceType(
        id=strawberry.ID(workspace.id),
        name=workspace.name,
        description=workspace.description,
        created_at=workspace.created_at,
        updated_at=workspace.updated_at,
    )


def project_to_type(project: Project) -> ProjectType:
    return ProjectType(
        id=strawberry.ID(project.id),
        name=project.name,
        description=project.description,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def task_to_type(task: Task) -> TaskType:
    return TaskType(
        id=strawberry.ID(task.id),
        title=task.title,
        description=task.description,
        status=TaskStatusType(task.status.value),
        priority=TaskPriorityType(task.priority.value),
        created_at=task.created_at,
        updated_at=task.updated_at,
        project_id=task.project_id,
    )


@strawberry.type
class Query:
    @strawberry.field
    def health(self) -> str:
        return "ok"

    @strawberry.field
    async def workspaces(self, info: GraphQLInfo) -> list[WorkspaceType]:
        rows = await info.context.session.scalars(select(Workspace).order_by(Workspace.created_at))
        return [workspace_to_type(row) for row in rows]

    @strawberry.field
    async def project(self, info: GraphQLInfo, id: strawberry.ID) -> ProjectType | None:
        project = await info.context.session.get(Project, str(id))
        return project_to_type(project) if project else None

    @strawberry.field
    async def tasks(
        self, info: GraphQLInfo, project_id: strawberry.ID | None = None
    ) -> list[TaskType]:
        statement = select(Task).order_by(Task.created_at)
        if project_id is not None:
            statement = statement.where(Task.project_id == str(project_id))
        rows = await info.context.session.scalars(statement)
        return [task_to_type(row) for row in rows]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_workspace(
        self, info: GraphQLInfo, input: CreateWorkspaceInput
    ) -> WorkspaceType:
        workspace = Workspace(name=input.name.strip(), description=input.description)
        info.context.session.add(workspace)
        await info.context.session.commit()
        await info.context.session.refresh(workspace)
        return workspace_to_type(workspace)

    @strawberry.mutation
    async def create_project(self, info: GraphQLInfo, input: CreateProjectInput) -> ProjectType:
        workspace = await info.context.session.get(Workspace, str(input.workspace_id))
        if workspace is None:
            raise ValueError("Workspace not found")
        project = Project(
            workspace_id=workspace.id,
            name=input.name.strip(),
            description=input.description,
        )
        info.context.session.add(project)
        await info.context.session.commit()
        await info.context.session.refresh(project)
        clear_loader(info.context.projects_by_workspace_loader, workspace.id)
        return project_to_type(project)

    @strawberry.mutation
    async def create_task(self, info: GraphQLInfo, input: CreateTaskInput) -> TaskType:
        project = await info.context.session.get(Project, str(input.project_id))
        if project is None:
            raise ValueError("Project not found")
        task = Task(
            project_id=project.id,
            title=input.title.strip(),
            description=input.description,
            priority=ModelTaskPriority(input.priority.value),
        )
        info.context.session.add(task)
        await info.context.session.commit()
        await info.context.session.refresh(task)
        clear_loader(info.context.tasks_by_project_loader, project.id)
        return task_to_type(task)

    @strawberry.mutation
    async def update_task_status(self, info: GraphQLInfo, input: UpdateTaskStatusInput) -> TaskType:
        task = await info.context.session.get(Task, str(input.task_id))
        if task is None:
            raise ValueError("Task not found")
        task.status = ModelTaskStatus(input.status.value)
        await info.context.session.commit()
        await info.context.session.refresh(task)
        clear_loader(info.context.tasks_by_project_loader, task.project_id)
        return task_to_type(task)


schema = strawberry.Schema(query=Query, mutation=Mutation)
