/**
 * BugHuntStart - Component for selecting difficulty and starting the game
 */
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import type { Difficulty } from '../types/bugHunt';
import './BugHuntStart.css';

interface BugHuntStartProps {
  onStart: (difficulty?: Difficulty) => void;
  isLoading: boolean;
}

export const BugHuntStart: React.FC<BugHuntStartProps> = ({
  onStart,
  isLoading,
}) => {
  const { t } = useTranslation();
  const [selectedDifficulty, setSelectedDifficulty] = useState<
    Difficulty | undefined
  >(undefined);

  const handleStart = () => {
    onStart(selectedDifficulty);
  };

  const difficulties: Array<{ value: Difficulty; label: string; description: string }> = [
    {
      value: 'easy',
      label: t('bugHunt.start.easy'),
      description: t('bugHunt.start.easyDesc'),
    },
    {
      value: 'medium',
      label: t('bugHunt.start.medium'),
      description: t('bugHunt.start.mediumDesc'),
    },
    {
      value: 'hard',
      label: t('bugHunt.start.hard'),
      description: t('bugHunt.start.hardDesc'),
    },
  ];

  return (
    <div className="bug-hunt-start">
      <div className="start-container">
        <h1 className="title">{t('bugHunt.title')}</h1>
        <p className="subtitle">{t('bugHunt.subtitle')}</p>

        <div className="difficulty-section">
          <h2>{t('bugHunt.start.selectDifficulty')}</h2>
          <div className="difficulty-options">
            <button
              className={`difficulty-card ${
                selectedDifficulty === undefined ? 'selected' : ''
              }`}
              onClick={() => setSelectedDifficulty(undefined)}
              disabled={isLoading}
            >
              <div className="difficulty-icon">🎲</div>
              <div className="difficulty-label">{t('bugHunt.start.random')}</div>
              <div className="difficulty-desc">{t('bugHunt.start.randomDesc')}</div>
            </button>
            {difficulties.map((diff) => (
              <button
                key={diff.value}
                className={`difficulty-card ${
                  selectedDifficulty === diff.value ? 'selected' : ''
                }`}
                onClick={() => setSelectedDifficulty(diff.value)}
                disabled={isLoading}
              >
                <div className="difficulty-icon">
                  {diff.value === 'easy' && '🟢'}
                  {diff.value === 'medium' && '🟡'}
                  {diff.value === 'hard' && '🔴'}
                </div>
                <div className="difficulty-label">{diff.label}</div>
                <div className="difficulty-desc">{diff.description}</div>
              </button>
            ))}
          </div>
        </div>

        <button
          className="start-button"
          onClick={handleStart}
          disabled={isLoading}
        >
          {isLoading ? t('common.loading') : t('bugHunt.start.startGame')}
        </button>

        <div className="instructions">
          <h3>{t('bugHunt.start.howToPlay')}</h3>
          <ul>
            <li>{t('bugHunt.start.instructions.1')}</li>
            <li>{t('bugHunt.start.instructions.2')}</li>
            <li>{t('bugHunt.start.instructions.3')}</li>
            <li>{t('bugHunt.start.instructions.4')}</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
