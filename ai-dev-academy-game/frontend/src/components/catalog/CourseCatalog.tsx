/**
 * CourseCatalog - Main course catalog component
 * NFLOW-2: Fetch and display all available courses
 */
import { useState, useEffect } from 'react';
import { CourseCard } from './CourseCard';
import { fetchCourses } from '../../services/catalogApi';
import type { Course } from '../../types/course';
import './CourseCatalog.css';

export const CourseCatalog = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCourses = async () => {
      try {
        setLoading(true);
        const data = await fetchCourses();
        setCourses(data.courses);
        setError(null);
      } catch (err) {
        console.error('[CourseCatalog] Error loading courses:', err);
        setError('Failed to load courses. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    loadCourses();
  }, []);

  if (loading) {
    return (
      <div className="catalog-container">
        <div className="catalog-loading">
          <div className="loading-spinner"></div>
          <p>Loading courses...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="catalog-container">
        <div className="catalog-error">
          <span className="error-icon">⚠️</span>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="catalog-container">
      {/* Catalog Header */}
      <header className="catalog-header">
        <h1 className="catalog-title">
          <span className="catalog-icon">🎓</span>
          NeuralFlow Courses
        </h1>
        <p className="catalog-subtitle">
          Choose your learning path. Master modern development with AI as your assistant.
        </p>
      </header>

      {/* Course Grid */}
      <div className="courses-grid">
        {courses.map((course) => (
          <CourseCard key={course.course_id} course={course} />
        ))}
      </div>

      {/* Empty State */}
      {courses.length === 0 && (
        <div className="catalog-empty">
          <p>No courses available at the moment.</p>
        </div>
      )}
    </div>
  );
};
