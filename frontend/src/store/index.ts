import { create } from 'zustand';

// User Store
interface UserState {
  userId: string | null;
  profileId: string | null;
  profile: any | null;
  setUser: (userId: string, profileId: string) => void;
  setProfile: (profile: any) => void;
  logout: () => void;
}

export const useUserStore = create<UserState>((set) => ({
  userId: 'demo-user-001', // Default demo user
  profileId: null,
  profile: null,
  setUser: (userId, profileId) => set({ userId, profileId }),
  setProfile: (profile) => set({ profile, profileId: profile?.id }),
  logout: () => set({ userId: null, profileId: null, profile: null }),
}));

// Chat Store
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: any[];
  timestamp: Date;
}

interface ChatState {
  messages: Message[];
  sessionId: string | null;
  isLoading: boolean;
  addMessage: (message: Message) => void;
  setMessages: (messages: Message[]) => void;
  setSessionId: (sessionId: string) => void;
  setLoading: (loading: boolean) => void;
  clearChat: () => void;
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  sessionId: null,
  isLoading: false,
  addMessage: (message) => set((state) => ({ messages: [...state.messages, message] })),
  setMessages: (messages) => set({ messages }),
  setSessionId: (sessionId) => set({ sessionId }),
  setLoading: (isLoading) => set({ isLoading }),
  clearChat: () => set({ messages: [], sessionId: null }),
}));

// Learning Store
interface LearningState {
  currentConcept: any | null;
  currentLesson: any | null;
  analytics: any | null;
  setCurrentConcept: (concept: any) => void;
  setCurrentLesson: (lesson: any) => void;
  setAnalytics: (analytics: any) => void;
}

export const useLearningStore = create<LearningState>((set) => ({
  currentConcept: null,
  currentLesson: null,
  analytics: null,
  setCurrentConcept: (concept) => set({ currentConcept: concept }),
  setCurrentLesson: (lesson) => set({ currentLesson: lesson }),
  setAnalytics: (analytics) => set({ analytics }),
}));
