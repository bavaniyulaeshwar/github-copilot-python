const test = require('node:test');
const assert = require('node:assert/strict');
const { addScore, getScores, STORAGE_KEY } = require('../static/leaderboard.js');

function createStorage(initialScores = []) {
  let value = JSON.stringify(initialScores);
  return {
    getItem(key) {
      return key === STORAGE_KEY ? value : null;
    },
    setItem(key, nextValue) {
      if (key === STORAGE_KEY) value = nextValue;
    }
  };
}

test('stores scores sorted by completion time and keeps only the top 10', () => {
  const storage = createStorage();

  for (let index = 0; index < 12; index += 1) {
    addScore(storage, {
      name: `Player ${index}`,
      completionTime: 120 - index,
      difficulty: 'Medium',
      hintsUsed: index
    });
  }

  const scores = getScores(storage);
  assert.equal(scores.length, 10);
  assert.deepEqual(scores.map((score) => score.completionTime), [109, 110, 111, 112, 113, 114, 115, 116, 117, 118]);
  assert.deepEqual(scores[0], {
    name: 'Player 11',
    completionTime: 109,
    difficulty: 'Medium',
    hintsUsed: 11,
    createdAt: scores[0].createdAt
  });
});

test('preserves player name, difficulty, and hints used', () => {
  const storage = createStorage();

  addScore(storage, {
    name: 'Ava',
    completionTime: 87,
    difficulty: 'Hard',
    hintsUsed: 2
  });

  assert.deepEqual(getScores(storage)[0], {
    name: 'Ava',
    completionTime: 87,
    difficulty: 'Hard',
    hintsUsed: 2,
    createdAt: getScores(storage)[0].createdAt
  });
});