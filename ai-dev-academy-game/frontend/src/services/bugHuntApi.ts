/**
 * Bug Hunt API service
 * Handles all API calls for Bug Hunt mini-game
 */
import { apiClient } from './api';
import type {
  BugHuntStartRequest,
  BugHuntStartResponse,
  BugHuntSubmitRequest,
  BugHuntSubmitResponse,
  LeaderboardResponse,
  PlayerBugHuntStatsResponse,
  Difficulty,
} from '../types/bugHunt';

const BASE_PATH = '/api/minigames/bug-hunt';

export const bugHuntApi = {
  /**
   * Start a new Bug Hunt game session
   */
  async startGame(
    playerId: number,
    difficulty?: Difficulty
  ): Promise<BugHuntStartResponse> {
    const request: BugHuntStartRequest = {
      player_id: playerId,
      difficulty,
    };

    const response = await apiClient.post<BugHuntStartResponse>(
      `${BASE_PATH}/start`,
      request
    );
    return response.data;
  },

  /**
   * Submit Bug Hunt answers and get results
   */
  async submitGame(
    sessionId: number,
    playerId: number,
    foundBugLines: number[],
    timeSeconds: number
  ): Promise<BugHuntSubmitResponse> {
    const request: BugHuntSubmitRequest = {
      session_id: sessionId,
      player_id: playerId,
      found_bug_lines: foundBugLines,
      time_seconds: timeSeconds,
    };

    const response = await apiClient.post<BugHuntSubmitResponse>(
      `${BASE_PATH}/submit`,
      request
    );
    return response.data;
  },

  /**
   * Get Bug Hunt leaderboard
   */
  async getLeaderboard(
    difficulty?: Difficulty,
    limit: number = 10
  ): Promise<LeaderboardResponse> {
    const params = new URLSearchParams();
    if (difficulty) params.append('difficulty', difficulty);
    params.append('limit', limit.toString());

    const response = await apiClient.get<LeaderboardResponse>(
      `${BASE_PATH}/leaderboard?${params.toString()}`
    );
    return response.data;
  },

  /**
   * Get player's Bug Hunt statistics
   */
  async getPlayerStats(
    playerId: number
  ): Promise<PlayerBugHuntStatsResponse> {
    const response = await apiClient.get<PlayerBugHuntStatsResponse>(
      `${BASE_PATH}/stats/${playerId}`
    );
    return response.data;
  },
};
