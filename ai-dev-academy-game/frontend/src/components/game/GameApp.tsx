/**
 * GameApp - Main AI Dev Academy Game application
 * NFLOW-2: Receive courseId from URL parameter
 * Professional Tailwind design with glassmorphism
 */
import { useEffect } from 'react';
import { useParams, Navigate, Link } from 'react-router-dom';
import { BookOpen, Award, User, LogOut, Home } from 'lucide-react';
import { useGameStore } from '../../stores/gameStore';
import { useAuthStore } from '../../stores/authStore';
import { Dashboard } from './Dashboard';
import { ModuleViewer } from './ModuleViewer';
import { ClassViewer } from './ClassViewer';
import { Notifications } from './Notifications';

export const GameApp = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const { currentView, selectedModuleNumber, selectedClassNumber, setCourseId } = useGameStore();
  const { logout } = useAuthStore();

  // Set courseId in store when component mounts or courseId changes
  useEffect(() => {
    if (courseId) {
      setCourseId(courseId);
    }
  }, [courseId, setCourseId]);

  // If no courseId in URL (should not happen due to redirect), show error
  if (!courseId) {
    return <Navigate to="/game/master-ia" replace />;
  }

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <Notifications />

      {/* Professional Header with Glassmorphism */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/80 dark:bg-gray-900/80 border-b border-gray-200/50 dark:border-gray-700/50 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link
              to="/catalog"
              className="flex items-center gap-3 group transition-all duration-300 hover:scale-105"
            >
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-secondary flex items-center justify-center shadow-lg group-hover:shadow-xl transition-shadow">
                <span className="text-2xl" role="img" aria-label="Logo">
                  🤖
                </span>
              </div>
              <div className="flex flex-col">
                <span className="text-lg font-bold text-gray-900 dark:text-white">
                  AI Dev Academy
                </span>
                <span className="text-xs text-gray-600 dark:text-gray-400">
                  Master IA
                </span>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-2">
              <Link
                to="/catalog"
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Volver al catálogo"
              >
                <Home className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Catalog</span>
              </Link>

              <button
                onClick={() => useGameStore.getState().setCurrentView('achievements')}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Ver logros"
              >
                <Award className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Achievements</span>
              </button>

              <button
                onClick={() => useGameStore.getState().setCurrentView('profile')}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
                aria-label="Ver perfil"
              >
                <User className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Profile</span>
              </button>

              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-semibold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                aria-label="Cerrar sesión"
              >
                <LogOut className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'module' && <ModuleViewer />}
        {currentView === 'class' && selectedModuleNumber !== null && selectedClassNumber !== null && (
          <ClassViewer />
        )}
        {currentView === 'achievements' && <AchievementsPlaceholder />}
        {currentView === 'profile' && <ProfilePlaceholder />}
      </main>

      {/* Professional Footer */}
      <footer className="mt-16 border-t border-gray-200 dark:border-gray-700 bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              © 2025 AI Dev Academy. Aprende desarrollo moderno con IA.
            </p>
            <div className="flex items-center gap-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors"
              >
                GitHub
              </a>
              <a
                href="#"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors"
              >
                Docs
              </a>
              <a
                href="#"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors"
              >
                Community
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

// Placeholder components for future development
const AchievementsPlaceholder = () => {
  const { setCurrentView, unlockedAchievements } = useGameStore();

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8">
        <button
          onClick={() => setCurrentView('dashboard')}
          className="flex items-center gap-2 text-primary hover:text-primary-600 transition-colors mb-6"
        >
          ← Back to Dashboard
        </button>

        <div className="text-center">
          <div className="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-yellow-400 to-orange-500 mb-4">
            <Award className="w-10 h-10 text-white" aria-hidden="true" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
            All Achievements
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-6">
            You have unlocked <span className="font-bold text-primary">{unlockedAchievements.length}</span> achievements!
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            Full achievements gallery coming soon...
          </p>
        </div>
      </div>
    </div>
  );
};

const ProfilePlaceholder = () => {
  const { setCurrentView, player } = useGameStore();

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl rounded-2xl shadow-2xl p-8">
        <button
          onClick={() => setCurrentView('dashboard')}
          className="flex items-center gap-2 text-primary hover:text-primary-600 transition-colors mb-6"
        >
          ← Back to Dashboard
        </button>

        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-br from-primary to-secondary text-5xl mb-4 shadow-xl">
            {player?.avatar || '👤'}
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Profile</h2>

          {player && (
            <div className="space-y-4">
              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
                <div className="text-sm text-gray-600 dark:text-gray-400">Username</div>
                <div className="text-xl font-semibold text-gray-900 dark:text-white">
                  {player.username}
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">Level</div>
                  <div className="text-2xl font-bold text-primary">{player.level}</div>
                </div>
                <div className="bg-gray-50 dark:bg-gray-700/50 rounded-xl p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400">XP</div>
                  <div className="text-2xl font-bold text-secondary">{player.xp}</div>
                </div>
              </div>
            </div>
          )}

          <p className="text-gray-500 dark:text-gray-400 mt-8">
            Full profile editor coming soon...
          </p>
        </div>
      </div>
    </div>
  );
};
