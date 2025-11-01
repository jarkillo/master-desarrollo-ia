/**
 * ModuleViewer - Shows all classes in a module with their status
 */
import { useGameStore } from '../../stores/gameStore';
import './ModuleViewer.css';

export const ModuleViewer = () => {
  const {
    currentModule,
    fullProgress,
    selectedModuleNumber,
    selectClass,
    setCurrentView,
  } = useGameStore();

  if (!currentModule || selectedModuleNumber === null || !fullProgress) {
    return <div className="module-loading">Loading module...</div>;
  }

  const moduleProgress = fullProgress.modules.find(
    (m) => m.module_number === selectedModuleNumber
  );

  if (!moduleProgress) {
    return <div className="module-error">Module not found</div>;
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
        ← Back to Dashboard
      </button>

      {/* Module Header */}
      <div className="module-header-section">
        <h1 className="module-title">
          Module {currentModule.module_number}: {currentModule.title}
        </h1>
        <p className="module-description">{currentModule.description}</p>

        {/* Module Progress */}
        <div className="module-progress-overview">
          <div className="progress-stats">
            <span>
              {moduleProgress.classes_completed} / {moduleProgress.total_classes}{' '}
              classes completed
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
        <h2>Classes</h2>
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
                    Class {classInfo.class_number}: {classInfo.title}
                  </h3>
                  <div className="class-meta">
                    <span className={`difficulty ${classInfo.difficulty}`}>
                      {classInfo.difficulty}
                    </span>
                    <span className="time-estimate">
                      ⏱️ {classInfo.estimated_time_minutes} min
                    </span>
                    <span className="xp-reward">
                      ⭐ {classInfo.xp_reward} XP
                    </span>
                  </div>
                </div>

                {/* Class Description */}
                <p className="class-description">{classInfo.description}</p>

                {/* Learning Objectives */}
                {classInfo.learning_objectives.length > 0 && (
                  <div className="learning-objectives">
                    <strong>You will learn:</strong>
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
                        📝 {progress.exercises_completed} exercises completed
                      </span>
                    )}
                    {progress.completed_at && (
                      <span className="completion-date">
                        Completed on{' '}
                        {new Date(progress.completed_at).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Action Button */}
              {isClickable && (
                <div className="class-action">
                  {status === 'completed' && (
                    <button className="btn-review">Review</button>
                  )}
                  {status === 'in_progress' && (
                    <button className="btn-continue">Continue</button>
                  )}
                  {status === 'unlocked' && (
                    <button className="btn-start">Start</button>
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
