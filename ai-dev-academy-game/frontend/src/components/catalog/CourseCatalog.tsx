/**
 * CourseCatalog - Main course catalog component
 * NFLOW-2: Professional design with honest, value-focused messaging
 */
import { useState, useEffect } from 'react';
import { BookOpen, Code, Zap, Award } from 'lucide-react';
import { CourseCard } from './CourseCard';
import { fetchCourses } from '../../services/catalogApi';
import type { Course } from '../../types/course';

export const CourseCatalog = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCourses = async () => {
      try {
        setLoading(true);
        const data = await fetchCourses();
        setCourses(data);
        setError(null);
      } catch (err) {
        console.error('[CourseCatalog] Error loading courses:', err);
        setError('No se pudieron cargar los cursos. Por favor, intenta más tarde.');
      } finally {
        setLoading(false);
      }
    };

    loadCourses();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-primary mb-4"></div>
          <p className="text-lg text-gray-600 dark:text-gray-400">Cargando cursos...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <div className="text-center max-w-md mx-auto p-8">
          <span className="text-6xl mb-4 block">⚠️</span>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-6">{error}</p>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary-600 transition-colors"
          >
            Reintentar
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16 lg:py-20">
        {/* Hero Section */}
        <header className="text-center mb-16" role="banner">
          <div className="relative inline-block mb-6">
            <div className="absolute inset-0 bg-gradient-to-r from-primary to-secondary blur-2xl opacity-20 animate-pulse"></div>
            <h1 className="relative text-5xl sm:text-6xl lg:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary via-secondary to-accent">
              Aprende con IA
            </h1>
          </div>

          <p className="text-xl sm:text-2xl text-gray-700 dark:text-gray-300 max-w-4xl mx-auto mb-8 leading-relaxed">
            Domina el desarrollo moderno con la inteligencia artificial como tu asistente personal.
            <span className="block mt-2 text-lg text-gray-600 dark:text-gray-400">
              Proyectos reales. Aprendizaje práctico. Contenido de calidad.
            </span>
          </p>

          {/* Value Propositions - Honest Features */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 max-w-4xl mx-auto mb-12">
            <div
              className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              role="group"
              aria-label="Aprendizaje práctico con proyectos reales"
            >
              <Code className="w-8 h-8 text-primary mx-auto mb-2" aria-hidden="true" />
              <div className="text-sm font-semibold text-gray-900 dark:text-white">Proyectos Reales</div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Aprende haciendo</div>
            </div>

            <div
              className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              role="group"
              aria-label="Contenido estructurado en módulos"
            >
              <BookOpen className="w-8 h-8 text-secondary mx-auto mb-2" aria-hidden="true" />
              <div className="text-sm font-semibold text-gray-900 dark:text-white">Bien Estructurado</div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Paso a paso</div>
            </div>

            <div
              className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              role="group"
              aria-label="Asistencia de IA integrada"
            >
              <Zap className="w-8 h-8 text-accent mx-auto mb-2" aria-hidden="true" />
              <div className="text-sm font-semibold text-gray-900 dark:text-white">IA Integrada</div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Tu asistente 24/7</div>
            </div>

            <div
              className="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              role="group"
              aria-label="A tu propio ritmo"
            >
              <Award className="w-8 h-8 text-primary mx-auto mb-2" aria-hidden="true" />
              <div className="text-sm font-semibold text-gray-900 dark:text-white">A Tu Ritmo</div>
              <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Sin presiones</div>
            </div>
          </div>
        </header>

        {/* Course Grid */}
        <main role="main" aria-label="Lista de cursos disponibles">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">
            Elige tu Camino de Aprendizaje
          </h2>

          <div className="grid lg:grid-cols-2 gap-8 mb-12">
            {courses.map((course) => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>

          {/* Empty State */}
          {courses.length === 0 && (
            <div className="text-center py-16 bg-white/50 dark:bg-gray-800/50 backdrop-blur-sm rounded-2xl">
              <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" aria-hidden="true" />
              <p className="text-xl text-gray-600 dark:text-gray-400">
                No hay cursos disponibles en este momento.
              </p>
              <p className="text-gray-500 dark:text-gray-500 mt-2">
                Estamos preparando contenido increíble para ti. Vuelve pronto.
              </p>
            </div>
          )}
        </main>

        {/* Footer - Open Source & Transparency */}
        <footer className="mt-16 pt-12 border-t border-gray-200 dark:border-gray-700" role="contentinfo">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400 text-sm">
              Proyecto educativo de código abierto. Aprende desarrollo moderno con IA.
            </p>
          </div>
        </footer>
      </div>
    </div>
  );
};
