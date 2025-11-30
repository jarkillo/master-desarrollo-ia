/**
 * CourseCard - Individual course card component
 * NFLOW-2: Professional glassmorphism design with honest value messaging
 */
import { Link } from 'react-router-dom';
import { BookOpen, Lock, Clock, CheckCircle2, ArrowRight } from 'lucide-react';
import type { Course } from '../../types/course';

interface CourseCardProps {
  course: Course;
}

export const CourseCard = ({ course }: CourseCardProps) => {
  const isAvailable = course.status === 'available';
  const isComingSoon = course.status === 'coming_soon';

  // Real course features - no fake data
  const courseFeatures = {
    'master-ia': [
      'Fundamentos de IA aplicada al desarrollo',
      'Proyectos prácticos con FastAPI y React',
      'Integración con Claude, GPT y otras IAs',
    ],
    'data-engineering': [
      'Pipeline de datos a escala empresarial',
      'Airflow, DBT y orquestación moderna',
      'Data Warehousing con Snowflake/BigQuery',
    ],
  };

  const features = courseFeatures[course.id as keyof typeof courseFeatures] || [
    'Contenido estructurado y progresivo',
    'Ejercicios prácticos en cada módulo',
    'Acceso al código fuente completo',
  ];

  // Status badge configuration
  const getStatusBadge = () => {
    if (isAvailable) {
      return {
        label: 'Disponible Ahora',
        className: 'bg-emerald-500/90 text-white',
        icon: null,
      };
    }
    if (isComingSoon) {
      return {
        label: 'Próximamente',
        className: 'bg-blue-500/90 text-white',
        icon: <Clock className="w-3 h-3 mr-1" />,
      };
    }
    return {
      label: 'Mantenimiento',
      className: 'bg-orange-500/90 text-white',
      icon: <Lock className="w-3 h-3 mr-1" />,
    };
  };

  const badge = getStatusBadge();

  return (
    <article
      className={`
        group relative rounded-2xl overflow-hidden
        transition-all duration-500 ease-out
        ${
          isAvailable
            ? 'hover:scale-[1.02] hover:-translate-y-1 cursor-pointer'
            : 'opacity-75'
        }
      `}
      aria-label={`Curso: ${course.name} - ${badge.label}`}
    >
      {/* Animated gradient border */}
      <div
        className={`
          absolute -inset-0.5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500
          ${
            isAvailable
              ? 'bg-gradient-to-r from-primary via-secondary to-accent blur-sm'
              : 'bg-gray-300'
          }
        `}
        aria-hidden="true"
      />

      {/* Main card content */}
      <div
        className={`
          relative h-full rounded-2xl p-8
          ${
            isAvailable
              ? 'bg-white/90 dark:bg-gray-800/90 backdrop-blur-xl shadow-2xl'
              : 'bg-gray-100/90 dark:bg-gray-700/90 backdrop-blur-xl shadow-lg'
          }
        `}
      >
        {/* Status Badge */}
        <div className="absolute top-6 right-6 flex gap-2">
          <span
            className={`
              inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold shadow-md
              ${badge.className}
            `}
          >
            {badge.icon}
            {badge.label}
          </span>
        </div>

        {/* Course Icon */}
        <div className="mb-6">
          <div
            className={`
              inline-flex items-center justify-center w-20 h-20 rounded-2xl shadow-lg
              ${
                isAvailable
                  ? 'bg-gradient-to-br from-primary-100 to-secondary-100 dark:from-primary-900/30 dark:to-secondary-900/30'
                  : 'bg-gray-200 dark:bg-gray-600'
              }
            `}
          >
            <span className="text-5xl" role="img" aria-label={`Icono del curso ${course.name}`}>
              {course.icon}
            </span>
          </div>
        </div>

        {/* Course Title */}
        <h3 className="text-3xl font-extrabold text-gray-900 dark:text-white mb-3 leading-tight">
          {course.name}
        </h3>

        {/* Course Description */}
        <p className="text-gray-600 dark:text-gray-300 mb-6 leading-relaxed">
          {course.description}
        </p>

        {/* Course Features */}
        <div className="mb-6 space-y-2">
          {features.map((feature, index) => (
            <div key={index} className="flex items-start gap-2">
              <CheckCircle2 className="w-5 h-5 text-emerald-500 flex-shrink-0 mt-0.5" aria-hidden="true" />
              <span className="text-sm text-gray-700 dark:text-gray-300">{feature}</span>
            </div>
          ))}
        </div>

        {/* Course Metadata */}
        <div className="flex items-center gap-4 mb-6 text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center gap-1">
            <BookOpen className="w-4 h-4" aria-hidden="true" />
            <span>{course.modules} módulos</span>
          </div>
          <div className="text-gray-300 dark:text-gray-600">•</div>
          <span>100% online</span>
          <div className="text-gray-300 dark:text-gray-600">•</div>
          <span>A tu ritmo</span>
        </div>

        {/* Divider */}
        <div className="border-t border-gray-200 dark:border-gray-700 mb-6" />

        {/* Action Button */}
        <div>
          {isAvailable ? (
            <Link
              to={`/game/${course.id}`}
              className="
                group/btn relative block w-full text-center px-8 py-4 rounded-xl font-bold text-lg
                bg-gradient-to-r from-primary to-secondary text-white
                shadow-lg hover:shadow-2xl
                transform transition-all duration-300
                hover:scale-[1.02]
                focus:outline-none focus:ring-4 focus:ring-primary/50
                overflow-hidden
              "
              aria-label={`Comenzar el curso ${course.name}`}
            >
              {/* Button shine effect */}
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover/btn:translate-x-[100%] transition-transform duration-1000" />

              <span className="relative flex items-center justify-center gap-2">
                Comenzar Curso
                <ArrowRight className="w-5 h-5 group-hover/btn:translate-x-1 transition-transform" aria-hidden="true" />
              </span>
            </Link>
          ) : isComingSoon ? (
            <div className="text-center">
              <button
                className="
                  w-full px-8 py-4 rounded-xl font-bold text-lg
                  bg-gray-300 text-gray-600 dark:bg-gray-700 dark:text-gray-400
                  cursor-not-allowed
                "
                disabled
                aria-label={`El curso ${course.name} estará disponible próximamente`}
              >
                <span className="flex items-center justify-center gap-2">
                  <Clock className="w-5 h-5" aria-hidden="true" />
                  Próximamente
                </span>
              </button>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-3">
                Estamos trabajando en este curso
              </p>
            </div>
          ) : (
            <button
              className="
                w-full px-8 py-4 rounded-xl font-bold text-lg
                bg-gray-300 text-gray-600 dark:bg-gray-700 dark:text-gray-400
                cursor-not-allowed
              "
              disabled
              aria-label={`El curso ${course.name} no está disponible actualmente`}
            >
              <span className="flex items-center justify-center gap-2">
                <Lock className="w-5 h-5" aria-hidden="true" />
                No Disponible
              </span>
            </button>
          )}
        </div>
      </div>
    </article>
  );
};
