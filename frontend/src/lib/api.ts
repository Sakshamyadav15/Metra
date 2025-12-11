import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// LTP API
export const ltpApi = {
  // Profile
  createProfile: (userId: string) => api.post(`/ltp/profiles/${userId}`),
  getProfile: (userId: string) => api.get(`/ltp/profiles/user/${userId}`),
  updateProfile: (profileId: string, data: any) => api.patch(`/ltp/profiles/${profileId}`, data),
  
  // Concepts
  getConcepts: (subject?: string) => api.get('/ltp/concepts', { params: { subject } }),
  createConcept: (data: any) => api.post('/ltp/concepts', data),
  
  // Masteries
  getMasteries: (profileId: string) => api.get(`/ltp/profiles/${profileId}/masteries`),
  updateMastery: (profileId: string, conceptId: string, data: any) => 
    api.post(`/ltp/profiles/${profileId}/masteries/${conceptId}`, data),
  getDueForReview: (profileId: string) => api.get(`/ltp/profiles/${profileId}/due-for-review`),
  
  // Misconceptions
  getMisconceptions: (profileId: string) => api.get(`/ltp/profiles/${profileId}/misconceptions`),
  createMisconception: (profileId: string, data: any) => 
    api.post(`/ltp/profiles/${profileId}/misconceptions`, data),
  resolveMisconception: (misconceptionId: string, data: any) => 
    api.patch(`/misconceptions/${misconceptionId}`, data),
  
  // Sessions
  startSession: (profileId: string, data: any) => api.post(`/ltp/profiles/${profileId}/sessions`, data),
  endSession: (sessionId: string, data: any) => api.patch(`/ltp/sessions/${sessionId}`, data),
  
  // Analytics
  getAnalytics: (profileId: string) => api.get(`/ltp/profiles/${profileId}/analytics`),
  getKnowledgeGraph: (profileId: string) => api.get(`/ltp/profiles/${profileId}/knowledge-graph`),
  
  // Modality
  getPreferredModality: (profileId: string) => api.get(`/ltp/profiles/${profileId}/preferred-modality`),
  updateModalityFeedback: (profileId: string, modality: string, success: boolean) =>
    api.post(`/ltp/profiles/${profileId}/modality-feedback`, null, { params: { modality, success } }),
};

// Dual RAG API
export const ragApi = {
  // Query
  query: (data: {
    profile_id: string;
    query: string;
    session_id?: string;
    concept_id?: string;
    subject?: string;
    topic?: string;
  }) => api.post('/rag/query', data),
  
  // Explain
  explain: (data: {
    profile_id: string;
    concept_id: string;
    question?: string;
    preferred_modality?: string;
  }) => api.post('/rag/explain', data),
  
  // Student Contexts
  addStudentContext: (profileId: string, data: any) => api.post(`/rag/contexts/${profileId}`, data),
  getStudentContexts: (profileId: string) => api.get(`/rag/contexts/${profileId}`),
  
  // Academic Documents
  addDocument: (data: any) => api.post('/rag/documents', data),
  addDocumentsBulk: (documents: any[]) => api.post('/rag/documents/bulk', { documents }),
  getDocuments: (subject?: string, topic?: string) => 
    api.get('/rag/documents', { params: { subject, topic } }),
  
  // Gaps
  getGaps: (profileId: string) => api.get(`/rag/gaps/${profileId}`),
  resolveGap: (gapId: string, resolution: string) => 
    api.post(`/rag/gaps/${gapId}/resolve`, { resolution_strategy: resolution }),
  
  // Search
  search: (query: string, source?: string, subject?: string, topic?: string) =>
    api.post('/rag/search', { query, source, subject, topic }),
  
  // Chat
  getChatHistory: (profileId: string, sessionId?: string) =>
    api.get(`/rag/chat/${profileId}`, { params: { session_id: sessionId } }),
  submitFeedback: (messageId: string, wasHelpful: boolean) =>
    api.post('/rag/chat/feedback', { message_id: messageId, was_helpful: wasHelpful }),
  
  // Stats
  getStats: () => api.get('/rag/stats'),
};

// Micro Lessons API (Mock)
export const lessonsApi = {
  getLessons: (conceptId?: string) => api.get('/lessons', { params: { concept_id: conceptId } }),
  getLesson: (lessonId: string) => api.get(`/lessons/${lessonId}`),
  generateLesson: (data: {
    profile_id: string;
    concept_id: string;
    preferred_modality?: string;
    include_analogies?: boolean;
    include_quiz?: boolean;
  }) => api.post('/lessons/generate', data),
  getDailyFeed: (profileId: string) => api.get(`/lessons/feed/${profileId}`),
  updateProgress: (profileId: string, lessonId: string, data: any) =>
    api.post(`/lessons/progress/${profileId}/${lessonId}`, data),
  getProgress: (profileId: string) => api.get(`/lessons/progress/${profileId}`),
};

export default api;
