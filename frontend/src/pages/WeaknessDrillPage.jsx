import { useState, useEffect } from 'react'
import { analyzeWeaknesses, generateWeaknessDrill } from '../api/client'
import { Target, Zap, TrendingDown, AlertTriangle, Loader2, BarChart3 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

export default function WeaknessDrillPage({ userId, user }) {
  const [analysis, setAnalysis] = useState(null)
  const [drill, setDrill] = useState(null)
  const [loading, setLoading] = useState('')
  const [config, setConfig] = useState({ focus_pattern: '', difficulty: '', num_problems: 5 })

  useEffect(() => { loadAnalysis() }, [userId])

  const loadAnalysis = async () => {
    setLoading('analyze')
    try { const data = await analyzeWeaknesses(userId); setAnalysis(data) } catch {}
    setLoading('')
  }

  const handleGenerate = async (pattern = null) => {
    setLoading('generate'); setDrill(null)
    try {
      const data = await generateWeaknessDrill({
        user_id: userId,
        focus_pattern: pattern || config.focus_pattern || undefined,
        difficulty: config.difficulty || undefined,
        num_problems: config.num_problems,
      })
      setDrill(data)
    } catch (e) { alert('Failed: ' + e.message) }
    setLoading('')
  }

  const BarMeter = ({ value, max = 100, color = 'indigo' }) => (
    <div className="h-2 bg-gray-700 rounded-full flex-1"><div className={`h-2 rounded-full bg-${color}-500`} style={{ width: `${Math.min(value, max)}%` }} /></div>
  )

  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold gradient-text">Weakness Drill</h1><p className="text-gray-400 mt-1">AI-targeted practice sessions for your weak areas</p></div>

      {loading === 'analyze' ? (
        <div className="flex items-center justify-center py-20"><Loader2 className="w-8 h-8 animate-spin text-indigo-400" /></div>
      ) : analysis ? (
        <div className="space-y-6">
          {/* Overview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
              <p className="text-sm text-gray-400">Total Attempts</p>
              <p className="text-3xl font-bold text-white mt-1">{analysis.total_attempts}</p>
            </div>
            <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
              <p className="text-sm text-gray-400">Solve Rate</p>
              <p className="text-3xl font-bold text-emerald-400 mt-1">{analysis.overall_solve_rate}%</p>
            </div>
            <div className="bg-gray-800/60 rounded-xl p-5 border border-gray-700">
              <p className="text-sm text-gray-400">Weak Patterns Found</p>
              <p className="text-3xl font-bold text-amber-400 mt-1">{analysis.weak_patterns?.length || 0}</p>
            </div>
          </div>

          {/* Weak Patterns */}
          {analysis.weak_patterns?.length > 0 && (
            <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><TrendingDown className="w-5 h-5 text-red-400" />Weakness Analysis</h2>
              <div className="space-y-3">
                {analysis.weak_patterns.map((wp, i) => (
                  <div key={i} className="flex items-center gap-4 p-3 bg-gray-900/50 rounded-lg">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-medium text-sm">{wp.pattern.replace(/_/g, ' ')}</span>
                        <span className={`text-xs px-2 py-0.5 rounded ${wp.weakness_score > 60 ? 'bg-red-500/20 text-red-400' : wp.weakness_score > 40 ? 'bg-amber-500/20 text-amber-400' : 'bg-green-500/20 text-green-400'}`}>
                          {wp.weakness_score > 60 ? 'Weak' : wp.weakness_score > 40 ? 'Needs Work' : 'OK'}
                        </span>
                      </div>
                      <div className="flex items-center gap-4 text-xs text-gray-400">
                        <span>Success: {wp.success_rate}%</span>
                        <span>Hints: {wp.hint_usage_rate}%</span>
                        <span>Avg time: {wp.avg_time_minutes}m</span>
                        <span>Attempts: {wp.total_attempts}</span>
                      </div>
                    </div>
                    <button onClick={() => handleGenerate(wp.pattern)} disabled={!!loading} className="px-3 py-1.5 bg-indigo-600/80 rounded-lg text-xs hover:bg-indigo-500 disabled:opacity-50 whitespace-nowrap flex items-center gap-1">
                      <Target className="w-3 h-3" />Drill This
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Difficulty Breakdown */}
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><BarChart3 className="w-5 h-5 text-indigo-400" />Difficulty Breakdown</h2>
            <div className="grid grid-cols-3 gap-4">
              {Object.entries(analysis.difficulty_breakdown || {}).map(([diff, stats]) => (
                <div key={diff} className="bg-gray-900/50 rounded-lg p-4">
                  <p className={`text-sm font-medium capitalize ${diff === 'easy' ? 'text-green-400' : diff === 'medium' ? 'text-amber-400' : 'text-red-400'}`}>{diff}</p>
                  <p className="text-lg font-bold mt-1">{stats.solved}/{stats.solved + stats.failed}</p>
                  <p className="text-xs text-gray-400">Avg: {stats.avg_time}m</p>
                </div>
              ))}
            </div>
          </div>

          {/* Custom Drill */}
          <div className="bg-gray-800/60 rounded-xl p-6 border border-gray-700">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2"><Zap className="w-5 h-5 text-amber-400" />Custom Drill Session</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div><label className="text-xs text-gray-400 block mb-1">Focus Pattern</label><input value={config.focus_pattern} onChange={e => setConfig({...config, focus_pattern: e.target.value})} className="w-full bg-gray-700 rounded-lg px-3 py-2 text-sm border border-gray-600" placeholder="e.g. sliding_window" /></div>
              <div><label className="text-xs text-gray-400 block mb-1">Difficulty</label>
                <select value={config.difficulty} onChange={e => setConfig({...config, difficulty: e.target.value})} className="w-full bg-gray-700 rounded-lg px-3 py-2 text-sm border border-gray-600">
                  <option value="">Progressive</option><option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option>
                </select></div>
              <div><label className="text-xs text-gray-400 block mb-1">Problems</label><input type="number" value={config.num_problems} onChange={e => setConfig({...config, num_problems: parseInt(e.target.value) || 5})} min={3} max={10} className="w-full bg-gray-700 rounded-lg px-3 py-2 text-sm border border-gray-600" /></div>
            </div>
            <button onClick={() => handleGenerate()} disabled={!!loading} className="px-6 py-2.5 bg-gradient-to-r from-indigo-600 to-emerald-600 rounded-lg text-sm font-semibold hover:opacity-90 disabled:opacity-50">
              {loading === 'generate' ? 'Generating...' : 'Generate Drill'}
            </button>
          </div>
        </div>
      ) : (
        <div className="text-center py-20 text-gray-400">
          <AlertTriangle className="w-12 h-12 mx-auto mb-4 text-gray-600" />
          <p>No attempt data yet. Solve some problems first!</p>
        </div>
      )}

      {/* Generated Drill */}
      {drill && (
        <div className="bg-gray-800/60 rounded-xl p-6 border border-indigo-500/30">
          <h2 className="text-xl font-bold text-indigo-400 mb-1">{drill.drill_title || 'Practice Drill'}</h2>
          {drill.target_weakness && <p className="text-sm text-gray-400 mb-2">Targeting: {drill.target_weakness}</p>}
          {drill.why_these_problems && <p className="text-sm text-gray-300 mb-4">{drill.why_these_problems}</p>}
          <div className="space-y-4">
            {(drill.problems || []).map((p, i) => (
              <div key={i} className="bg-gray-900/50 rounded-lg p-4 border border-gray-700">
                <div className="flex items-center gap-2 mb-2">
                  <span className="w-6 h-6 rounded-full bg-indigo-600/30 text-indigo-400 text-xs flex items-center justify-center font-bold">{i + 1}</span>
                  <span className="font-medium">{p.title}</span>
                  <span className={`text-xs px-2 py-0.5 rounded ${p.difficulty === 'easy' ? 'bg-green-500/20 text-green-400' : p.difficulty === 'hard' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'}`}>{p.difficulty}</span>
                  {p.target_pattern && <span className="text-xs text-gray-400">| {p.target_pattern}</span>}
                  {p.time_target_minutes && <span className="text-xs text-gray-400 ml-auto">{p.time_target_minutes} min</span>}
                </div>
                <div className="text-sm text-gray-300 prose prose-invert max-w-none"><ReactMarkdown>{p.description}</ReactMarkdown></div>
                {p.what_to_focus_on && <p className="text-xs text-amber-400 mt-2">Focus: {p.what_to_focus_on}</p>}
              </div>
            ))}
          </div>
          {drill.success_criteria && <p className="text-sm text-emerald-400 mt-4">Success: {drill.success_criteria}</p>}
        </div>
      )}
    </div>
  )
}
