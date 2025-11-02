/**
 * BugHuntResults - Display game results and statistics
 */
import { useTranslation } from 'react-i18next';
import type { BugHuntSubmitResponse } from '../types/bugHunt';
import './BugHuntResults.css';

interface BugHuntResultsProps {
  results: BugHuntSubmitResponse;
  onPlayAgain: () => void;
  onViewLeaderboard: () => void;
}

export const BugHuntResults: React.FC<BugHuntResultsProps> = ({
  results,
  onPlayAgain,
  onViewLeaderboard,
}) => {
  const { t } = useTranslation();

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
  };

  const getPerformanceRating = (accuracy: number): string => {
    if (accuracy === 100 && results.is_perfect) return t('bugHunt.results.performance.perfect');
    if (accuracy >= 90) return t('bugHunt.results.performance.excellent');
    if (accuracy >= 75) return t('bugHunt.results.performance.great');
    if (accuracy >= 50) return t('bugHunt.results.performance.good');
    return t('bugHunt.results.performance.keepPracticing');
  };

  return (
    <div className="bug-hunt-results">
      <div className="results-container">
        {results.is_perfect && (
          <div className="perfect-banner">
            <h2>🏆 {t('bugHunt.results.perfectBanner')} 🏆</h2>
            <p>{t('bugHunt.results.perfectDesc')}</p>
          </div>
        )}

        <div className="results-header">
          <h1>{t('bugHunt.results.gameResults')}</h1>
          <p className="performance-rating">
            {getPerformanceRating(results.accuracy)}
          </p>
        </div>

        <div className="results-stats">
          <div className="stat-card primary">
            <div className="stat-icon">🎯</div>
            <div className="stat-value">{results.score}</div>
            <div className="stat-label">{t('bugHunt.results.score')}</div>
          </div>

          <div className="stat-card primary">
            <div className="stat-icon">⭐</div>
            <div className="stat-value">{results.xp_earned}</div>
            <div className="stat-label">{t('bugHunt.results.xpEarned')}</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🐛</div>
            <div className="stat-value">
              {results.bugs_found}/{results.bugs_total}
            </div>
            <div className="stat-label">{t('bugHunt.results.bugsFound')}</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-value">{results.accuracy.toFixed(1)}%</div>
            <div className="stat-label">{t('bugHunt.results.accuracy')}</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-value">{formatTime(results.time_seconds)}</div>
            <div className="stat-label">{t('bugHunt.results.time')}</div>
          </div>

          {results.performance_bonus > 0 && (
            <div className="stat-card bonus">
              <div className="stat-icon">🚀</div>
              <div className="stat-value">+{results.performance_bonus}</div>
              <div className="stat-label">{t('bugHunt.results.speedBonus')}</div>
            </div>
          )}
        </div>

        {(results.bugs_missed > 0 || results.false_positives > 0) && (
          <div className="results-breakdown">
            {results.bugs_missed > 0 && (
              <div className="breakdown-item missed">
                <span className="breakdown-icon">❌</span>
                <span className="breakdown-text">
                  {t('bugHunt.results.bugsMissed', { count: results.bugs_missed })}
                </span>
              </div>
            )}
            {results.false_positives > 0 && (
              <div className="breakdown-item false-positive">
                <span className="breakdown-icon">⚠️</span>
                <span className="breakdown-text">
                  {t('bugHunt.results.falsePositivesCount', { count: results.false_positives })}
                </span>
              </div>
            )}
          </div>
        )}

        <div className="results-details">
          <h3>{t('bugHunt.results.bugDetails')}</h3>
          <div className="bug-results-list">
            {results.results.map((bug, index) => (
              <div
                key={index}
                className={`bug-result-item ${
                  bug.is_correct
                    ? bug.found
                      ? 'correct-found'
                      : 'correct-missed'
                    : 'false-positive'
                }`}
              >
                <div className="bug-result-header">
                  <span className="bug-result-icon">
                    {bug.is_correct
                      ? bug.found
                        ? '✅'
                        : '❌'
                      : '⚠️'}
                  </span>
                  <span className="bug-result-line">
                    {t('bugHunt.results.lineLabel', { line: bug.line })}
                  </span>
                  {bug.bug_type && (
                    <span className="bug-result-type">{bug.bug_type}</span>
                  )}
                </div>
                {bug.description && (
                  <p className="bug-result-description">{bug.description}</p>
                )}
              </div>
            ))}
          </div>
        </div>

        {results.achievements_unlocked.length > 0 && (
          <div className="achievements-section">
            <h3>🏆 {t('bugHunt.results.achievements')}</h3>
            <div className="achievements-list">
              {results.achievements_unlocked.map((achievement, index) => (
                <div key={index} className="achievement-badge">
                  {achievement}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="results-actions">
          <button className="play-again-button" onClick={onPlayAgain}>
            🎮 {t('bugHunt.results.playAgain')}
          </button>
          <button className="leaderboard-button" onClick={onViewLeaderboard}>
            📊 {t('bugHunt.results.viewLeaderboard')}
          </button>
        </div>
      </div>
    </div>
  );
};
