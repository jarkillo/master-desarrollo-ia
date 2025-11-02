/**
 * App - Main application with routing for Game and Bug Hunt
 */
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { GameApp } from './components/game/GameApp';
import { BugHuntApp } from './components/BugHuntApp';
import './i18n/config'; // Initialize i18n
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
  const { t } = useTranslation();

  return (
    <div className="home">
      <div className="home-container">
        <h1 className="home-title">
          <span className="home-icon">🤖</span>
          {t('home.title')}
        </h1>
        <p className="home-subtitle">{t('home.subtitle')}</p>

        <div className="game-selection">
          <Link to="/game" className="game-card main-game">
            <div className="game-icon">🎓</div>
            <h2>{t('home.mainGame.title')}</h2>
            <p>{t('home.mainGame.description')}</p>
            <button className="game-btn">{t('home.mainGame.button')}</button>
          </Link>

          <Link to="/bug-hunt" className="game-card bug-hunt">
            <div className="game-icon">🐛</div>
            <h2>{t('home.bugHunt.title')}</h2>
            <p>{t('home.bugHunt.description')}</p>
            <button className="game-btn">{t('home.bugHunt.button')}</button>
          </Link>
        </div>
      </div>
    </div>
  );
}

export default App;
