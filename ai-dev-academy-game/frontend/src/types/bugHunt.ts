/**
 * TypeScript types for Bug Hunt mini-game
 * Generated from backend Pydantic schemas
 */

export type Difficulty = 'easy' | 'medium' | 'hard';

export interface BugHuntStartRequest {
  player_id: number;
  difficulty?: Difficulty;
}

export interface BugHuntStartResponse {
  session_id: number;
  template_id: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  code: string;
  bugs_count: number;
  max_xp: number;
  started_at: string;
}

export interface BugHuntSubmitRequest {
  session_id: number;
  player_id: number;
  found_bug_lines: number[];
  time_seconds: number;
}

export interface BugResult {
  line: number;
  found: boolean;
  is_correct: boolean;
  bug_type: string | null;
  description: string | null;
}

export interface BugHuntSubmitResponse {
  success: boolean;
  score: number;
  xp_earned: number;
  bugs_found: number;
  bugs_total: number;
  bugs_missed: number;
  false_positives: number;
  accuracy: number;
  time_seconds: number;
  is_perfect: boolean;
  results: BugResult[];
  performance_bonus: number;
  achievements_unlocked: string[];
}

export interface LeaderboardEntry {
  rank: number;
  player_id: number;
  username: string;
  score: number;
  bugs_found: number;
  bugs_total: number;
  time_seconds: number;
  accuracy: number;
  difficulty: Difficulty;
  completed_at: string;
}

export interface LeaderboardResponse {
  total_entries: number;
  entries: LeaderboardEntry[];
  difficulty_filter: Difficulty | null;
}

export interface PlayerBugHuntStatsResponse {
  total_games_played: number;
  total_bugs_found: number;
  total_perfect_games: number;
  best_score: number;
  average_score: number;
  average_accuracy: number;
  favorite_difficulty: Difficulty | null;
  total_xp_earned: number;
}

/**
 * Game state types for UI
 */
export type GameState = 'start' | 'playing' | 'results' | 'leaderboard';

export interface SelectedLine {
  line: number;
  selected: boolean;
}
