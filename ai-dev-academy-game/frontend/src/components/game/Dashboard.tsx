/**
 * Dashboard - Main view showing player stats, progress, and next steps
 */
import { useEffect } from 'react';
import { useGameStore } from '../../stores/gameStore';
import './Dashboard.css';

export const Dashboard = () => {
  const {
    player,
    playerStats,
    fullProgress,
    unlockedAchievements,
    loadPlayer,
    loadFullProgress,
    loadPlayerAchievements,
    loadAllModules,
    selectModule,
    setCurrentView,
  } = useGameStore();

  useEffect(() => {
    const playerId = player?.id || parseInt(import.meta.env.VITE_DEFAULT_PLAYER_ID || '1', 10);

    // Load all data
    Promise.all([
      loadPlayer(playerId),
      loadFullProgress(playerId),
      loadPlayerAchievements(playerId),
      loadAllModules(),
    ]).catch(console.error);
  }, []);

  if (!player || !playerStats || !fullProgress) {
    return <div className="dashboard-loading">Loading...</div>;
  }

  const levelTitle = getLevelTitle(player.level);
  const xpProgress = getXPProgress(player.xp);
  const recentAchievements = unlockedAchievements.slice(-3).reverse();

  return (
    <div className="dashboard">
      {/* Header Section */}
      <div className="dashboard-header">
        <div className="player-info">
          <div className="player-avatar">{player.avatar}</div>
          <div className="player-details">
            <h1>{player.username}</h1>
            <div className="player-level">
              Level {player.level} • {levelTitle}
            </div>
          </div>
        </div>

        <div className="quick-actions">
          <button onClick={() => setCurrentView('profile')} className="btn-secondary">
            Profile
          </button>
          <button onClick={() => setCurrentView('achievements')} className="btn-secondary">
            Achievements ({unlockedAchievements.length})
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎓</div>
          <div className="stat-value">{playerStats.classes_completed}</div>
          <div className="stat-label">Classes Completed</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💪</div>
          <div className="stat-value">{playerStats.exercises_completed}</div>
          <div className="stat-label">Exercises Done</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🐛</div>
          <div className="stat-value">{playerStats.bug_hunt_wins}</div>
          <div className="stat-label">Bug Hunt Wins</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-value">{playerStats.current_streak}</div>
          <div className="stat-label">Day Streak</div>
        </div>
      </div>

      {/* XP Progress */}
      <div className="xp-section">
        <div className="xp-header">
          <span>Level {player.level}</span>
          <span>{player.xp} XP</span>
          <span>Level {player.level + 1}</span>
        </div>
        <div className="xp-bar">
          <div
            className="xp-fill"
            style={{ width: `${xpProgress.progressPercentage}%` }}
          />
        </div>
        <div className="xp-info">
          {xpProgress.xpNeeded} XP to next level
        </div>
      </div>

      {/* Overall Progress */}
      <div className="progress-overview">
        <h2>Your Progress</h2>
        <div className="overall-progress">
          <div className="progress-stats">
            <span>
              {fullProgress.classes_completed} / {fullProgress.total_classes} classes
            </span>
            <span>{Math.round(fullProgress.overall_progress_percentage)}%</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${fullProgress.overall_progress_percentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div className="modules-section">
        <h2>Modules</h2>
        <div className="modules-grid">
          {fullProgress.modules.map((module) => (
            <div
              key={module.module_number}
              className={`module-card ${
                module.classes_completed === 0 ? 'locked' : ''
              } ${
                module.classes_completed === module.total_classes ? 'completed' : ''
              }`}
              onClick={() => selectModule(module.module_number)}
            >
              <div className="module-header">
                <h3>Module {module.module_number}</h3>
                {module.classes_completed === module.total_classes && (
                  <span className="completion-badge">✓</span>
                )}
              </div>
              <div className="module-title">{module.module_title}</div>
              <div className="module-progress">
                <div className="module-progress-bar">
                  <div
                    className="module-progress-fill"
                    style={{ width: `${module.module_progress_percentage}%` }}
                  />
                </div>
                <div className="module-progress-text">
                  {module.classes_completed} / {module.total_classes} classes
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Achievements */}
      {recentAchievements.length > 0 && (
        <div className="achievements-section">
          <h2>Recent Achievements</h2>
          <div className="achievements-grid">
            {recentAchievements.map((achievement) => (
              <div
                key={achievement.id}
                className={`achievement-card rarity-${achievement.rarity}`}
              >
                <div className="achievement-icon">{achievement.icon}</div>
                <div className="achievement-info">
                  <div className="achievement-title">{achievement.title}</div>
                  <div className="achievement-description">
                    {achievement.description}
                  </div>
                  <div className="achievement-xp">+{achievement.xp_reward} XP</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Helper functions
function getLevelTitle(level: number): string {
  if (level <= 5) return 'Junior Developer';
  if (level <= 10) return 'Mid Developer';
  if (level <= 15) return 'Senior Developer';
  if (level <= 20) return 'Tech Lead';
  if (level <= 25) return 'Architect';
  if (level <= 30) return 'CTO';
  return 'Legend';
}

function getXPProgress(xp: number): {
  currentLevel: number;
  nextLevel: number;
  xpForCurrentLevel: number;
  xpForNextLevel: number;
  xpProgress: number;
  xpNeeded: number;
  progressPercentage: number;
} {
  // Formula: level = int((xp / 100) ** 0.5) + 1
  const currentLevel = Math.floor((xp / 100) ** 0.5) + 1;
  const nextLevel = currentLevel + 1;

  // Reverse formula: xp = (level - 1)^2 * 100
  const xpForCurrentLevel = (currentLevel - 1) ** 2 * 100;
  const xpForNextLevel = (nextLevel - 1) ** 2 * 100;

  const xpProgress = xp - xpForCurrentLevel;
  const xpNeeded = xpForNextLevel - xp;
  const progressPercentage = (xpProgress / (xpForNextLevel - xpForCurrentLevel)) * 100;

  return {
    currentLevel,
    nextLevel,
    xpForCurrentLevel,
    xpForNextLevel,
    xpProgress,
    xpNeeded,
    progressPercentage,
  };
}
