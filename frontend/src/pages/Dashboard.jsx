import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  Trophy, Flame, Target, TrendingUp, BookOpen, Code2,
  ChevronRight, Zap, Star, BarChart3, Clock
} from 'lucide-react'
import { getProgress, getRoadmap, getTodayPlan } from '../api/client'
import { RadialBarChart, RadialBar, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'

const DIFFICULTY_COLORS = { easy: '#10b981', medium: '#f59e0b', hard: '#ef4444' }
const STATUS_COLORS = {
  locked: '#374151', available: '#6366f1', in_progress: '#f59e0b',
  completed: '#10b981', mastered: '#8b5cf6'
}

export default function Dashboard({ userId }) {
  const [progress, setProgress] = useState(null)
  const [roadmap, setRoadmap] = useState(null)
  const [dailyPlan, setDailyPlan] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      try {
        const [prog, rm] = await Promise.all([
          getProgress(userId).catch(() => null),
          getRoadmap(userId).catch(() => null),
        ])
        setProgress(prog)
        setRoadmap(rm)
        // try loading daily plan
        try { setDailyPlan(await getTodayPlan(userId)) } catch {}
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [userId])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin" />
      </div>
    )
  }

  const stats = progress?.stats || {}
  const rp = progress?.roadmap_progress || {}
  const topicProgress = progress?.topic_progress || []

  // Chart data
  const difficultyData = [
    { name: 'Easy', value: stats.easy_solved || 0, fill: DIFFICULTY_COLORS.easy },
    { name: 'Medium', value: stats.medium_solved || 0, fill: DIFFICULTY_COLORS.medium },
    { name: 'Hard', value: stats.hard_solved || 0, fill: DIFFICULTY_COLORS.hard },
  ]

  const completionData = [
    { name: 'Progress', value: rp.completion_percentage || 0, fill: '#6366f1' },
  ]

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Dashboard</h1>
          <p className="text-gray-400 mt-1">Your DSA preparation at a glance</p>
        </div>
        <Link
          to="/daily"
          className="inline-flex items-center gap-2 px-5 py-2.5 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 rounded-xl text-white font-medium transition-all shadow-lg shadow-indigo-500/20"
        >
          <Zap className="w-4 h-4" /> Start Today's Plan
        </Link>
      </div>

      {/* Stats cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard icon={Code2} label="Problems Solved" value={stats.total_problems_solved || 0} color="text-indigo-400" />
        <StatCard icon={Flame} label="Current Streak" value={`${stats.current_streak || 0} days`} color="text-orange-400" />
        <StatCard icon={Trophy} label="XP Points" value={stats.xp_points || 0} color="text-yellow-400" />
        <StatCard icon={Star} label="Level" value={stats.level || 1} color="text-purple-400" />
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Progress Ring */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-indigo-400" /> Overall Progress
          </h3>
          <div className="flex items-center justify-center">
            <div className="relative">
              <ResponsiveContainer width={180} height={180}>
                <RadialBarChart cx="50%" cy="50%" innerRadius="60%" outerRadius="90%" data={completionData} startAngle={90} endAngle={-270}>
                  <RadialBar dataKey="value" cornerRadius={8} background={{ fill: '#1f2937' }} />
                </RadialBarChart>
              </ResponsiveContainer>
              <div className="absolute inset-0 flex flex-col items-center justify-center">
                <span className="text-3xl font-bold">{Math.round(rp.completion_percentage || 0)}%</span>
                <span className="text-xs text-gray-400">Complete</span>
              </div>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs">
            <div>
              <p className="text-lg font-bold text-emerald-400">{rp.completed_topics || 0}</p>
              <p className="text-gray-500">Completed</p>
            </div>
            <div>
              <p className="text-lg font-bold text-purple-400">{rp.mastered_topics || 0}</p>
              <p className="text-gray-500">Mastered</p>
            </div>
            <div>
              <p className="text-lg font-bold text-gray-400">{rp.total_topics || 0}</p>
              <p className="text-gray-500">Total</p>
            </div>
          </div>
        </div>

        {/* Difficulty Breakdown */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" /> Problems by Difficulty
          </h3>
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={difficultyData} barSize={40}>
              <XAxis dataKey="name" tick={{ fill: '#9ca3af', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: '#9ca3af', fontSize: 12 }} axisLine={false} tickLine={false} />
              <Tooltip
                contentStyle={{ background: '#1f2937', border: '1px solid #374151', borderRadius: 8 }}
                labelStyle={{ color: '#fff' }}
              />
              <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                {difficultyData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Today's Plan Preview */}
        <div className="glass-card p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-yellow-400" /> Today's Focus
          </h3>
          {dailyPlan?.concept_lesson ? (
            <div className="space-y-4">
              <div className="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-lg">
                <p className="text-sm font-medium text-indigo-300">{dailyPlan.concept_lesson.title || 'Today\'s Lesson'}</p>
                <p className="text-xs text-gray-400 mt-1">{dailyPlan.concept_lesson.summary || 'Click to start learning'}</p>
              </div>
              {dailyPlan.concept_lesson.key_points?.slice(0, 3).map((point, i) => (
                <div key={i} className="flex items-start gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 mt-1.5 flex-shrink-0" />
                  <p className="text-sm text-gray-300">{point}</p>
                </div>
              ))}
              <Link
                to="/daily"
                className="flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300 font-medium mt-2"
              >
                View full plan <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          ) : (
            <div className="text-center py-8">
              <Clock className="w-10 h-10 text-gray-600 mx-auto mb-3" />
              <p className="text-gray-500 text-sm">No plan generated yet</p>
              <Link
                to="/daily"
                className="inline-flex items-center gap-1 text-sm text-indigo-400 hover:text-indigo-300 mt-2"
              >
                Generate plan <ChevronRight className="w-4 h-4" />
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Roadmap Quick View */}
      <div className="glass-card p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-indigo-400" /> Roadmap Progress
          </h3>
          <Link to="/roadmap" className="text-sm text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
            View full roadmap <ChevronRight className="w-4 h-4" />
          </Link>
        </div>
        <div className="flex flex-wrap gap-2">
          {topicProgress.slice(0, 20).map((topic) => (
            <div
              key={topic.id}
              className="px-3 py-1.5 rounded-lg text-xs font-medium border"
              style={{
                backgroundColor: `${STATUS_COLORS[topic.status]}15`,
                borderColor: `${STATUS_COLORS[topic.status]}40`,
                color: STATUS_COLORS[topic.status],
              }}
              title={`${topic.name} - ${topic.status} (${Math.round(topic.mastery_score)}%)`}
            >
              {topic.name.length > 25 ? topic.name.substring(0, 22) + '...' : topic.name}
            </div>
          ))}
        </div>
        {/* Day progress bar */}
        <div className="mt-4">
          <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
            <span>Day {rp.current_day || 1}</span>
            <span>{rp.total_days || 90} days total</span>
          </div>
          <div className="h-2 bg-gray-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-indigo-500 to-emerald-500 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, ((rp.current_day || 1) / (rp.total_days || 90)) * 100)}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

function StatCard({ icon: Icon, label, value, color }) {
  return (
    <div className="glass-card p-4">
      <div className="flex items-center gap-3">
        <div className={`p-2 rounded-lg bg-gray-800 ${color}`}>
          <Icon className="w-5 h-5" />
        </div>
        <div>
          <p className="text-2xl font-bold">{value}</p>
          <p className="text-xs text-gray-500">{label}</p>
        </div>
      </div>
    </div>
  )
}
