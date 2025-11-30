/**
 * Catalog API Service - Course catalog endpoints
 * Implements NFLOW-1 backend multi-course endpoints
 */
import { apiClient } from './api';
import type { CourseListResponse, AllCoursesProgressResponse } from '../types/course';

/**
 * Fetch all available courses from the catalog
 * GET /api/courses
 */
export const fetchCourses = async (): Promise<CourseListResponse> => {
  const response = await apiClient.get<CourseListResponse>('/api/courses');
  return response.data;
};

/**
 * Fetch player progress across all courses
 * GET /api/courses/progress/:playerId
 */
export const fetchAllCoursesProgress = async (
  playerId: number
): Promise<AllCoursesProgressResponse> => {
  const response = await apiClient.get<AllCoursesProgressResponse>(
    `/api/courses/progress/${playerId}`
  );
  return response.data;
};

/**
 * Validate if a course_id is valid and available
 * Helper function for routing guards
 */
export const validateCourseId = async (courseId: string): Promise<boolean> => {
  try {
    const { courses } = await fetchCourses();
    return courses.some(
      (course) => course.course_id === courseId && course.status === 'available'
    );
  } catch (error) {
    console.error('[Catalog API] Error validating course ID:', error);
    return false;
  }
};
