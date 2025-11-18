import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts'
import api from '@/services/api'
import { authService } from '@/services/auth'
import type { DashboardAnalytics } from '@/types'

export default function DashboardPage() {
  const navigate = useNavigate()

  const { data: analytics, isLoading } = useQuery<DashboardAnalytics>({
    queryKey: ['dashboard'],
    queryFn: async () => {
      const response = await api.get('/api/analytics/dashboard')
      return response.data
    },
  })

  const handleLogout = () => {
    authService.logout()
  }

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-xl text-gray-600">Loading...</div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">MCAT Prep Dashboard</h1>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/study')}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
            >
              Study
            </button>
            <button
              onClick={() => navigate('/quiz')}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Take Quiz
            </button>
            <button onClick={handleLogout} className="px-4 py-2 text-gray-700 hover:text-gray-900">
              Logout
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Welcome back, {analytics?.user.name}!
          </h2>
          {analytics?.user.target_score && (
            <p className="text-gray-600">
              Target Score: {analytics.user.target_score} | Exam Date:{' '}
              {analytics.user.exam_date || 'Not set'}
            </p>
          )}
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600">Questions Answered</h3>
            <p className="text-3xl font-bold text-blue-600 mt-2">
              {analytics?.summary.total_questions_answered || 0}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600">Correct Answers</h3>
            <p className="text-3xl font-bold text-green-600 mt-2">
              {analytics?.summary.total_correct || 0}
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600">Overall Accuracy</h3>
            <p className="text-3xl font-bold text-purple-600 mt-2">
              {analytics?.summary.overall_accuracy || 0}%
            </p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-sm font-medium text-gray-600">Review Queue</h3>
            <p className="text-3xl font-bold text-orange-600 mt-2">
              {analytics?.summary.review_queue_count || 0}
            </p>
          </div>
        </div>

        {/* Score History Chart */}
        {analytics?.score_history && analytics.score_history.length > 0 && (
          <div className="bg-white rounded-lg shadow p-6 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Score Progress Over Time</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={analytics.score_history}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="date"
                  tickFormatter={(value) => new Date(value).toLocaleDateString()}
                />
                <YAxis domain={[0, 100]} label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }} />
                <Tooltip
                  labelFormatter={(value) => new Date(value).toLocaleDateString()}
                  formatter={(value: any) => [`${value}%`, 'Accuracy']}
                />
                <Legend />
                <Line type="monotone" dataKey="accuracy" stroke="#3b82f6" strokeWidth={2} name="Quiz Accuracy" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Concept Mastery */}
        {analytics?.concept_mastery && analytics.concept_mastery.length > 0 && (
          <>
            {/* Concept Mastery Chart */}
            <div className="bg-white rounded-lg shadow p-6 mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Concept Mastery Chart</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.concept_mastery}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="concept_code" />
                  <YAxis domain={[0, 100]} label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }} />
                  <Tooltip
                    formatter={(value: any) => [`${value.toFixed(1)}%`, 'Accuracy']}
                    labelFormatter={(label) => `Concept ${label}`}
                  />
                  <Legend />
                  <Bar
                    dataKey="accuracy"
                    fill="#3b82f6"
                    name="Accuracy"
                    radius={[8, 8, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Concept Mastery List */}
            <div className="bg-white rounded-lg shadow p-6 mb-8">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Detailed Concept Breakdown</h3>
              <div className="space-y-2">
                {analytics.concept_mastery.map((concept) => (
                  <div key={concept.concept_code} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">{concept.title}</p>
                      <p className="text-sm text-gray-600">
                        {concept.concept_code} | {concept.mcat_section} | {concept.total_attempts} attempts
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      {/* Progress Bar */}
                      <div className="w-32">
                        <div className="bg-gray-200 rounded-full h-2">
                          <div
                            className={`h-2 rounded-full ${
                              concept.proficiency === 'green'
                                ? 'bg-green-500'
                                : concept.proficiency === 'yellow'
                                ? 'bg-yellow-400'
                                : 'bg-red-500'
                            }`}
                            style={{ width: `${concept.accuracy}%` }}
                          />
                        </div>
                      </div>
                      <span className="text-lg font-bold w-16 text-right">{concept.accuracy.toFixed(1)}%</span>
                      <span
                        className={`px-3 py-1 rounded-full text-sm font-medium w-24 text-center ${
                          concept.proficiency === 'green'
                            ? 'bg-green-100 text-green-800'
                            : concept.proficiency === 'yellow'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}
                      >
                        {concept.proficiency === 'green' ? '✓ Strong' : concept.proficiency === 'yellow' ? '○ Developing' : '✗ Weak'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {/* Get Started Message */}
        {analytics?.summary.total_questions_answered === 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 text-center">
            <h3 className="text-xl font-bold text-blue-900 mb-2">Get Started with MCAT Prep!</h3>
            <p className="text-blue-700 mb-4">
              Begin your journey by taking a practice quiz or exploring study materials.
            </p>
            <div className="flex gap-4 justify-center">
              <button
                onClick={() => navigate('/quiz')}
                className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 font-medium"
              >
                Start Your First Quiz
              </button>
              <button
                onClick={() => navigate('/study')}
                className="px-6 py-3 bg-white text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50 font-medium"
              >
                Browse Study Materials
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
