/**
 * Dashboard - Main view showing player stats, progress, and next steps
 */
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useGameStore } from '../../stores/gameStore';
import './Dashboard.css';

export const Dashboard = () => {
  const { t } = useTranslation();
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
    return <div className="dashboard-loading">{t('common.loading')}</div>;
  }

  const levelTitle = getLevelTitle(player.level, t);
  const xpProgress = getXPProgress(player.xp);
  const recentAchievements = (unlockedAchievements || []).slice(-3).reverse();

  return (
    <div className="dashboard">
      {/* Header Section */}
      <div className="dashboard-header">
        <div className="player-info">
          <div className="player-avatar">{player.avatar}</div>
          <div className="player-details">
            <h1>{player.username}</h1>
            <div className="player-level">
              {t('game.dashboard.level', { level: player.level })} • {levelTitle}
            </div>
          </div>
        </div>

        <div className="quick-actions">
          <button onClick={() => setCurrentView('profile')} className="btn-secondary">
            {t('game.dashboard.profile')}
          </button>
          <button onClick={() => setCurrentView('achievements')} className="btn-secondary">
            {t('game.dashboard.achievements')} ({(unlockedAchievements || []).length})
          </button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">🎓</div>
          <div className="stat-value">{playerStats.classes_completed}</div>
          <div className="stat-label">{t('game.dashboard.stats.classesCompleted')}</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">💪</div>
          <div className="stat-value">{playerStats.exercises_completed}</div>
          <div className="stat-label">{t('game.dashboard.stats.exercisesCompleted')}</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🐛</div>
          <div className="stat-value">{playerStats.bug_hunt_wins}</div>
          <div className="stat-label">{t('game.dashboard.stats.bugHuntWins')}</div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🔥</div>
          <div className="stat-value">{playerStats.current_streak}</div>
          <div className="stat-label">{t('game.dashboard.stats.dayStreak')}</div>
        </div>
      </div>

      {/* XP Progress */}
      <div className="xp-section">
        <div className="xp-header">
          <span>{t('game.dashboard.level', { level: player.level })}</span>
          <span>{player.xp} XP</span>
          <span>{t('game.dashboard.level', { level: player.level + 1 })}</span>
        </div>
        <div className="xp-bar">
          <div
            className="xp-fill"
            style={{ width: `${xpProgress.progressPercentage}%` }}
          />
        </div>
        <div className="xp-info">
          {t('game.dashboard.xpToNextLevel', { xp: xpProgress.xpNeeded })}
        </div>
      </div>

      {/* Overall Progress */}
      <div className="progress-overview">
        <h2>{t('game.dashboard.yourProgress')}</h2>
        <div className="overall-progress">
          <div className="progress-stats">
            <span>
              {fullProgress.classes_completed} / {fullProgress.total_classes} {t('game.dashboard.classes')}
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
        <h2>{t('game.modules.title')}</h2>
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
                <h3>{t('game.modules.module', { number: module.module_number })}</h3>
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
                  {module.classes_completed} / {module.total_classes} {t('game.dashboard.classes')}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Achievements */}
      {recentAchievements.length > 0 && (
        <div className="achievements-section">
          <h2>{t('game.dashboard.recentAchievements')}</h2>
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
function getLevelTitle(level: number, t: (key: string) => string): string {
  if (level <= 5) return t('game.dashboard.levelTitle.juniorDev');
  if (level <= 10) return t('game.dashboard.levelTitle.midDev');
  if (level <= 15) return t('game.dashboard.levelTitle.seniorDev');
  if (level <= 20) return t('game.dashboard.levelTitle.techLead');
  if (level <= 25) return t('game.dashboard.levelTitle.architect');
  if (level <= 30) return t('game.dashboard.levelTitle.cto');
  return t('game.dashboard.levelTitle.legend');
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
