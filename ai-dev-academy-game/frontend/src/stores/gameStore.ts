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
  ClassInfo,
} from '../types/game';
import { playerApi, progressApi, achievementApi, completeClass } from '../services/gameApi';

interface GameState {
  // Current player
  player: Player | null;
  playerStats: PlayerStats | null;

  // Course context (NFLOW-2)
  courseId: string;

  // Progress data
  fullProgress: FullProgressResponse | null;
  currentModule: ModuleInfo | null;
  allModules: ModuleInfo[];

  // Class viewer state
  currentClassContent: ClassInfo | null;
  exercisesCompleted: Set<string>;

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
  setCourseId: (courseId: string) => void;
  setPlayer: (player: Player) => void;
  setPlayerStats: (stats: PlayerStats) => void;
  loadPlayer: (playerId: number) => Promise<void>;
  loadFullProgress: (playerId: number) => Promise<void>;
  loadPlayerAchievements: (playerId: number) => Promise<void>;
  loadAllModules: () => Promise<void>;
  setCurrentView: (view: ViewMode) => void;
  selectModule: (moduleNumber: number) => Promise<void>;
  selectClass: (moduleNumber: number, classNumber: number) => void;
  loadClassContent: (moduleNumber: number, classNumber: number) => Promise<void>;
  toggleExerciseComplete: (exerciseId: string) => void;
  completeCurrentClass: () => Promise<void>;
  addNotification: (notification: Omit<NotificationMessage, 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
  setError: (error: string | null) => void;
  reset: () => void;
}

const initialState = {
  player: null,
  playerStats: null,
  courseId: 'master-ia', // NFLOW-2: Default course
  fullProgress: null,
  currentModule: null,
  allModules: [],
  currentClassContent: null,
  exercisesCompleted: new Set<string>(),
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

      setCourseId: (courseId) => set({ courseId }),

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
          const { courseId } = get(); // NFLOW-2: Get current courseId from store
          const fullProgress = await progressApi.getFullProgress(playerId, courseId);
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
          const { courseId } = get(); // NFLOW-2: Get current courseId from store
          const response = await achievementApi.getPlayerAchievements(playerId, courseId);
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
          const { courseId } = get(); // NFLOW-2: Get current courseId from store
          const allModules = await progressApi.getAllModules(courseId);
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
          const { courseId } = get(); // NFLOW-2: Get current courseId from store
          const currentModule = await progressApi.getModuleInfo(moduleNumber, courseId);
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

      loadClassContent: async (moduleNumber: number, classNumber: number) => {
        set({ isLoading: true, error: null });
        try {
          // Load or refresh module info if needed
          const state = get();
          let currentModule = state.currentModule;
          const { courseId } = state; // NFLOW-2: Get current courseId from store

          if (!currentModule || currentModule.module_number !== moduleNumber) {
            currentModule = await progressApi.getModuleInfo(moduleNumber, courseId);
            set({ currentModule });
          }

          const classInfo = currentModule?.classes.find(
            (c) => c.class_number === classNumber
          );

          set({
            currentClassContent: classInfo || null,
            exercisesCompleted: new Set(),
            isLoading: false
          });
        } catch (error) {
          console.error('Failed to load class content:', error);
          set({ error: 'Failed to load class content', isLoading: false });
          throw error;
        }
      },

      toggleExerciseComplete: (exerciseId: string) => {
        set((state) => {
          const newSet = new Set(state.exercisesCompleted);
          if (newSet.has(exerciseId)) {
            newSet.delete(exerciseId);
          } else {
            newSet.add(exerciseId);
          }
          return { exercisesCompleted: newSet };
        });
      },

      completeCurrentClass: async () => {
        const state = get();
        const { player, fullProgress, selectedModuleNumber, selectedClassNumber, courseId } = state;

        if (!player || selectedModuleNumber === null || selectedClassNumber === null || !fullProgress) {
          throw new Error('Invalid state for completing class');
        }

        set({ isLoading: true, error: null });

        try {
          // Find the progress record for this class
          const moduleProgress = fullProgress.modules.find(
            (m) => m.module_number === selectedModuleNumber
          );
          const classProgress = moduleProgress?.classes.find(
            (p) => p.class_number === selectedClassNumber
          );

          if (!classProgress) {
            throw new Error('Class progress not found');
          }

          // Complete the class and check achievements (NFLOW-2: pass courseId)
          const result = await completeClass(
            player.id,
            classProgress.id,
            selectedModuleNumber,
            selectedClassNumber,
            courseId
          );

          // Update player XP
          const updatedPlayer = await playerApi.getPlayer(player.id);
          set({ player: updatedPlayer });

          // Refresh progress
          await get().loadFullProgress(player.id);

          // Show notifications for XP and achievements
          get().addNotification({
            type: 'success',
            message: `Class completed! +${result.xpEarned} XP earned`,
          });

          if (result.achievements.length > 0) {
            result.achievements.forEach((achievement) => {
              get().addNotification({
                type: 'achievement',
                message: `Achievement unlocked: ${achievement.title}`,
                achievement,
              });
            });

            // Refresh achievements list
            await get().loadPlayerAchievements(player.id);
          }

          set({ isLoading: false });
        } catch (error) {
          console.error('Failed to complete class:', error);
          set({ error: 'Failed to complete class', isLoading: false });
          get().addNotification({
            type: 'error',
            message: 'Failed to complete class. Please try again.',
          });
          throw error;
        }
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
