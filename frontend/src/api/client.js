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
