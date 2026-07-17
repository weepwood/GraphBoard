import { ApolloClient, HttpLink, InMemoryCache } from '@apollo/client/core'
import { DefaultApolloClient } from '@vue/apollo-composable'
import { createApp, h, provide } from 'vue'

import App from './App.vue'
import './styles.css'

const apolloClient = new ApolloClient({
  link: new HttpLink({ uri: import.meta.env.VITE_GRAPHQL_URL ?? '/graphql' }),
  cache: new InMemoryCache({
    typePolicies: {
      WorkspaceType: { keyFields: ['id'] },
      ProjectType: { keyFields: ['id'] },
      TaskType: { keyFields: ['id'] },
    },
  }),
})

createApp({
  setup() {
    provide(DefaultApolloClient, apolloClient)
  },
  render: () => h(App),
}).mount('#app')
