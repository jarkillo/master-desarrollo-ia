/**
 * BugHuntStart - Component for selecting difficulty and starting the game
 */
import { useState } from 'react';
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
  const [selectedDifficulty, setSelectedDifficulty] = useState<
    Difficulty | undefined
  >(undefined);

  const handleStart = () => {
    onStart(selectedDifficulty);
  };

  const difficulties: Array<{ value: Difficulty; label: string; description: string }> = [
    {
      value: 'easy',
      label: 'Easy',
      description: '1-2 bugs, basic patterns',
    },
    {
      value: 'medium',
      label: 'Medium',
      description: '2-3 bugs, moderate complexity',
    },
    {
      value: 'hard',
      label: 'Hard',
      description: '3+ bugs, advanced patterns',
    },
  ];

  return (
    <div className="bug-hunt-start">
      <div className="start-container">
        <h1 className="title">Bug Hunt</h1>
        <p className="subtitle">Find bugs in code and earn XP!</p>

        <div className="difficulty-section">
          <h2>Select Difficulty</h2>
          <div className="difficulty-options">
            <button
              className={`difficulty-card ${
                selectedDifficulty === undefined ? 'selected' : ''
              }`}
              onClick={() => setSelectedDifficulty(undefined)}
              disabled={isLoading}
            >
              <div className="difficulty-icon">🎲</div>
              <div className="difficulty-label">Random</div>
              <div className="difficulty-desc">Surprise me!</div>
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
          {isLoading ? 'Loading...' : 'Start Game'}
        </button>

        <div className="instructions">
          <h3>How to Play</h3>
          <ul>
            <li>Read the code carefully</li>
            <li>Click on lines you think have bugs</li>
            <li>Submit your answers before time runs out</li>
            <li>Earn XP based on accuracy and speed!</li>
          </ul>
        </div>
      </div>
    </div>
  );
};
