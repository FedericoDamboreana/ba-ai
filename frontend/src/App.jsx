import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-background">
          <h1 className="text-4xl font-bold text-primary p-8">ReqScribe</h1>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  )
}

export default App
