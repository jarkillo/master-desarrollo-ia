/**
 * ModuleViewer - Shows all classes in a module with their status
 * Professional corporate design for IT professionals
 */
import { Clock, Award, CheckCircle2, Lock, Play, RotateCcw, ArrowLeft } from 'lucide-react';
import { useGameStore } from '../../stores/gameStore';
import { LoadingSkeleton } from '../common/LoadingSkeleton';

export const ModuleViewer = () => {
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
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <p className="text-lg text-gray-600 dark:text-gray-400">Módulo no encontrado</p>
        </div>
      </div>
    );
  }

  const classesWithStatus = currentModule.classes.map((classInfo) => {
    const progress = moduleProgress.classes.find(
      (p) => p.class_number === classInfo.class_number
    );
    return { classInfo, progress };
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'locked':
        return <Lock className="w-5 h-5 text-gray-400" />;
      case 'unlocked':
        return <Play className="w-5 h-5 text-blue-600" />;
      case 'in_progress':
        return <Clock className="w-5 h-5 text-orange-500" />;
      case 'completed':
        return <CheckCircle2 className="w-5 h-5 text-green-500" />;
      default:
        return <Lock className="w-5 h-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'locked':
        return 'border-gray-300 dark:border-gray-600';
      case 'unlocked':
        return 'border-blue-500';
      case 'in_progress':
        return 'border-orange-500';
      case 'completed':
        return 'border-green-500';
      default:
        return 'border-gray-300';
    }
  };

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
      {/* Back Button */}
      <button
        onClick={() => setCurrentView('dashboard')}
        className="flex items-center gap-2 mb-6 px-4 py-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Volver al Panel
      </button>

      {/* Module Header */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8 mb-8">
        <h1 className="text-3xl font-semibold text-gray-900 dark:text-white mb-3">
          Módulo {currentModule.module_number}: {currentModule.title}
        </h1>
        <p className="text-gray-600 dark:text-gray-300 mb-6 text-lg">
          {currentModule.description}
        </p>

        {/* Module Progress */}
        <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
          <div className="flex justify-between text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            <span>
              {moduleProgress.classes_completed} / {moduleProgress.total_classes} clases completadas
            </span>
            <span className="text-blue-600 dark:text-blue-400">
              {Math.round(moduleProgress.module_progress_percentage)}%
            </span>
          </div>
          <div className="h-3 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 rounded-full transition-all duration-500"
              style={{ width: `${moduleProgress.module_progress_percentage}%` }}
            />
          </div>
        </div>
      </div>

      {/* Classes List */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Clases</h2>
        <div className="space-y-4">
          {classesWithStatus.map(({ classInfo, progress }) => {
            const status = progress?.status || 'locked';
            const isClickable = status !== 'locked';

            return (
              <div
                key={classInfo.class_number}
                className={`bg-white dark:bg-gray-800 rounded-lg shadow p-6 border-l-4 ${getStatusColor(
                  status
                )} ${
                  isClickable
                    ? 'cursor-pointer hover:shadow-md transition-shadow'
                    : 'opacity-60 cursor-not-allowed'
                }`}
                onClick={() => {
                  if (isClickable) {
                    selectClass(currentModule.module_number, classInfo.class_number);
                  }
                }}
              >
                <div className="flex items-start gap-4">
                  {/* Status Icon */}
                  <div className="flex-shrink-0 w-12 h-12 rounded-lg bg-gray-50 dark:bg-gray-700 flex items-center justify-center">
                    {getStatusIcon(status)}
                  </div>

                  {/* Class Content */}
                  <div className="flex-1 min-w-0">
                    <div className="flex items-start justify-between gap-4 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                        Clase {classInfo.class_number}: {classInfo.title}
                      </h3>
                    </div>

                    {/* Meta Info */}
                    <div className="flex flex-wrap items-center gap-3 mb-3 text-sm">
                      {classInfo.difficulty && (
                        <span
                          className={`px-2 py-1 rounded-md font-medium ${getDifficultyColor(
                            classInfo.difficulty
                          )}`}
                        >
                          {getDifficultyLabel(classInfo.difficulty)}
                        </span>
                      )}
                      {classInfo.estimated_time_minutes && (
                        <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                          <Clock className="w-4 h-4" />
                          {classInfo.estimated_time_minutes} min
                        </span>
                      )}
                      <span className="flex items-center gap-1 text-gray-600 dark:text-gray-400">
                        <Award className="w-4 h-4" />
                        {classInfo.xp_reward} XP
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-gray-600 dark:text-gray-300 mb-3 leading-relaxed">
                      {classInfo.description}
                    </p>

                    {/* Learning Objectives */}
                    {classInfo.learning_objectives && classInfo.learning_objectives.length > 0 && (
                      <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4 mb-3">
                        <strong className="block text-sm font-semibold text-gray-900 dark:text-white mb-2">
                          Aprenderás:
                        </strong>
                        <ul className="space-y-1 text-sm text-gray-600 dark:text-gray-300">
                          {classInfo.learning_objectives.map((objective, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span className="text-blue-600 dark:text-blue-400 mt-0.5">•</span>
                              <span>{objective}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Progress Info */}
                    {progress && (
                      <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                        {progress.exercises_completed > 0 && (
                          <span className="flex items-center gap-1">
                            <CheckCircle2 className="w-4 h-4" />
                            {progress.exercises_completed} ejercicios completados
                          </span>
                        )}
                        {progress.completed_at && (
                          <span className="text-green-600 dark:text-green-400 font-medium">
                            Completado el{' '}
                            {new Date(progress.completed_at).toLocaleDateString('es-ES')}
                          </span>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Action Button */}
                  {isClickable && (
                    <div className="flex-shrink-0">
                      {status === 'completed' && (
                        <button className="px-4 py-2 bg-green-600 text-white rounded-md font-medium hover:bg-green-700 transition-colors flex items-center gap-2">
                          <RotateCcw className="w-4 h-4" />
                          Repasar
                        </button>
                      )}
                      {status === 'in_progress' && (
                        <button className="px-4 py-2 bg-orange-500 text-white rounded-md font-medium hover:bg-orange-600 transition-colors flex items-center gap-2">
                          <Play className="w-4 h-4" />
                          Continuar
                        </button>
                      )}
                      {status === 'unlocked' && (
                        <button className="px-4 py-2 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors flex items-center gap-2">
                          <Play className="w-4 h-4" />
                          Comenzar
                        </button>
                      )}
                    </div>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
