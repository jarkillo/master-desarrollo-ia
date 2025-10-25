/**
 * BugHuntResults - Display game results and statistics
 */
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
  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}m ${secs}s`;
  };

  const getPerformanceRating = (accuracy: number): string => {
    if (accuracy === 100 && results.is_perfect) return '🏆 Perfect!';
    if (accuracy >= 90) return '🌟 Excellent!';
    if (accuracy >= 75) return '⭐ Great!';
    if (accuracy >= 50) return '👍 Good!';
    return '💪 Keep practicing!';
  };

  return (
    <div className="bug-hunt-results">
      <div className="results-container">
        {results.is_perfect && (
          <div className="perfect-banner">
            <h2>🏆 PERFECT GAME! 🏆</h2>
            <p>You found all bugs with no false positives!</p>
          </div>
        )}

        <div className="results-header">
          <h1>Game Results</h1>
          <p className="performance-rating">
            {getPerformanceRating(results.accuracy)}
          </p>
        </div>

        <div className="results-stats">
          <div className="stat-card primary">
            <div className="stat-icon">🎯</div>
            <div className="stat-value">{results.score}</div>
            <div className="stat-label">Score</div>
          </div>

          <div className="stat-card primary">
            <div className="stat-icon">⭐</div>
            <div className="stat-value">{results.xp_earned}</div>
            <div className="stat-label">XP Earned</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">🐛</div>
            <div className="stat-value">
              {results.bugs_found}/{results.bugs_total}
            </div>
            <div className="stat-label">Bugs Found</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">📊</div>
            <div className="stat-value">{results.accuracy.toFixed(1)}%</div>
            <div className="stat-label">Accuracy</div>
          </div>

          <div className="stat-card">
            <div className="stat-icon">⏱️</div>
            <div className="stat-value">{formatTime(results.time_seconds)}</div>
            <div className="stat-label">Time</div>
          </div>

          {results.performance_bonus > 0 && (
            <div className="stat-card bonus">
              <div className="stat-icon">🚀</div>
              <div className="stat-value">+{results.performance_bonus}</div>
              <div className="stat-label">Speed Bonus</div>
            </div>
          )}
        </div>

        {(results.bugs_missed > 0 || results.false_positives > 0) && (
          <div className="results-breakdown">
            {results.bugs_missed > 0 && (
              <div className="breakdown-item missed">
                <span className="breakdown-icon">❌</span>
                <span className="breakdown-text">
                  {results.bugs_missed} bug{results.bugs_missed !== 1 ? 's' : ''} missed
                </span>
              </div>
            )}
            {results.false_positives > 0 && (
              <div className="breakdown-item false-positive">
                <span className="breakdown-icon">⚠️</span>
                <span className="breakdown-text">
                  {results.false_positives} false positive{results.false_positives !== 1 ? 's' : ''}
                </span>
              </div>
            )}
          </div>
        )}

        <div className="results-details">
          <h3>Bug Details</h3>
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
                  <span className="bug-result-line">Line {bug.line}</span>
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
            <h3>🏆 Achievements Unlocked!</h3>
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
            🎮 Play Again
          </button>
          <button className="leaderboard-button" onClick={onViewLeaderboard}>
            📊 View Leaderboard
          </button>
        </div>
      </div>
    </div>
  );
};
