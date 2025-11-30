/**
 * App - Main application with routing for Game and Bug Hunt
 * NFLOW-2: Multi-course routing with courseId parameter
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { GameApp } from './components/game/GameApp';
import { BugHuntApp } from './components/BugHuntApp';
import { CourseCatalog } from './components/catalog/CourseCatalog';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<CourseCatalog />} />
        <Route path="/catalog" element={<CourseCatalog />} />
        <Route path="/game/:courseId" element={<GameApp />} />
        {/* Backward compatibility: /game redirects to /game/master-ia */}
        <Route path="/game" element={<Navigate to="/game/master-ia" replace />} />
        <Route path="/bug-hunt" element={<BugHuntApp />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
