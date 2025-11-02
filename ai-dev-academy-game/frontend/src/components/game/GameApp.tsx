/**
 * GameApp - Main AI Dev Academy Game application
 */
import { useGameStore } from '../../stores/gameStore';
import { Dashboard } from './Dashboard';
import { ModuleViewer } from './ModuleViewer';
import { ClassViewer } from './ClassViewer';
import { Notifications } from './Notifications';
import './GameApp.css';

export const GameApp = () => {
  const { currentView, selectedModuleNumber, selectedClassNumber } = useGameStore();

  return (
    <div className="game-app">
      <Notifications />

      {/* Navigation Header */}
      <header className="game-header">
        <div className="game-logo">
          <span className="logo-icon">🤖</span>
          <span className="logo-text">AI Dev Academy</span>
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
        <p>&copy; 2025 AI Dev Academy. Learn, code, grow.</p>
      </footer>
    </div>
  );
};

// Placeholder components for future development
const AchievementsPlaceholder = () => {
  const { setCurrentView, unlockedAchievements } = useGameStore();

  return (
    <div className="placeholder">
      <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
        ← Back to Dashboard
      </button>
      <h2>All Achievements</h2>
      <p>You have unlocked {(unlockedAchievements || []).length} achievements!</p>
      <p>Full achievements gallery coming soon...</p>
    </div>
  );
};

const ProfilePlaceholder = () => {
  const { setCurrentView, player } = useGameStore();

  return (
    <div className="placeholder">
      <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
        ← Back to Dashboard
      </button>
      <h2>Profile</h2>
      {player && (
        <div>
          <p>Username: {player.username}</p>
          <p>Level: {player.level}</p>
          <p>XP: {player.xp}</p>
        </div>
      )}
      <p>Full profile editor coming soon...</p>
    </div>
  );
};
