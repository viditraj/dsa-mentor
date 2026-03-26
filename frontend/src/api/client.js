/** API client for DSA Mentor backend */
const API_BASE = '/api';

async function request(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };
  const res = await fetch(url, config);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || 'Request failed');
  }
  return res.json();
}

// ── Users ──
export const createUser = (data) =>
  request('/users/', { method: 'POST', body: JSON.stringify(data) });

export const getUser = (id) => request(`/users/${id}`);

export const getUserByEmail = (email) => request(`/users/by-email/${email}`);

export const updateUser = (id, data) =>
  request(`/users/${id}`, { method: 'PUT', body: JSON.stringify(data) });

// ── Roadmap ──
export const generateRoadmap = (userId) =>
  request(`/roadmap/${userId}/generate`, { method: 'POST' });

export const getRoadmap = (userId) => request(`/roadmap/${userId}`);

export const updateTopicStatus = (topicId, status) =>
  request(`/roadmap/topic/${topicId}/status?status=${status}`, { method: 'PUT' });

export const updateMasteryScore = (topicId, score) =>
  request(`/roadmap/topic/${topicId}/mastery?score=${score}`, { method: 'PUT' });

// ── Problems ──
export const getProblemsForTopic = (topicId) =>
  request(`/problems/topic/${topicId}`);

export const getTopicProblems = getProblemsForTopic;

export const getProblem = (id) => request(`/problems/${id}`);

export const submitSolution = (problemId, data) =>
  request(`/problems/${problemId}/submit`, { method: 'POST', body: JSON.stringify(data) });

export const getHint = (problemId, hintLevel = 1) =>
  request(`/problems/${problemId}/hint?hint_level=${hintLevel}`, { method: 'POST' });

export const aiSolve = (problemId) =>
  request(`/problems/${problemId}/ai-solve`, { method: 'POST' });

export const getAttempts = (userId, problemId) =>
  request(`/problems/${userId}/attempts/${problemId}`);

// ── Daily Plan ──
export const getTodayPlan = (userId) => request(`/daily-plan/${userId}/today`);

export const completeDay = (userId) =>
  request(`/daily-plan/${userId}/complete-day`, { method: 'POST' });

export const getLesson = (userId, topic, subtopic = null) => {
  let url = `/daily-plan/${userId}/teach/${encodeURIComponent(topic)}`;
  if (subtopic) url += `?subtopic=${encodeURIComponent(subtopic)}`;
  return request(url);
};

// ── Chat ──
export const sendMessage = (message, context = null) =>
  request('/chat/', { method: 'POST', body: JSON.stringify({ message, context }) });

export const chatWithMentor = (data) =>
  request('/chat/', { method: 'POST', body: JSON.stringify(data) });

// ── Stats ──
export const getStats = (userId) => request(`/stats/${userId}`);

export const getProgress = (userId) => request(`/stats/${userId}/progress`);

// ── Skill Tree ──
export const getSkillTree = (userId) => request(`/skill-tree/${userId}`);

export const getNodeDetails = (userId, topicName) =>
  request(`/skill-tree/${userId}/node/${encodeURIComponent(topicName)}`);

export const getBridgeLesson = (userId, fromTopic, toTopic) =>
  request(`/skill-tree/${userId}/bridge-lesson`, {
    method: 'POST',
    body: JSON.stringify({ from_topic: fromTopic, to_topic: toTopic }),
  });

// ── Spaced Repetition / Review ──
export const getReviewQueue = (userId, limit = 20) =>
  request(`/review/${userId}/queue?limit=${limit}`);

export const getUpcomingReviews = (userId, days = 7) =>
  request(`/review/${userId}/upcoming?days=${days}`);

export const getReviewStats = (userId) => request(`/review/${userId}/stats`);

export const createReviewCards = (userId, topicId) =>
  request(`/review/${userId}/cards/create`, {
    method: 'POST',
    body: JSON.stringify({ topic_id: topicId }),
  });

export const submitReview = (userId, cardId, quality) =>
  request(`/review/${userId}/cards/${cardId}/review`, {
    method: 'POST',
    body: JSON.stringify({ quality }),
  });

export const getReviewQuestion = (userId, cardId) =>
  request(`/review/${userId}/cards/${cardId}/question`);

export const triggerDecay = (userId) =>
  request(`/review/${userId}/decay`, { method: 'POST' });

// ── Video Tutorials ──
export const searchVideos = (topic, { problem, query, limit } = {}) => {
  const params = new URLSearchParams({ topic });
  if (problem) params.set('problem', problem);
  if (query) params.set('q', query);
  if (limit) params.set('limit', limit);
  return request(`/videos/search?${params}`);
};

export const getRecommendedVideos = (topic, limit = 5) =>
  request(`/videos/recommend/${encodeURIComponent(topic)}?limit=${limit}`);

// ── Pattern Recognition ──
export const getPatternCatalog = () => request('/patterns/catalog');

export const getPatternDetail = (key) => request(`/patterns/catalog/${key}`);

export const getProblemPatterns = (problemId) =>
  request(`/patterns/for-problem/${problemId}`);

export const matchPatterns = (title, description = '') => {
  const params = new URLSearchParams({ title });
  if (description) params.set('description', description);
  return request(`/patterns/match?${params}`);
};

export const analyzeCodePattern = (data) =>
  request('/patterns/analyze-code', { method: 'POST', body: JSON.stringify(data) });


export const generateTestCases = (data) =>
  request('/patterns/test-cases', { method: 'POST', body: JSON.stringify(data) });

// ── FAANG Prep ──
export const getFAANGOverview = () => request('/faang-prep/overview');

export const getFAANGProgress = (userId) => request(`/faang-prep/${userId}/progress`);

export const getFAANGQuestions = () => request('/faang-prep/questions');

export const getFAANGPatternQuestions = (patternKey) =>
  request(`/faang-prep/questions/pattern/${patternKey}`);

export const getFAANGPhaseQuestions = (phase) =>
  request(`/faang-prep/questions/phase/${phase}`);

export const getFAANGQuestionDetail = (questionId) =>
  request(`/faang-prep/question/${questionId}`);

export const getFAANGPatternDetail = (patternKey) =>
  request(`/faang-prep/pattern/${patternKey}`);

export const getFAANGPatternStory = (patternKey, language = 'python') =>
  request(`/faang-prep/pattern/${patternKey}/story?language=${language}`);

export const getFAANGQuestionWalkthrough = (questionId, language = 'python') =>
  request(`/faang-prep/question/${questionId}/walkthrough?language=${language}`);

export const submitFAANGQuestion = (data) =>
  request('/faang-prep/submit', { method: 'POST', body: JSON.stringify(data) });

export const markFAANGStoryRead = (userId, patternKey) =>
  request(`/faang-prep/${userId}/pattern/${patternKey}/mark-story-read`, { method: 'POST' });

export const markFAANGTemplatePracticed = (userId, patternKey) =>
  request(`/faang-prep/${userId}/pattern/${patternKey}/mark-template-practiced`, { method: 'POST' });

export const getFAANGMilestones = (userId) =>
  request(`/faang-prep/${userId}/milestones`);

export const getFAANGMotivation = (context = 'progress') =>
  request(`/faang-prep/motivation?context=${context}`);

// ── System Design ──
export const getSystemDesignOverview = () => request('/system-design/overview');

export const getSystemDesignConcepts = (phase = null, tag = null) => {
  const params = new URLSearchParams();
  if (phase) params.set('phase', phase);
  if (tag) params.set('tag', tag);
  const qs = params.toString();
  return request(`/system-design/concepts${qs ? `?${qs}` : ''}`);
};

export const getSystemDesignConcept = (conceptId) =>
  request(`/system-design/concept/${conceptId}`);

// ── AI/ML Concepts ──
export const getAIConceptsOverview = () => request('/ai-concepts/overview');

export const getAIConcepts = (phase = null, tag = null) => {
  const params = new URLSearchParams();
  if (phase) params.set('phase', phase);
  if (tag) params.set('tag', tag);
  const qs = params.toString();
  return request(`/ai-concepts/concepts${qs ? `?${qs}` : ''}`);
};

export const getAIConcept = (conceptId) =>
  request(`/ai-concepts/concept/${conceptId}`);

// ── Code Execution ──
export const executeCode = (data) =>
  request('/code/execute', { method: 'POST', body: JSON.stringify(data) });

export const runTestCases = (data) =>
  request('/code/run-tests', { method: 'POST', body: JSON.stringify(data) });

export const getSupportedLanguages = () => request('/code/languages');

// ── Mock Interview ──
export const startMockInterview = (data) =>
  request('/mock-interview/start', { method: 'POST', body: JSON.stringify(data) });

export const sendInterviewMessage = (data) =>
  request('/mock-interview/respond', { method: 'POST', body: JSON.stringify(data) });

export const endMockInterview = (sessionId) =>
  request(`/mock-interview/${sessionId}/end`, { method: 'POST' });

export const getInterviewHistory = (userId, limit = 10) =>
  request(`/mock-interview/${userId}/history?limit=${limit}`);

// ── Weakness Drill ──
export const analyzeWeaknesses = (userId) =>
  request(`/weakness-drill/${userId}/analyze`);

export const generateWeaknessDrill = (data) =>
  request('/weakness-drill/generate', { method: 'POST', body: JSON.stringify(data) });

// ── Complexity Analyzer ──
export const analyzeComplexity = (data) =>
  request('/complexity/analyze', { method: 'POST', body: JSON.stringify(data) });

// ── Interview Toolkit ──
export const getPatternQuiz = (userId, numQuestions = 10) =>
  request(`/interview-toolkit/${userId}/quiz?num_questions=${numQuestions}`);

export const scoreQuiz = (userId, answers) =>
  request(`/interview-toolkit/${userId}/quiz/score`, { method: 'POST', body: JSON.stringify({ answers }) });

export const getCheatSheet = (userId, focus = null) => {
  const params = focus ? `?focus=${encodeURIComponent(focus)}` : '';
  return request(`/interview-toolkit/${userId}/cheat-sheet${params}`);
};

export const getWarmup = (userId) =>
  request(`/interview-toolkit/${userId}/warmup`);

export const getCompanyFocus = (userId, company = 'google') =>
  request(`/interview-toolkit/${userId}/company-focus?company=${encodeURIComponent(company)}`);

// ── Problem Similarity ──
export const getSimilarProblems = (problemId, limit = 5) =>
  request(`/similarity/similar/${problemId}?limit=${limit}`);

export const getPatternFamily = (patternKey) =>
  request(`/similarity/pattern-family/${patternKey}`);

export const getPatternEvolution = (problemId) =>
  request(`/similarity/evolution/${problemId}`);

export const getProblemRecommendations = (userId, limit = 5) =>
  request(`/similarity/${userId}/recommendations?limit=${limit}`);

// ── Behavioral Prep ──
export const getBehavioralFrameworks = () => request('/behavioral/frameworks');

export const getCompanyFramework = (company) =>
  request(`/behavioral/frameworks/${company}`);

export const generateBehavioralQuestions = (data) =>
  request('/behavioral/questions', { method: 'POST', body: JSON.stringify(data) });

export const reviewBehavioralAnswer = (data) =>
  request('/behavioral/review-answer', { method: 'POST', body: JSON.stringify(data) });

export const getStarCoaching = (data) =>
  request('/behavioral/star-coaching', { method: 'POST', body: JSON.stringify(data) });

// ── Teaching Modes ──
export const teachELI5 = (data) =>
  request('/teaching/eli5', { method: 'POST', body: JSON.stringify(data) });

export const teachSocratic = (data) =>
  request('/teaching/socratic', { method: 'POST', body: JSON.stringify(data) });

// ── Trending Topics ──
export const getTrendingTopics = (category = 'all') =>
  request(`/trending/?category=${encodeURIComponent(category)}`);

export const getTopicDeepDive = (data) =>
  request('/trending/deep-dive', { method: 'POST', body: JSON.stringify(data) });
