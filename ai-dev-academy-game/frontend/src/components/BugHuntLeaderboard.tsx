/**
 * BugHuntLeaderboard - Display leaderboard rankings
 */
import { useState, useEffect } from 'react';
import { bugHuntApi } from '../services/bugHuntApi';
import type { LeaderboardResponse, Difficulty } from '../types/bugHunt';
import './BugHuntLeaderboard.css';

interface BugHuntLeaderboardProps {
  onBack: () => void;
}

export const BugHuntLeaderboard: React.FC<BugHuntLeaderboardProps> = ({
  onBack,
}) => {
  const [leaderboard, setLeaderboard] = useState<LeaderboardResponse | null>(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState<Difficulty | undefined>(
    undefined
  );
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadLeaderboard();
  }, [selectedDifficulty]);

  const loadLeaderboard = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await bugHuntApi.getLeaderboard(selectedDifficulty, 20);
      setLeaderboard(data);
    } catch (err) {
      console.error('Failed to load leaderboard:', err);
      setError('Failed to load leaderboard. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getDifficultyColor = (difficulty: string): string => {
    switch (difficulty) {
      case 'easy':
        return '#4caf50';
      case 'medium':
        return '#ff9800';
      case 'hard':
        return '#f44336';
      default:
        return '#888';
    }
  };

  const getMedalEmoji = (rank: number): string => {
    switch (rank) {
      case 1:
        return '🥇';
      case 2:
        return '🥈';
      case 3:
        return '🥉';
      default:
        return '';
    }
  };

  return (
    <div className="bug-hunt-leaderboard">
      <div className="leaderboard-container">
        <div className="leaderboard-header">
          <button className="back-button" onClick={onBack}>
            ← Back
          </button>
          <h1>🏆 Leaderboard</h1>
        </div>

        <div className="difficulty-filter">
          <button
            className={`filter-button ${selectedDifficulty === undefined ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty(undefined)}
          >
            All
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'easy' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('easy')}
          >
            🟢 Easy
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'medium' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('medium')}
          >
            🟡 Medium
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'hard' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('hard')}
          >
            🔴 Hard
          </button>
        </div>

        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>Loading leaderboard...</p>
          </div>
        )}

        {error && (
          <div className="error-state">
            <p>{error}</p>
            <button onClick={loadLeaderboard}>Retry</button>
          </div>
        )}

        {!isLoading && !error && leaderboard && (
          <>
            {leaderboard.entries.length === 0 ? (
              <div className="empty-state">
                <p>No games played yet. Be the first!</p>
              </div>
            ) : (
              <div className="leaderboard-table-container">
                <table className="leaderboard-table">
                  <thead>
                    <tr>
                      <th>Rank</th>
                      <th>Player</th>
                      <th>Score</th>
                      <th>Bugs</th>
                      <th>Accuracy</th>
                      <th>Time</th>
                      <th>Difficulty</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {leaderboard.entries.map((entry) => (
                      <tr
                        key={`${entry.player_id}-${entry.completed_at}`}
                        className={entry.rank <= 3 ? `top-${entry.rank}` : ''}
                      >
                        <td className="rank-cell">
                          {getMedalEmoji(entry.rank)}
                          {entry.rank}
                        </td>
                        <td className="player-cell">{entry.username}</td>
                        <td className="score-cell">{entry.score}</td>
                        <td className="bugs-cell">
                          {entry.bugs_found}/{entry.bugs_total}
                        </td>
                        <td className="accuracy-cell">
                          {entry.accuracy.toFixed(1)}%
                        </td>
                        <td className="time-cell">{formatTime(entry.time_seconds)}</td>
                        <td className="difficulty-cell">
                          <span
                            className="difficulty-badge"
                            style={{
                              backgroundColor: getDifficultyColor(entry.difficulty),
                            }}
                          >
                            {entry.difficulty}
                          </span>
                        </td>
                        <td className="date-cell">{formatDate(entry.completed_at)}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}

            {leaderboard.total_entries > leaderboard.entries.length && (
              <p className="more-entries-hint">
                Showing top {leaderboard.entries.length} of {leaderboard.total_entries}{' '}
                entries
              </p>
            )}
          </>
        )}
      </div>
    </div>
  );
};
