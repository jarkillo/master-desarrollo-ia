/**
 * ClassViewer - Shows class content with exercises and completion tracking
 */
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useGameStore } from '../../stores/gameStore';
import type { ClassInfo } from '../../types/game';
import './ClassViewer.css';

export const ClassViewer = () => {
  const { t, i18n } = useTranslation();
  const {
    selectedModuleNumber,
    selectedClassNumber,
    currentModule,
    fullProgress,
    player,
    loadClassContent,
    toggleExerciseComplete,
    completeCurrentClass,
    setCurrentView,
    isLoading,
    error,
  } = useGameStore();

  const [classContent, setClassContent] = useState<ClassInfo | null>(null);
  const [completedExercises, setCompletedExercises] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (selectedModuleNumber !== null && selectedClassNumber !== null) {
      loadClassContentData();
    }
  }, [selectedModuleNumber, selectedClassNumber]);

  const loadClassContentData = async () => {
    if (selectedModuleNumber === null || selectedClassNumber === null) return;

    try {
      await loadClassContent(selectedModuleNumber, selectedClassNumber);

      // Get class content from currentModule
      if (currentModule) {
        const classInfo = currentModule.classes.find(
          (c) => c.class_number === selectedClassNumber
        );
        setClassContent(classInfo || null);
      }
    } catch (err) {
      console.error('Failed to load class content:', err);
    }
  };

  const handleToggleExercise = (exerciseId: string) => {
    setCompletedExercises((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(exerciseId)) {
        newSet.delete(exerciseId);
      } else {
        newSet.add(exerciseId);
      }
      return newSet;
    });
    toggleExerciseComplete(exerciseId);
  };

  const handleCompleteClass = async () => {
    if (!player || selectedModuleNumber === null || selectedClassNumber === null) return;

    try {
      await completeCurrentClass();
    } catch (err) {
      console.error('Failed to complete class:', err);
    }
  };

  const handleBack = () => {
    setCurrentView('module');
  };

  const handleNextClass = () => {
    if (nextClass && selectedModuleNumber !== null) {
      const { selectClass } = useGameStore.getState();
      selectClass(selectedModuleNumber, nextClass.class_number);
    }
  };

  if (isLoading && !classContent) {
    return (
      <div className="class-viewer-loading">
        <div className="loading-spinner"></div>
        <p>{t('game.class.loadingContent')}</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="class-viewer-error">
        <div className="error-icon">⚠️</div>
        <h2>{t('game.class.errorLoading')}</h2>
        <p>{error}</p>
        <button onClick={handleBack} className="btn-back">
          {t('game.class.backToModule')}
        </button>
      </div>
    );
  }

  if (!classContent || selectedModuleNumber === null || selectedClassNumber === null) {
    return (
      <div className="class-viewer-error">
        <p>{t('game.class.contentNotFound')}</p>
        <button onClick={handleBack} className="btn-back">
          {t('game.class.backToModule')}
        </button>
      </div>
    );
  }

  // Get progress info for this class
  const moduleProgress = fullProgress?.modules.find(
    (m) => m.module_number === selectedModuleNumber
  );
  const classProgress = moduleProgress?.classes.find(
    (p) => p.class_number === selectedClassNumber
  );

  // Generate exercise list (for demo purposes - in production, these would come from backend)
  const exercises = classContent.learning_objectives.map((objective, idx) => ({
    id: `exercise-${selectedModuleNumber}-${selectedClassNumber}-${idx}`,
    title: `${t('game.class.exercise')} ${idx + 1}`,
    description: objective,
    completed: completedExercises.has(`exercise-${selectedModuleNumber}-${selectedClassNumber}-${idx}`),
  }));

  const allExercisesCompleted = exercises.length > 0 && exercises.every((ex) => ex.completed);
  const isCompleted = classProgress?.status === 'completed';

  // Check if there's a next class
  const nextClass = currentModule?.classes.find(
    (c) => c.class_number === selectedClassNumber + 1
  );

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'var(--color-success)';
      case 'intermediate':
        return 'var(--color-warning)';
      case 'advanced':
        return 'var(--color-error)';
      default:
        return 'var(--color-text-secondary)';
    }
  };

  return (
    <div className="class-viewer">
      {/* Navigation */}
      <div className="class-nav">
        <button onClick={handleBack} className="btn-back">
          ← {t('game.class.backToModule')}
        </button>
        {nextClass && isCompleted && (
          <button onClick={handleNextClass} className="btn-next">
            {t('game.class.nextClass')} →
          </button>
        )}
      </div>

      {/* Class Header */}
      <div className="class-header">
        <div className="class-header-content">
          <div className="class-title-section">
            <h1 className="class-title">
              {t('game.modules.class', { number: selectedClassNumber })}: {classContent.title}
            </h1>
            {isCompleted && <span className="completion-badge">✅ {t('game.class.completedBadge')}</span>}
          </div>

          <div className="class-meta">
            <span
              className="difficulty-badge"
              style={{ backgroundColor: getDifficultyColor(classContent.difficulty) }}
            >
              {classContent.difficulty}
            </span>
            <span className="meta-item">
              <span className="meta-icon">⏱️</span>
              {classContent.estimated_time_minutes} min
            </span>
            <span className="meta-item">
              <span className="meta-icon">⭐</span>
              {classContent.xp_reward} XP
            </span>
          </div>
        </div>
      </div>

      {/* Class Content */}
      <div className="class-content">
        {/* Description */}
        <section className="content-section">
          <h2>{t('game.class.aboutThisClass')}</h2>
          <p className="class-description">{classContent.description}</p>
        </section>

        {/* Prerequisites */}
        {classContent.prerequisites.length > 0 && (
          <section className="content-section prerequisites">
            <h2>{t('game.class.prerequisites')}</h2>
            <ul className="prerequisites-list">
              {classContent.prerequisites.map((prereq, idx) => (
                <li key={idx}>
                  <span className="prereq-icon">✓</span>
                  {prereq}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Learning Objectives */}
        {classContent.learning_objectives.length > 0 && (
          <section className="content-section learning-objectives">
            <h2>{t('game.class.whatYouWillLearn')}</h2>
            <ul className="objectives-list">
              {classContent.learning_objectives.map((objective, idx) => (
                <li key={idx}>
                  <span className="objective-icon">🎯</span>
                  {objective}
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Exercises */}
        <section className="content-section exercises">
          <h2>{t('game.class.exercises')}</h2>
          <div className="exercises-progress">
            <span>
              {completedExercises.size} / {exercises.length} {t('game.class.exercisesCompleted')}
            </span>
            <div className="exercises-progress-bar">
              <div
                className="exercises-progress-fill"
                style={{
                  width: `${exercises.length > 0 ? (completedExercises.size / exercises.length) * 100 : 0}%`,
                }}
              />
            </div>
          </div>

          <div className="exercises-list">
            {exercises.map((exercise) => (
              <div
                key={exercise.id}
                className={`exercise-item ${exercise.completed ? 'completed' : ''}`}
              >
                <label className="exercise-checkbox">
                  <input
                    type="checkbox"
                    checked={exercise.completed}
                    onChange={() => handleToggleExercise(exercise.id)}
                    disabled={isCompleted}
                  />
                  <span className="checkbox-custom"></span>
                </label>
                <div className="exercise-content">
                  <h3 className="exercise-title">{exercise.title}</h3>
                  <p className="exercise-description">{exercise.description}</p>
                </div>
                {exercise.completed && (
                  <span className="exercise-complete-icon">✓</span>
                )}
              </div>
            ))}
          </div>
        </section>

        {/* Complete Class Button */}
        {!isCompleted && (
          <div className="complete-section">
            <button
              onClick={handleCompleteClass}
              className="btn-complete-class"
              disabled={!allExercisesCompleted || isLoading}
            >
              {isLoading ? (
                <>
                  <span className="btn-spinner"></span>
                  {t('game.class.completing')}
                </>
              ) : (
                <>
                  <span className="btn-icon">🎉</span>
                  {t('game.class.completeClassButton', { xp: classContent.xp_reward })}
                </>
              )}
            </button>
            {!allExercisesCompleted && (
              <p className="complete-hint">
                {t('game.class.completeAllExercises')}
              </p>
            )}
          </div>
        )}

        {/* Completion Info */}
        {isCompleted && classProgress?.completed_at && (
          <div className="completion-info">
            <div className="completion-message">
              <span className="completion-icon">🎉</span>
              <div>
                <h3>{t('game.class.classCompletedTitle')}</h3>
                <p>
                  {t('game.class.completedOnDate', {
                    date: new Date(classProgress.completed_at).toLocaleDateString(i18n.language, {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })
                  })}
                </p>
              </div>
            </div>
            {nextClass ? (
              <button onClick={handleNextClass} className="btn-next-class">
                {t('game.class.continueToNextClass')} →
              </button>
            ) : (
              <p className="module-complete-message">
                🏆 {t('game.class.moduleCompleteMessage')}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
