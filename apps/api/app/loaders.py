from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader

from .models import Project, Task


def create_project_loader(session: AsyncSession) -> DataLoader[str, Project | None]:
    async def load_projects(keys: list[str]) -> list[Project | None]:
        rows = await session.scalars(select(Project).where(Project.id.in_(keys)))
        indexed = {project.id: project for project in rows}
        return [indexed.get(key) for key in keys]

    return DataLoader(load_fn=load_projects)


def create_projects_by_workspace_loader(session: AsyncSession) -> DataLoader[str, list[Project]]:
    async def load_projects(keys: list[str]) -> list[list[Project]]:
        rows = await session.scalars(select(Project).where(Project.workspace_id.in_(keys)))
        grouped: dict[str, list[Project]] = defaultdict(list)
        for project in rows:
            grouped[project.workspace_id].append(project)
        return [grouped[key] for key in keys]

    return DataLoader(load_fn=load_projects)


def create_tasks_by_project_loader(session: AsyncSession) -> DataLoader[str, list[Task]]:
    async def load_tasks(keys: list[str]) -> list[list[Task]]:
        rows = await session.scalars(select(Task).where(Task.project_id.in_(keys)))
        grouped: dict[str, list[Task]] = defaultdict(list)
        for task in rows:
            grouped[task.project_id].append(task)
        return [grouped[key] for key in keys]

    return DataLoader(load_fn=load_tasks)
