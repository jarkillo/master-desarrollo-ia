import React from 'react'
import ReactDOM from 'react-dom/client'
import ErrorBoundary from './components/common/ErrorBoundary.tsx'
import App from './App.tsx'
import './index.css'
import './i18n/config'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ErrorBoundary>
      <App />
    </ErrorBoundary>
  </React.StrictMode>,
)
