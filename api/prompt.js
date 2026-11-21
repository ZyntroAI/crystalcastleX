/**
 * prompt.js — CrystalCastleX / ZyntroAI
 * Prompt building, validation, and templating for AI generation
 */

const PROMPT_PRESETS = {
  social_video: `Create an engaging short-form video script optimized for social media.
Keep it concise, visually descriptive, and engaging from the very first second.
Include: Scene description, Voiceover text, Visual style/mood, and Duration breakdown.`,
  tiktok_hook: `Write a high-converting TikTok opening hook.
Max 2–3 sentences. High energy, clear value, curiosity-inducing.`,
  image_style: `Photorealistic, cinematic lighting, high detail, 8k resolution, sharp focus.
--ar 9:16 --style raw`,
  creative_story: `You are a creative storyteller. Write vivid, immersive narratives.
Be specific with imagery, pacing, and emotional tone.`
};

/**
 * Build a full prompt from user input + preset + style
 */
function buildPrompt({ userInput, preset = '', style = '', context = '' }) {
  const parts = [];

  if (preset && PROMPT_PRESETS[preset]) {
    parts.push(PROMPT_PRESETS[preset]);
  }
  if (context) {
    parts.push(`CONTEXT:\n${context}`);
  }
  if (userInput) {
    parts.push(`PROMPT:\n${userInput}`);
  }
  if (style) {
    parts.push(`STYLE:\n${style}`);
  }

  return parts.join('\n\n---\n\n').trim();
}

/**
 * Validate prompt length & basic safety
 */
function validatePrompt(text, maxChars = 4000) {
  if (!text || typeof text !== 'string') {
    return { valid: false, error: 'Prompt is empty or invalid' };
  }
  if (text.length > maxChars) {
    return { valid: false, error: `Prompt too long (${text.length}/${maxChars})` };
  }
  return { valid: true, length: text.length };
}

/**
 * Format prompt for specific provider API
 */
function formatForProvider(promptText, systemPrompt = '', provider = 'openai') {
  switch (provider.toLowerCase()) {
    case 'openai':
    case 'nexa':
    case 'pika':
    case 'wavespeedai':
      return {
        messages: [
          ...(systemPrompt ? [{ role: 'system', content: systemPrompt }] : []),
          { role: 'user', content: promptText }
        ]
      };
    case 'anthropic':
      return {
        system: systemPrompt,
        messages: [{ role: 'user', content: promptText }]
      };
    default:
      return { prompt: systemPrompt ? `${systemPrompt}\n\n${promptText}` : promptText };
  }
}

/**
 * List available presets
 */
function listPresets() {
  return Object.keys(PROMPT_PRESETS);
}

module.exports = {
  PROMPT_PRESETS,
  buildPrompt,
  validatePrompt,
  formatForProvider,
  listPresets
};
