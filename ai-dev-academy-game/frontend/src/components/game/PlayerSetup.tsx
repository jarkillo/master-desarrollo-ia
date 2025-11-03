/**
 * PlayerSetup - Initial screen for creating or loading a player
 */
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useGameStore } from '../../stores/gameStore';
import { initializePlayer, playerApi } from '../../services/gameApi';
import './PlayerSetup.css';

export const PlayerSetup = () => {
  const { t } = useTranslation();
  const { setPlayer } = useGameStore();
  const [mode, setMode] = useState<'choice' | 'new' | 'existing'>('choice');
  const [username, setUsername] = useState('');
  const [playerId, setPlayerId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleCreatePlayer = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!username.trim() || username.length < 3) {
      setError(t('game.setup.errors.usernameRequired'));
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const { player } = await initializePlayer(username.trim());
      setPlayer(player);
      // Force reload to trigger Dashboard data loading
      window.location.reload();
    } catch (err: any) {
      console.error('Failed to create player:', err);
      if (err.response?.status === 409) {
        setError(t('game.setup.errors.usernameTaken'));
      } else {
        setError(t('game.setup.errors.createFailed'));
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleLoadPlayer = async (e: React.FormEvent) => {
    e.preventDefault();

    const id = parseInt(playerId, 10);
    if (isNaN(id) || id < 1) {
      setError(t('game.setup.errors.invalidPlayerId'));
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const player = await playerApi.getPlayer(id);
      setPlayer(player);
      // Force reload to trigger Dashboard data loading
      window.location.reload();
    } catch (err: any) {
      console.error('Failed to load player:', err);
      if (err.response?.status === 404) {
        setError(t('game.setup.errors.playerNotFound'));
      } else {
        setError(t('game.setup.errors.loadFailed'));
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (mode === 'choice') {
    return (
      <div className="player-setup">
        <div className="setup-container">
          <div className="setup-header">
            <div className="setup-icon">🤖</div>
            <h1>{t('game.setup.welcome')}</h1>
            <p className="setup-subtitle">{t('game.setup.subtitle')}</p>
          </div>

          <div className="setup-choices">
            <button
              className="setup-choice-btn new-player"
              onClick={() => setMode('new')}
            >
              <div className="choice-icon">✨</div>
              <h2>{t('game.setup.newPlayer')}</h2>
              <p>{t('game.setup.newPlayerDesc')}</p>
            </button>

            <button
              className="setup-choice-btn existing-player"
              onClick={() => setMode('existing')}
            >
              <div className="choice-icon">🎮</div>
              <h2>{t('game.setup.existingPlayer')}</h2>
              <p>{t('game.setup.existingPlayerDesc')}</p>
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (mode === 'new') {
    return (
      <div className="player-setup">
        <div className="setup-container">
          <button
            className="back-btn"
            onClick={() => {
              setMode('choice');
              setError(null);
              setUsername('');
            }}
          >
            ← {t('common.back')}
          </button>

          <div className="setup-header">
            <div className="setup-icon">✨</div>
            <h1>{t('game.setup.createAccount')}</h1>
            <p className="setup-subtitle">{t('game.setup.createAccountDesc')}</p>
          </div>

          <form onSubmit={handleCreatePlayer} className="setup-form">
            <div className="form-group">
              <label htmlFor="username">{t('game.setup.username')}</label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder={t('game.setup.usernamePlaceholder')}
                minLength={3}
                maxLength={20}
                disabled={isLoading}
                autoFocus
              />
              <small className="form-hint">{t('game.setup.usernameHint')}</small>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              type="submit"
              className="submit-btn"
              disabled={isLoading || !username.trim()}
            >
              {isLoading ? t('common.loading') : t('game.setup.startJourney')}
            </button>
          </form>
        </div>
      </div>
    );
  }

  if (mode === 'existing') {
    return (
      <div className="player-setup">
        <div className="setup-container">
          <button
            className="back-btn"
            onClick={() => {
              setMode('choice');
              setError(null);
              setPlayerId('');
            }}
          >
            ← {t('common.back')}
          </button>

          <div className="setup-header">
            <div className="setup-icon">🎮</div>
            <h1>{t('game.setup.continueGame')}</h1>
            <p className="setup-subtitle">{t('game.setup.continueGameDesc')}</p>
          </div>

          <form onSubmit={handleLoadPlayer} className="setup-form">
            <div className="form-group">
              <label htmlFor="playerId">{t('game.setup.playerId')}</label>
              <input
                type="number"
                id="playerId"
                value={playerId}
                onChange={(e) => setPlayerId(e.target.value)}
                placeholder="1"
                min="1"
                disabled={isLoading}
                autoFocus
              />
              <small className="form-hint">{t('game.setup.playerIdHint')}</small>
            </div>

            {error && <div className="error-message">{error}</div>}

            <button
              type="submit"
              className="submit-btn"
              disabled={isLoading || !playerId}
            >
              {isLoading ? t('common.loading') : t('game.setup.loadGame')}
            </button>
          </form>
        </div>
      </div>
    );
  }

  return null;
};
