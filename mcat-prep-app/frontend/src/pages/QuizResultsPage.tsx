import { useNavigate, useLocation } from 'react-router-dom'
import { useEffect } from 'react'

interface QuestionResult {
  id: string
  question_id: string
  is_correct: boolean
  selected_answer: string
  correct_answer: string
  correct_explanation: string
  incorrect_explanations: Record<string, string>
  time_spent_seconds: number
}

export default function QuizResultsPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { results, quizState } = location.state as { results: QuestionResult[]; quizState: any } || {}

  useEffect(() => {
    if (!results) {
      navigate('/dashboard')
    }
  }, [results, navigate])

  if (!results) {
    return null
  }

  const totalQuestions = results.length
  const correctAnswers = results.filter(r => r.is_correct).length
  const percentage = Math.round((correctAnswers / totalQuestions) * 100)

  // Calculate MCAT scaled score (approximation)
  // MCAT sections: 118-132 scale
  const scaledScore = Math.round(118 + (percentage / 100) * 14)

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Quiz Results</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Score Summary */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-800 rounded-lg shadow-xl p-8 text-white mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div>
              <p className="text-sm opacity-90 mb-2">Score</p>
              <p className="text-5xl font-bold">{percentage}%</p>
            </div>
            <div>
              <p className="text-sm opacity-90 mb-2">Scaled Score (Est.)</p>
              <p className="text-5xl font-bold">{scaledScore}</p>
              <p className="text-xs opacity-75 mt-1">118-132 scale</p>
            </div>
            <div>
              <p className="text-sm opacity-90 mb-2">Correct Answers</p>
              <p className="text-5xl font-bold">{correctAnswers}</p>
              <p className="text-sm opacity-75 mt-1">out of {totalQuestions}</p>
            </div>
            <div>
              <p className="text-sm opacity-90 mb-2">Performance</p>
              <p className="text-3xl font-bold">
                {percentage >= 80 ? '🎉 Excellent' : percentage >= 70 ? '😊 Good' : percentage >= 60 ? '📚 Fair' : '💪 Keep Studying'}
              </p>
            </div>
          </div>
        </div>

        {/* Performance Breakdown */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Performance Analysis</h2>

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <h3 className="font-semibold text-green-800 mb-2">Strengths</h3>
              <ul className="text-sm text-green-700 space-y-1">
                {percentage >= 80 && <li>• Excellent overall performance</li>}
                {percentage >= 70 && <li>• Strong fundamental understanding</li>}
                {percentage >= 60 && <li>• Good knowledge base to build on</li>}
              </ul>
            </div>

            <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
              <h3 className="font-semibold text-orange-800 mb-2">Areas to Improve</h3>
              <ul className="text-sm text-orange-700 space-y-1">
                {percentage < 80 && <li>• Review incorrect questions carefully</li>}
                {percentage < 70 && <li>• Focus on foundational concepts</li>}
                {percentage < 60 && <li>• Consider more study time needed</li>}
              </ul>
            </div>
          </div>

          <div className="bg-gray-50 rounded-lg p-4">
            <p className="text-sm text-gray-700">
              <strong>Recommendation:</strong>
              {percentage >= 80
                ? ' Excellent work! Continue practicing to maintain this level. Consider more difficult questions.'
                : percentage >= 70
                ? ' Good job! Review your incorrect answers and focus on weak areas to push your score higher.'
                : percentage >= 60
                ? ' You have a decent foundation. Spend more time on study materials and practice regularly.'
                : ' More preparation is needed. Review fundamental concepts thoroughly and practice more questions.'}
            </p>
          </div>
        </div>

        {/* Question-by-Question Review */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Question Review</h2>

          <div className="space-y-4">
            {results.map((result, index) => (
              <div
                key={result.id}
                className={`border-l-4 ${
                  result.is_correct ? 'border-green-500 bg-green-50' : 'border-red-500 bg-red-50'
                } p-6 rounded-r-lg`}
              >
                <div className="flex justify-between items-start mb-3">
                  <h3 className="font-bold text-lg text-gray-900">
                    Question {index + 1}
                    <span className={`ml-3 text-sm ${result.is_correct ? 'text-green-600' : 'text-red-600'}`}>
                      {result.is_correct ? '✓ Correct' : '✗ Incorrect'}
                    </span>
                  </h3>
                </div>

                <div className="space-y-3 text-sm">
                  <div>
                    <span className="font-semibold text-gray-700">Your Answer: </span>
                    <span className={result.is_correct ? 'text-green-700' : 'text-red-700'}>
                      {result.selected_answer}
                    </span>
                  </div>

                  {!result.is_correct && (
                    <div>
                      <span className="font-semibold text-gray-700">Correct Answer: </span>
                      <span className="text-green-700">{result.correct_answer}</span>
                    </div>
                  )}

                  <div className="bg-white p-4 rounded border border-gray-200">
                    <p className="font-semibold text-gray-900 mb-2">Explanation:</p>
                    <p className="text-gray-700">{result.correct_explanation}</p>
                  </div>

                  {!result.is_correct && result.incorrect_explanations && result.incorrect_explanations[result.selected_answer] && (
                    <div className="bg-red-100 border border-red-200 p-4 rounded">
                      <p className="font-semibold text-red-900 mb-2">Why Your Answer Was Wrong:</p>
                      <p className="text-red-800">{result.incorrect_explanations[result.selected_answer]}</p>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="mt-8 flex gap-4 justify-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-8 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 font-medium"
          >
            Return to Dashboard
          </button>
          <button
            onClick={() => navigate('/quiz')}
            className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
          >
            Take Another Quiz
          </button>
        </div>
      </main>
    </div>
  )
}
