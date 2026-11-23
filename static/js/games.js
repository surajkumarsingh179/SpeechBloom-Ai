/**
 * SpeechBloom AI - Games Engine
 */

async function saveGameScore(gameType, score, stars) {
  const childId = getSelectedChildId();
  try {
    return await apiCall('/api/games/save', 'POST', {
      child_id: childId,
      game_type: gameType,
      score: score,
      stars: stars,
      level: 1
    });
  } catch (err) {
    console.error('Failed to save game score:', err);
  }
}

function renderStars(count) {
  return '⭐'.repeat(count) + '☆'.repeat(3 - count);
}
