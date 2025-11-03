/**
 * App - Main application with routing for Game and Bug Hunt
 */
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { GameApp } from './components/game/GameApp';
import { BugHuntApp } from './components/BugHuntApp';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/game" element={<GameApp />} />
        <Route path="/bug-hunt" element={<BugHuntApp />} />
      </Routes>
    </BrowserRouter>
  );
}

function Home() {
  return (
    <div className="home">
      <div className="home-container">
        <h1 className="home-title">
          <span className="home-icon">🤖</span>
          AI Dev Academy
        </h1>
        <p className="home-subtitle">Choose your adventure</p>

        <div className="game-selection">
          <Link to="/game" className="game-card main-game">
            <div className="game-icon">🎓</div>
            <h2>Main Game</h2>
            <p>Complete modules, unlock achievements, and level up your skills</p>
            <button className="game-btn">Play Now</button>
          </Link>

          <Link to="/bug-hunt" className="game-card bug-hunt">
            <div className="game-icon">🐛</div>
            <h2>Bug Hunt</h2>
            <p>Find bugs in code snippets and compete on the leaderboard</p>
            <button className="game-btn">Hunt Bugs</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default App;
