# GraphBoard

GraphBoard 是一个面向 GraphQL 学习的全栈项目。它以“工作区 → 项目 → 任务”的真实关系为主线，把 Schema、Resolver、Mutation、DataLoader、Apollo Client、类型生成、测试与部署放进同一个可运行仓库中。

## 当前版本

首个里程碑已经包含：

- FastAPI + Strawberry GraphQL API
- SQLAlchemy 2 异步访问与 PostgreSQL 16
- Workspace、Project、Task 数据模型
- Query、Mutation、Enum 与嵌套字段
- 按请求创建的 DataLoader，演示批量加载与 N+1 控制
- Vue 3 + TypeScript + Apollo Client 前端
- GraphQL Code Generator 配置与生成类型
- Alembic 初始迁移
- Pytest Schema 集成测试
- Docker Compose 本地环境
- GitHub Actions 前后端持续集成

认证、角色权限、Cursor Pagination、Subscription、Redis 与查询复杂度限制会在后续里程碑逐步加入。

## 架构

```text
Vue 3 + Apollo Client
          │
          │ GraphQL over HTTP
          ▼
FastAPI + Strawberry GraphQL
          │
          ├── Resolver
          ├── Request-scoped DataLoader
          └── SQLAlchemy AsyncSession
          │
          ▼
PostgreSQL 16
```

## 一键运行

需要 Docker 与 Docker Compose：

```bash
git clone https://github.com/weepwood/GraphBoard.git
cd GraphBoard
docker compose up --build
```

启动后访问：

- Web：`http://localhost:8080`
- GraphiQL：`http://localhost:8000/graphql`
- API 健康检查：`http://localhost:8000/health`
- PostgreSQL：`localhost:5432`

默认数据库配置仅用于本地学习：

```text
Database: graphboard
Username: graphboard
Password: graphboard
```

## 本地开发

### 后端

```bash
cd apps/api
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

运行测试与检查：

```bash
pytest
ruff check app tests
mypy app
```

数据库迁移：

```bash
alembic upgrade head
```

### 前端

```bash
cd apps/web
npm install
npm run codegen
npm run dev
```

开发服务器会把 `/graphql` 和 `/health` 代理到 `http://localhost:8000`。

## 示例 GraphQL 操作

创建工作区：

```graphql
mutation {
  createWorkspace(
    input: {
      name: "GraphQL 学习空间"
      description: "记录 Schema、Resolver 与客户端缓存实验"
    }
  ) {
    id
    name
  }
}
```

创建项目：

```graphql
mutation CreateProject($workspaceId: ID!) {
  createProject(
    input: {
      workspaceId: $workspaceId
      name: "GraphBoard"
      description: "通过真实项目学习 GraphQL"
    }
  ) {
    id
    name
  }
}
```

嵌套查询：

```graphql
query Dashboard {
  workspaces {
    id
    name
    projects {
      id
      name
      tasks {
        id
        title
        status
        priority
        project {
          id
          name
        }
      }
    }
  }
}
```

这条查询会触发多个关联字段。后端通过 request-scoped DataLoader 批量加载项目与任务，避免每个父对象单独执行一次 SQL。

## 目录结构

```text
GraphBoard/
├── apps/
│   ├── api/                 # FastAPI + Strawberry + SQLAlchemy
│   └── web/                 # Vue 3 + Apollo Client
├── docs/                    # 学习路线和设计说明
├── .github/workflows/       # CI
├── docker-compose.yml
├── schema.graphql           # 前端代码生成使用的 Schema 快照
└── Makefile
```

## 学习路线

1. 阅读 `schema.graphql`，理解输出类型、输入类型、Enum 与 Nullability。
2. 在 GraphiQL 中手动执行 Query 与 Mutation。
3. 阅读 `apps/api/app/schema.py`，追踪字段如何进入 Resolver。
4. 阅读 `apps/api/app/loaders.py`，比较直接逐条查询与 DataLoader 批量加载。
5. 阅读前端 `operations.ts` 与 `generated.ts`，观察查询文档如何生成 TypeScript 类型。
6. 修改 Schema 后运行 `npm run codegen`，体会 Schema 驱动的前后端契约。
7. 按 `docs/roadmap.md` 继续实现认证、分页、订阅与安全控制。

## 设计原则

- GraphQL Schema 面向客户端业务能力，不直接复制数据库表。
- Resolver 保持轻量，复杂业务逐步迁移到 Service 层。
- DataLoader 生命周期限制在单次请求内，避免跨用户缓存污染。
- 数据库实体 ID 与 `__typename` 共同支持 Apollo Client 规范化缓存。
- 初始版本保持可读，不提前引入 Federation、微服务或 Kubernetes。

## License

MIT
