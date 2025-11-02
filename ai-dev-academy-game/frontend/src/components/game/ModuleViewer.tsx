/**
 * ModuleViewer - Shows all classes in a module with their status
 */
import { useTranslation } from 'react-i18next';
import { useGameStore } from '../../stores/gameStore';
import { LoadingSkeleton } from '../common/LoadingSkeleton';
import './ModuleViewer.css';

export const ModuleViewer = () => {
  const { t } = useTranslation();
  const {
    currentModule,
    fullProgress,
    selectedModuleNumber,
    selectClass,
    setCurrentView,
  } = useGameStore();

  if (!currentModule || selectedModuleNumber === null || !fullProgress) {
    return <LoadingSkeleton type="module" count={1} />;
  }

  const moduleProgress = fullProgress.modules.find(
    (m) => m.module_number === selectedModuleNumber
  );

  if (!moduleProgress) {
    return <div className="module-error">{t('game.modules.moduleNotFound')}</div>;
  }

  const classesWithStatus = currentModule.classes.map((classInfo) => {
    const progress = moduleProgress.classes.find(
      (p) => p.class_number === classInfo.class_number
    );
    return { classInfo, progress };
  });

  return (
    <div className="module-viewer">
      {/* Back Button */}
      <button className="back-btn" onClick={() => setCurrentView('dashboard')}>
        ← {t('game.modules.backToDashboard')}
      </button>

      {/* Module Header */}
      <div className="module-header-section">
        <h1 className="module-title">
          {t('game.modules.module', { number: currentModule.module_number })}: {currentModule.title}
        </h1>
        <p className="module-description">{currentModule.description}</p>

        {/* Module Progress */}
        <div className="module-progress-overview">
          <div className="progress-stats">
            <span>
              {moduleProgress.classes_completed} / {moduleProgress.total_classes}{' '}
              {t('game.modules.classesCompleted')}
            </span>
            <span>{Math.round(moduleProgress.module_progress_percentage)}%</span>
          </div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${moduleProgress.module_progress_percentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Classes List */}
      <div className="classes-list">
        <h2>{t('game.modules.classesTitle')}</h2>
        {classesWithStatus.map(({ classInfo, progress }) => {
          const status = progress?.status || 'locked';
          const isClickable = status !== 'locked';

          return (
            <div
              key={classInfo.class_number}
              className={`class-card ${status} ${!isClickable ? 'disabled' : ''}`}
              onClick={() => {
                if (isClickable) {
                  selectClass(currentModule.module_number, classInfo.class_number);
                }
              }}
            >
              {/* Status Badge */}
              <div className="class-status-badge">
                {status === 'locked' && '🔒'}
                {status === 'unlocked' && '🔓'}
                {status === 'in_progress' && '⏳'}
                {status === 'completed' && '✅'}
              </div>

              <div className="class-content">
                {/* Class Header */}
                <div className="class-header">
                  <h3 className="class-title">
                    {t('game.modules.class', { number: classInfo.class_number })}: {classInfo.title}
                  </h3>
                  <div className="class-meta">
                    <span className={`difficulty ${classInfo.difficulty}`}>
                      {classInfo.difficulty}
                    </span>
                    <span className="time-estimate">
                      ⏱️ {t('game.modules.timeEstimate', { minutes: classInfo.estimated_time_minutes })}
                    </span>
                    <span className="xp-reward">
                      ⭐ {t('game.modules.xpReward', { xp: classInfo.xp_reward })}
                    </span>
                  </div>
                </div>

                {/* Class Description */}
                <p className="class-description">{classInfo.description}</p>

                {/* Learning Objectives */}
                {classInfo.learning_objectives.length > 0 && (
                  <div className="learning-objectives">
                    <strong>{t('game.modules.youWillLearn')}</strong>
                    <ul>
                      {classInfo.learning_objectives.map((objective, idx) => (
                        <li key={idx}>{objective}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Progress Info */}
                {progress && (
                  <div className="class-progress-info">
                    {progress.exercises_completed > 0 && (
                      <span>
                        📝 {t('game.modules.exercisesCompleted', { count: progress.exercises_completed })}
                      </span>
                    )}
                    {progress.completed_at && (
                      <span className="completion-date">
                        {t('game.modules.completedOn', {
                          date: new Date(progress.completed_at).toLocaleDateString()
                        })}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Action Button */}
              {isClickable && (
                <div className="class-action">
                  {status === 'completed' && (
                    <button className="btn-review">{t('game.modules.actions.review')}</button>
                  )}
                  {status === 'in_progress' && (
                    <button className="btn-continue">{t('game.modules.actions.continue')}</button>
                  )}
                  {status === 'unlocked' && (
                    <button className="btn-start">{t('game.modules.actions.start')}</button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
