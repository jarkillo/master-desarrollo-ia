/**
 * Notifications - Toast notifications for achievements and game events
 */
import { useGameStore } from '../../stores/gameStore';
import './Notifications.css';

export const Notifications = () => {
  const { notifications, removeNotification } = useGameStore();

  if (notifications.length === 0) {
    return null;
  }

  return (
    <div className="notifications-container">
      {notifications.map((notification) => (
        <div
          key={notification.id}
          className={`notification ${notification.type}`}
          onClick={() => removeNotification(notification.id)}
        >
          {notification.type === 'achievement' && notification.achievement && (
            <div className="achievement-notification">
              <div className="achievement-icon-large">
                {notification.achievement.icon}
              </div>
              <div className="achievement-details">
                <div className="achievement-header">
                  <span className="achievement-badge">Achievement Unlocked!</span>
                  <span className={`rarity-badge ${notification.achievement.rarity}`}>
                    {notification.achievement.rarity}
                  </span>
                </div>
                <div className="achievement-title">
                  {notification.achievement.title}
                </div>
                <div className="achievement-description">
                  {notification.achievement.description}
                </div>
                <div className="achievement-xp">
                  +{notification.achievement.xp_reward} XP
                </div>
              </div>
            </div>
          )}

          {notification.type !== 'achievement' && (
            <div className="simple-notification">
              <span className="notification-icon">
                {notification.type === 'success' && '✓'}
                {notification.type === 'error' && '✕'}
                {notification.type === 'info' && 'ℹ'}
              </span>
              <span className="notification-message">{notification.message}</span>
            </div>
          )}

          <button
            className="notification-close"
            onClick={(e) => {
              e.stopPropagation();
              removeNotification(notification.id);
            }}
          >
            ✕
          </button>
        </div>
      ))}
    </div>
  );
};
