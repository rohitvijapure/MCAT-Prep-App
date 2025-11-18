import { useState, useEffect } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import api from '@/services/api'
import type { Question, QuestionAttempt } from '@/types'

interface QuizState {
  questions: Question[]
  currentIndex: number
  answers: Record<string, string>
  flagged: Record<string, boolean>
  startTime: number
  timeLimit?: number
  mode: 'timed' | 'untimed'
}

export default function QuizTakingPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const quizData = location.state as { questions: Question[]; timeLimit?: number; mode: 'timed' | 'untimed' }

  const [quizState, setQuizState] = useState<QuizState>({
    questions: quizData?.questions || [],
    currentIndex: 0,
    answers: {},
    flagged: {},
    startTime: Date.now(),
    timeLimit: quizData?.timeLimit,
    mode: quizData?.mode || 'timed',
  })

  const [timeRemaining, setTimeRemaining] = useState(quizData?.timeLimit || 0)
  const [showExitConfirm, setShowExitConfirm] = useState(false)

  // Timer countdown
  useEffect(() => {
    if (quizState.mode !== 'timed' || !quizState.timeLimit) return

    const interval = setInterval(() => {
      const elapsed = Math.floor((Date.now() - quizState.startTime) / 1000)
      const remaining = (quizState.timeLimit || 0) - elapsed

      if (remaining <= 0) {
        handleSubmitQuiz()
      } else {
        setTimeRemaining(remaining)
      }
    }, 1000)

    return () => clearInterval(interval)
  }, [quizState.startTime, quizState.timeLimit, quizState.mode])

  const currentQuestion = quizState.questions[quizState.currentIndex]

  const handleAnswerSelect = (answer: string) => {
    setQuizState(prev => ({
      ...prev,
      answers: { ...prev.answers, [currentQuestion.id]: answer }
    }))
  }

  const handleFlagQuestion = () => {
    setQuizState(prev => ({
      ...prev,
      flagged: { ...prev.flagged, [currentQuestion.id]: !prev.flagged[currentQuestion.id] }
    }))
  }

  const handleNextQuestion = () => {
    if (quizState.currentIndex < quizState.questions.length - 1) {
      setQuizState(prev => ({ ...prev, currentIndex: prev.currentIndex + 1 }))
    }
  }

  const handlePreviousQuestion = () => {
    if (quizState.currentIndex > 0) {
      setQuizState(prev => ({ ...prev, currentIndex: prev.currentIndex - 1 }))
    }
  }

  const handleJumpToQuestion = (index: number) => {
    setQuizState(prev => ({ ...prev, currentIndex: index }))
  }

  const submitMutation = useMutation({
    mutationFn: async (attempts: QuestionAttempt[]) => {
      const results = await Promise.all(
        attempts.map(attempt => api.post('/api/questions/attempt', attempt))
      )
      return results
    },
  })

  const handleSubmitQuiz = async () => {
    const totalTime = Math.floor((Date.now() - quizState.startTime) / 1000)
    const avgTimePerQuestion = totalTime / quizState.questions.length

    const attempts: QuestionAttempt[] = quizState.questions.map(q => ({
      question_id: q.id,
      selected_answer: quizState.answers[q.id] || 'X',
      time_spent_seconds: Math.floor(avgTimePerQuestion),
      is_flagged: quizState.flagged[q.id] || false,
      attempt_mode: quizState.mode,
    }))

    try {
      const results = await submitMutation.mutateAsync(attempts)
      navigate('/quiz/results', { state: { results: results.map(r => r.data), quizState } })
    } catch (error) {
      console.error('Error submitting quiz:', error)
      alert('Error submitting quiz. Please try again.')
    }
  }

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const answeredCount = Object.keys(quizState.answers).length
  const flaggedCount = Object.values(quizState.flagged).filter(Boolean).length

  if (!quizData || quizState.questions.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-gray-700 mb-4">No quiz data available</p>
          <button
            onClick={() => navigate('/quiz')}
            className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Go to Quiz Builder
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header with Timer */}
      <header className="bg-white shadow-md sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-xl font-bold text-gray-900">MCAT Practice Quiz</h1>
              <p className="text-sm text-gray-600">
                Question {quizState.currentIndex + 1} of {quizState.questions.length}
              </p>
            </div>

            {quizState.mode === 'timed' && (
              <div className={`text-2xl font-bold ${timeRemaining < 300 ? 'text-red-600' : 'text-blue-600'}`}>
                ⏱ {formatTime(timeRemaining)}
              </div>
            )}

            <div className="flex gap-2">
              <button
                onClick={() => setShowExitConfirm(true)}
                className="px-4 py-2 text-gray-700 hover:text-gray-900 border border-gray-300 rounded-md"
              >
                Exit Quiz
              </button>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="mt-3 bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all"
              style={{ width: `${((quizState.currentIndex + 1) / quizState.questions.length) * 100}%` }}
            />
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-12 gap-6">
        {/* Main Question Area */}
        <div className="col-span-9">
          <div className="bg-white rounded-lg shadow p-8">
            {/* Question Text */}
            <div className="mb-6">
              <div className="flex justify-between items-start mb-4">
                <span className="text-sm font-medium text-gray-500">
                  {currentQuestion.mcat_section} | {currentQuestion.question_type === 'passage_based' ? 'Passage-Based' : 'Standalone'}
                </span>
                <button
                  onClick={handleFlagQuestion}
                  className={`px-3 py-1 rounded ${
                    quizState.flagged[currentQuestion.id]
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {quizState.flagged[currentQuestion.id] ? '🚩 Flagged' : '🏳 Flag'}
                </button>
              </div>

              <p className="text-lg text-gray-900 leading-relaxed">{currentQuestion.question_text}</p>
            </div>

            {/* Answer Options */}
            <div className="space-y-3">
              {Object.entries(currentQuestion.options).map(([letter, text]) => (
                <button
                  key={letter}
                  onClick={() => handleAnswerSelect(letter)}
                  className={`w-full text-left p-4 border-2 rounded-lg transition ${
                    quizState.answers[currentQuestion.id] === letter
                      ? 'border-blue-600 bg-blue-50'
                      : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                  }`}
                >
                  <span className="font-bold text-blue-600 mr-3">{letter}.</span>
                  <span className="text-gray-900">{text}</span>
                </button>
              ))}
            </div>

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8 pt-6 border-t">
              <button
                onClick={handlePreviousQuestion}
                disabled={quizState.currentIndex === 0}
                className="px-6 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                ← Previous
              </button>

              {quizState.currentIndex === quizState.questions.length - 1 ? (
                <button
                  onClick={handleSubmitQuiz}
                  className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 font-medium"
                >
                  Submit Quiz
                </button>
              ) : (
                <button
                  onClick={handleNextQuestion}
                  className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  Next →
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar - Question Navigator */}
        <div className="col-span-3">
          <div className="bg-white rounded-lg shadow p-4 sticky top-24">
            <h3 className="font-bold text-gray-900 mb-3">Question Navigator</h3>

            <div className="mb-4 text-sm text-gray-600 space-y-1">
              <p>Answered: {answeredCount}/{quizState.questions.length}</p>
              <p>Flagged: {flaggedCount}</p>
            </div>

            <div className="grid grid-cols-5 gap-2 max-h-96 overflow-y-auto">
              {quizState.questions.map((q, idx) => (
                <button
                  key={q.id}
                  onClick={() => handleJumpToQuestion(idx)}
                  className={`
                    aspect-square rounded flex items-center justify-center text-sm font-medium
                    ${idx === quizState.currentIndex ? 'ring-2 ring-blue-600' : ''}
                    ${quizState.answers[q.id]
                      ? 'bg-blue-600 text-white'
                      : quizState.flagged[q.id]
                      ? 'bg-yellow-200 text-yellow-900'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                    }
                  `}
                >
                  {idx + 1}
                </button>
              ))}
            </div>

            <div className="mt-4 pt-4 border-t space-y-2 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-blue-600 rounded"></div>
                <span className="text-gray-600">Answered</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-yellow-200 rounded"></div>
                <span className="text-gray-600">Flagged</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-gray-200 rounded"></div>
                <span className="text-gray-600">Unanswered</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Exit Confirmation Modal */}
      {showExitConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-md">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Exit Quiz?</h2>
            <p className="text-gray-600 mb-6">
              Your progress will be lost. Are you sure you want to exit?
            </p>
            <div className="flex gap-4">
              <button
                onClick={() => setShowExitConfirm(false)}
                className="flex-1 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={() => navigate('/dashboard')}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
              >
                Exit Quiz
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
