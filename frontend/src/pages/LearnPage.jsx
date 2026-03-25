import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import {
  BookOpen, Code2, Clock, AlertTriangle, Lightbulb,
  Eye, ChevronLeft, ChevronRight, Play, Pause, Youtube,
  ExternalLink, ThumbsUp, Search, Star, Loader2, X
} from 'lucide-react'
import { getLesson, getRecommendedVideos, searchVideos } from '../api/client'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import AlgorithmVisualizer from '../visualizations/AlgorithmVisualizer'

/** Strip markdown code fences (```python ... ```) that LLM may wrap around code */
function stripCodeFences(code) {
  if (!code) return ''
  let s = code.trim()
  // Remove opening fence: ```python or ```js or just ```
  s = s.replace(/^```[\w]*\n?/, '')
  // Remove closing fence
  s = s.replace(/\n?```\s*$/, '')
  return s.trim()
}

export default function LearnPage({ userId, user }) {
  const { topic } = useParams()
  const [lesson, setLesson] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('explanation')
  const [currentStep, setCurrentStep] = useState(0)

  const topicName = topic ? decodeURIComponent(topic) : 'Arrays - Basics & Traversal'

  useEffect(() => {
    if (topicName) {
      loadLesson(topicName)
    }
  }, [topicName, userId])

  async function loadLesson(t) {
    setLoading(true)
    try {
      const data = await getLesson(userId, t)
      setLesson(data)
      setCurrentStep(0)
    } catch (err) {
      // Use fallback lesson
      setLesson({
        title: t,
        explanation: `# ${t}\n\nLoading lesson content...`,
        walkthrough_steps: [],
        code: '# Code example will appear here',
        complexity: { time: 'O(?)', space: 'O(?)' },
        common_mistakes: [],
        practice_tips: [],
        visualization_type: 'array',
        visualization_data: { initial_state: [5, 3, 8, 1, 9, 2, 7], operations: [] }
      })
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="w-8 h-8 border-2 border-indigo-500/30 border-t-indigo-500 rounded-full animate-spin mx-auto mb-4" />
          <p className="text-gray-400">Generating lesson with AI...</p>
        </div>
      </div>
    )
  }

  if (!lesson) {
    return (
      <div className="text-center py-20">
        <BookOpen className="w-12 h-12 text-gray-600 mx-auto mb-4" />
        <h2 className="text-xl font-bold mb-2">Select a topic to learn</h2>
        <p className="text-gray-400">Choose a topic from your roadmap or search for one.</p>
      </div>
    )
  }

  const tabs = [
    { id: 'explanation', label: 'Explanation', icon: BookOpen },
    { id: 'videos', label: 'Videos', icon: Youtube },
    { id: 'visualization', label: 'Visualization', icon: Eye },
    { id: 'code', label: 'Code', icon: Code2 },
    { id: 'tips', label: 'Tips & Mistakes', icon: AlertTriangle },
  ]

  const steps = lesson.walkthrough_steps || []

  return (
    <div className="space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold">{lesson.title || topicName}</h1>
        {lesson.analogy && (
          <p className="text-gray-400 mt-2 italic">💡 {lesson.analogy}</p>
        )}
        <div className="flex items-center gap-4 mt-3">
          {lesson.complexity && (
            <>
              <span className="flex items-center gap-1 text-xs px-2.5 py-1 bg-indigo-500/10 text-indigo-400 rounded-full border border-indigo-500/20">
                <Clock className="w-3 h-3" /> Time: {lesson.complexity.time}
              </span>
              <span className="flex items-center gap-1 text-xs px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20">
                Space: {lesson.complexity.space}
              </span>
            </>
          )}
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 p-1 bg-gray-900 rounded-lg w-fit">
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all
              ${activeTab === tab.id
                ? 'bg-indigo-600 text-white'
                : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800'
              }`}
          >
            <tab.icon className="w-4 h-4" />
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      <div className="glass-card p-6">
        {activeTab === 'explanation' && (
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                code({ node, inline, className, children, ...props }) {
                  const match = /language-(\w+)/.exec(className || '')
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={oneDark}
                      language={match[1]}
                      PreTag="div"
                      customStyle={{ borderRadius: '8px', margin: '16px 0' }}
                      {...props}
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className="bg-gray-800 px-1.5 py-0.5 rounded text-indigo-300 text-sm" {...props}>
                      {children}
                    </code>
                  )
                },
                table: ({children}) => (
                  <div className="overflow-x-auto my-4 rounded-lg border border-gray-700">
                    <table className="w-full text-sm text-left">{children}</table>
                  </div>
                ),
                thead: ({children}) => <thead className="bg-gray-800 text-gray-200 text-xs uppercase">{children}</thead>,
                tbody: ({children}) => <tbody className="divide-y divide-gray-700">{children}</tbody>,
                tr: ({children}) => <tr className="hover:bg-gray-800/40 transition-colors">{children}</tr>,
                th: ({children}) => <th className="px-4 py-3 font-semibold text-gray-200">{children}</th>,
                td: ({children}) => <td className="px-4 py-2.5 text-gray-300">{children}</td>,
                h1: ({children}) => <h1 className="text-2xl font-bold text-white mb-4">{children}</h1>,
                h2: ({children}) => <h2 className="text-xl font-bold text-white mt-8 mb-3 pb-2 border-b border-gray-800">{children}</h2>,
                h3: ({children}) => <h3 className="text-lg font-semibold text-gray-200 mt-5 mb-2">{children}</h3>,
                p: ({children}) => <p className="text-gray-300 leading-relaxed mb-3">{children}</p>,
                ul: ({children}) => <ul className="space-y-2 mb-4 ml-4">{children}</ul>,
                ol: ({children}) => <ol className="space-y-2 mb-4 ml-4 list-decimal">{children}</ol>,
                li: ({children}) => <li className="text-gray-300 list-disc">{children}</li>,
                strong: ({children}) => <strong className="text-white font-semibold">{children}</strong>,
                blockquote: ({children}) => (
                  <blockquote className="border-l-4 border-indigo-500 pl-4 my-4 italic text-gray-400">{children}</blockquote>
                ),
              }}
            >
              {lesson.explanation || 'No explanation available.'}
            </ReactMarkdown>

            {/* Supplementary sections from lesson data */}
            {lesson.variations?.length > 0 && !lesson.explanation?.includes('Variation') && (
              <div className="mt-8 p-5 rounded-xl bg-indigo-500/5 border border-indigo-500/20">
                <h3 className="text-lg font-semibold text-indigo-300 mb-3 flex items-center gap-2">🔀 Variations & Related Techniques</h3>
                <ul className="space-y-2">
                  {lesson.variations.map((v, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="text-indigo-400 mt-0.5">•</span>
                      <span>{v}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {lesson.common_mistakes?.length > 0 && !lesson.explanation?.includes('Common Mistake') && (
              <div className="mt-4 p-5 rounded-xl bg-red-500/5 border border-red-500/20">
                <h3 className="text-lg font-semibold text-red-300 mb-3 flex items-center gap-2">⚠️ Common Mistakes</h3>
                <ul className="space-y-2">
                  {lesson.common_mistakes.map((m, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="text-red-400 mt-0.5">✗</span>
                      <span>{m}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {lesson.practice_tips?.length > 0 && !lesson.explanation?.includes('Practice') && (
              <div className="mt-4 p-5 rounded-xl bg-emerald-500/5 border border-emerald-500/20">
                <h3 className="text-lg font-semibold text-emerald-300 mb-3 flex items-center gap-2">🎯 Practice Tips</h3>
                <ul className="space-y-2">
                  {lesson.practice_tips.map((t, i) => (
                    <li key={i} className="flex items-start gap-2 text-sm text-gray-300">
                      <span className="text-emerald-400 mt-0.5">✓</span>
                      <span>{t}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {lesson.interview_problems?.length > 0 && (
              <div className="mt-4 p-5 rounded-xl bg-purple-500/5 border border-purple-500/20">
                <h3 className="text-lg font-semibold text-purple-300 mb-3 flex items-center gap-2">📝 Practice These Problems</h3>
                <div className="flex flex-wrap gap-2">
                  {lesson.interview_problems.map((p, i) => (
                    <span key={i} className="px-3 py-1.5 rounded-lg bg-purple-500/10 text-purple-300 text-sm border border-purple-500/20">
                      {p}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === 'videos' && (
          <VideoTutorials topicName={topicName} />
        )}

        {activeTab === 'visualization' && (
          <div>
            {/* Step-by-step walkthrough */}
            {steps.length > 0 && (
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold">Step-by-Step Walkthrough</h3>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => setCurrentStep(Math.max(0, currentStep - 1))}
                      disabled={currentStep === 0}
                      className="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 disabled:opacity-30 transition-all"
                    >
                      <ChevronLeft className="w-4 h-4" />
                    </button>
                    <span className="text-sm text-gray-400 mx-2">
                      Step {currentStep + 1} / {steps.length}
                    </span>
                    <button
                      onClick={() => setCurrentStep(Math.min(steps.length - 1, currentStep + 1))}
                      disabled={currentStep >= steps.length - 1}
                      className="p-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 disabled:opacity-30 transition-all"
                    >
                      <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>

                {/* Current Step */}
                <div className="p-4 bg-gray-800/50 border border-gray-700/50 rounded-lg animate-slide-up" key={currentStep}>
                  <p className="text-gray-200 font-medium mb-2">{steps[currentStep]?.description}</p>
                  <div className="flex items-center gap-4 text-sm">
                    {steps[currentStep]?.state && (
                      <span className="text-gray-400">State: <code className="text-indigo-300">{steps[currentStep].state}</code></span>
                    )}
                    {steps[currentStep]?.highlight && (
                      <span className="text-yellow-400">🎯 {steps[currentStep].highlight}</span>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Visual Algorithm Display */}
            <AlgorithmVisualizer
              type={lesson.visualization_type || 'array'}
              data={lesson.visualization_data || { initial_state: [5, 3, 8, 1, 9, 2, 7] }}
              step={currentStep}
              topicName={topicName}
            />
          </div>
        )}

        {activeTab === 'code' && (
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold">Implementation</h3>
              <span className="text-xs px-2 py-1 bg-gray-800 rounded text-gray-400">
                {user?.preferred_language || 'python'}
              </span>
            </div>
            <SyntaxHighlighter
              language={user?.preferred_language === 'cpp' ? 'cpp' : user?.preferred_language || 'python'}
              style={oneDark}
              customStyle={{ borderRadius: '8px', fontSize: '14px' }}
              showLineNumbers
            >
              {stripCodeFences(lesson.code) || '# Code will appear here when AI generates the lesson'}
            </SyntaxHighlighter>
          </div>
        )}

        {activeTab === 'tips' && (
          <div className="space-y-6">
            {/* Common Mistakes */}
            {lesson.common_mistakes?.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2 mb-3">
                  <AlertTriangle className="w-5 h-5 text-red-400" /> Common Mistakes
                </h3>
                <div className="space-y-2">
                  {lesson.common_mistakes.map((mistake, i) => (
                    <div key={i} className="flex items-start gap-3 p-3 bg-red-500/5 border border-red-500/20 rounded-lg">
                      <span className="text-red-400 font-bold text-sm mt-0.5">✗</span>
                      <p className="text-sm text-gray-300">{mistake}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Practice Tips */}
            {lesson.practice_tips?.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold flex items-center gap-2 mb-3">
                  <Lightbulb className="w-5 h-5 text-yellow-400" /> Practice Tips
                </h3>
                <div className="space-y-2">
                  {lesson.practice_tips.map((tip, i) => (
                    <div key={i} className="flex items-start gap-3 p-3 bg-yellow-500/5 border border-yellow-500/20 rounded-lg">
                      <span className="text-yellow-400 font-bold text-sm mt-0.5">💡</span>
                      <p className="text-sm text-gray-300">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Variations */}
            {lesson.variations?.length > 0 && (
              <div>
                <h3 className="text-lg font-semibold mb-3">Variations</h3>
                <div className="flex flex-wrap gap-2">
                  {lesson.variations.map((v, i) => (
                    <span key={i} className="px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-lg text-sm text-gray-300">
                      {v}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}


/* ─── Video Tutorials Component ─── */
function VideoTutorials({ topicName }) {
  const [videos, setVideos] = useState([])
  const [bestPick, setBestPick] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeVideo, setActiveVideo] = useState(null)
  const [customSearch, setCustomSearch] = useState('')
  const [searching, setSearching] = useState(false)

  useEffect(() => {
    loadVideos()
  }, [topicName])

  async function loadVideos() {
    setLoading(true)
    setActiveVideo(null)
    try {
      const data = await getRecommendedVideos(topicName, 8)
      setVideos(data.videos || [])
      setBestPick(data.best_pick || null)
    } catch (e) {
      console.error('Failed to load videos:', e)
      setVideos([])
    } finally {
      setLoading(false)
    }
  }

  async function handleCustomSearch(e) {
    e.preventDefault()
    if (!customSearch.trim()) return
    setSearching(true)
    try {
      const data = await searchVideos(topicName, { query: customSearch.trim(), limit: 8 })
      setVideos(data.videos || [])
      setBestPick(data.best_pick || null)
    } catch (e) {
      console.error(e)
    } finally {
      setSearching(false)
    }
  }

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-16">
        <Loader2 className="w-8 h-8 animate-spin text-red-400 mb-3" />
        <p className="text-sm text-gray-500">Finding the best video tutorials...</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Custom search */}
      <form onSubmit={handleCustomSearch} className="flex gap-2">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          <input
            type="text"
            value={customSearch}
            onChange={e => setCustomSearch(e.target.value)}
            placeholder={`Search videos for "${topicName}"...`}
            className="w-full pl-10 pr-4 py-2.5 bg-gray-800/60 border border-gray-700 rounded-lg text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-indigo-500/50"
          />
        </div>
        <button
          type="submit"
          disabled={searching}
          className="px-4 py-2.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg text-sm font-medium border border-red-500/30 disabled:opacity-50 flex items-center gap-2"
        >
          {searching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Youtube className="w-4 h-4" />}
          Search
        </button>
        <button
          type="button"
          onClick={loadVideos}
          className="px-3 py-2.5 text-gray-400 hover:text-gray-200 text-sm"
          title="Reset to recommendations"
        >
          Reset
        </button>
      </form>

      {/* Embedded player */}
      {activeVideo && (
        <div className="space-y-2 animate-fade-in">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-semibold text-gray-200 truncate flex-1 mr-3">
              <Play className="w-4 h-4 inline mr-1 text-red-400" />
              {activeVideo.title}
            </h3>
            <button
              onClick={() => setActiveVideo(null)}
              className="p-1 text-gray-500 hover:text-gray-300 rounded"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
          <div className="relative w-full rounded-xl overflow-hidden bg-black" style={{ paddingBottom: '56.25%' }}>
            <iframe
              className="absolute inset-0 w-full h-full"
              src={`${activeVideo.embed_url}?autoplay=1&rel=0`}
              title={activeVideo.title}
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          </div>
          <div className="flex items-center gap-3 text-xs text-gray-500">
            <span>{activeVideo.channel}</span>
            <span>•</span>
            <span>{activeVideo.views}</span>
            <span>•</span>
            <span>{activeVideo.duration}</span>
            <a
              href={activeVideo.url}
              target="_blank"
              rel="noopener noreferrer"
              className="ml-auto flex items-center gap-1 text-red-400 hover:text-red-300"
            >
              Open in YouTube <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      )}

      {/* Best pick highlight */}
      {bestPick && !activeVideo && (
        <div
          className="p-4 bg-gradient-to-r from-red-950/30 to-gray-900 border border-red-500/20 rounded-xl cursor-pointer hover:border-red-500/40 transition-all group"
          onClick={() => setActiveVideo(bestPick)}
        >
          <div className="flex gap-4">
            <div className="relative flex-shrink-0 w-48 h-28 rounded-lg overflow-hidden bg-gray-800">
              {bestPick.thumbnail ? (
                <img src={bestPick.thumbnail} alt={bestPick.title} className="w-full h-full object-cover" />
              ) : (
                <div className="w-full h-full flex items-center justify-center">
                  <Youtube className="w-8 h-8 text-gray-600" />
                </div>
              )}
              <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <Play className="w-10 h-10 text-white" fill="white" />
              </div>
              <span className="absolute bottom-1 right-1 text-[10px] bg-black/80 text-white px-1.5 py-0.5 rounded">
                {bestPick.duration}
              </span>
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <Star className="w-4 h-4 text-yellow-400" />
                <span className="text-xs font-medium text-yellow-400">TOP PICK</span>
              </div>
              <h3 className="font-semibold text-gray-100 line-clamp-2 group-hover:text-white transition-colors">
                {bestPick.title}
              </h3>
              <div className="flex items-center gap-2 mt-2 text-xs text-gray-500">
                <span className={bestPick.is_trusted_channel ? 'text-green-400 font-medium' : ''}>
                  {bestPick.channel}
                </span>
                {bestPick.is_trusted_channel && <span className="text-green-600">✓ Trusted</span>}
                <span>•</span>
                <span>{bestPick.views}</span>
                <span>•</span>
                <span>{bestPick.published}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Video grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {videos
          .filter(v => !activeVideo || v.id !== activeVideo.id)
          .filter(v => !bestPick || activeVideo || v.id !== bestPick.id)
          .map(video => (
            <div
              key={video.id}
              className="flex gap-3 p-3 bg-gray-800/30 border border-gray-700/50 rounded-lg cursor-pointer hover:border-gray-600 hover:bg-gray-800/50 transition-all group"
              onClick={() => setActiveVideo(video)}
            >
              <div className="relative flex-shrink-0 w-36 h-20 rounded-lg overflow-hidden bg-gray-800">
                {video.thumbnail ? (
                  <img src={video.thumbnail} alt={video.title} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <Youtube className="w-6 h-6 text-gray-600" />
                  </div>
                )}
                <div className="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                  <Play className="w-7 h-7 text-white" fill="white" />
                </div>
                <span className="absolute bottom-0.5 right-0.5 text-[10px] bg-black/80 text-white px-1 py-0.5 rounded">
                  {video.duration}
                </span>
              </div>
              <div className="flex-1 min-w-0">
                <h4 className="text-sm font-medium text-gray-200 line-clamp-2 group-hover:text-white transition-colors">
                  {video.title}
                </h4>
                <div className="flex items-center gap-2 mt-1.5 text-xs text-gray-500">
                  <span className={video.is_trusted_channel ? 'text-green-400' : ''}>
                    {video.channel}
                  </span>
                  {video.is_trusted_channel && <span className="text-green-600 text-[10px]">✓</span>}
                </div>
                <div className="flex items-center gap-2 mt-0.5 text-[11px] text-gray-600">
                  <span>{video.views}</span>
                  <span>•</span>
                  <span>{video.published}</span>
                </div>
              </div>
            </div>
          ))}
      </div>

      {videos.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          <Youtube className="w-10 h-10 mx-auto mb-3 opacity-40" />
          <p>No videos found. Try a different search.</p>
        </div>
      )}
    </div>
  )
}
