import { useNavigate } from 'react-router-dom'

export default function StudyPage() {
  const navigate = useNavigate()

  const sections = [
    {
      code: 'CPBS',
      name: 'Chemical and Physical Foundations of Biological Systems',
      topics: 10,
      modules: 25,
    },
    {
      code: 'CARS',
      name: 'Critical Analysis and Reasoning Skills',
      topics: 8,
      modules: 20,
    },
    {
      code: 'BBLS',
      name: 'Biological and Biochemical Foundations of Living Systems',
      topics: 12,
      modules: 30,
    },
    {
      code: 'PSBB',
      name: 'Psychological, Social, and Biological Foundations of Behavior',
      topics: 10,
      modules: 22,
    },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Study Materials</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="px-4 py-2 text-gray-700 hover:text-gray-900"
          >
            Back to Dashboard
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-2">MCAT Sections</h2>
          <p className="text-gray-600">
            Explore comprehensive study materials organized by MCAT sections and topics.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sections.map((section) => (
            <div key={section.code} className="bg-white rounded-lg shadow hover:shadow-lg transition p-6">
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{section.name}</h3>
                  <p className="text-sm text-gray-500 mt-1">{section.code}</p>
                </div>
                <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {section.code}
                </span>
              </div>

              <div className="flex gap-4 text-sm text-gray-600 mb-4">
                <span>{section.topics} Topics</span>
                <span>•</span>
                <span>{section.modules} Study Modules</span>
              </div>

              <button className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 font-medium">
                Start Studying
              </button>
            </div>
          ))}
        </div>

        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">Coming Soon</h3>
          <p className="text-blue-700">
            Detailed study modules with text summaries, flashcards, videos, and equation sheets will be
            available soon. This is a preview of the study materials interface.
          </p>
        </div>
      </main>
    </div>
  )
}
