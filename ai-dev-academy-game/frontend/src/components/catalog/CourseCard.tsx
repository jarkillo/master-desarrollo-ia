/**
 * CourseCard - Individual course card component
 * NFLOW-2: Display course information with status badges
 */
import { Link } from 'react-router-dom';
import type { Course } from '../../types/course';
import './CourseCard.css';

interface CourseCardProps {
  course: Course;
}

export const CourseCard = ({ course }: CourseCardProps) => {
  const isAvailable = course.status === 'available';
  const isComingSoon = course.status === 'coming_soon';

  const difficultyColors: Record<string, string> = {
    beginner: '#4CAF50',
    intermediate: '#FF9800',
    advanced: '#F44336',
  };

  const statusBadges: Record<string, { label: string; className: string }> = {
    available: { label: 'Available', className: 'status-available' },
    coming_soon: { label: 'Coming Soon', className: 'status-coming-soon' },
    maintenance: { label: 'Maintenance', className: 'status-maintenance' },
  };

  const badge = statusBadges[course.status];

  return (
    <div className={`course-card ${!isAvailable ? 'disabled' : ''}`}>
      {/* Status Badge */}
      <div className={`course-status-badge ${badge.className}`}>
        {badge.label}
      </div>

      {/* Course Icon */}
      <div className="course-icon">{course.icon}</div>

      {/* Course Title */}
      <h2 className="course-title">{course.title}</h2>

      {/* Course Description */}
      <p className="course-description">{course.description}</p>

      {/* Course Metadata */}
      <div className="course-metadata">
        <div
          className="course-difficulty"
          style={{ color: difficultyColors[course.difficulty] }}
        >
          <span className="metadata-icon">📊</span>
          {course.difficulty.charAt(0).toUpperCase() + course.difficulty.slice(1)}
        </div>
        <div className="course-duration">
          <span className="metadata-icon">⏱️</span>
          {course.estimated_hours}h
        </div>
        <div className="course-classes">
          <span className="metadata-icon">📚</span>
          {course.total_classes} classes
        </div>
      </div>

      {/* Course Tags */}
      <div className="course-tags">
        {course.tags.slice(0, 3).map((tag) => (
          <span key={tag} className="course-tag">
            {tag}
          </span>
        ))}
      </div>

      {/* Action Button */}
      {isAvailable ? (
        <Link to={`/game/${course.course_id}`} className="course-btn">
          Start Learning
        </Link>
      ) : isComingSoon ? (
        <button className="course-btn disabled" disabled>
          Coming Soon
        </button>
      ) : (
        <button className="course-btn disabled" disabled>
          Unavailable
        </button>
      )}
    </div>
  );
};
