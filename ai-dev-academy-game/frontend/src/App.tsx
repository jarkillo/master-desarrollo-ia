/**
 * App - Main application component that orchestrates the Bug Hunt game
 */
import { useState } from 'react';
import { BugHuntStart } from './components/BugHuntStart';
import { BugHuntGame } from './components/BugHuntGame';
import { BugHuntResults } from './components/BugHuntResults';
import { BugHuntLeaderboard } from './components/BugHuntLeaderboard';
import { bugHuntApi } from './services/bugHuntApi';
import type {
  GameState,
  BugHuntStartResponse,
  BugHuntSubmitResponse,
  Difficulty,
} from './types/bugHunt';
import './App.css';

function App() {
  const [gameState, setGameState] = useState<GameState>('start');
  const [gameData, setGameData] = useState<BugHuntStartResponse | null>(null);
  const [results, setResults] = useState<BugHuntSubmitResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // In a real app, this would come from authentication
  const playerId = parseInt(
    import.meta.env.VITE_DEFAULT_PLAYER_ID || '1',
    10
  );

  const handleStartGame = async (difficulty?: Difficulty) => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await bugHuntApi.startGame(playerId, difficulty);
      setGameData(data);
      setGameState('playing');
    } catch (err) {
      console.error('Failed to start game:', err);
      setError('Failed to start game. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitGame = async (
    selectedLines: number[],
    timeSeconds: number
  ) => {
    if (!gameData) return;

    setIsLoading(true);
    setError(null);

    try {
      const submitResults = await bugHuntApi.submitGame(
        gameData.session_id,
        playerId,
        selectedLines,
        timeSeconds
      );
      setResults(submitResults);
      setGameState('results');
    } catch (err) {
      console.error('Failed to submit game:', err);
      setError('Failed to submit game. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handlePlayAgain = () => {
    setGameData(null);
    setResults(null);
    setError(null);
    setGameState('start');
  };

  const handleViewLeaderboard = () => {
    setGameState('leaderboard');
  };

  const handleBackToStart = () => {
    setGameState('start');
  };

  return (
    <div className="app">
      {error && (
        <div className="error-banner">
          <span>⚠️ {error}</span>
          <button onClick={() => setError(null)}>✕</button>
        </div>
      )}

      {gameState === 'start' && (
        <BugHuntStart onStart={handleStartGame} isLoading={isLoading} />
      )}

      {gameState === 'playing' && gameData && (
        <BugHuntGame
          gameData={gameData}
          onSubmit={handleSubmitGame}
          isSubmitting={isLoading}
        />
      )}

      {gameState === 'results' && results && (
        <BugHuntResults
          results={results}
          onPlayAgain={handlePlayAgain}
          onViewLeaderboard={handleViewLeaderboard}
        />
      )}

      {gameState === 'leaderboard' && (
        <BugHuntLeaderboard onBack={handleBackToStart} />
      )}
    </div>
  );
}

export default App;
