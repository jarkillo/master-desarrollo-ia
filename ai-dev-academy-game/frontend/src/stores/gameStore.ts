/**
 * Zustand store for AI Dev Academy Game state management
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  Player,
  PlayerStats,
  FullProgressResponse,
  AchievementWithDetails,
  ViewMode,
  NotificationMessage,
  ModuleInfo,
} from '../types/game';
import { playerApi, progressApi, achievementApi } from '../services/gameApi';

interface GameState {
  // Current player
  player: Player | null;
  playerStats: PlayerStats | null;

  // Progress data
  fullProgress: FullProgressResponse | null;
  currentModule: ModuleInfo | null;
  allModules: ModuleInfo[];

  // Achievements
  unlockedAchievements: AchievementWithDetails[];

  // UI state
  currentView: ViewMode;
  selectedModuleNumber: number | null;
  selectedClassNumber: number | null;
  notifications: NotificationMessage[];

  // Loading states
  isLoading: boolean;
  error: string | null;

  // Actions
  setPlayer: (player: Player) => void;
  setPlayerStats: (stats: PlayerStats) => void;
  loadPlayer: (playerId: number) => Promise<void>;
  loadFullProgress: (playerId: number) => Promise<void>;
  loadPlayerAchievements: (playerId: number) => Promise<void>;
  loadAllModules: () => Promise<void>;
  setCurrentView: (view: ViewMode) => void;
  selectModule: (moduleNumber: number) => Promise<void>;
  selectClass: (moduleNumber: number, classNumber: number) => void;
  addNotification: (notification: Omit<NotificationMessage, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  player: null,
  playerStats: null,
  fullProgress: null,
  currentModule: null,
  allModules: [],
  unlockedAchievements: [],
  currentView: 'dashboard' as ViewMode,
  selectedModuleNumber: null,
  selectedClassNumber: null,
  notifications: [],
  isLoading: false,
  error: null,
};

export const useGameStore = create<GameState>()(
  persist(
    (set, get) => ({
      ...initialState,

      setPlayer: (player) => set({ player }),

      setPlayerStats: (playerStats) => set({ playerStats }),

      loadPlayer: async (playerId: number) => {
        set({ isLoading: true, error: null });
        try {
          const [player, playerStats] = await Promise.all([
            playerApi.getPlayer(playerId),
            playerApi.getPlayerStats(playerId),
          ]);
          set({ player, playerStats, isLoading: false });
        } catch (error) {
          console.error('Failed to load player:', error);
          set({ error: 'Failed to load player data', isLoading: false });
          throw error;
        }
      },

      loadFullProgress: async (playerId: number) => {
        set({ isLoading: true, error: null });
        try {
          const fullProgress = await progressApi.getFullProgress(playerId);
          set({ fullProgress, isLoading: false });
        } catch (error) {
          console.error('Failed to load progress:', error);
          set({ error: 'Failed to load progress data', isLoading: false });
          throw error;
        }
      },

      loadPlayerAchievements: async (playerId: number) => {
        set({ isLoading: true, error: null });
        try {
          const response = await achievementApi.getPlayerAchievements(playerId);
          set({
            unlockedAchievements: response.achievements,
            isLoading: false
          });
        } catch (error) {
          console.error('Failed to load achievements:', error);
          set({ error: 'Failed to load achievements', isLoading: false });
          throw error;
        }
      },

      loadAllModules: async () => {
        set({ isLoading: true, error: null });
        try {
          const allModules = await progressApi.getAllModules();
          set({ allModules, isLoading: false });
        } catch (error) {
          console.error('Failed to load modules:', error);
          set({ error: 'Failed to load modules', isLoading: false });
          throw error;
        }
      },

      setCurrentView: (currentView) => set({ currentView }),

      selectModule: async (moduleNumber: number) => {
        set({ isLoading: true, error: null });
        try {
          const currentModule = await progressApi.getModuleInfo(moduleNumber);
          set({
            currentModule,
            selectedModuleNumber: moduleNumber,
            selectedClassNumber: null,
            currentView: 'module',
            isLoading: false
          });
        } catch (error) {
          console.error('Failed to load module:', error);
          set({ error: 'Failed to load module', isLoading: false });
          throw error;
        }
      },

      selectClass: (moduleNumber, classNumber) => {
        set({
          selectedModuleNumber: moduleNumber,
          selectedClassNumber: classNumber,
          currentView: 'class'
        });
      },

      addNotification: (notification) => {
        const id = `notif-${Date.now()}-${Math.random()}`;
        const newNotification: NotificationMessage = {
          ...notification,
          id,
          timestamp: Date.now(),
        };

        set((state) => ({
          notifications: [...state.notifications, newNotification],
        }));

        // Auto-remove after 5 seconds
        setTimeout(() => {
          get().removeNotification(id);
        }, 5000);
      },

      removeNotification: (id) => {
        set((state) => ({
          notifications: state.notifications.filter((n) => n.id !== id),
        }));
      },

      clearNotifications: () => set({ notifications: [] }),

      setError: (error) => set({ error }),

      reset: () => set(initialState),
    }),
    {
      name: 'game-storage',
      partialize: (state) => ({
        player: state.player,
        selectedModuleNumber: state.selectedModuleNumber,
        selectedClassNumber: state.selectedClassNumber,
      }),
    }
  )
);
