import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Sun, Coffee, BookOpen, Code2, Brain, CheckCircle2,
  ChevronRight, Clock, Sparkles, ArrowRight
} from 'lucide-react'
import { getTodayPlan, completeDay, getRoadmap } from '../api/client'

export default function DailyPlanPage({ userId }) {
  const [plan, setPlan] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [completing, setCompleting] = useState(false)
  const [checkedSteps, setCheckedSteps] = useState(new Set())

  useEffect(() => {
    async function load() {
      try {
        const [p, r] = await Promise.all([
          getTodayPlan(userId).catch(() => null),
          getRoadmap(userId).catch(() => null),
        ])
        setPlan(p)
        setRoadmap(r)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [userId])

  async function handleCompleteDay() {
    setCompleting(true)
    try {
      await completeDay(userId)
      // Reload plan for next day
      const p = await getTodayPlan(userId).catch(() => null)
      setPlan(p)
      setCheckedSteps(new Set())
    } finally {
      setCompleting(false)
    }
  }

  function toggleStep(idx) {
    setCheckedSteps(prev => {
      const next = new Set(prev)
      next.has(idx) ? next.delete(idx) : next.add(idx)
      return next
    })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    )
  }

  const lesson = plan?.concept_lesson || {}
  const currentTopic = roadmap?.topics?.find(t => t.status === 'in_progress' || t.status === 'available')

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl">
      {/* Header */}
      <div className="glass-card p-6 bg-gradient-to-r from-indigo-500/10 to-emerald-500/10">
        <div className="flex items-start gap-4">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-yellow-400 to-orange-500 flex items-center justify-center flex-shrink-0">
            <Sun className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">
              Day {plan?.day_number || roadmap?.current_day || 1}
            </h1>
            <p className="text-gray-400 mt-1">
              {plan?.ai_summary || 'Ready to learn something amazing today!'}
            </p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Today's Concept */}
          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <Brain className="w-5 h-5 text-indigo-400" />
              Today's Concept: {lesson.title || currentTopic?.name || 'DSA Fundamentals'}
            </h2>
            {lesson.summary && (
              <p className="text-gray-300 text-sm mb-4">{lesson.summary}</p>
            )}
            {lesson.key_points?.length > 0 && (
              <div className="space-y-2 mb-4">
                <h4 className="text-sm font-medium text-gray-400">Key Points:</h4>
                {lesson.key_points.map((point, i) => (
                  <div key={i} className="flex items-start gap-3 p-2 rounded-lg hover:bg-gray-800/30">
                    <Sparkles className="w-4 h-4 text-indigo-400 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-300">{point}</p>
                  </div>
                ))}
              </div>
            )}
            {currentTopic && (
              <Link
                to={`/learn/${encodeURIComponent(currentTopic.name)}`}
                className="inline-flex items-center gap-2 px-4 py-2 bg-indigo-600/80 hover:bg-indigo-500 rounded-lg text-sm font-medium text-white transition-all"
              >
                <BookOpen className="w-4 h-4" /> Deep Dive into Lesson
              </Link>
            )}
          </div>

          {/* Study Plan Steps */}
          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
              <Clock className="w-5 h-5 text-emerald-400" /> Study Plan
            </h2>
            <div className="space-y-3">
              {(lesson.estimated_time_minutes ? [
                { time: '0-30 min', activity: 'Learn the concept', details: `Study ${lesson.title || 'today\'s topic'} with visualizations` },
                { time: '30-60 min', activity: 'Solve easy problem', details: 'Apply the concept to an easy problem' },
                { time: '60-90 min', activity: 'Solve medium problem', details: 'Challenge yourself with a harder problem' },
                { time: '90-120 min', activity: 'Review & reflect', details: 'Review solutions, note patterns' },
              ] : [
                { time: '0-20 min', activity: 'Warm up', details: 'Review yesterday\'s concepts' },
                { time: '20-50 min', activity: 'Learn new concept', details: 'Study with visualizations and examples' },
                { time: '50-80 min', activity: 'Practice problems', details: 'Solve 2-3 problems on the topic' },
                { time: '80-100 min', activity: 'Review & notes', details: 'Review solutions and identify patterns' },
              ]).map((step, idx) => (
                <button
                  key={idx}
                  onClick={() => toggleStep(idx)}
                  className={`w-full text-left flex items-center gap-4 p-3 rounded-lg border transition-all
                    ${checkedSteps.has(idx)
                      ? 'bg-emerald-500/10 border-emerald-500/30'
                      : 'bg-gray-800/30 border-gray-700/50 hover:border-gray-600'
                    }`}
                >
                  <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all
                    ${checkedSteps.has(idx)
                      ? 'border-emerald-500 bg-emerald-500'
                      : 'border-gray-600'
                    }`}
                  >
                    {checkedSteps.has(idx) && <CheckCircle2 className="w-4 h-4 text-white" />}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs text-gray-500 font-mono">{step.time}</span>
                      <span className={`text-sm font-medium ${checkedSteps.has(idx) ? 'text-emerald-400 line-through' : 'text-gray-200'}`}>
                        {step.activity}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500 mt-0.5">{step.details}</p>
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-4">
          {/* Current Topic */}
          {currentTopic && (
            <div className="glass-card p-4">
              <h3 className="text-sm font-semibold text-gray-400 mb-3">Current Topic</h3>
              <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-lg">
                <h4 className="font-medium text-sm">{currentTopic.name}</h4>
                <p className="text-xs text-gray-400 mt-1">{currentTopic.category}</p>
                {currentTopic.key_concepts?.length > 0 && (
                  <div className="flex flex-wrap gap-1 mt-2">
                    {currentTopic.key_concepts.slice(0, 4).map((c, i) => (
                      <span key={i} className="px-2 py-0.5 bg-gray-800/80 rounded text-xs text-gray-400">{c}</span>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Quick Actions */}
          <div className="glass-card p-4 space-y-2">
            <h3 className="text-sm font-semibold text-gray-400 mb-3">Quick Actions</h3>
            {currentTopic && (
              <Link
                to={`/practice/${currentTopic.id}`}
                className="flex items-center justify-between p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
              >
                <div className="flex items-center gap-2">
                  <Code2 className="w-4 h-4 text-emerald-400" />
                  <span className="text-sm">Practice Problems</span>
                </div>
                <ChevronRight className="w-4 h-4 text-gray-500" />
              </Link>
            )}
            <Link
              to="/chat"
              className="flex items-center justify-between p-3 bg-gray-800/50 hover:bg-gray-800 rounded-lg transition-colors"
            >
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-indigo-400" />
                <span className="text-sm">Ask AI Mentor</span>
              </div>
              <ChevronRight className="w-4 h-4 text-gray-500" />
            </Link>
          </div>

          {/* Complete Day Button */}
          <button
            onClick={handleCompleteDay}
            disabled={completing || checkedSteps.size < 3}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 disabled:from-gray-700 disabled:to-gray-700 disabled:text-gray-500 rounded-xl text-white font-semibold transition-all"
          >
            {completing ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <>
                <CheckCircle2 className="w-5 h-5" />
                Complete Day
              </>
            )}
          </button>
          {checkedSteps.size < 3 && (
            <p className="text-xs text-gray-500 text-center">Complete at least 3 steps to finish the day</p>
          )}
        </div>
      </div>
    </div>
  )
}
