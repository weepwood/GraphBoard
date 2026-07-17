# 架构说明

## 为什么选择这个业务模型

工作区、项目与任务构成稳定的多层关系，能够自然展示 GraphQL 的核心价值：客户端可以按照页面需要选择字段，同时通过单个查询获取嵌套数据。

## 后端请求路径

```text
GraphQL Document
  → Parse / Validate
  → Query or Mutation Resolver
  → AsyncSession / DataLoader
  → PostgreSQL
  → 根据查询选择集组装响应
```

`GraphQLContext` 在每个请求中持有独立的 `AsyncSession` 与 DataLoader。DataLoader 不做全局缓存，仅在当前 GraphQL 请求中合并相同实体或同类关系的读取。

## 当前分层

初始版本为了方便学习，把较短的写入逻辑保留在 Mutation Resolver 中。下一阶段会加入：

```text
Resolver → Service → Repository → SQLAlchemy
```

当业务规则增长后，Resolver 只负责 GraphQL 参数、上下文和输出类型转换。

## Schema 快照

根目录的 `schema.graphql` 是前端代码生成使用的契约快照。修改后端 Schema 时，应同步更新快照，并执行：

```bash
cd apps/web
npm run codegen
```

后续 CI 会增加自动导出 Schema 和 breaking change 检查。
