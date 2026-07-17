# GraphBoard 学习路线

## Milestone 1：核心 GraphQL 闭环

- [x] Query 与 Mutation
- [x] Workspace / Project / Task 关联
- [x] Enum 与 Input Object
- [x] PostgreSQL 与异步 SQLAlchemy
- [x] DataLoader
- [x] Vue Apollo 前端
- [x] GraphQL Code Generator
- [x] Docker 与 CI

## Milestone 2：认证与权限

- [ ] User、WorkspaceMember 数据模型
- [ ] 注册、登录、Access Token、Refresh Token
- [ ] GraphQL Context 当前用户
- [ ] OWNER、ADMIN、MEMBER、VIEWER
- [ ] 工作区级与对象级权限
- [ ] 统一业务错误 Payload

## Milestone 3：Schema 设计进阶

- [ ] Cursor Pagination
- [ ] TaskFilterInput 与 TaskOrderInput
- [ ] Node Interface
- [ ] SearchResult Union
- [ ] Fragment 示例页面
- [ ] 字段废弃与 Schema 演进

## Milestone 4：性能与安全

- [ ] SQL 查询计数测试
- [ ] N+1 优化前后对比
- [ ] 查询深度限制
- [ ] Token 数量或复杂度限制
- [ ] 请求速率限制
- [ ] Persisted Operations / Safelist
- [ ] 慢 Resolver 观测

## Milestone 5：实时协作

- [ ] Task Updated Subscription
- [ ] Comment Added Subscription
- [ ] Redis Pub/Sub
- [ ] 多实例事件同步
- [ ] 前端断线重连
- [ ] Subscription 驱动 Apollo Cache 更新

## Milestone 6：生产化

- [ ] Service 与 Repository 分层
- [ ] Alembic 自动迁移检查
- [ ] Schema breaking change 检查
- [ ] Playwright E2E
- [ ] OpenTelemetry
- [ ] 生产环境 GraphiQL 与 introspection 策略
