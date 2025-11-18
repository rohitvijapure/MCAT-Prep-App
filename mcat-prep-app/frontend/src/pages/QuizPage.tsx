import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import api from '@/services/api'
import type { Question } from '@/types'

export default function QuizPage() {
  const navigate = useNavigate()

  const [quizConfig, setQuizConfig] = useState({
    mcat_section: '',
    num_questions: 10,
    difficulty_level: '',
    question_type: '',
  })

  const createQuizMutation = useMutation({
    mutationFn: async (config: typeof quizConfig) => {
      const response = await api.post('/api/tests/quiz/create', {
        mcat_section: config.mcat_section || undefined,
        num_questions: config.num_questions,
        difficulty_level: config.difficulty_level ? parseInt(config.difficulty_level) : undefined,
        question_type: config.question_type || undefined,
      })
      return response.data
    },
  })

  const fetchQuestionsMutation = useMutation({
    mutationFn: async (practiceTestId: string) => {
      // Get questions from the practice test
      const response = await api.get(`/api/questions`, {
        params: {
          mcat_section: quizConfig.mcat_section || undefined,
          difficulty_level: quizConfig.difficulty_level || undefined,
          limit: quizConfig.num_questions,
        },
      })
      return response.data
    },
  })

  const handleStartQuiz = async (mode: 'timed' | 'untimed') => {
    try {
      // Create the quiz
      const practiceTest = await createQuizMutation.mutateAsync(quizConfig)

      // Fetch the questions
      const questions: Question[] = await fetchQuestionsMutation.mutateAsync(practiceTest.id)

      // Calculate time limit for timed mode (2 minutes per question)
      const timeLimit = mode === 'timed' ? quizConfig.num_questions * 120 : undefined

      // Navigate to quiz taking page
      navigate('/quiz/take', {
        state: {
          questions,
          timeLimit,
          mode,
        },
      })
    } catch (error) {
      console.error('Error starting quiz:', error)
      alert('Error starting quiz. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Quiz Builder</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 text-gray-700 hover:text-gray-900"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="bg-white rounded-lg shadow p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Create Custom Quiz</h2>

          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">MCAT Section</label>
              <select
                value={quizConfig.mcat_section}
                onChange={(e) => setQuizConfig({ ...quizConfig, mcat_section: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="">All Sections</option>
                <option value="CPBS">Chemical and Physical Foundations (CPBS)</option>
                <option value="CARS">Critical Analysis and Reasoning Skills (CARS)</option>
                <option value="BBLS">Biological and Biochemical Foundations (BBLS)</option>
                <option value="PSBB">Psychological, Social, and Biological Foundations (PSBB)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Number of Questions
              </label>
              <input
                type="number"
                min="5"
                max="59"
                value={quizConfig.num_questions}
                onChange={(e) => setQuizConfig({ ...quizConfig, num_questions: parseInt(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-sm text-gray-500 mt-1">
                Recommended: 10-20 for practice, 59 for full section
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Difficulty</label>
              <select
                value={quizConfig.difficulty_level}
                onChange={(e) => setQuizConfig({ ...quizConfig, difficulty_level: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Mixed</option>
                <option value="1">Easy</option>
                <option value="2">Medium</option>
                <option value="3">Hard</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Question Type</label>
              <select
                value={quizConfig.question_type}
                onChange={(e) => setQuizConfig({ ...quizConfig, question_type: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              >
                <option value="">Mixed</option>
                <option value="standalone">Standalone Questions Only</option>
                <option value="passage_based">Passage-Based Questions Only</option>
              </select>
            </div>

            <div className="flex gap-4 pt-4">
              <button
                onClick={() => handleStartQuiz('timed')}
                disabled={createQuizMutation.isPending || fetchQuestionsMutation.isPending}
                className="flex-1 bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {createQuizMutation.isPending || fetchQuestionsMutation.isPending
                  ? 'Loading...'
                  : 'Start Timed Quiz ⏱'}
              </button>
              <button
                onClick={() => handleStartQuiz('untimed')}
                disabled={createQuizMutation.isPending || fetchQuestionsMutation.isPending}
                className="flex-1 bg-gray-600 text-white py-3 px-6 rounded-md hover:bg-gray-700 font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {createQuizMutation.isPending || fetchQuestionsMutation.isPending
                  ? 'Loading...'
                  : 'Start Practice Mode 📚'}
              </button>
            </div>
          </div>
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Quiz Modes</h3>
          <div className="space-y-2 text-blue-800 text-sm">
            <p>
              <strong>⏱ Timed Mode:</strong> Simulates real MCAT conditions with countdown timer (2
              min/question)
            </p>
            <p>
              <strong>📚 Practice Mode:</strong> Take your time, no timer, review at your own pace
            </p>
          </div>
        </div>
      </main>
    </div>
  )
}
