// src/App.tsx
import { TareasLista } from './components/TareasLista';
import './App.css';

/**
 * Componente raíz de la aplicación.
 *
 * Responsabilidades:
 * - Layout general de la aplicación
 * - Contiene el componente TareasLista
 */
function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>Tareas App</h1>
        <p>React + TypeScript + FastAPI</p>
      </header>
      <main className="app-main">
        <TareasLista />
      </main>
      <footer className="app-footer">
        <p>Módulo 5 - Clase 1 | Master en IA</p>
      </footer>
    </div>
  );
}

export default App;
