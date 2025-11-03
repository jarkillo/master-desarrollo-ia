/**
 * BugHuntGame - Main game component with code display and bug selection
 */
import { useState, useMemo } from 'react';
import { useTranslation } from 'react-i18next';
import { useTimer } from '../hooks/useTimer';
import type { BugHuntStartResponse } from '../types/bugHunt';
import './BugHuntGame.css';

interface BugHuntGameProps {
  gameData: BugHuntStartResponse;
  onSubmit: (selectedLines: number[], timeSeconds: number) => void;
  isSubmitting: boolean;
}

export const BugHuntGame: React.FC<BugHuntGameProps> = ({
  gameData,
  onSubmit,
  isSubmitting,
}) => {
  const { t } = useTranslation();
  const [selectedLines, setSelectedLines] = useState<Set<number>>(new Set());
  const { time, isRunning, pause } = useTimer(0, true);

  // Split code into lines
  const codeLines = useMemo(() => {
    return gameData.code.split('\n');
  }, [gameData.code]);

  const toggleLine = (lineNumber: number) => {
    setSelectedLines((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(lineNumber)) {
        newSet.delete(lineNumber);
      } else {
        newSet.add(lineNumber);
      }
      return newSet;
    });
  };

  const handleSubmit = () => {
    pause();
    const selectedArray = Array.from(selectedLines).sort((a, b) => a - b);
    onSubmit(selectedArray, parseFloat(time.toFixed(1)));
  };

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds % 1) * 10);
    return `${mins.toString().padStart(2, '0')}:${secs
      .toString()
      .padStart(2, '0')}.${ms}`;
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

  return (
    <div className="bug-hunt-game">
      <div className="game-header">
        <div className="game-info">
          <h2 className="game-title">{gameData.title}</h2>
          <p className="game-description">{gameData.description}</p>
          <div className="game-meta">
            <span
              className="difficulty-badge"
              style={{ backgroundColor: getDifficultyColor(gameData.difficulty) }}
            >
              {gameData.difficulty.toUpperCase()}
            </span>
            <span className="bugs-count">
              🐛 {gameData.bugs_count} {t('bugHunt.game.bugs', { count: gameData.bugs_count })}
            </span>
            <span className="max-xp">⭐ {t('bugHunt.game.maxXp', { xp: gameData.max_xp })}</span>
          </div>
        </div>

        <div className="game-controls">
          <div className="timer">
            <span className="timer-icon">{isRunning ? '⏱️' : '⏸️'}</span>
            <span className="timer-value">{formatTime(time)}</span>
          </div>
          <div className="selected-count">
            {t('bugHunt.game.selectedLines', { count: selectedLines.size })}
          </div>
        </div>
      </div>

      <div className="code-container">
        <div className="code-header">
          <span>{t('bugHunt.game.clickToSelect')}</span>
        </div>
        <div className="code-display">
          {codeLines.map((line, index) => {
            const lineNumber = index + 1;
            const isSelected = selectedLines.has(lineNumber);
            const isEmpty = line.trim() === '';

            return (
              <div
                key={lineNumber}
                className={`code-line ${isSelected ? 'selected' : ''} ${
                  isEmpty ? 'empty' : ''
                }`}
                onClick={() => !isEmpty && toggleLine(lineNumber)}
                style={{ cursor: isEmpty ? 'default' : 'pointer' }}
              >
                <span className="line-number">{lineNumber}</span>
                <span className="line-content">
                  {line || '\u00A0'}
                </span>
                {isSelected && <span className="bug-marker">🐛</span>}
              </div>
            );
          })}
        </div>
      </div>

      <div className="game-actions">
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={isSubmitting || selectedLines.size === 0}
        >
          {isSubmitting ? t('bugHunt.game.submitting') : t('bugHunt.game.submitButton', { count: selectedLines.size })}
        </button>
        <p className="hint">
          {t('bugHunt.game.tip')}
        </p>
      </div>
    </div>
  );
};
