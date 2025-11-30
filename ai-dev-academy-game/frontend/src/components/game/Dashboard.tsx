/**
 * Dashboard - Main view showing player stats, progress, and next steps
 * Professional corporate design for IT professionals
 */
import { useEffect } from 'react';
import { Trophy, BookOpen, Dumbbell, Bug, Flame, TrendingUp, ArrowRight, Star, User as UserIcon } from 'lucide-react';
import { useGameStore } from '../../stores/gameStore';

export const Dashboard = () => {
  const {
    player,
    playerStats,
    fullProgress,
    unlockedAchievements,
    loadPlayer,
    loadFullProgress,
    loadPlayerAchievements,
    loadAllModules,
    selectModule,
    selectClass,
  } = useGameStore();

  useEffect(() => {
    const playerId = player?.id || parseInt(import.meta.env.VITE_DEFAULT_PLAYER_ID || '1', 10);

    // Load all data
    Promise.all([
      loadPlayer(playerId),
      loadFullProgress(playerId),
      loadPlayerAchievements(playerId),
      loadAllModules(),
    ]).catch(console.error);
  }, []);

  if (!player || !playerStats || !fullProgress) {
    return (
      <div className="flex items-center justify-center min-h-[50vh]">
        <div className="text-center">
          <div className="inline-block w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-lg text-gray-600 dark:text-gray-400">Cargando tu progreso...</p>
        </div>
      </div>
    );
  }

  const levelTitle = getLevelTitle(player.level);
  const xpProgress = getXPProgress(player.xp);
  const recentAchievements = unlockedAchievements.slice(-3).reverse();

  // Find next recommended class
  const nextRecommendedClass = findNextRecommendedClass(fullProgress);

  const handleStartNextClass = () => {
    if (nextRecommendedClass) {
      selectClass(nextRecommendedClass.moduleNumber, nextRecommendedClass.classNumber);
    }
  };

  // Avatar display function - same logic as ProfilePlaceholder
  const getAvatarDisplay = () => {
    if (!player?.avatar || player.avatar === 'default.png' || player.avatar.includes('.png')) {
      return <UserIcon className="w-14 h-14 text-white" />;
    }
    return <span className="text-5xl">{player.avatar}</span>;
  };

  return (
    <div className="space-y-6">
      {/* Welcome Header with Player Info */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 rounded-full bg-blue-600 flex items-center justify-center border-4 border-blue-100 dark:border-blue-900">
              {getAvatarDisplay()}
            </div>
            <div>
              <h1 className="text-3xl font-semibold text-gray-900 dark:text-white mb-1">
                Bienvenido/a, {player.username}
              </h1>
              <div className="flex items-center gap-3 text-gray-600 dark:text-gray-300 text-base">
                <span className="font-medium">Nivel {player.level}</span>
                <span>•</span>
                <span>{levelTitle}</span>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => useGameStore.getState().setCurrentView('profile')}
              className="px-5 py-2.5 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200 rounded-md font-medium hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
            >
              Ver Perfil
            </button>
            <button
              onClick={() => useGameStore.getState().setCurrentView('achievements')}
              className="px-5 py-2.5 bg-blue-600 text-white rounded-md font-medium hover:bg-blue-700 transition-colors flex items-center gap-2"
            >
              <Trophy className="w-5 h-5" aria-hidden="true" />
              Logros ({unlockedAchievements.length})
            </button>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<BookOpen className="w-7 h-7" aria-hidden="true" />}
          value={playerStats.classes_completed}
          label="Clases Completadas"
          color="blue"
        />
        <StatCard
          icon={<Dumbbell className="w-7 h-7" aria-hidden="true" />}
          value={playerStats.exercises_completed}
          label="Ejercicios Realizados"
          color="purple"
        />
        <StatCard
          icon={<Bug className="w-7 h-7" aria-hidden="true" />}
          value={playerStats.bug_hunt_wins}
          label="Victorias Bug Hunt"
          color="green"
        />
        <StatCard
          icon={<Flame className="w-7 h-7" aria-hidden="true" />}
          value={playerStats.current_streak}
          label="Racha de Días"
          color="orange"
        />
      </div>

      {/* XP Progress Section */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-6 h-6 text-blue-600 dark:text-blue-400" aria-hidden="true" />
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Tu Progreso</h2>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-600 dark:text-gray-400">Siguiente Nivel</div>
            <div className="text-xl font-semibold text-blue-600 dark:text-blue-400">{xpProgress.xpNeeded} XP</div>
          </div>
        </div>

        {/* XP Progress Bar */}
        <div className="relative">
          <div className="flex justify-between text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            <span>Nivel {player.level}</span>
            <span className="text-blue-600 dark:text-blue-400">{player.xp} XP</span>
            <span>Nivel {player.level + 1}</span>
          </div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 rounded-full transition-all duration-500"
              style={{ width: `${xpProgress.progressPercentage}%` }}
            ></div>
          </div>
          <div className="text-center mt-2 text-sm text-gray-600 dark:text-gray-400">
            {Math.round(xpProgress.progressPercentage)}% para el siguiente nivel
          </div>
        </div>
      </div>

      {/* Suggested Next Card */}
      {nextRecommendedClass && (
        <div className="bg-blue-50 dark:bg-blue-900/10 border-2 border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <div className="flex items-start gap-4 mb-4">
            <div className="flex-shrink-0 w-14 h-14 rounded-lg bg-blue-600 flex items-center justify-center">
              <BookOpen className="w-7 h-7 text-white" aria-hidden="true" />
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="px-3 py-1 bg-blue-600 text-white text-xs font-semibold rounded-md">
                  RECOMENDADO A CONTINUACIÓN
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                {nextRecommendedClass.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-300 mb-3">
                {nextRecommendedClass.description}
              </p>
              <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400">
                <span className="flex items-center gap-1">
                  <span className="text-base">{nextRecommendedClass.difficulty}</span>
                  {nextRecommendedClass.estimatedTime}
                </span>
                <span className="flex items-center gap-1">
                  <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
                  {nextRecommendedClass.xpReward} XP
                </span>
              </div>
            </div>
          </div>

          <button
            onClick={handleStartNextClass}
            className="w-full px-6 py-3 bg-blue-600 text-white rounded-md font-semibold hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
          >
            Continuar Aprendiendo
            <ArrowRight className="w-5 h-5" aria-hidden="true" />
          </button>
        </div>
      )}

      {/* Overall Progress */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">Progreso del Curso</h2>
        <div className="space-y-3">
          <div className="flex justify-between text-sm font-medium text-gray-700 dark:text-gray-300">
            <span>{fullProgress.classes_completed} / {fullProgress.total_classes} clases</span>
            <span className="text-blue-600 dark:text-blue-400">{Math.round(fullProgress.overall_progress_percentage)}%</span>
          </div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-600 rounded-full transition-all duration-500"
              style={{ width: `${fullProgress.overall_progress_percentage}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-6">Módulos</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {fullProgress.modules.map((module) => (
            <button
              key={module.module_number}
              onClick={() => selectModule(module.module_number)}
              className={`relative text-left rounded-lg p-6 transition-colors ${
                module.classes_completed === 0
                  ? 'bg-gray-100 dark:bg-gray-700 cursor-not-allowed opacity-60'
                  : 'bg-white dark:bg-gray-800 shadow hover:shadow-md cursor-pointer'
              } ${
                module.classes_completed === module.total_classes
                  ? 'ring-2 ring-green-500'
                  : ''
              }`}
              disabled={module.classes_completed === 0}
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-base font-semibold text-blue-600 dark:text-blue-400">Módulo {module.module_number}</h3>
                {module.classes_completed === module.total_classes && (
                  <div className="w-7 h-7 rounded-full bg-green-500 flex items-center justify-center text-white text-sm font-bold">
                    ✓
                  </div>
                )}
              </div>

              <p className="text-gray-900 dark:text-white font-medium mb-4 text-sm">
                {module.module_title}
              </p>

              <div className="space-y-2">
                <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-600 rounded-full transition-all duration-500"
                    style={{ width: `${module.module_progress_percentage}%` }}
                  ></div>
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400 text-center">
                  {module.classes_completed} / {module.total_classes} clases
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Achievements */}
      {recentAchievements.length > 0 && (
        <div>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Logros Recientes</h2>
            <button
              onClick={() => useGameStore.getState().setCurrentView('achievements')}
              className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-medium flex items-center gap-1 group"
            >
              Ver Todos
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" aria-hidden="true" />
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recentAchievements.map((achievement) => (
              <div
                key={achievement.id}
                className={`rounded-lg p-5 bg-white dark:bg-gray-800 shadow hover:shadow-md transition-shadow border-l-4 ${getBorderColor(achievement.rarity)}`}
              >
                <div className="flex items-start gap-4">
                  <div className="text-4xl flex-shrink-0">
                    {achievement.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1 text-sm">
                      {achievement.title}
                    </h3>
                    <p className="text-xs text-gray-600 dark:text-gray-400 mb-2">
                      {achievement.description}
                    </p>
                    <div className="text-xs font-medium text-green-600 dark:text-green-400">
                      +{achievement.xp_reward} XP
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

// Stat Card Component
interface StatCardProps {
  icon: React.ReactNode;
  value: number;
  label: string;
  color: 'blue' | 'purple' | 'green' | 'orange';
}

const getColorClasses = (color: StatCardProps['color']) => {
  const colors = {
    blue: 'bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400',
    purple: 'bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400',
    green: 'bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400',
    orange: 'bg-orange-100 dark:bg-orange-900/30 text-orange-600 dark:text-orange-400',
  };
  return colors[color];
};

const StatCard = ({ icon, value, label, color }: StatCardProps) => (
  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-5 hover:shadow-md transition-shadow">
    <div className={`inline-flex items-center justify-center w-12 h-12 rounded-lg ${getColorClasses(color)} mb-3`}>
      {icon}
    </div>
    <div className="text-3xl font-bold text-gray-900 dark:text-white mb-1">
      {value}
    </div>
    <div className="text-sm text-gray-600 dark:text-gray-400">
      {label}
    </div>
  </div>
);

// Helper Functions
function getLevelTitle(level: number): string {
  if (level <= 5) return 'Desarrollador Junior';
  if (level <= 10) return 'Desarrollador Mid';
  if (level <= 15) return 'Desarrollador Senior';
  if (level <= 20) return 'Tech Lead';
  if (level <= 25) return 'Arquitecto';
  if (level <= 30) return 'CTO';
  return 'Leyenda';
}

function getXPProgress(xp: number): {
  currentLevel: number;
  nextLevel: number;
  xpForCurrentLevel: number;
  xpForNextLevel: number;
  xpProgress: number;
  xpNeeded: number;
  progressPercentage: number;
} {
  const currentLevel = Math.floor((xp / 100) ** 0.5) + 1;
  const nextLevel = currentLevel + 1;
  const xpForCurrentLevel = (currentLevel - 1) ** 2 * 100;
  const xpForNextLevel = (nextLevel - 1) ** 2 * 100;
  const xpProgress = xp - xpForCurrentLevel;
  const xpNeeded = xpForNextLevel - xp;
  const progressPercentage = (xpProgress / (xpForNextLevel - xpForCurrentLevel)) * 100;

  return {
    currentLevel,
    nextLevel,
    xpForCurrentLevel,
    xpForNextLevel,
    xpProgress,
    xpNeeded,
    progressPercentage,
  };
}

function findNextRecommendedClass(fullProgress: any): {
  moduleNumber: number;
  classNumber: number;
  title: string;
  description: string;
  difficulty: string;
  estimatedTime: string;
  xpReward: number;
} | null {
  // Find first module with incomplete classes
  for (const module of fullProgress.modules) {
    // Find first incomplete class in this module
    const nextClass = module.classes.find(
      (c: any) => c.status === 'unlocked' || c.status === 'in_progress'
    );
    if (nextClass) {
      return {
        moduleNumber: module.module_number,
        classNumber: nextClass.class_number,
        title: `Class ${nextClass.class_number}: ${nextClass.title || 'Next Class'}`,
        description: nextClass.description || 'Continue your learning journey',
        difficulty: nextClass.difficulty || 'intermediate',
        estimatedTime: nextClass.estimated_time_minutes ? `${nextClass.estimated_time_minutes} min` : '30 min',
        xpReward: nextClass.xp_reward || 100,
      };
    }
  }
  return null;
}

function getBorderColor(rarity: string): string {
  switch (rarity) {
    case 'common':
      return 'border-gray-400';
    case 'rare':
      return 'border-blue-500';
    case 'epic':
      return 'border-purple-500';
    case 'legendary':
      return 'border-yellow-500';
    default:
      return 'border-gray-300';
  }
}
