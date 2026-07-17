import gql from 'graphql-tag'

export const DASHBOARD_QUERY = gql`
  query Dashboard {
    workspaces {
      id
      name
      description
      projects {
        id
        name
        description
        tasks {
          id
          title
          description
          status
          priority
        }
      }
    }
  }
`

export const CREATE_WORKSPACE_MUTATION = gql`
  mutation CreateWorkspace($input: CreateWorkspaceInput!) {
    createWorkspace(input: $input) {
      id
      name
      description
    }
  }
`

export const CREATE_PROJECT_MUTATION = gql`
  mutation CreateProject($input: CreateProjectInput!) {
    createProject(input: $input) {
      id
      name
      description
    }
  }
`

export const CREATE_TASK_MUTATION = gql`
  mutation CreateTask($input: CreateTaskInput!) {
    createTask(input: $input) {
      id
      title
      status
      priority
    }
  }
`

export const UPDATE_TASK_STATUS_MUTATION = gql`
  mutation UpdateTaskStatus($input: UpdateTaskStatusInput!) {
    updateTaskStatus(input: $input) {
      id
      status
    }
  }
`
