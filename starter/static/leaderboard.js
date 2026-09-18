(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    root.SudokuLeaderboard = factory();
  }
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  const STORAGE_KEY = 'sudoku-top-10';
  const SCORE_LIMIT = 10;

  function readScores(storage) {
    try {
      const stored = storage.getItem(STORAGE_KEY);
      const scores = stored ? JSON.parse(stored) : [];
      return Array.isArray(scores) ? scores : [];
    } catch (error) {
      return [];
    }
  }

  function sortScores(scores) {
    return scores
      .filter((score) => Number.isFinite(score.completionTime) && score.completionTime >= 0)
      .sort((left, right) => {
        if (left.completionTime !== right.completionTime) {
          return left.completionTime - right.completionTime;
        }
        return (left.createdAt || 0) - (right.createdAt || 0);
      })
      .slice(0, SCORE_LIMIT);
  }

  function getScores(storage) {
    return sortScores(readScores(storage));
  }

  function addScore(storage, score) {
    const normalizedScore = {
      name: String(score.name || 'Anonymous').trim() || 'Anonymous',
      completionTime: Number(score.completionTime),
      difficulty: String(score.difficulty || 'Medium'),
      hintsUsed: Number.isFinite(Number(score.hintsUsed)) ? Number(score.hintsUsed) : 0,
      createdAt: Date.now()
    };
    const scores = sortScores(getScores(storage).concat(normalizedScore));
    storage.setItem(STORAGE_KEY, JSON.stringify(scores));
    return scores;
  }

  return { STORAGE_KEY, SCORE_LIMIT, getScores, addScore };
});