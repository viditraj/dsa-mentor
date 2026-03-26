import { useState } from 'react'
import { Zap, ArrowRight, Target, Clock, Code2, Building2, LogIn } from 'lucide-react'
import { createUser, getUserByEmail, generateRoadmap } from '../api/client'

const EXPERIENCE_LEVELS = [
  { value: 'beginner', label: 'Beginner', desc: 'New to DSA, know basic programming', color: 'from-green-500 to-emerald-600' },
  { value: 'intermediate', label: 'Intermediate', desc: 'Know arrays, basic sorting, some trees', color: 'from-yellow-500 to-orange-500' },
  { value: 'advanced', label: 'Advanced', desc: 'Familiar with most topics, need practice', color: 'from-red-500 to-pink-600' },
]

const LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'go', label: 'Go' },
]

export default function Onboarding({ onComplete }) {
  const [step, setStep] = useState(0)
  const [mode, setMode] = useState('signup') // 'signup' or 'login'
  const [loading, setLoading] = useState(false)
  const [loginEmail, setLoginEmail] = useState('')
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    experience_level: 'beginner',
    preferred_language: 'python',
    daily_hours: 2,
    target_company: '',
  })

  const handleLogin = async () => {
    if (!loginEmail.trim()) return
    setLoading(true)
    try {
      const user = await getUserByEmail(loginEmail.trim())
      onComplete(user)
    } catch (err) {
      alert('No account found with that email. Please sign up first.')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const user = await createUser(formData)
      // Auto-generate roadmap
      await generateRoadmap(user.id)
      onComplete(user)
    } catch (err) {
      // If email already registered, try to log them in automatically
      if (err.message?.toLowerCase().includes('already registered')) {
        try {
          const user = await getUserByEmail(formData.email)
          onComplete(user)
          return
        } catch {}
      }
      alert(err.message || 'Failed to create profile')
    } finally {
      setLoading(false)
    }
  }

  const steps = [
    // Step 0: Welcome
    <div key="welcome" className="text-center animate-fade-in">
      <div className="w-20 h-20 mx-auto mb-6 rounded-2xl bg-gradient-to-br from-indigo-500 to-emerald-500 flex items-center justify-center animate-pulse-glow">
        <Zap className="w-10 h-10 text-white" />
      </div>
      <h1 className="text-4xl font-bold mb-3">
        <span className="gradient-text">DSA Mentor</span>
      </h1>
      <p className="text-gray-400 text-lg mb-8 max-w-md mx-auto">
        Your AI-powered personal coach for mastering Data Structures & Algorithms.
        Get a personalized roadmap, daily lessons, and crack any tech interview.
      </p>

      {mode === 'signup' ? (
        <>
          <button
            onClick={() => setStep(1)}
            className="inline-flex items-center gap-2 px-8 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 rounded-xl text-white font-semibold transition-all duration-200 shadow-lg shadow-indigo-500/25"
          >
            Get Started <ArrowRight className="w-5 h-5" />
          </button>
          <p className="mt-4 text-sm text-gray-500">
            Already have an account?{' '}
            <button onClick={() => setMode('login')} className="text-indigo-400 hover:text-indigo-300 font-medium">
              Sign In
            </button>
          </p>
        </>
      ) : (
        <div className="max-w-sm mx-auto text-left">
          <label className="block text-sm font-medium text-gray-300 mb-1.5">Email</label>
          <input
            type="email"
            value={loginEmail}
            onChange={e => setLoginEmail(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleLogin()}
            placeholder="your@email.com"
            className="w-full px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          />
          <button
            onClick={handleLogin}
            disabled={loading || !loginEmail.trim()}
            className="mt-4 w-full inline-flex items-center justify-center gap-2 px-8 py-3 bg-gradient-to-r from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 rounded-xl text-white font-semibold transition-all duration-200 shadow-lg shadow-indigo-500/25 disabled:opacity-50"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            ) : (
              <><LogIn className="w-5 h-5" /> Sign In</>
            )}
          </button>
          <p className="mt-4 text-sm text-gray-500 text-center">
            Don't have an account?{' '}
            <button onClick={() => setMode('signup')} className="text-indigo-400 hover:text-indigo-300 font-medium">
              Sign Up
            </button>
          </p>
        </div>
      )}
    </div>,

    // Step 1: Name & Email
    <div key="info" className="animate-slide-up max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-2">Let's get to know you</h2>
      <p className="text-gray-400 mb-6">Tell us about yourself so we can personalize your learning journey.</p>
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1.5">Your Name</label>
          <input
            type="text"
            value={formData.name}
            onChange={e => setFormData({ ...formData, name: e.target.value })}
            placeholder="Enter your name"
            className="w-full px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-300 mb-1.5">Email</label>
          <input
            type="email"
            value={formData.email}
            onChange={e => setFormData({ ...formData, email: e.target.value })}
            placeholder="your@email.com"
            className="w-full px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          />
        </div>
      </div>
      <button
        onClick={() => setStep(2)}
        disabled={!formData.name || !formData.email}
        className="mt-6 w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:bg-gray-700 disabled:text-gray-500 rounded-xl text-white font-semibold transition-all"
      >
        Continue <ArrowRight className="w-5 h-5" />
      </button>
    </div>,

    // Step 2: Experience Level
    <div key="experience" className="animate-slide-up max-w-lg mx-auto">
      <h2 className="text-2xl font-bold mb-2">What's your DSA experience?</h2>
      <p className="text-gray-400 mb-6">This helps us calibrate your learning roadmap.</p>
      <div className="space-y-3">
        {EXPERIENCE_LEVELS.map(level => (
          <button
            key={level.value}
            onClick={() => setFormData({ ...formData, experience_level: level.value })}
            className={`w-full text-left p-4 rounded-xl border transition-all duration-200
              ${formData.experience_level === level.value
                ? 'border-indigo-500 bg-indigo-500/10'
                : 'border-gray-700 bg-gray-800/50 hover:border-gray-600'}`}
          >
            <div className="flex items-center gap-3">
              <div className={`w-3 h-3 rounded-full bg-gradient-to-r ${level.color}`} />
              <span className="font-semibold">{level.label}</span>
            </div>
            <p className="text-sm text-gray-400 mt-1 ml-6">{level.desc}</p>
          </button>
        ))}
      </div>
      <button
        onClick={() => setStep(3)}
        className="mt-6 w-full flex items-center justify-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 rounded-xl text-white font-semibold transition-all"
      >
        Continue <ArrowRight className="w-5 h-5" />
      </button>
    </div>,

    // Step 3: Preferences
    <div key="prefs" className="animate-slide-up max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-2">Your preferences</h2>
      <p className="text-gray-400 mb-6">Fine-tune your study plan.</p>
      <div className="space-y-4">
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-1.5">
            <Code2 className="w-4 h-4" /> Preferred Language
          </label>
          <div className="flex flex-wrap gap-2">
            {LANGUAGES.map(lang => (
              <button
                key={lang.value}
                onClick={() => setFormData({ ...formData, preferred_language: lang.value })}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all
                  ${formData.preferred_language === lang.value
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}
              >
                {lang.label}
              </button>
            ))}
          </div>
        </div>
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-1.5">
            <Clock className="w-4 h-4" /> Daily Study Hours
          </label>
          <input
            type="range"
            min="0.5"
            max="6"
            step="0.5"
            value={formData.daily_hours}
            onChange={e => setFormData({ ...formData, daily_hours: parseFloat(e.target.value) })}
            className="w-full accent-indigo-500"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>30 min</span>
            <span className="text-indigo-400 font-semibold">{formData.daily_hours} hours/day</span>
            <span>6 hours</span>
          </div>
        </div>
        <div>
          <label className="flex items-center gap-2 text-sm font-medium text-gray-300 mb-1.5">
            <Building2 className="w-4 h-4" /> Target Company (optional)
          </label>
          <input
            type="text"
            value={formData.target_company}
            onChange={e => setFormData({ ...formData, target_company: e.target.value })}
            placeholder="e.g. Google, Amazon, Meta..."
            className="w-full px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none text-white placeholder-gray-500"
          />
        </div>
      </div>
      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-6 w-full flex items-center justify-center gap-2 px-6 py-3 bg-gradient-to-r from-indigo-600 to-emerald-600 hover:from-indigo-500 hover:to-emerald-500 rounded-xl text-white font-semibold transition-all shadow-lg shadow-indigo-500/25 disabled:opacity-50"
      >
        {loading ? (
          <>
            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
            Building your personalized roadmap...
          </>
        ) : (
          <>
            <Target className="w-5 h-5" /> Launch My DSA Journey
          </>
        )}
      </button>
    </div>,
  ]

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-6">
      {/* Background decoration */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-600/10 rounded-full blur-3xl" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-emerald-600/10 rounded-full blur-3xl" />
      </div>

      <div className="relative z-10 w-full max-w-2xl">
        {/* Progress dots */}
        <div className="flex items-center justify-center gap-2 mb-8">
          {[0, 1, 2, 3].map(i => (
            <div
              key={i}
              className={`h-1.5 rounded-full transition-all duration-300
                ${i === step ? 'w-8 bg-indigo-500' : i < step ? 'w-4 bg-indigo-400' : 'w-4 bg-gray-700'}`}
            />
          ))}
        </div>

        {steps[step]}
      </div>
    </div>
  )
}
