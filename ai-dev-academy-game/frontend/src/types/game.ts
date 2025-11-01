/**
 * TypeScript types for AI Dev Academy Game
 * Matches backend schemas from JAR-233
 */

// ============================================
// PLAYER TYPES
// ============================================

export interface Player {
  id: number;
  username: string;
  avatar: string;
  level: number;
  xp: number;
  created_at: string;
  last_login: string;
}

export interface PlayerCreate {
  username: string;
  avatar?: string;
}

export interface PlayerUpdate {
  username?: string;
  avatar?: string;
}

export interface PlayerStats {
  player_id: number;
  classes_completed: number;
  exercises_completed: number;
  bug_hunt_wins: number;
  bug_hunt_games_played: number;
  current_streak: number;
  longest_streak: number;
  last_activity_date: string;
}

// ============================================
// PROGRESS TYPES
// ============================================

export type ProgressStatus = 'locked' | 'unlocked' | 'in_progress' | 'completed';

export interface Progress {
  id: number;
  player_id: number;
  module_number: number;
  class_number: number;
  status: ProgressStatus;
  exercises_completed: number;
  started_at: string | null;
  completed_at: string | null;
  last_accessed_at: string | null;
}

export interface ProgressCreate {
  player_id: number;
  module_number: number;
  class_number: number;
  status: ProgressStatus;
}

export interface ProgressUpdate {
  status?: ProgressStatus;
  exercises_completed?: number;
}

export interface ClassInfo {
  class_number: number;
  title: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  estimated_time_minutes: number;
  xp_reward: number;
  prerequisites: string[];
  learning_objectives: string[];
}

export interface ModuleInfo {
  module_number: number;
  title: string;
  description: string;
  total_classes: number;
  classes: ClassInfo[];
}

export interface FullProgressResponse {
  player_id: number;
  total_modules: number;
  total_classes: number;
  classes_completed: number;
  overall_progress_percentage: number;
  modules: {
    module_number: number;
    module_title: string;
    total_classes: number;
    classes_completed: number;
    module_progress_percentage: number;
    classes: Progress[];
  }[];
}

export interface NextUnlockableClass {
  module_number: number;
  class_number: number;
  title: string;
  xp_reward: number;
}

// ============================================
// ACHIEVEMENT TYPES
// ============================================

export type AchievementCategory = 'learning' | 'minigame' | 'streak' | 'mastery' | 'special';
export type AchievementRarity = 'common' | 'rare' | 'epic' | 'legendary';

export interface Achievement {
  id: number;
  player_id: number;
  achievement_id: string;
  unlocked_at: string;
}

export interface AchievementDefinition {
  achievement_id: string;
  title: string;
  description: string;
  icon: string;
  category: AchievementCategory;
  rarity: AchievementRarity;
  xp_reward: number;
}

export interface AchievementWithDetails extends Achievement {
  title: string;
  description: string;
  icon: string;
  category: AchievementCategory;
  rarity: AchievementRarity;
  xp_reward: number;
}

export interface AllAchievementsResponse {
  total_achievements: number;
  achievements: AchievementDefinition[];
}

export interface PlayerAchievementsResponse {
  player_id: number;
  total_achievements: number;
  achievements: AchievementWithDetails[];
}

export interface UnlockAchievementRequest {
  player_id: number;
  achievement_id: string;
}

export interface CheckAchievementsRequest {
  player_id: number;
  action_type: 'complete_class' | 'bug_hunt_win' | 'complete_exercise';
  action_data?: Record<string, any>;
}

export interface CheckAchievementsResponse {
  achievements_unlocked: AchievementWithDetails[];
  xp_earned: number;
}

// ============================================
// XP & LEVELING TYPES
// ============================================

export interface XPProgress {
  current_level: number;
  next_level: number;
  xp_for_current_level: number;
  xp_for_next_level: number;
  xp_progress: number;
  xp_needed: number;
  progress_percentage: number;
}

export interface LevelInfo {
  level: number;
  title: string;
  xp: number;
  xp_progress: XPProgress;
}

// ============================================
// UI STATE TYPES
// ============================================

export type ViewMode = 'dashboard' | 'module' | 'class' | 'achievements' | 'profile';

export interface NotificationMessage {
  id: string;
  type: 'success' | 'error' | 'info' | 'achievement';
  message: string;
  achievement?: AchievementWithDetails;
  timestamp: number;
}
