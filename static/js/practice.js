/**
 * SpeechBloom AI — Practice logic (used by child dashboard inline section)
 * Functions here are called from child_dashboard.html inline scripts.
 * Keep this file minimal — the dashboard handles its own state.
 */

// Utility: build recording URL with child context
function buildRecordingUrl(word, phoneme, lang) {
  const childId = getSelectedChildId();
  const base    = `/recording/?word=${encodeURIComponent(word)}&phoneme=${encodeURIComponent(phoneme||'')}&lang=${lang}`;
  return childId ? `${base}&child_id=${childId}` : base;
}
