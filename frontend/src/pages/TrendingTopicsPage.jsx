import { useState, useEffect } from 'react'
import { getTrendingTopics, getTopicDeepDive } from '../api/client'
import {
  TrendingUp, Loader2, ExternalLink, ChevronRight, ChevronDown, ChevronUp,
  Sparkles, Brain, Code2, MessageSquare, ArrowLeft, RefreshCw, Filter
} from 'lucide-react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import ReactMarkdown from 'react-markdown'
import TeachingModeWidget from '../components/TeachingModeWidget'

const CATEGORIES = [
  { value: 'all', label: 'All Topics' },
  { value: 'AI/ML', label: 'AI / ML' },
  { value: 'System Design', label: 'System Design' },
  { value: 'Languages & Frameworks', label: 'Languages' },
  { value: 'DevOps & Cloud', label: 'DevOps & Cloud' },
  { value: 'Architecture', label: 'Architecture' },
  { value: 'Security', label: 'Security' },
]

const CAT_COLORS = {
  'AI/ML': 'bg-purple-500/15 text-purple-400 border-purple-500/30',
  'System Design': 'bg-blue-500/15 text-blue-400 border-blue-500/30',
  'Languages & Frameworks': 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  'DevOps & Cloud': 'bg-amber-500/15 text-amber-400 border-amber-500/30',
  'Architecture': 'bg-indigo-500/15 text-indigo-400 border-indigo-500/30',
  'Security': 'bg-red-500/15 text-red-400 border-red-500/30',
  'Algorithms': 'bg-cyan-500/15 text-cyan-400 border-cyan-500/30',
}

export default function TrendingTopicsPage({ userId, user }) {
  const [loading, setLoading] = useState(true)
  const [data, setData] = useState(null)
  const [category, setCategory] = useState('all')
  const [expandedTopic, setExpandedTopic] = useState(null)
  const [deepDive, setDeepDive] = useState(null)
  const [deepDiveLoading, setDeepDiveLoading] = useState(false)
  const [deepDiveTopic, setDeepDiveTopic] = useState(null)

  const loadTopics = async (cat) => {
    setLoading(true); setExpandedTopic(null); setDeepDive(null); setDeepDiveTopic(null)
    try { setData(await getTrendingTopics(cat)) } catch {}
    setLoading(false)
  }

  useEffect(() => { loadTopics(category) }, [])

  const handleCategoryChange = (cat) => { setCategory(cat); loadTopics(cat) }

  const handleDeepDive = async (topic) => {
    setDeepDiveTopic(topic); setDeepDive(null); setDeepDiveLoading(true)
    try { setDeepDive(await getTopicDeepDive({ topic_title: topic.title, topic_context: topic.why_trending || '' })) } catch {}
    setDeepDiveLoading(false)
  }

  // Deep dive view
  if (deepDiveTopic) {
    return (
      <div className="space-y-6 animate-fade-in">
        <button onClick={() => { setDeepDiveTopic(null); setDeepDive(null) }} className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors">
          <ArrowLeft className="w-4 h-4" /> Back to Trending Topics
        </button>

        <div className="glass-card p-6 rounded-xl border border-indigo-500/30">
          <div className="flex items-center gap-3 mb-2">
            <span className={`text-xs px-2 py-0.5 rounded-full border ${CAT_COLORS[deepDiveTopic.category] || 'bg-gray-500/15 text-gray-400 border-gray-500/30'}`}>{deepDiveTopic.category}</span>
            <span className="text-[10px] text-gray-500">{deepDiveTopic.source}</span>
          </div>
          <h1 className="text-2xl font-bold gradient-text">{deepDiveTopic.title}</h1>
          <p className="text-gray-400 mt-1">{deepDiveTopic.why_trending}</p>
        </div>

        {deepDiveLoading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Brain className="w-10 h-10 text-indigo-400 animate-pulse mx-auto mb-3" />
              <p className="text-gray-400">Generating interview-ready deep dive...</p>
              <p className="text-gray-600 text-xs mt-1">Analyzing the topic from a senior engineer's perspective</p>
            </div>
          </div>
        ) : deepDive ? (
          <div className="space-y-6">
            {/* Overview */}
            {deepDive.overview && (
              <div className="p-4 bg-gradient-to-r from-indigo-500/10 to-emerald-500/10 rounded-xl border border-indigo-500/20">
                <p className="text-gray-200 font-medium">{deepDive.overview}</p>
              </div>
            )}

            {/* Sections */}
            {deepDive.sections?.map((section, i) => (
              <div key={i} className="glass-card p-6 rounded-xl">
                <h2 className="text-lg font-bold mb-3">{section.heading}</h2>
                <div className="prose prose-invert prose-sm max-w-none">
                  <ReactMarkdown components={{
                    code({ inline, className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '')
                      return !inline && match ? (
                        <SyntaxHighlighter style={oneDark} language={match[1]} PreTag="div" customStyle={{ borderRadius: '8px', fontSize: '0.8rem' }} {...props}>
                          {String(children).replace(/\n$/, '')}
                        </SyntaxHighlighter>
                      ) : <code className="text-indigo-300 bg-gray-800 px-1 rounded text-xs" {...props}>{children}</code>
                    }
                  }}>{section.content}</ReactMarkdown>
                </div>
                {section.key_points?.length > 0 && (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {section.key_points.map((kp, j) => <span key={j} className="text-xs px-2.5 py-1 bg-gray-800 rounded-lg text-gray-300 border border-gray-700">{kp}</span>)}
                  </div>
                )}
              </div>
            ))}

            {/* Code Example */}
            {deepDive.code_example?.code && (
              <div className="glass-card p-6 rounded-xl border border-emerald-500/20">
                <h2 className="text-lg font-bold mb-2 flex items-center gap-2"><Code2 className="w-5 h-5 text-emerald-400" /> Code Example</h2>
                {deepDive.code_example.explanation && <p className="text-sm text-gray-400 mb-3">{deepDive.code_example.explanation}</p>}
                <SyntaxHighlighter style={oneDark} language={deepDive.code_example.language || 'python'} customStyle={{ borderRadius: '8px', fontSize: '0.8rem' }}>
                  {deepDive.code_example.code}
                </SyntaxHighlighter>
              </div>
            )}

            {/* Interview Q&A */}
            {deepDive.interview_qa?.length > 0 && (
              <div className="glass-card p-6 rounded-xl border border-amber-500/20">
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2"><MessageSquare className="w-5 h-5 text-amber-400" /> Interview Questions & Answers</h2>
                <div className="space-y-4">
                  {deepDive.interview_qa.map((qa, i) => (
                    <div key={i} className="space-y-2">
                      <p className="text-sm font-semibold text-amber-300">Q: {qa.question}</p>
                      <div className="p-3 bg-gray-900/60 rounded-lg">
                        <p className="text-sm text-gray-300 leading-relaxed">{qa.strong_answer}</p>
                      </div>
                      {qa.follow_up && <p className="text-xs text-gray-500 italic ml-3">Follow-up: {qa.follow_up}</p>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Related Topics */}
            {deepDive.related_topics?.length > 0 && (
              <div className="glass-card p-6 rounded-xl">
                <h3 className="text-sm font-semibold text-gray-400 mb-3">Related Topics to Study</h3>
                <div className="flex flex-wrap gap-2">
                  {deepDive.related_topics.map((rt, i) => <span key={i} className="px-3 py-1.5 bg-indigo-500/10 text-indigo-300 rounded-lg text-sm border border-indigo-500/20">{rt}</span>)}
                </div>
              </div>
            )}

            {/* Teaching Modes */}
            <TeachingModeWidget topic={deepDiveTopic.title} compact />
          </div>
        ) : null}
      </div>
    )
  }

  // Main list view
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text">Trending in Tech</h1>
          <p className="text-gray-400 mt-1">Latest topics from the web, curated for interview prep</p>
        </div>
        <button onClick={() => loadTopics(category)} disabled={loading} className="flex items-center gap-2 px-4 py-2 bg-gray-800 rounded-lg text-sm text-gray-300 hover:bg-gray-700 disabled:opacity-50">
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} /> Refresh
        </button>
      </div>

      {/* Category Filters */}
      <div className="flex flex-wrap gap-2">
        {CATEGORIES.map(cat => (
          <button key={cat.value} onClick={() => handleCategoryChange(cat.value)} className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${category === cat.value ? 'bg-indigo-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-gray-200'}`}>
            {cat.label}
          </button>
        ))}
      </div>

      {data?.summary && <p className="text-sm text-indigo-400 bg-indigo-500/10 rounded-lg p-3 border border-indigo-500/20">{data.summary}</p>}

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="text-center">
            <TrendingUp className="w-10 h-10 text-indigo-400 animate-pulse mx-auto mb-3" />
            <p className="text-gray-400">Scanning Hacker News & dev.to for trending topics...</p>
            <p className="text-gray-600 text-xs mt-1">Filtering for interview relevance with AI</p>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Topic Cards */}
          {data?.topics?.map((topic, i) => (
            <div key={i} className="glass-card rounded-xl overflow-hidden hover:border-indigo-500/40 transition-all">
              <div className="p-5">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`text-[10px] px-2 py-0.5 rounded-full border ${CAT_COLORS[topic.category] || 'bg-gray-500/15 text-gray-400 border-gray-500/30'}`}>{topic.category}</span>
                      <span className="text-[10px] text-gray-600">{topic.source}</span>
                    </div>
                    <h3 className="text-lg font-semibold text-white">{topic.title}</h3>
                    <p className="text-sm text-gray-400 mt-1">{topic.why_trending}</p>
                  </div>
                  <button onClick={() => setExpandedTopic(expandedTopic === i ? null : i)} className="p-1.5 rounded-lg hover:bg-gray-800 text-gray-400">
                    {expandedTopic === i ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
                  </button>
                </div>

                {/* Key concepts */}
                {topic.key_concepts?.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-3">
                    {topic.key_concepts.map((kc, j) => <span key={j} className="text-[10px] px-2 py-0.5 bg-gray-800 rounded text-gray-300">{kc}</span>)}
                  </div>
                )}

                {/* Interview relevance badge */}
                {topic.interview_relevance && (
                  <p className="text-xs text-amber-400 mt-2 flex items-center gap-1"><Sparkles className="w-3 h-3" />{topic.interview_relevance}</p>
                )}
              </div>

              {/* Expanded Content */}
              {expandedTopic === i && (
                <div className="px-5 pb-5 space-y-4 border-t border-gray-800 pt-4 animate-fade-in">
                  {/* Deep Dive Text */}
                  {topic.deep_dive && (
                    <div className="prose prose-invert prose-sm max-w-none">
                      <ReactMarkdown>{topic.deep_dive}</ReactMarkdown>
                    </div>
                  )}

                  {/* Interview Questions */}
                  {topic.interview_questions?.length > 0 && (
                    <div className="space-y-2">
                      <h4 className="text-sm font-semibold text-amber-400">Sample Interview Questions</h4>
                      {topic.interview_questions.map((q, j) => (
                        <div key={j} className="flex items-start gap-2 p-2.5 bg-amber-500/5 rounded-lg border border-amber-500/10">
                          <MessageSquare className="w-3.5 h-3.5 text-amber-400 mt-0.5 flex-shrink-0" />
                          <p className="text-sm text-gray-300">{q}</p>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Resources */}
                  {topic.resources?.length > 0 && (
                    <div>
                      <h4 className="text-xs font-semibold text-gray-400 mb-1.5">Study Further</h4>
                      <div className="flex flex-wrap gap-2">
                        {topic.resources.map((r, j) => <span key={j} className="text-xs px-2.5 py-1 bg-gray-800 rounded-lg text-indigo-300 border border-gray-700">{r}</span>)}
                      </div>
                    </div>
                  )}

                  {/* Deep Dive Button */}
                  <button onClick={() => handleDeepDive(topic)} className="w-full py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg text-sm font-medium hover:opacity-90 transition-opacity flex items-center justify-center gap-2">
                    <Brain className="w-4 h-4" /> Full Interview Deep Dive
                  </button>
                </div>
              )}
            </div>
          ))}

          {(!data?.topics || data.topics.length === 0) && (
            <div className="text-center py-12 text-gray-500">
              <TrendingUp className="w-12 h-12 mx-auto mb-3 opacity-40" />
              <p>No topics found. Try a different category or refresh.</p>
            </div>
          )}

          {/* Source Attribution */}
          {data?._sources && (
            <div className="glass-card p-4 rounded-xl">
              <h4 className="text-xs font-semibold text-gray-500 mb-2">Sources</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <p className="text-[10px] text-orange-400 font-semibold mb-1.5">Hacker News</p>
                  {data._sources.hackernews?.slice(0, 5).map((s, i) => (
                    <div key={i} className="text-[11px] text-gray-400 truncate">
                      {s.url ? <a href={s.url} target="_blank" rel="noopener noreferrer" className="hover:text-indigo-300 flex items-center gap-1">{s.title} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" /></a> : s.title}
                    </div>
                  ))}
                </div>
                <div>
                  <p className="text-[10px] text-blue-400 font-semibold mb-1.5">dev.to</p>
                  {data._sources.devto?.slice(0, 5).map((s, i) => (
                    <div key={i} className="text-[11px] text-gray-400 truncate">
                      {s.url ? <a href={s.url} target="_blank" rel="noopener noreferrer" className="hover:text-indigo-300 flex items-center gap-1">{s.title} <ExternalLink className="w-2.5 h-2.5 flex-shrink-0" /></a> : s.title}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
