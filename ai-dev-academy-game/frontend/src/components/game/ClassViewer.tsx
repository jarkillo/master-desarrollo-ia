/**
 * ClassViewer - Shows class content with exercises and completion tracking
 * Professional corporate design for IT professionals
 */
import { useState, useEffect } from 'react';
import {
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  Circle,
  Clock,
  Award,
  Target,
  BookOpen,
  AlertCircle,
  Loader2,
  Trophy,
} from 'lucide-react';
import { useGameStore } from '../../stores/gameStore';
import type { ClassInfo } from '../../types/game';
import ClassContentViewer from './ClassContentViewer';

export const ClassViewer = () => {
  const {
    selectedModuleNumber,
    selectedClassNumber,
    currentModule,
    fullProgress,
    player,
    loadClassContent,
    completeCurrentClass,
    setCurrentView,
    isLoading,
    error,
  } = useGameStore();

  const [classContent, setClassContent] = useState<ClassInfo | null>(null);
  const [readingSectionsViewed, setReadingSectionsViewed] = useState(0);
  const [readingSectionsTotal, setReadingSectionsTotal] = useState(0);

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
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-lg text-gray-600 dark:text-gray-400">Cargando contenido...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-center max-w-md">
          <AlertCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-2">
            Error al Cargar la Clase
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">{error}</p>
          <button
            onClick={handleBack}
            className="px-5 py-2.5 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors"
          >
            Volver al Módulo
          </button>
        </div>
      </div>
    );
  }

  if (!classContent || selectedModuleNumber === null || selectedClassNumber === null) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-center max-w-md">
          <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-lg text-gray-600 dark:text-gray-400 mb-6">
            Contenido de la clase no encontrado
          </p>
          <button
            onClick={handleBack}
            className="px-5 py-2.5 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors"
          >
            Volver al Módulo
          </button>
        </div>
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

  const isCompleted = classProgress?.status === 'completed';
  const hasReadAllContent = readingSectionsViewed === readingSectionsTotal && readingSectionsTotal > 0;

  // Check if there's a next class
  const nextClass = currentModule?.classes.find(
    (c) => c.class_number === selectedClassNumber + 1
  );

  const getDifficultyLabel = (difficulty: string) => {
    const labels: Record<string, string> = {
      beginner: 'Principiante',
      intermediate: 'Intermedio',
      advanced: 'Avanzado',
    };
    return labels[difficulty] || difficulty;
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner':
        return 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400';
      case 'intermediate':
        return 'bg-orange-100 text-orange-700 dark:bg-orange-900/30 dark:text-orange-400';
      case 'advanced':
        return 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="max-w-5xl mx-auto">
      {/* Navigation */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={handleBack}
          className="flex items-center gap-2 px-4 py-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Volver al Módulo
        </button>
        {nextClass && isCompleted && (
          <button
            onClick={handleNextClass}
            className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors"
          >
            Siguiente Clase
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Class Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 mb-8">
        <div className="flex items-start justify-between gap-4 mb-4">
          <div className="flex-1">
            <h1 className="text-3xl font-semibold text-gray-900 dark:text-white mb-2">
              Clase {selectedClassNumber}: {classContent.title}
            </h1>
            {isCompleted && (
              <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 rounded-md text-sm font-medium">
                <CheckCircle2 className="w-4 h-4" />
                Completada
              </div>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-sm">
          <span
            className={`px-3 py-1 rounded-md font-medium ${getDifficultyColor(
              classContent.difficulty
            )}`}
          >
            {getDifficultyLabel(classContent.difficulty)}
          </span>
          <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
            <Clock className="w-4 h-4" />
            {classContent.estimated_time_minutes} min
          </span>
          <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
            <Award className="w-4 h-4" />
            {classContent.xp_reward} XP
          </span>
        </div>
      </div>

      {/* Class Content */}
      <div className="space-y-8">
        {/* Description */}
        <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            Acerca de esta Clase
          </h2>
          <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
            {classContent.description}
          </p>
        </section>

        {/* Prerequisites */}
        {classContent.prerequisites.length > 0 && (
          <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Requisitos Previos
            </h2>
            <ul className="space-y-2">
              {classContent.prerequisites.map((prereq, idx) => (
                <li key={idx} className="flex items-start gap-3 text-gray-600 dark:text-gray-300">
                  <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                  <span>{prereq}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Learning Objectives */}
        {classContent.learning_objectives.length > 0 && (
          <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
              Qué Aprenderás
            </h2>
            <ul className="space-y-2">
              {classContent.learning_objectives.map((objective, idx) => (
                <li key={idx} className="flex items-start gap-3 text-gray-600 dark:text-gray-300">
                  <Target className="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
                  <span>{objective}</span>
                </li>
              ))}
            </ul>
          </section>
        )}

        {/* Educational Content */}
        <section className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">
            Contenido de la Clase
          </h2>
          <ClassContentViewer
            moduleNumber={selectedModuleNumber}
            classNumber={selectedClassNumber}
            onReadingProgress={(viewed, total) => {
              setReadingSectionsViewed(viewed);
              setReadingSectionsTotal(total);
            }}
          />
        </section>

        {/* TODO: Exercises section - to be implemented with real exercises from markdown */}

        {/* Complete Class Button */}
        {!isCompleted && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 text-center">
            <button
              onClick={handleCompleteClass}
              disabled={!hasReadAllContent || isLoading}
              className={`px-8 py-4 rounded-lg font-semibold text-lg transition-colors flex items-center justify-center gap-3 mx-auto ${
                hasReadAllContent && !isLoading
                  ? 'bg-blue-600 text-white hover:bg-blue-700'
                  : 'bg-gray-300 dark:bg-gray-700 text-gray-500 dark:text-gray-400 cursor-not-allowed'
              }`}
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Completando...
                </>
              ) : (
                <>
                  <Trophy className="w-5 h-5" />
                  Completar Clase y Ganar {classContent.xp_reward} XP
                </>
              )}
            </button>
            {!hasReadAllContent && readingSectionsTotal > 0 && (
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-4">
                Lee todas las secciones del contenido para completar la clase ({readingSectionsViewed}/{readingSectionsTotal} leídas)
              </p>
            )}
          </div>
        )}

        {/* Completion Info */}
        {isCompleted && classProgress?.completed_at && (
          <div className="bg-green-50 dark:bg-green-900/10 border-2 border-green-500 rounded-lg p-8">
            <div className="flex items-start gap-4 mb-6">
              <Trophy className="w-8 h-8 text-green-600 dark:text-green-400 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-semibold text-green-900 dark:text-green-100 mb-1">
                  ¡Clase Completada!
                </h3>
                <p className="text-green-700 dark:text-green-300">
                  Completado el{' '}
                  {new Date(classProgress.completed_at).toLocaleDateString('es-ES', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </p>
              </div>
            </div>
            {nextClass ? (
              <button
                onClick={handleNextClass}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
              >
                Continuar con la Siguiente Clase
                <ArrowRight className="w-5 h-5" />
              </button>
            ) : (
              <div className="text-center">
                <p className="text-lg font-semibold text-green-900 dark:text-green-100 flex items-center justify-center gap-2">
                  <Trophy className="w-6 h-6" />
                  ¡Has completado todas las clases de este módulo!
                </p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
