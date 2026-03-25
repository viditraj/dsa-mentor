import { useState, useRef, useEffect } from 'react'
import { Send, Bot, User, Sparkles, Loader2, Trash2, BookOpen, Code2, Lightbulb, Target } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import * as api from '../api/client'

const SUGGESTED_PROMPTS = [
  { icon: BookOpen, text: 'Explain two-pointer technique', color: 'text-blue-400' },
  { icon: Code2, text: 'How do I solve the "Two Sum" problem?', color: 'text-emerald-400' },
  { icon: Lightbulb, text: 'When should I use dynamic programming?', color: 'text-amber-400' },
  { icon: Target, text: 'What topics should I focus on for FAANG interviews?', color: 'text-purple-400' },
]

export default function ChatPage({ userId }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Hey! 👋 I'm your DSA Mentor AI. I can help you with:\n\n- **Explaining concepts** (arrays, trees, graphs, DP, etc.)\n- **Solving problems** step-by-step\n- **Interview tips** and strategies\n- **Time/space complexity** analysis\n- **Pattern recognition** for common problem types\n\nAsk me anything about Data Structures & Algorithms!`,
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)
  const inputRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  async function sendMessage(text) {
    const msg = text || input.trim()
    if (!msg || loading) return

    const userMessage = { role: 'user', content: msg }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await api.chatWithMentor({
        user_id: userId,
        message: msg,
        context: messages.slice(-6).map(m => `${m.role}: ${m.content}`).join('\n'),
      })
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: response.response || response.message || 'I couldn\'t process that. Try again!',
        suggestions: response.follow_up_questions || [],
      }])
    } catch (err) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I ran into an error. Please try again.',
      }])
    } finally {
      setLoading(false)
      inputRef.current?.focus()
    }
  }

  function clearChat() {
    setMessages([{
      role: 'assistant',
      content: 'Chat cleared! What would you like to learn about?',
    }])
  }

  return (
    <div className="flex flex-col h-[calc(100vh-2rem)] max-h-[calc(100vh-2rem)]">
      {/* Header */}
      <div className="flex items-center justify-between mb-4 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-white">DSA Mentor Chat</h1>
            <p className="text-xs text-gray-400">Ask anything about algorithms & data structures</p>
          </div>
        </div>
        <button
          onClick={clearChat}
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-gray-800 hover:bg-gray-700 text-gray-400 text-xs transition-colors"
        >
          <Trash2 className="w-3 h-3" /> Clear
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2 min-h-0">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 animate-fade-in ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}
          >
            {/* Avatar */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center ${
              msg.role === 'user'
                ? 'bg-indigo-500/20'
                : 'bg-gradient-to-br from-indigo-500/20 to-purple-500/20'
            }`}>
              {msg.role === 'user'
                ? <User className="w-4 h-4 text-indigo-400" />
                : <Sparkles className="w-4 h-4 text-purple-400" />
              }
            </div>

            {/* Message bubble */}
            <div className={`max-w-[80%] ${msg.role === 'user' ? 'ml-auto' : ''}`}>
              <div className={`rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-indigo-600 text-white rounded-tr-md'
                  : 'glass-card rounded-tl-md'
              }`}>
                {msg.role === 'assistant' ? (
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
                            customStyle={{ borderRadius: '0.5rem', fontSize: '0.8rem', margin: '0.5rem 0' }}
                            {...props}
                          >
                            {String(children).replace(/\n$/, '')}
                          </SyntaxHighlighter>
                        ) : (
                          <code className="px-1.5 py-0.5 rounded bg-gray-800 text-indigo-300 text-xs font-mono" {...props}>
                            {children}
                          </code>
                        )
                      },
                      p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                      ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                      ol: ({ children }) => <ol className="list-decimal list-inside mb-2 space-y-1">{children}</ol>,
                      strong: ({ children }) => <strong className="text-indigo-300 font-semibold">{children}</strong>,
                      h3: ({ children }) => <h3 className="font-bold text-white mt-3 mb-1">{children}</h3>,
                      h2: ({ children }) => <h2 className="font-bold text-white text-lg mt-3 mb-1">{children}</h2>,
                      table: ({ children }) => (
                        <div className="overflow-x-auto my-3 rounded-lg border border-gray-700">
                          <table className="w-full text-sm text-left">{children}</table>
                        </div>
                      ),
                      thead: ({ children }) => <thead className="bg-gray-800/80 text-gray-300 uppercase text-xs">{children}</thead>,
                      tbody: ({ children }) => <tbody className="divide-y divide-gray-800">{children}</tbody>,
                      tr: ({ children }) => <tr className="hover:bg-gray-800/40 transition-colors">{children}</tr>,
                      th: ({ children }) => <th className="px-3 py-2 font-semibold text-indigo-300 whitespace-nowrap">{children}</th>,
                      td: ({ children }) => <td className="px-3 py-2 text-gray-300">{children}</td>,
                      a: ({ href, children }) => <a href={href} target="_blank" rel="noopener noreferrer" className="text-indigo-400 hover:text-indigo-300 underline">{children}</a>,
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                ) : (
                  msg.content
                )}
              </div>

              {/* Follow-up suggestions */}
              {msg.suggestions?.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {msg.suggestions.map((q, idx) => (
                    <button
                      key={idx}
                      onClick={() => sendMessage(q)}
                      className="px-3 py-1.5 rounded-full bg-gray-800 hover:bg-gray-700 text-xs text-gray-300 hover:text-white border border-gray-700 transition-all"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="flex gap-3 animate-fade-in">
            <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-purple-400" />
            </div>
            <div className="glass-card rounded-2xl rounded-tl-md px-4 py-3 flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="w-2 h-2 rounded-full bg-gray-500 animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested prompts (show when few messages) */}
      {messages.length <= 1 && (
        <div className="grid grid-cols-2 gap-2 my-4 flex-shrink-0">
          {SUGGESTED_PROMPTS.map((prompt, i) => (
            <button
              key={i}
              onClick={() => sendMessage(prompt.text)}
              className="glass-card rounded-xl p-3 text-left hover:border-indigo-500/50 transition-all group"
            >
              <prompt.icon className={`w-4 h-4 ${prompt.color} mb-1.5`} />
              <p className="text-xs text-gray-400 group-hover:text-gray-300 transition-colors">{prompt.text}</p>
            </button>
          ))}
        </div>
      )}

      {/* Input */}
      <div className="flex-shrink-0 mt-3">
        <div className="flex items-center gap-2 glass-card rounded-xl p-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage()}
            placeholder="Ask about DSA concepts, problems, or interview tips..."
            className="flex-1 bg-transparent px-3 py-2 text-sm text-white placeholder-gray-500 focus:outline-none"
            disabled={loading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={!input.trim() || loading}
            className="flex items-center justify-center w-10 h-10 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 disabled:hover:bg-indigo-600 text-white transition-all"
          >
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  )
}
