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
   */
  createProgress: async (data: ProgressCreate): Promise<Progress> => {
    const response = await axios.post<Progress>(`${API_BASE_URL}/progress/`, data);
    return response.data;
  },

  /**
   * Get full progress for a player
   */
  getFullProgress: async (playerId: number): Promise<FullProgressResponse> => {
    const response = await axios.get<FullProgressResponse>(`${API_BASE_URL}/progress/${playerId}`);
    return response.data;
  },

  /**
   * Get progress for a specific module
   */
  getModuleProgress: async (playerId: number, moduleNumber: number): Promise<Progress[]> => {
    const response = await axios.get<Progress[]>(
      `${API_BASE_URL}/progress/${playerId}/module/${moduleNumber}`
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
   */
  getNextUnlockable: async (playerId: number): Promise<NextUnlockableClass | null> => {
    const response = await axios.get<NextUnlockableClass | null>(
      `${API_BASE_URL}/progress/${playerId}/next-unlockable`
    );
    return response.data;
  },

  /**
   * Get all modules info
   */
  getAllModules: async (): Promise<ModuleInfo[]> => {
    const response = await axios.get<ModuleInfo[]>(`${API_BASE_URL}/progress/modules`);
    return response.data;
  },

  /**
   * Get specific module info
   */
  getModuleInfo: async (moduleNumber: number): Promise<ModuleInfo> => {
    const response = await axios.get<ModuleInfo>(`${API_BASE_URL}/progress/modules/${moduleNumber}`);
    return response.data;
  },
};

// ============================================
// ACHIEVEMENT API
// ============================================

export const achievementApi = {
  /**
   * Get all available achievements
   */
  getAllAchievements: async (): Promise<AllAchievementsResponse> => {
    const response = await axios.get<AllAchievementsResponse>(`${API_BASE_URL}/achievements/`);
    return response.data;
  },

  /**
   * Get player's unlocked achievements
   */
  getPlayerAchievements: async (playerId: number): Promise<PlayerAchievementsResponse> => {
    const response = await axios.get<PlayerAchievementsResponse>(
      `${API_BASE_URL}/achievements/player/${playerId}`
    );
    return response.data;
  },

  /**
   * Manually unlock an achievement (for testing)
   */
  unlockAchievement: async (playerId: number, achievementId: string): Promise<AchievementWithDetails> => {
    const response = await axios.post<AchievementWithDetails>(
      `${API_BASE_URL}/achievements/unlock`,
      { player_id: playerId, achievement_id: achievementId }
    );
    return response.data;
  },

  /**
   * Check and auto-unlock achievements after an action
   */
  checkAchievements: async (data: CheckAchievementsRequest): Promise<CheckAchievementsResponse> => {
    const response = await axios.post<CheckAchievementsResponse>(
      `${API_BASE_URL}/achievements/check`,
      data
    );
    return response.data;
  },
};

// ============================================
// COMBINED HELPER FUNCTIONS
// ============================================

/**
 * Complete a class and check for achievements
 */
export const completeClass = async (
  playerId: number,
  progressId: number,
  moduleNumber: number,
  classNumber: number
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
  });

  return {
    progress,
    achievements: achievementResult.achievements_unlocked,
    xpEarned: achievementResult.xp_earned,
  };
};

/**
 * Initialize a new player with first class unlocked
 */
export const initializePlayer = async (username: string, avatar: string = 'default.png'): Promise<{
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
  });

  return { player, stats, firstClass };
};
