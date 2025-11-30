/**
 * GameApp - Main AI Dev Academy Game application
 * NFLOW-2: Receive courseId from URL parameter
 * Professional corporate design for IT professionals
 */
import { useEffect } from 'react';
import { useParams, Navigate, Link } from 'react-router-dom';
import { Award, User, Home, GraduationCap } from 'lucide-react';
import { useGameStore } from '../../stores/gameStore';
import { Dashboard } from './Dashboard';
import { ModuleViewer } from './ModuleViewer';
import { ClassViewer } from './ClassViewer';
import { Notifications } from './Notifications';

export const GameApp = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const { currentView, selectedModuleNumber, selectedClassNumber, setCourseId } = useGameStore();

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

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Notifications />

      {/* Professional Corporate Header */}
      <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo */}
            <Link
              to="/catalog"
              className="flex items-center gap-3 group"
            >
              <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
                <GraduationCap className="w-6 h-6 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-base font-semibold text-gray-900 dark:text-white">
                  NeuralFlow
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  Plataforma de Formación
                </span>
              </div>
            </Link>

            {/* Navigation */}
            <nav className="flex items-center gap-1">
              <Link
                to="/catalog"
                className="flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Volver al catálogo"
              >
                <Home className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Catálogo</span>
              </Link>

              <button
                onClick={() => useGameStore.getState().setCurrentView('achievements')}
                className="flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Ver logros"
              >
                <Award className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Logros</span>
              </button>

              <button
                onClick={() => useGameStore.getState().setCurrentView('profile')}
                className="flex items-center gap-2 px-4 py-2 rounded-md text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                aria-label="Ver perfil"
              >
                <User className="w-4 h-4" aria-hidden="true" />
                <span className="hidden sm:inline">Perfil</span>
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
      <footer className="mt-16 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              © 2025 NeuralFlow. Formación profesional en desarrollo con IA.
            </p>
            <div className="flex items-center gap-6">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                GitHub
              </a>
              <a
                href="#"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                Documentación
              </a>
              <a
                href="#"
                className="text-sm text-gray-600 dark:text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                Soporte
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
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
        <button
          onClick={() => setCurrentView('dashboard')}
          className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors mb-6 font-medium"
        >
          ← Volver al Panel
        </button>

        <div className="text-center">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-lg bg-blue-100 dark:bg-blue-900/30 mb-4">
            <Award className="w-8 h-8 text-blue-600 dark:text-blue-400" aria-hidden="true" />
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-4">
            Todos los Logros
          </h2>
          <p className="text-lg text-gray-600 dark:text-gray-300 mb-6">
            Has desbloqueado <span className="font-semibold text-blue-600 dark:text-blue-400">{unlockedAchievements.length}</span> logros
          </p>
          <p className="text-gray-500 dark:text-gray-400">
            Galería completa de logros próximamente...
          </p>
        </div>
      </div>
    </div>
  );
};

const ProfilePlaceholder = () => {
  const { setCurrentView, player } = useGameStore();

  // Default professional avatar icon
  const getAvatarDisplay = () => {
    if (!player?.avatar || player.avatar === 'default.png' || player.avatar.includes('.png')) {
      return <User className="w-12 h-12 text-gray-600 dark:text-gray-300" />;
    }
    return <span className="text-4xl">{player.avatar}</span>;
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-8">
        <button
          onClick={() => setCurrentView('dashboard')}
          className="flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 transition-colors mb-6 font-medium"
        >
          ← Volver al Panel
        </button>

        <div className="text-center">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gray-100 dark:bg-gray-700 mb-4 border-4 border-gray-200 dark:border-gray-600">
            {getAvatarDisplay()}
          </div>
          <h2 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">Mi Perfil</h2>

          {player && (
            <div className="space-y-4">
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Nombre de usuario</div>
                <div className="text-lg font-medium text-gray-900 dark:text-white">
                  {player.username}
                </div>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Nivel</div>
                  <div className="text-2xl font-semibold text-blue-600 dark:text-blue-400">{player.level}</div>
                </div>
                <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Experiencia</div>
                  <div className="text-2xl font-semibold text-blue-600 dark:text-blue-400">{player.xp}</div>
                </div>
              </div>
            </div>
          )}

          <p className="text-gray-500 dark:text-gray-400 mt-8">
            Editor completo de perfil próximamente...
          </p>
        </div>
      </div>
    </div>
  );
};
