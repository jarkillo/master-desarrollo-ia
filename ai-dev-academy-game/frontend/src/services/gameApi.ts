/**
 * API client for AI Dev Academy Game
 * Connects to FastAPI backend from JAR-233
 */
import axios from 'axios';
import type {
  Player,
  PlayerCreate,
  PlayerUpdate,
  PlayerStats,
  Progress,
  ProgressCreate,
  ProgressUpdate,
  FullProgressResponse,
  NextUnlockableClass,
  AllAchievementsResponse,
  PlayerAchievementsResponse,
  AchievementWithDetails,
  CheckAchievementsRequest,
  CheckAchievementsResponse,
  ModuleInfo,
} from '../types/game';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// ============================================
// PLAYER API
// ============================================

export const playerApi = {
  /**
   * Create a new player
   */
  createPlayer: async (data: PlayerCreate): Promise<Player> => {
    const response = await axios.post<Player>(`${API_BASE_URL}/player/`, data);
    return response.data;
  },

  /**
   * Get player by ID
   */
  getPlayer: async (playerId: number): Promise<Player> => {
    const response = await axios.get<Player>(`${API_BASE_URL}/player/${playerId}`);
    return response.data;
  },

  /**
   * Update player info
   */
  updatePlayer: async (playerId: number, data: PlayerUpdate): Promise<Player> => {
    const response = await axios.patch<Player>(`${API_BASE_URL}/player/${playerId}`, data);
    return response.data;
  },

  /**
   * Get player stats
   */
  getPlayerStats: async (playerId: number): Promise<PlayerStats> => {
    const response = await axios.get<PlayerStats>(`${API_BASE_URL}/player/${playerId}/stats`);
    return response.data;
  },

  /**
   * Delete player
   */
  deletePlayer: async (playerId: number): Promise<void> => {
    await axios.delete(`${API_BASE_URL}/player/${playerId}`);
  },
};

// ============================================
// PROGRESS API
// ============================================

export const progressApi = {
  /**
   * Create or unlock a class
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  createProgress: async (data: ProgressCreate, courseId: string = 'master-ia'): Promise<Progress> => {
    const response = await axios.post<Progress>(`${API_BASE_URL}/progress/`, data, {
      params: { course_id: courseId }
    });
    return response.data;
  },

  /**
   * Get full progress for a player
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getFullProgress: async (playerId: number, courseId: string = 'master-ia'): Promise<FullProgressResponse> => {
    const response = await axios.get<FullProgressResponse>(`${API_BASE_URL}/progress/${playerId}`, {
      params: { course_id: courseId }
    });
    return response.data;
  },

  /**
   * Get progress for a specific module
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getModuleProgress: async (playerId: number, moduleNumber: number, courseId: string = 'master-ia'): Promise<Progress[]> => {
    const response = await axios.get<Progress[]>(
      `${API_BASE_URL}/progress/${playerId}/module/${moduleNumber}`,
      {
        params: { course_id: courseId }
      }
    );
    return response.data;
  },

  /**
   * Update progress status
   */
  updateProgress: async (progressId: number, data: ProgressUpdate): Promise<Progress> => {
    const response = await axios.patch<Progress>(`${API_BASE_URL}/progress/${progressId}`, data);
    return response.data;
  },

  /**
   * Get next unlockable class
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getNextUnlockable: async (playerId: number, courseId: string = 'master-ia'): Promise<NextUnlockableClass | null> => {
    const response = await axios.get<NextUnlockableClass | null>(
      `${API_BASE_URL}/progress/${playerId}/next-unlockable`,
      {
        params: { course_id: courseId }
      }
    );
    return response.data;
  },

  /**
   * Get all modules info
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getAllModules: async (courseId: string = 'master-ia'): Promise<ModuleInfo[]> => {
    const response = await axios.get<ModuleInfo[]>(`${API_BASE_URL}/progress/modules`, {
      params: { course_id: courseId }
    });
    return response.data;
  },

  /**
   * Get specific module info
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getModuleInfo: async (moduleNumber: number, courseId: string = 'master-ia'): Promise<ModuleInfo> => {
    const response = await axios.get<ModuleInfo>(`${API_BASE_URL}/progress/modules/${moduleNumber}`, {
      params: { course_id: courseId }
    });
    return response.data;
  },
};

// ============================================
// ACHIEVEMENT API
// ============================================

export const achievementApi = {
  /**
   * Get all available achievements
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getAllAchievements: async (courseId: string = 'master-ia'): Promise<AllAchievementsResponse> => {
    const response = await axios.get<AllAchievementsResponse>(`${API_BASE_URL}/achievements/`, {
      params: { course_id: courseId }
    });
    return response.data;
  },

  /**
   * Get player's unlocked achievements
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  getPlayerAchievements: async (playerId: number, courseId: string = 'master-ia'): Promise<PlayerAchievementsResponse> => {
    const response = await axios.get<PlayerAchievementsResponse>(
      `${API_BASE_URL}/achievements/player/${playerId}`,
      {
        params: { course_id: courseId }
      }
    );
    return response.data;
  },

  /**
   * Manually unlock an achievement (for testing)
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  unlockAchievement: async (playerId: number, achievementId: string, courseId: string = 'master-ia'): Promise<AchievementWithDetails> => {
    const response = await axios.post<AchievementWithDetails>(
      `${API_BASE_URL}/achievements/unlock`,
      { player_id: playerId, achievement_id: achievementId },
      {
        params: { course_id: courseId }
      }
    );
    return response.data;
  },

  /**
   * Check and auto-unlock achievements after an action
   * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
   */
  checkAchievements: async (data: CheckAchievementsRequest, courseId: string = 'master-ia'): Promise<CheckAchievementsResponse> => {
    const response = await axios.post<CheckAchievementsResponse>(
      `${API_BASE_URL}/achievements/check`,
      data,
      {
        params: { course_id: courseId }
      }
    );
    return response.data;
  },
};

// ============================================
// COMBINED HELPER FUNCTIONS
// ============================================

/**
 * Complete a class and check for achievements
 * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
 */
export const completeClass = async (
  playerId: number,
  progressId: number,
  moduleNumber: number,
  classNumber: number,
  courseId: string = 'master-ia'
): Promise<{
  progress: Progress;
  achievements: AchievementWithDetails[];
  xpEarned: number;
}> => {
  // Update progress to completed
  const progress = await progressApi.updateProgress(progressId, { status: 'completed' });

  // Check for achievements
  const achievementResult = await achievementApi.checkAchievements({
    player_id: playerId,
    action_type: 'complete_class',
    action_data: { module_number: moduleNumber, class_number: classNumber },
  }, courseId);

  return {
    progress,
    achievements: achievementResult.achievements_unlocked,
    xpEarned: achievementResult.xp_earned,
  };
};

/**
 * Initialize a new player with first class unlocked
 * NFLOW-2: Added courseId parameter (defaults to 'master-ia')
 */
export const initializePlayer = async (username: string, avatar: string = 'default.png', courseId: string = 'master-ia'): Promise<{
  player: Player;
  stats: PlayerStats;
  firstClass: Progress;
}> => {
  // Create player
  const player = await playerApi.createPlayer({ username, avatar });

  // Get stats (auto-created by backend)
  const stats = await playerApi.getPlayerStats(player.id);

  // Unlock first class (Module 0, Class 0)
  const firstClass = await progressApi.createProgress({
    player_id: player.id,
    module_number: 0,
    class_number: 0,
    status: 'unlocked',
  }, courseId);

  return { player, stats, firstClass };
};
