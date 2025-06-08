import Home from './pages/Home'
import NavBar from './components/NavBar'
import "./css/App.css"
import { LogProvider } from './contexts/LogContext'

function App() {
  return (
    <LogProvider>
      <div className="app">
        <NavBar/>
        <Home/>
      </div>
    </LogProvider>
  )
}

export default App
