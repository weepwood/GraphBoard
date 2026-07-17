<script setup lang="ts">
import { useMutation, useQuery } from '@vue/apollo-composable'
import { computed, reactive, ref } from 'vue'

import type {
  CreateProjectMutation,
  CreateProjectMutationVariables,
  CreateTaskMutation,
  CreateTaskMutationVariables,
  CreateWorkspaceMutation,
  CreateWorkspaceMutationVariables,
  DashboardQuery,
  TaskPriority,
  TaskStatus,
  UpdateTaskStatusMutation,
  UpdateTaskStatusMutationVariables,
} from './graphql/generated'
import {
  CREATE_PROJECT_MUTATION,
  CREATE_TASK_MUTATION,
  CREATE_WORKSPACE_MUTATION,
  DASHBOARD_QUERY,
  UPDATE_TASK_STATUS_MUTATION,
} from './graphql/operations'

const { result, loading, error, refetch } = useQuery<DashboardQuery>(DASHBOARD_QUERY)
const workspaces = computed(() => result.value?.workspaces ?? [])
const projects = computed(() => workspaces.value.flatMap((workspace) => workspace.projects))

const workspaceForm = reactive({ name: '', description: '' })
const projectForm = reactive({ workspaceId: '', name: '', description: '' })
const taskForm = reactive<{ projectId: string; title: string; priority: TaskPriority }>({
  projectId: '',
  title: '',
  priority: 'MEDIUM',
})
const mutationError = ref('')

const { mutate: createWorkspace, loading: creatingWorkspace } = useMutation<
  CreateWorkspaceMutation,
  CreateWorkspaceMutationVariables
>(CREATE_WORKSPACE_MUTATION)
const { mutate: createProject, loading: creatingProject } = useMutation<
  CreateProjectMutation,
  CreateProjectMutationVariables
>(CREATE_PROJECT_MUTATION)
const { mutate: createTask, loading: creatingTask } = useMutation<
  CreateTaskMutation,
  CreateTaskMutationVariables
>(CREATE_TASK_MUTATION)
const { mutate: updateTaskStatus } = useMutation<
  UpdateTaskStatusMutation,
  UpdateTaskStatusMutationVariables
>(UPDATE_TASK_STATUS_MUTATION)

async function submitWorkspace() {
  mutationError.value = ''
  try {
    await createWorkspace({ input: { ...workspaceForm } })
    workspaceForm.name = ''
    workspaceForm.description = ''
    await refetch()
  } catch (cause) {
    mutationError.value = cause instanceof Error ? cause.message : '创建工作区失败'
  }
}

async function submitProject() {
  mutationError.value = ''
  try {
    await createProject({ input: { ...projectForm } })
    projectForm.name = ''
    projectForm.description = ''
    await refetch()
  } catch (cause) {
    mutationError.value = cause instanceof Error ? cause.message : '创建项目失败'
  }
}

async function submitTask() {
  mutationError.value = ''
  try {
    await createTask({ input: { ...taskForm } })
    taskForm.title = ''
    await refetch()
  } catch (cause) {
    mutationError.value = cause instanceof Error ? cause.message : '创建任务失败'
  }
}

async function changeStatus(taskId: string, status: TaskStatus) {
  await updateTaskStatus({ input: { taskId, status } })
  await refetch()
}

async function onStatusChange(taskId: string, event: Event) {
  const select = event.target as HTMLSelectElement
  await changeStatus(taskId, select.value as TaskStatus)
}
</script>

<template>
  <main class="shell">
    <header class="hero">
      <div>
        <p class="eyebrow">GRAPHQL LEARNING PLATFORM</p>
        <h1>GraphBoard</h1>
        <p class="subtitle">通过真实的工作区、项目和任务关系，学习 Schema、Resolver、Mutation 与 DataLoader。</p>
      </div>
      <a class="graphql-link" href="http://localhost:8000/graphql" target="_blank" rel="noreferrer">
        打开 GraphiQL
      </a>
    </header>

    <p v-if="error" class="notice error">GraphQL 请求失败：{{ error.message }}</p>
    <p v-if="mutationError" class="notice error">{{ mutationError }}</p>

    <section class="forms" aria-label="创建数据">
      <form class="panel" @submit.prevent="submitWorkspace">
        <span class="step">01</span>
        <h2>创建工作区</h2>
        <input v-model.trim="workspaceForm.name" required placeholder="工作区名称" />
        <textarea v-model.trim="workspaceForm.description" placeholder="工作区说明" />
        <button :disabled="creatingWorkspace">{{ creatingWorkspace ? '创建中…' : '创建工作区' }}</button>
      </form>

      <form class="panel" @submit.prevent="submitProject">
        <span class="step">02</span>
        <h2>创建项目</h2>
        <select v-model="projectForm.workspaceId" required>
          <option value="" disabled>选择工作区</option>
          <option v-for="workspace in workspaces" :key="workspace.id" :value="workspace.id">
            {{ workspace.name }}
          </option>
        </select>
        <input v-model.trim="projectForm.name" required placeholder="项目名称" />
        <textarea v-model.trim="projectForm.description" placeholder="项目说明" />
        <button :disabled="creatingProject || !workspaces.length">
          {{ creatingProject ? '创建中…' : '创建项目' }}
        </button>
      </form>

      <form class="panel" @submit.prevent="submitTask">
        <span class="step">03</span>
        <h2>创建任务</h2>
        <select v-model="taskForm.projectId" required>
          <option value="" disabled>选择项目</option>
          <option v-for="project in projects" :key="project.id" :value="project.id">
            {{ project.name }}
          </option>
        </select>
        <input v-model.trim="taskForm.title" required placeholder="任务标题" />
        <select v-model="taskForm.priority">
          <option value="LOW">低优先级</option>
          <option value="MEDIUM">中优先级</option>
          <option value="HIGH">高优先级</option>
        </select>
        <button :disabled="creatingTask || !projects.length">
          {{ creatingTask ? '创建中…' : '创建任务' }}
        </button>
      </form>
    </section>

    <section class="board-section">
      <div class="section-heading">
        <div>
          <p class="eyebrow">LIVE QUERY RESULT</p>
          <h2>任务看板</h2>
        </div>
        <button class="secondary" type="button" @click="refetch()">刷新查询</button>
      </div>

      <p v-if="loading" class="notice">正在执行 Dashboard GraphQL Query…</p>
      <p v-else-if="!workspaces.length" class="empty">先创建工作区，观察嵌套 Query 如何逐层返回数据。</p>

      <article v-for="workspace in workspaces" :key="workspace.id" class="workspace">
        <div class="workspace-title">
          <div>
            <span>WORKSPACE</span>
            <h3>{{ workspace.name }}</h3>
          </div>
          <code>{{ workspace.id }}</code>
        </div>

        <div class="project-grid">
          <section v-for="project in workspace.projects" :key="project.id" class="project-card">
            <header>
              <span>PROJECT</span>
              <h4>{{ project.name }}</h4>
              <p>{{ project.description || '暂无项目说明' }}</p>
            </header>

            <ul class="task-list">
              <li v-for="task in project.tasks" :key="task.id" class="task-item">
                <div>
                  <strong>{{ task.title }}</strong>
                  <small>{{ task.priority }}</small>
                </div>
                <select
                  :value="task.status"
                  :aria-label="`修改 ${task.title} 状态`"
                  @change="onStatusChange(task.id, $event)"
                >
                  <option value="TODO">待处理</option>
                  <option value="IN_PROGRESS">进行中</option>
                  <option value="DONE">已完成</option>
                </select>
              </li>
              <li v-if="!project.tasks.length" class="task-empty">这个项目还没有任务</li>
            </ul>
          </section>
        </div>
      </article>
    </section>
  </main>
</template>
