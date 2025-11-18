// User types
export interface User {
  id: string
  email: string
  full_name: string
  target_mcat_score?: number
  target_exam_date?: string
  subscription_tier: string
  created_at: string
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData {
  email: string
  password: string
  full_name: string
  target_mcat_score?: number
  target_exam_date?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

// Question types
export interface Question {
  id: string
  question_type: 'passage_based' | 'standalone'
  mcat_section: 'CPBS' | 'CARS' | 'BBLS' | 'PSBB'
  passage_id?: string
  question_text: string
  question_images?: string[]
  options: {
    A: string
    B: string
    C: string
    D: string
  }
  difficulty_level?: number
  tags?: string[]
  estimated_time_seconds: number
}

export interface QuestionWithAnswer extends Question {
  correct_answer: 'A' | 'B' | 'C' | 'D'
  correct_explanation: string
  incorrect_explanations?: Record<string, string>
}

export interface QuestionAttempt {
  question_id: string
  selected_answer: 'A' | 'B' | 'C' | 'D' | 'X'
  time_spent_seconds: number
  is_flagged: boolean
  confidence_level?: number
  test_attempt_id?: string
  attempt_mode: 'timed' | 'untimed' | 'review'
}

// Study types
export interface StudyModule {
  id: number
  title: string
  mcat_section: string
  topic_id?: number
  content_type: 'text' | 'video' | 'flashcard' | 'equation_sheet'
  content: Record<string, any>
  order_index?: number
  estimated_time_minutes?: number
  created_at: string
}

export interface Topic {
  id: number
  name: string
  mcat_section: string
  description?: string
  difficulty_level?: number
}

// Test types
export interface QuizCreateRequest {
  mcat_section?: string
  topic_ids?: number[]
  difficulty_level?: number
  num_questions: number
  question_type?: 'passage_based' | 'standalone'
}

export interface TestAttempt {
  id: string
  practice_test_id: string
  started_at: string
  completed_at?: string
  status: 'in_progress' | 'paused' | 'completed' | 'abandoned'
  total_score?: number
  cpbs_score?: number
  cars_score?: number
  bbls_score?: number
  psbb_score?: number
  total_correct?: number
  total_questions?: number
  accuracy_percentage?: number
}

// Analytics types
export interface DashboardAnalytics {
  user: {
    name: string
    target_score?: number
    exam_date?: string
  }
  summary: {
    total_questions_answered: number
    total_correct: number
    overall_accuracy: number
    review_queue_count: number
  }
  score_history: Array<{
    date: string
    total_score?: number
    accuracy?: number
    cpbs_score?: number
    cars_score?: number
    bbls_score?: number
    psbb_score?: number
  }>
  concept_mastery: Array<{
    concept_code: string
    title: string
    mcat_section: string
    accuracy: number
    proficiency: 'green' | 'yellow' | 'red'
    total_attempts: number
  }>
}
