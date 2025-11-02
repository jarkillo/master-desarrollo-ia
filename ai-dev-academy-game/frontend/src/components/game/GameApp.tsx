/**
 * GameApp - Main AI Dev Academy Game application
 */
import { useTranslation } from 'react-i18next';
import { useGameStore } from '../../stores/gameStore';
import { Dashboard } from './Dashboard';
import { ModuleViewer } from './ModuleViewer';
import { ClassViewer } from './ClassViewer';
import { Notifications } from './Notifications';
import './GameApp.css';

export const GameApp = () => {
  const { t } = useTranslation();
  const { currentView, selectedModuleNumber, selectedClassNumber } = useGameStore();

  return (
    <div className="game-app">
      <Notifications />

      {/* Navigation Header */}
      <header className="game-header">
        <div className="game-logo">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">{t('game.app.logoText')}</span>
        </div>
        <nav className="game-nav">
          {/* Navigation can be expanded later */}
        </nav>
      </header>

      {/* Main Content */}
      <main className="game-main">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'module' && <ModuleViewer />}
        {currentView === 'class' && selectedModuleNumber !== null && selectedClassNumber !== null && (
          <ClassViewer />
        )}
        {currentView === 'achievements' && <AchievementsPlaceholder />}
        {currentView === 'profile' && <ProfilePlaceholder />}
      </main>

      {/* Footer */}
      <footer className="game-footer">
        <p>&copy; 2025 {t('game.app.logoText')}. {t('game.app.footer')}</p>
      </footer>
    </div>
  );
};

// Placeholder components for future development
const AchievementsPlaceholder = () => {
  const { t } = useTranslation();
  const { setCurrentView, unlockedAchievements } = useGameStore();

  return (
    <div className="placeholder">
      <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
        ← {t('game.modules.backToDashboard')}
      </button>
      <h2>{t('game.app.allAchievements')}</h2>
      <p>{t('game.app.achievementsUnlocked', { count: (unlockedAchievements || []).length })}</p>
      <p>{t('game.app.achievementsComingSoon')}</p>
    </div>
  );
};

const ProfilePlaceholder = () => {
  const { t } = useTranslation();
  const { setCurrentView, player } = useGameStore();

  return (
    <div className="placeholder">
      <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
        ← {t('game.modules.backToDashboard')}
      </button>
      <h2>{t('game.app.profile')}</h2>
      {player && (
        <div>
          <p>{t('game.app.username')}: {player.username}</p>
          <p>{t('game.dashboard.level', { level: player.level })}</p>
          <p>XP: {player.xp}</p>
        </div>
      )}
      <p>{t('game.app.profileComingSoon')}</p>
    </div>
  );
};
