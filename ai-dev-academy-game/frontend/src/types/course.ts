/**
 * TypeScript types for NeuralFlow Multi-Course Platform
 * Matches backend courses from NFLOW-1
 */

// ============================================
// COURSE TYPES
// ============================================

export type CourseStatus = 'available' | 'coming_soon' | 'maintenance';

export interface Course {
  id: string;
  name: string;
  description: string;
  icon: string;
  status: CourseStatus;
  modules: number;
}

// Backend returns array directly, not wrapped object
export type CourseListResponse = Course[];

export interface CourseProgress {
  course_id: string;
  course_title: string;
  modules_completed: number;
  total_modules: number;
  classes_completed: number;
  total_classes: number;
  progress_percentage: number;
  last_accessed_at: string | null;
}

export interface AllCoursesProgressResponse {
  player_id: number;
  total_courses: number;
  courses_in_progress: number;
  courses_completed: number;
  courses: CourseProgress[];
}
