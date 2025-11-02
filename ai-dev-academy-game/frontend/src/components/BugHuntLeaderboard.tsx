/**
 * BugHuntLeaderboard - Display leaderboard rankings
 */
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { bugHuntApi } from '../services/bugHuntApi';
import type { LeaderboardResponse, Difficulty } from '../types/bugHunt';
import './BugHuntLeaderboard.css';

interface BugHuntLeaderboardProps {
  onBack: () => void;
}

export const BugHuntLeaderboard: React.FC<BugHuntLeaderboardProps> = ({
  onBack,
}) => {
  const { t, i18n } = useTranslation();
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
      setError(t('bugHunt.leaderboard.loadingError'));
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
    return date.toLocaleDateString(i18n.language, {
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
            ← {t('common.back')}
          </button>
          <h1>🏆 {t('bugHunt.leaderboard.title')}</h1>
        </div>

        <div className="difficulty-filter">
          <button
            className={`filter-button ${selectedDifficulty === undefined ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty(undefined)}
          >
            {t('bugHunt.leaderboard.allDifficulties')}
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'easy' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('easy')}
          >
            🟢 {t('bugHunt.start.easy')}
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'medium' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('medium')}
          >
            🟡 {t('bugHunt.start.medium')}
          </button>
          <button
            className={`filter-button ${selectedDifficulty === 'hard' ? 'active' : ''}`}
            onClick={() => setSelectedDifficulty('hard')}
          >
            🔴 {t('bugHunt.start.hard')}
          </button>
        </div>

        {isLoading && (
          <div className="loading-state">
            <div className="spinner"></div>
            <p>{t('bugHunt.leaderboard.loadingLeaderboard')}</p>
          </div>
        )}

        {error && (
          <div className="error-state">
            <p>{error}</p>
            <button onClick={loadLeaderboard}>{t('common.retry')}</button>
          </div>
        )}

        {!isLoading && !error && leaderboard && (
          <>
            {leaderboard.entries.length === 0 ? (
              <div className="empty-state">
                <p>{t('bugHunt.leaderboard.noEntries')}</p>
              </div>
            ) : (
              <div className="leaderboard-table-container">
                <table className="leaderboard-table">
                  <thead>
                    <tr>
                      <th>{t('bugHunt.leaderboard.rank')}</th>
                      <th>{t('bugHunt.leaderboard.player')}</th>
                      <th>{t('bugHunt.leaderboard.score')}</th>
                      <th>{t('bugHunt.leaderboard.bugs')}</th>
                      <th>{t('bugHunt.leaderboard.accuracy')}</th>
                      <th>{t('bugHunt.leaderboard.time')}</th>
                      <th>{t('bugHunt.leaderboard.difficulty')}</th>
                      <th>{t('bugHunt.leaderboard.date')}</th>
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
                {t('bugHunt.leaderboard.showingEntries', {
                  showing: leaderboard.entries.length,
                  total: leaderboard.total_entries,
                })}
              </p>
            )}
          </>
        )}
      </div>
    </div>
  );
};
