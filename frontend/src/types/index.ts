// ============ LTP Types ============

export interface LearningTwinProfile {
  id: string;
  user_id: string;
  overall_mastery_score: number;
  learning_velocity: number;
  retention_rate: number;
  modality_preferences: Record<string, number>;
  avg_speech_confidence: number;
  avg_articulation_score: number;
  total_study_time_minutes: number;
  total_concepts_attempted: number;
  total_concepts_mastered: number;
  current_streak_days: number;
  longest_streak_days: number;
  created_at: string;
  updated_at: string;
  last_activity_at: string | null;
}

export interface Concept {
  id: string;
  name: string;
  description: string | null;
  subject: string;
  topic: string;
  subtopic: string | null;
  difficulty_level: number;
  prerequisite_ids: string[];
  tags: string[];
  estimated_time_minutes: number;
  created_at: string;
}

export interface ConceptMastery {
  id: string;
  profile_id: string;
  concept_id: string;
  mastery_level: 'not_started' | 'learning' | 'partial' | 'mastered' | 'expert';
  mastery_score: number;
  confidence_score: number;
  attempts_count: number;
  correct_count: number;
  time_spent_minutes: number;
  next_review_at: string | null;
  review_interval_days: number;
  first_seen_at: string;
  last_practiced_at: string | null;
  mastered_at: string | null;
  concept?: Concept;
}

export interface Misconception {
  id: string;
  profile_id: string;
  concept_id: string | null;
  misconception_type: string;
  description: string;
  student_response: string;
  correct_understanding: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  is_resolved: boolean;
  resolution_notes: string | null;
  detected_at: string;
  resolved_at: string | null;
  detection_source: string;
}

export interface LearningSession {
  id: string;
  profile_id: string;
  session_type: string;
  duration_minutes: number;
  concepts_covered: string[];
  questions_attempted: number;
  questions_correct: number;
  focus_score: number | null;
  started_at: string;
  ended_at: string | null;
}

export interface LTPAnalytics {
  profile_id: string;
  overall_progress: number;
  concepts_by_mastery: Record<string, number>;
  subjects_progress: Record<string, number>;
  learning_velocity_trend: number[];
  top_strengths: string[];
  areas_for_improvement: string[];
  recommended_next_concepts: string[];
  study_time_weekly: number[];
  streak_info: {
    current: number;
    longest: number;
  };
}

export interface KnowledgeGraphNode {
  id: string;
  name: string;
  mastery_level: string;
  mastery_score: number;
  subject: string;
  topic: string;
}

export interface KnowledgeGraphEdge {
  source: string;
  target: string;
  relationship: string;
}

// ============ Dual RAG Types ============

export interface StudentContext {
  id: string;
  profile_id: string;
  context_type: 'question' | 'explanation' | 'chat' | 'assessment';
  content: string;
  concept_id: string | null;
  concept_name: string | null;
  subject: string | null;
  topic: string | null;
  tags: string[];
  was_correct: boolean | null;
  confidence_score: number | null;
  embedding_id: string | null;
  created_at: string;
}

export interface AcademicDocument {
  id: string;
  title: string;
  source_type: 'textbook' | 'lecture' | 'pdf' | 'curriculum';
  source_name: string;
  content: string;
  subject: string;
  topic: string;
  subtopic: string | null;
  grade_level: string | null;
  tags: string[];
  difficulty_level: number;
  chunk_index: number;
  total_chunks: number;
  embedding_id: string | null;
  is_verified: boolean;
  quality_score: number;
  created_at: string;
  updated_at: string;
}

export interface RetrievedContext {
  id: string;
  source: 'student' | 'academic';
  content: string;
  relevance_score: number;
  metadata: Record<string, any>;
}

export interface DualRAGResponse {
  answer: string;
  student_contexts: RetrievedContext[];
  academic_contexts: RetrievedContext[];
  gaps_detected: GapAnalysis[];
  confidence_score: number;
  modality_used: string;
  sources_cited: string[];
}

export interface GapAnalysis {
  id: string;
  profile_id: string;
  concept_id: string | null;
  concept_name: string;
  student_understanding: string;
  correct_understanding: string;
  gap_description: string;
  gap_severity: 'minor' | 'moderate' | 'significant' | 'critical';
  priority_score: number;
  is_resolved: boolean;
  resolution_strategy: string | null;
  student_context_ids: string[];
  academic_doc_ids: string[];
  detected_at: string;
  resolved_at: string | null;
}

// ============ Micro Lessons Types ============

export interface SlideContent {
  slide_number: number;
  title: string;
  content: string;
  visual_description: string | null;
  narration: string | null;
}

export interface QuizQuestion {
  question: string;
  options: string[];
  correct_index: number;
  explanation: string;
}

export interface MicroLesson {
  id: string;
  concept_id: string;
  title: string;
  description: string | null;
  slides: SlideContent[];
  narration_script: string | null;
  video_url: string | null;
  thumbnail_url: string | null;
  difficulty_level: number;
  duration_minutes: number;
  modality: string;
  analogy_style: string | null;
  quiz_questions: QuizQuestion[];
  is_generated: boolean;
  generation_status: string;
  created_at: string;
  updated_at: string;
}

export interface LessonProgress {
  id: string;
  profile_id: string;
  lesson_id: string;
  is_completed: boolean;
  progress_percentage: number;
  time_spent_seconds: number;
  quiz_score: number | null;
  quiz_attempts: number;
  started_at: string;
  completed_at: string | null;
}

export interface DailyLessonFeed {
  profile_id: string;
  date: string;
  recommended_lessons: MicroLesson[];
  review_lessons: MicroLesson[];
  total_estimated_time: number;
}

// ============ Chat Types ============

export interface ChatMessage {
  id: string;
  profile_id: string;
  session_id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  student_context_ids: string[];
  academic_doc_ids: string[];
  concept_id: string | null;
  was_helpful: boolean | null;
  created_at: string;
}
