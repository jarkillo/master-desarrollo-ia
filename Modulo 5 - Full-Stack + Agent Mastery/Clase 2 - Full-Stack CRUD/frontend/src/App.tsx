/**
 * Componente raíz de la aplicación.
 */
import { TareasLista } from './components/TareasLista';
import './App.css';

function App() {
  return (
    <div className="app">
      <TareasLista />
    </div>
  );
}

export default App;
