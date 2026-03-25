import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, Map, CalendarDays, Code2, MessageCircle,
  GraduationCap, LogOut, Zap, Trophy, GitBranch, Brain, Flame
} from 'lucide-react'

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/faang-prep', label: 'FAANG 75', icon: Flame },
  { path: '/roadmap', label: 'Roadmap', icon: Map },
  { path: '/daily', label: 'Daily Plan', icon: CalendarDays },
  { path: '/learn', label: 'Learn', icon: GraduationCap },
  { path: '/practice', label: 'Practice', icon: Code2 },
  { path: '/skill-tree', label: 'Skill Tree', icon: GitBranch },
  { path: '/review', label: 'Review', icon: Brain },
  { path: '/chat', label: 'AI Mentor', icon: MessageCircle },
]

export default function Layout({ children, user, onLogout }) {
  const location = useLocation()

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 flex-shrink-0 bg-gray-900/80 border-r border-gray-800 flex flex-col">
        {/* Logo */}
        <div className="p-5 border-b border-gray-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-emerald-500 flex items-center justify-center">
              <Zap className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-lg font-bold gradient-text">DSA Mentor</h1>
              <p className="text-xs text-gray-500">AI Interview Prep</p>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {navItems.map(({ path, label, icon: Icon }) => (
            <NavLink
              key={path}
              to={path}
              end={path === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-200
                ${isActive
                  ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-gray-800/60'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              {label}
            </NavLink>
          ))}
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-sm font-bold">
              {user?.name?.charAt(0)?.toUpperCase() || 'U'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium truncate">{user?.name || 'User'}</p>
              <p className="text-xs text-gray-500 truncate">{user?.experience_level || 'beginner'}</p>
            </div>
          </div>
          <button
            onClick={onLogout}
            className="flex items-center gap-2 text-xs text-gray-500 hover:text-red-400 transition-colors w-full px-2 py-1.5 rounded hover:bg-gray-800/50"
          >
            <LogOut className="w-3.5 h-3.5" />
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-gray-950">
        <div className="max-w-7xl mx-auto p-6">
          {children}
        </div>
      </main>
    </div>
  )
}
