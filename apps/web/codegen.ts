import type { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: '../../schema.graphql',
  documents: ['src/graphql/operations.ts'],
  generates: {
    'src/graphql/generated.ts': {
      plugins: ['typescript', 'typescript-operations', 'typed-document-node'],
      config: {
        enumsAsTypes: true,
        skipTypename: false,
      },
    },
  },
  ignoreNoDocuments: false,
}

export default config
