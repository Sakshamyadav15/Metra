const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Unknown error" }));
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    return response.json();
  }

  // LTP Module (3.1) - Learning Twin Profile
  ltp = {
    getProfile: (userId: string) =>
      this.request<LearningTwinProfile>(`/api/ltp/profile/${userId}`),
    
    createProfile: (userId: string, data: CreateProfileData) =>
      this.request<LearningTwinProfile>(`/api/ltp/profile/${userId}`, {
        method: "POST",
        body: JSON.stringify(data),
      }),

    getConcepts: (userId: string) =>
      this.request<ConceptMastery[]>(`/api/ltp/profile/${userId}/concepts`),

    updateMastery: (userId: string, conceptId: string, data: UpdateMasteryData) =>
      this.request<ConceptMastery>(
        `/api/ltp/profile/${userId}/concepts/${conceptId}/mastery`,
        {
          method: "PUT",
          body: JSON.stringify(data),
        }
      ),

    getMisconceptions: (userId: string) =>
      this.request<Misconception[]>(`/api/ltp/profile/${userId}/misconceptions`),

    getReviewSchedule: (userId: string) =>
      this.request<ReviewSchedule>(`/api/ltp/profile/${userId}/review-schedule`),

    recordSession: (userId: string, data: SessionData) =>
      this.request<LearningSession>(`/api/ltp/profile/${userId}/sessions`, {
        method: "POST",
        body: JSON.stringify(data),
      }),
  };

  // Dual RAG Module (3.2) - Personalized Reasoning
  dualRag = {
    chat: (userId: string, message: string) =>
      this.request<ChatResponse>(`/api/dual-rag/chat`, {
        method: "POST",
        body: JSON.stringify({ user_id: userId, message }),
      }),

    getGaps: (userId: string) =>
      this.request<GapAnalysis[]>(`/api/dual-rag/gaps/${userId}`),

    analyzeGaps: (userId: string) =>
      this.request<GapAnalysis>(`/api/dual-rag/analyze-gaps/${userId}`, {
        method: "POST",
      }),

    addDocument: (data: AddDocumentData) =>
      this.request<AcademicDocument>(`/api/dual-rag/documents`, {
        method: "POST",
        body: JSON.stringify(data),
      }),

    searchDocuments: (query: string, topK?: number) =>
      this.request<SearchResult[]>(
        `/api/dual-rag/documents/search?query=${encodeURIComponent(query)}${topK ? `&top_k=${topK}` : ""}`
      ),
  };

  // Micro Lessons Module (3.3) - Mock for now
  microLessons = {
    getLessons: (userId: string) =>
      this.request<MicroLesson[]>(`/api/micro-lessons/${userId}`),

    getLesson: (lessonId: string) =>
      this.request<MicroLesson>(`/api/micro-lessons/lesson/${lessonId}`),

    generateLesson: (userId: string, conceptId: string) =>
      this.request<MicroLesson>(`/api/micro-lessons/generate`, {
        method: "POST",
        body: JSON.stringify({ user_id: userId, concept_id: conceptId }),
      }),
  };
}

// Types
interface LearningTwinProfile {
  id: string;
  user_id: string;
  overall_mastery: number;
  learning_velocity: number;
  cognitive_state: string;
  total_learning_time: number;
  created_at: string;
  updated_at: string;
}

interface CreateProfileData {
  preferred_learning_style?: string;
  goals?: string[];
}

interface ConceptMastery {
  id: string;
  concept_id: string;
  concept_name: string;
  mastery_level: number;
  ease_factor: number;
  review_interval: number;
  last_reviewed: string;
  next_review: string;
  repetitions: number;
}

interface UpdateMasteryData {
  quality: number; // 0-5 rating
  time_spent?: number;
}

interface Misconception {
  id: string;
  concept_id: string;
  description: string;
  severity: string;
  identified_at: string;
  resolved: boolean;
}

interface ReviewSchedule {
  due_today: ConceptMastery[];
  upcoming: ConceptMastery[];
}

interface SessionData {
  concept_id: string;
  duration_minutes: number;
  quality_rating: number;
  notes?: string;
}

interface LearningSession {
  id: string;
  concept_id: string;
  started_at: string;
  ended_at: string;
  duration_minutes: number;
  quality_rating: number;
}

interface ChatResponse {
  response: string;
  sources: {
    student_context: string[];
    academic_sources: string[];
  };
  gaps_identified: string[];
}

interface GapAnalysis {
  id: string;
  concept: string;
  gap_type: string;
  severity: number;
  recommendation: string;
  created_at: string;
}

interface AddDocumentData {
  title: string;
  content: string;
  subject: string;
  source?: string;
}

interface AcademicDocument {
  id: string;
  title: string;
  subject: string;
  created_at: string;
}

interface SearchResult {
  id: string;
  title: string;
  content: string;
  relevance_score: number;
}

interface MicroLesson {
  id: string;
  title: string;
  concept_id: string;
  content_type: string;
  content: string;
  duration_minutes: number;
  difficulty: string;
}

export const api = new ApiClient(API_BASE_URL);
export type { 
  LearningTwinProfile, 
  ConceptMastery, 
  Misconception,
  ChatResponse,
  GapAnalysis,
  MicroLesson 
};
