from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.dataloader import DataLoader
from strawberry.fastapi import BaseContext

from .database import get_session
from .loaders import (
    create_project_loader,
    create_projects_by_workspace_loader,
    create_tasks_by_project_loader,
)
from .models import Project, Task


class GraphQLContext(BaseContext):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.project_loader: DataLoader[str, Project | None] = create_project_loader(session)
        self.projects_by_workspace_loader: DataLoader[str, list[Project]] = (
            create_projects_by_workspace_loader(session)
        )
        self.tasks_by_project_loader: DataLoader[str, list[Task]] = create_tasks_by_project_loader(
            session
        )


async def get_context(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> GraphQLContext:
    return GraphQLContext(session)
