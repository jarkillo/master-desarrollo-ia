/**
 * Dashboard - Main view showing player stats, progress, and next steps
 * Professional Tailwind design with "Suggested Next" card and XP animations
 */
import { useEffect } from 'react';
import { Trophy, BookOpen, Dumbbell, Bug, Flame, TrendingUp, ArrowRight, Sparkles } from 'lucide-react';
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
          <div className="inline-block w-16 h-16 border-4 border-primary border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-lg text-gray-600 dark:text-gray-400">Loading your progress...</p>
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

  return (
    <div className="space-y-8">
      {/* Welcome Header with Player Info */}
      <div className="bg-gradient-to-br from-primary via-secondary to-accent rounded-2xl p-8 text-white shadow-2xl relative overflow-hidden">
        {/* Animated background effect */}
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>

        <div className="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div className="w-24 h-24 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center text-6xl shadow-xl border-4 border-white/30">
              {player.avatar}
            </div>
            <div>
              <h1 className="text-4xl font-extrabold mb-2">
                Welcome back, {player.username}!
              </h1>
              <div className="flex items-center gap-3 text-white/90 text-lg">
                <span className="font-semibold">Level {player.level}</span>
                <span>•</span>
                <span>{levelTitle}</span>
              </div>
            </div>
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => useGameStore.getState().setCurrentView('profile')}
              className="px-6 py-3 bg-white/20 backdrop-blur-sm border-2 border-white/30 rounded-xl font-semibold hover:bg-white/30 transition-all duration-300 hover:scale-105"
            >
              View Profile
            </button>
            <button
              onClick={() => useGameStore.getState().setCurrentView('achievements')}
              className="px-6 py-3 bg-white/20 backdrop-blur-sm border-2 border-white/30 rounded-xl font-semibold hover:bg-white/30 transition-all duration-300 hover:scale-105 flex items-center gap-2"
            >
              <Trophy className="w-5 h-5" aria-hidden="true" />
              Achievements ({unlockedAchievements.length})
            </button>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<BookOpen className="w-8 h-8" aria-hidden="true" />}
          value={playerStats.classes_completed}
          label="Classes Completed"
          color="from-blue-500 to-cyan-500"
        />
        <StatCard
          icon={<Dumbbell className="w-8 h-8" aria-hidden="true" />}
          value={playerStats.exercises_completed}
          label="Exercises Done"
          color="from-purple-500 to-pink-500"
        />
        <StatCard
          icon={<Bug className="w-8 h-8" aria-hidden="true" />}
          value={playerStats.bug_hunt_wins}
          label="Bug Hunt Wins"
          color="from-green-500 to-emerald-500"
        />
        <StatCard
          icon={<Flame className="w-8 h-8" aria-hidden="true" />}
          value={playerStats.current_streak}
          label="Day Streak"
          color="from-orange-500 to-red-500"
        />
      </div>

      {/* XP Progress Section with Animation */}
      <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-2xl p-6 shadow-2xl">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <TrendingUp className="w-6 h-6 text-primary" aria-hidden="true" />
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Your Progress</h2>
          </div>
          <div className="text-right">
            <div className="text-sm text-gray-600 dark:text-gray-400">Next Level</div>
            <div className="text-2xl font-bold text-primary">{xpProgress.xpNeeded} XP</div>
          </div>
        </div>

        {/* Animated XP Bar */}
        <div className="relative">
          <div className="flex justify-between text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            <span>Level {player.level}</span>
            <span className="text-primary">{player.xp} XP</span>
            <span>Level {player.level + 1}</span>
          </div>
          <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden relative">
            <div
              className="h-full bg-gradient-to-r from-green-500 via-emerald-500 to-teal-500 rounded-full transition-all duration-1000 ease-out relative overflow-hidden"
              style={{ width: `${xpProgress.progressPercentage}%` }}
            >
              {/* Animated shine effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
            </div>
          </div>
          <div className="text-center mt-2 text-sm text-gray-600 dark:text-gray-400">
            {Math.round(xpProgress.progressPercentage)}% to next level
          </div>
        </div>
      </div>

      {/* Suggested Next Card - PROMINENT */}
      {nextRecommendedClass && (
        <div className="relative group">
          {/* Animated gradient border */}
          <div className="absolute -inset-0.5 bg-gradient-to-r from-primary via-secondary to-accent rounded-2xl opacity-75 group-hover:opacity-100 blur transition duration-1000 animate-pulse"></div>

          <div className="relative bg-white/95 dark:bg-gray-800/95 backdrop-blur-xl rounded-2xl p-8 shadow-2xl">
            <div className="flex items-start gap-4 mb-4">
              <div className="flex-shrink-0 w-16 h-16 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg">
                <Sparkles className="w-8 h-8 text-white" aria-hidden="true" />
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-3 py-1 bg-primary/10 text-primary text-xs font-bold rounded-full">
                    RECOMMENDED NEXT
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  {nextRecommendedClass.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400 mb-4">
                  {nextRecommendedClass.description}
                </p>
                <div className="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400">
                  <span className="flex items-center gap-1">
                    <span className="text-lg">{nextRecommendedClass.difficulty}</span>
                    {nextRecommendedClass.estimatedTime}
                  </span>
                  <span className="flex items-center gap-1">
                    ⭐ {nextRecommendedClass.xpReward} XP
                  </span>
                </div>
              </div>
            </div>

            <button
              onClick={handleStartNextClass}
              className="w-full group/btn relative px-8 py-4 bg-gradient-to-r from-primary to-secondary text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl transform transition-all duration-300 hover:scale-[1.02] overflow-hidden"
            >
              {/* Button shine effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover/btn:translate-x-[100%] transition-transform duration-1000"></div>

              <span className="relative flex items-center justify-center gap-2">
                Continue Learning
                <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" aria-hidden="true" />
              </span>
            </button>
          </div>
        </div>
      )}

      {/* Overall Progress */}
      <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-2xl p-6 shadow-2xl">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">Course Progress</h2>
        <div className="space-y-3">
          <div className="flex justify-between text-sm font-semibold text-gray-700 dark:text-gray-300">
            <span>{fullProgress.classes_completed} / {fullProgress.total_classes} classes</span>
            <span className="text-primary">{Math.round(fullProgress.overall_progress_percentage)}%</span>
          </div>
          <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${fullProgress.overall_progress_percentage}%` }}
            ></div>
          </div>
        </div>
      </div>

      {/* Modules Grid */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">Modules</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {fullProgress.modules.map((module) => (
            <button
              key={module.module_number}
              onClick={() => selectModule(module.module_number)}
              className={`group relative text-left rounded-2xl p-6 transition-all duration-300 hover:scale-[1.02] ${
                module.classes_completed === 0
                  ? 'bg-gray-100/90 dark:bg-gray-700/50 cursor-not-allowed opacity-60'
                  : 'bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-lg hover:shadow-2xl cursor-pointer'
              } ${
                module.classes_completed === module.total_classes
                  ? 'ring-2 ring-green-500'
                  : ''
              }`}
              disabled={module.classes_completed === 0}
            >
              <div className="flex items-start justify-between mb-3">
                <h3 className="text-lg font-bold text-primary">Module {module.module_number}</h3>
                {module.classes_completed === module.total_classes && (
                  <div className="w-8 h-8 rounded-full bg-green-500 flex items-center justify-center text-white font-bold">
                    ✓
                  </div>
                )}
              </div>

              <p className="text-gray-900 dark:text-white font-semibold mb-4">
                {module.module_title}
              </p>

              <div className="space-y-2">
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-primary to-secondary rounded-full transition-all duration-500"
                    style={{ width: `${module.module_progress_percentage}%` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-600 dark:text-gray-400 text-center">
                  {module.classes_completed} / {module.total_classes} classes
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
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Recent Achievements</h2>
            <button
              onClick={() => useGameStore.getState().setCurrentView('achievements')}
              className="text-primary hover:text-primary-600 font-semibold flex items-center gap-1 group"
            >
              View All
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" aria-hidden="true" />
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {recentAchievements.map((achievement) => (
              <div
                key={achievement.id}
                className={`relative overflow-hidden rounded-2xl p-6 bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-[1.02] border-l-4 ${getBorderColor(achievement.rarity)}`}
              >
                <div className="flex items-start gap-4">
                  <div className="text-5xl flex-shrink-0">
                    {achievement.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 dark:text-white mb-1">
                      {achievement.title}
                    </h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      {achievement.description}
                    </p>
                    <div className="text-sm font-semibold text-green-600 dark:text-green-400">
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
  color: string;
}

const StatCard = ({ icon, value, label, color }: StatCardProps) => (
  <div className="group relative bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-[1.02]">
    <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${color} opacity-10 rounded-full blur-2xl group-hover:opacity-20 transition-opacity`}></div>
    <div className="relative">
      <div className={`inline-flex items-center justify-center w-14 h-14 rounded-xl bg-gradient-to-br ${color} text-white shadow-lg mb-4`}>
        {icon}
      </div>
      <div className="text-4xl font-extrabold text-gray-900 dark:text-white mb-1">
        {value}
      </div>
      <div className="text-sm text-gray-600 dark:text-gray-400">
        {label}
      </div>
    </div>
  </div>
);

// Helper Functions
function getLevelTitle(level: number): string {
  if (level <= 5) return 'Junior Developer';
  if (level <= 10) return 'Mid Developer';
  if (level <= 15) return 'Senior Developer';
  if (level <= 20) return 'Tech Lead';
  if (level <= 25) return 'Architect';
  if (level <= 30) return 'CTO';
  return 'Legend';
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
