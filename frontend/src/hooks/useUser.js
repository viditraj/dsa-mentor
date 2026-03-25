import { useState, useEffect, useCallback } from 'react';

/** Persistent user state stored in localStorage.
 *  Validates user still exists in DB on mount — auto-clears if DB was reset. */
export function useUser() {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('dsa_mentor_user');
      return saved ? JSON.parse(saved) : null;
    } catch { return null; }
  });

  // Validate that the stored user still exists in the DB
  useEffect(() => {
    if (!user?.id) return;
    fetch(`/api/users/${user.id}`)
      .then(res => {
        if (!res.ok) {
          // User doesn't exist in DB anymore (DB was reset)
          console.warn('Stored user not found in DB — resetting to onboarding');
          setUser(null);
          localStorage.removeItem('dsa_mentor_user');
        }
      })
      .catch(() => { /* network error, keep user for now */ });
  }, []);

  const saveUser = useCallback((userData) => {
    setUser(userData);
    if (userData) {
      localStorage.setItem('dsa_mentor_user', JSON.stringify(userData));
    } else {
      localStorage.removeItem('dsa_mentor_user');
    }
  }, []);

  return [user, saveUser];
}

/** Generic async data fetcher with loading/error states */
export function useAsync(asyncFn, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const execute = useCallback(async (...args) => {
    setLoading(true);
    setError(null);
    try {
      const result = await asyncFn(...args);
      setData(result);
      return result;
    } catch (err) {
      setError(err.message);
      return null;
    } finally {
      setLoading(false);
    }
  }, deps);

  return { data, loading, error, execute, setData };
}
