import { print } from 'graphql'
import { describe, expect, it } from 'vitest'

import { DASHBOARD_QUERY } from './operations'

describe('GraphQL operations', () => {
  it('keeps the dashboard query connected to all three learning entities', () => {
    const document = print(DASHBOARD_QUERY)
    expect(document).toContain('workspaces')
    expect(document).toContain('projects')
    expect(document).toContain('tasks')
  })
})
