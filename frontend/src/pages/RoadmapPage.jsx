import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Lock, CheckCircle2, Star, Play, ChevronDown, ChevronRight,
  BookOpen, Code2, Award, RefreshCw
} from 'lucide-react'
import { getRoadmap, generateRoadmap, updateTopicStatus } from '../api/client'

const STATUS_CONFIG = {
  locked: { icon: Lock, color: '#4b5563', bg: 'bg-gray-800', label: 'Locked', border: 'border-gray-700' },
  available: { icon: Play, color: '#818cf8', bg: 'bg-indigo-500/10', label: 'Ready', border: 'border-indigo-500/30' },
  in_progress: { icon: BookOpen, color: '#fbbf24', bg: 'bg-yellow-500/10', label: 'In Progress', border: 'border-yellow-500/30' },
  completed: { icon: CheckCircle2, color: '#34d399', bg: 'bg-emerald-500/10', label: 'Completed', border: 'border-emerald-500/30' },
  mastered: { icon: Star, color: '#a78bfa', bg: 'bg-purple-500/10', label: 'Mastered', border: 'border-purple-500/30' },
}

const CATEGORY_LABELS = {
  foundations: '🏗️ Foundations',
  arrays_strings: '📊 Arrays & Strings',
  hashing: '#️⃣ Hashing',
  linked_lists: '🔗 Linked Lists',
  stacks_queues: '📚 Stacks & Queues',
  trees: '🌳 Trees',
  heaps: '⛰️ Heaps',
  graphs: '🕸️ Graphs',
  binary_search: '🔍 Binary Search',
  recursion_backtracking: '🔄 Recursion & Backtracking',
  dynamic_programming: '🧩 Dynamic Programming',
  greedy: '💡 Greedy Algorithms',
  advanced: '🚀 Advanced Topics',
  system_design_patterns: '🏛️ Design Patterns',
}

const DIFFICULTY_BADGE = {
  easy: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
  medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
  hard: 'bg-red-500/20 text-red-400 border-red-500/30',
}

export default function RoadmapPage({ userId }) {
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [regenerating, setRegenerating] = useState(false)
  const [expandedCategories, setExpandedCategories] = useState(new Set())

  useEffect(() => { loadRoadmap() }, [userId])

  async function loadRoadmap() {
    setLoading(true)
    try {
      const data = await getRoadmap(userId)
      setRoadmap(data)
      // Auto-expand categories with in-progress or available topics
      const autoExpand = new Set()
      data.topics?.forEach(t => {
        if (t.status === 'in_progress' || t.status === 'available') {
          autoExpand.add(t.category)
        }
      })
      setExpandedCategories(autoExpand)
    } catch {
      setRoadmap(null)
    } finally {
      setLoading(false)
    }
  }

  async function handleRegenerate() {
    setRegenerating(true)
    try {
      const data = await generateRoadmap(userId)
      setRoadmap(data)
    } finally {
      setRegenerating(false)
    }
  }

  async function handleStatusChange(topicId, newStatus) {
    await updateTopicStatus(topicId, newStatus)
    await loadRoadmap()
  }

  function toggleCategory(cat) {
    setExpandedCategories(prev => {
      const next = new Set(prev)
      next.has(cat) ? next.delete(cat) : next.add(cat)
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

  if (!roadmap) {
    return (
      <div className="text-center py-20">
        <h2 className="text-2xl font-bold mb-4">No roadmap yet</h2>
        <p className="text-gray-400 mb-6">Let's create your personalized DSA learning path!</p>
        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-white font-semibold"
        >
          {regenerating ? 'Generating...' : 'Generate My Roadmap'}
        </button>
      </div>
    )
  }

  // Group topics by category
  const grouped = {}
  roadmap.topics?.forEach(topic => {
    if (!grouped[topic.category]) grouped[topic.category] = []
    grouped[topic.category].push(topic)
  })

  // Calculate category stats
  const categoryStats = {}
  Object.entries(grouped).forEach(([cat, topics]) => {
    const done = topics.filter(t => t.status === 'completed' || t.status === 'mastered').length
    categoryStats[cat] = { total: topics.length, done, pct: Math.round((done / topics.length) * 100) }
  })

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Learning Roadmap</h1>
          <p className="text-gray-400 mt-1">
            Day {roadmap.current_day} of {roadmap.total_days} • {roadmap.topics?.length || 0} topics
          </p>
        </div>
        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="flex items-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg text-sm font-medium text-gray-300 transition-all disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${regenerating ? 'animate-spin' : ''}`} />
          Regenerate
        </button>
      </div>

      {/* Roadmap Timeline */}
      <div className="space-y-3">
        {Object.entries(grouped).map(([category, topics]) => {
          const stats = categoryStats[category]
          const isExpanded = expandedCategories.has(category)

          return (
            <div key={category} className="glass-card overflow-hidden">
              {/* Category Header */}
              <button
                onClick={() => toggleCategory(category)}
                className="w-full flex items-center justify-between p-4 hover:bg-gray-800/30 transition-colors"
              >
                <div className="flex items-center gap-3">
                  {isExpanded ? <ChevronDown className="w-5 h-5 text-gray-400" /> : <ChevronRight className="w-5 h-5 text-gray-400" />}
                  <span className="text-lg font-semibold">
                    {CATEGORY_LABELS[category] || category}
                  </span>
                  <span className="text-xs text-gray-500">{topics.length} topics</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-400">{stats.done}/{stats.total}</span>
                  <div className="w-24 h-2 bg-gray-800 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-indigo-500 to-emerald-500 rounded-full transition-all"
                      style={{ width: `${stats.pct}%` }}
                    />
                  </div>
                  <span className="text-xs text-gray-500 w-10 text-right">{stats.pct}%</span>
                </div>
              </button>

              {/* Topics */}
              {isExpanded && (
                <div className="px-4 pb-4 space-y-2">
                  {topics.map((topic, idx) => {
                    const config = STATUS_CONFIG[topic.status] || STATUS_CONFIG.locked
                    const StatusIcon = config.icon

                    return (
                      <div
                        key={topic.id}
                        className={`flex items-center gap-4 p-3 rounded-lg border ${config.border} ${config.bg} transition-all`}
                      >
                        {/* Timeline connector */}
                        <div className="flex flex-col items-center w-8">
                          <div
                            className="w-8 h-8 rounded-full flex items-center justify-center border-2"
                            style={{ borderColor: config.color, backgroundColor: `${config.color}20` }}
                          >
                            <StatusIcon className="w-4 h-4" style={{ color: config.color }} />
                          </div>
                          {idx < topics.length - 1 && (
                            <div className="w-0.5 h-4 mt-1" style={{ backgroundColor: `${config.color}40` }} />
                          )}
                        </div>

                        {/* Topic Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2">
                            <h4 className="font-medium text-sm">{topic.name}</h4>
                            <span className={`px-2 py-0.5 text-xs rounded-full border ${DIFFICULTY_BADGE[topic.difficulty] || ''}`}>
                              {topic.difficulty}
                            </span>
                          </div>
                          <div className="flex items-center gap-3 mt-1">
                            <span className="text-xs text-gray-500">
                              Days {topic.day_start}-{topic.day_end}
                            </span>
                            {topic.key_concepts?.length > 0 && (
                              <span className="text-xs text-gray-500">
                                {topic.key_concepts.length} concepts
                              </span>
                            )}
                          </div>
                          {/* Mastery bar */}
                          {topic.mastery_score > 0 && (
                            <div className="mt-1.5 flex items-center gap-2">
                              <div className="flex-1 h-1 bg-gray-800 rounded-full overflow-hidden max-w-32">
                                <div
                                  className="h-full bg-gradient-to-r from-indigo-500 to-emerald-500 rounded-full"
                                  style={{ width: `${topic.mastery_score}%` }}
                                />
                              </div>
                              <span className="text-xs text-gray-500">{Math.round(topic.mastery_score)}%</span>
                            </div>
                          )}
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-2">
                          {(topic.status === 'available' || topic.status === 'in_progress') && (
                            <>
                              <Link
                                to={`/learn/${encodeURIComponent(topic.name)}`}
                                className="px-3 py-1.5 bg-indigo-600/80 hover:bg-indigo-500 rounded-lg text-xs font-medium text-white transition-all"
                              >
                                Learn
                              </Link>
                              <Link
                                to={`/practice/${topic.id}`}
                                className="px-3 py-1.5 bg-emerald-600/80 hover:bg-emerald-500 rounded-lg text-xs font-medium text-white transition-all"
                              >
                                Practice
                              </Link>
                            </>
                          )}
                          {topic.status === 'in_progress' && (
                            <button
                              onClick={() => handleStatusChange(topic.id, 'completed')}
                              className="px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-lg text-xs font-medium text-gray-300 transition-all"
                            >
                              Mark Done
                            </button>
                          )}
                          {topic.status === 'completed' && (
                            <button
                              onClick={() => handleStatusChange(topic.id, 'mastered')}
                              className="flex items-center gap-1 px-3 py-1.5 bg-purple-600/80 hover:bg-purple-500 rounded-lg text-xs font-medium text-white transition-all"
                            >
                              <Award className="w-3 h-3" /> Master
                            </button>
                          )}
                        </div>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
