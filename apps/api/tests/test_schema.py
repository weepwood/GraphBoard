import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.context import GraphQLContext
from app.database import Base
from app.schema import schema


@pytest.mark.asyncio
async def test_health_query() -> None:
    result = await schema.execute("query { health }")
    assert result.errors is None
    assert result.data == {"health": "ok"}


@pytest.mark.asyncio
async def test_workspace_project_task_flow() -> None:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as session:
        context = GraphQLContext(session)
        workspace_result = await schema.execute(
            """
            mutation {
              createWorkspace(input: {name: "Learning"}) { id name }
            }
            """,
            context_value=context,
        )
        assert workspace_result.errors is None
        workspace_id = workspace_result.data["createWorkspace"]["id"]

        project_result = await schema.execute(
            """
            mutation CreateProject($workspaceId: ID!) {
              createProject(input: {workspaceId: $workspaceId, name: "GraphQL"}) { id }
            }
            """,
            variable_values={"workspaceId": workspace_id},
            context_value=context,
        )
        assert project_result.errors is None
        project_id = project_result.data["createProject"]["id"]

        task_result = await schema.execute(
            """
            mutation CreateTask($projectId: ID!) {
              createTask(input: {projectId: $projectId, title: "Learn DataLoader"}) {
                title
                status
                project { name }
              }
            }
            """,
            variable_values={"projectId": project_id},
            context_value=context,
        )
        assert task_result.errors is None
        assert task_result.data["createTask"]["project"]["name"] == "GraphQL"

    await engine.dispose()
