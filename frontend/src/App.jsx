import { Routes, Route, Navigate } from 'react-router-dom'
import { useUser } from './hooks/useUser'
import Layout from './components/Layout'
import Onboarding from './pages/Onboarding'
import Dashboard from './pages/Dashboard'
import RoadmapPage from './pages/RoadmapPage'
import DailyPlanPage from './pages/DailyPlanPage'
import PracticePage from './pages/PracticePage'
import ChatPage from './pages/ChatPage'
import LearnPage from './pages/LearnPage'
import SkillTreePage from './pages/SkillTreePage'
import ReviewQueuePage from './pages/ReviewQueuePage'
import FAANGPrepPage from './pages/FAANGPrepPage'
import SystemDesignPage from './pages/SystemDesignPage'
import AIConceptsPage from './pages/AIConceptsPage'
import MockInterviewPage from './pages/MockInterviewPage'
import WeaknessDrillPage from './pages/WeaknessDrillPage'
import InterviewToolkitPage from './pages/InterviewToolkitPage'
import BehavioralPrepPage from './pages/BehavioralPrepPage'
import TrendingTopicsPage from './pages/TrendingTopicsPage'

function App() {
  const [user, setUser] = useUser()

  if (!user) {
    return <Onboarding onComplete={setUser} />
  }

  return (
    <Layout user={user} onLogout={() => setUser(null)}>
      <Routes>
        <Route path="/" element={<Dashboard userId={user.id} />} />
        <Route path="/roadmap" element={<RoadmapPage userId={user.id} />} />
        <Route path="/daily" element={<DailyPlanPage userId={user.id} />} />
        <Route path="/practice/:topicId?" element={<PracticePage userId={user.id} user={user} />} />
        <Route path="/learn/:topic?" element={<LearnPage userId={user.id} user={user} />} />
        <Route path="/skill-tree" element={<SkillTreePage userId={user.id} />} />
        <Route path="/review" element={<ReviewQueuePage userId={user.id} />} />
        <Route path="/faang-prep" element={<FAANGPrepPage userId={user.id} user={user} />} />
        <Route path="/system-design" element={<SystemDesignPage userId={user.id} user={user} />} />
        <Route path="/ai-concepts" element={<AIConceptsPage userId={user.id} user={user} />} />
        <Route path="/chat" element={<ChatPage userId={user.id} />} />
        <Route path="/mock-interview" element={<MockInterviewPage userId={user.id} user={user} />} />
        <Route path="/weakness-drill" element={<WeaknessDrillPage userId={user.id} user={user} />} />
        <Route path="/interview-toolkit" element={<InterviewToolkitPage userId={user.id} user={user} />} />
        <Route path="/behavioral-prep" element={<BehavioralPrepPage userId={user.id} user={user} />} />
        <Route path="/trending" element={<TrendingTopicsPage userId={user.id} user={user} />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Layout>
  )
}

export default App
