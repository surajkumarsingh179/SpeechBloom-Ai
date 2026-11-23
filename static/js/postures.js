/**
 * SpeechBloom AI — Tongue & Mouth Posture Articulatory Engine
 * Provides clinically grounded, child-friendly tongue positions, lip shapes,
 * airflow directions, voicing cues, and dynamic SVG cross-section visuals.
 */

const POSTURE_GUIDES = {
  // ── English Consonants & Blends ──
  'b': {
    place: 'Bilabial Stop',
    placeLabel: 'Both Lips',
    shortCue: '👄 Lip Pop',
    tongue: 'Resting relaxed and flat at the bottom of the mouth.',
    lips: 'Press both lips firmly together, build gentle air pressure, then pop open!',
    airflow: 'A quick, energetic burst of air released forward as lips open.',
    voice: 'Voiced ⚡ — Vocal cords vibrate (place fingers on your neck to feel the buzz!)',
    tip: 'Press both lips together and make a gentle soap-bubble pop: b-b-butterfly! 🫧',
    isolatedSound: 'buh',
    svgType: 'bilabial_stop'
  },
  'p': {
    place: 'Bilabial Stop',
    placeLabel: 'Both Lips (Voiceless)',
    shortCue: '🍿 Popcorn Pop',
    tongue: 'Resting flat and low in the mouth.',
    lips: 'Close lips firmly, build slight air pressure, and pop them open cleanly.',
    airflow: 'Quick puff of cool air released forward without vocal buzz.',
    voice: 'Voiceless 🤫 — Whisper air only, no throat vibration.',
    tip: 'Pop your lips open like popping hot popcorn: p-p-pop! 🍿',
    isolatedSound: 'puh',
    svgType: 'bilabial_stop'
  },
  'm': {
    place: 'Bilabial Nasal',
    placeLabel: 'Both Lips (Nasal)',
    shortCue: '🍦 Sweet Hum',
    tongue: 'Resting flat and relaxed inside the mouth.',
    lips: 'Gently seal both lips together and keep them comfortably closed.',
    airflow: 'Continuous smooth air flows through the nose cavity.',
    voice: 'Voiced ⚡ — Steady vocal cord hum buzzing in your nose and lips.',
    tip: 'Keep your lips closed and hum like tasting delicious ice cream: mmmmm! 🍦',
    isolatedSound: 'mmm',
    svgType: 'bilabial_nasal'
  },
  's': {
    place: 'Alveolar Fricative',
    placeLabel: 'Teeth & Tongue Tip',
    shortCue: '🐍 Snake Hiss',
    tongue: 'Place tongue tip right behind upper front teeth without touching them, leaving a tiny air slot.',
    lips: 'Lips parted in a relaxed gentle smile, teeth close together.',
    airflow: 'A steady, narrow, continuous stream of cool hissing air.',
    voice: 'Voiceless 🤫 — Whisper breath only (no vocal buzz).',
    tip: 'Keep your teeth close and blow a continuous gentle hiss like a friendly snake: sssss! 🐍',
    isolatedSound: 'ssss',
    svgType: 'alveolar_fricative'
  },
  'sp': {
    place: 'Alveolar + Bilabial Blend',
    placeLabel: 'Hiss + Lip Pop',
    shortCue: '🥄 Hiss & Pop',
    tongue: 'Start with tongue tip behind upper teeth for the hiss /s/, then relax tongue for the lip pop /p/.',
    lips: 'Smile gently for "s", then press both lips together and pop open for "p".',
    airflow: 'Smooth continuous hiss followed immediately by a crisp air release.',
    voice: 'Voiceless 🤫 — Clean whisper transition from hiss to pop.',
    tip: 'First hiss like a snake "ssss", then pop your lips "puh" right away: sp-sp-spoon! 🥄',
    isolatedSound: 'spuh',
    svgType: 'blend_sp'
  },
  'st': {
    place: 'Alveolar Blend',
    placeLabel: 'Hiss + Tongue Tap',
    shortCue: '⭐ Hiss & Tap',
    tongue: 'Start tongue tip behind upper teeth for "s", then tap the bumpy ridge firmly for "t".',
    lips: 'Gentle relaxed smile.',
    airflow: 'Continuous hiss followed by an abrupt clean air tap.',
    voice: 'Voiceless 🤫 — Quick clean air sound.',
    tip: 'Hiss like a snake "ssss" then tap your tongue "tuh": st-st-star! ⭐',
    isolatedSound: 'stuh',
    svgType: 'blend_st'
  },
  'str': {
    place: 'Triple Blend',
    placeLabel: 'Hiss + Tap + Curl',
    shortCue: '🍓 Hiss, Tap & Curl',
    tongue: 'Hiss behind teeth for "s", tap ridge for "t", then curl tongue back for "r".',
    lips: 'Start in a smile, then slightly flare lips for the "r".',
    airflow: 'Flowing continuous multi-step airflow.',
    voice: 'Transitions from whisper "st" to voiced throat buzz "r" ⚡.',
    tip: 'Hiss, tap, and curl your tongue: str-str-strawberry! 🍓',
    isolatedSound: 'struh',
    svgType: 'blend_str'
  },
  'r': {
    place: 'Retroflex / Alveolar Approximant',
    placeLabel: 'Tongue Curled Back',
    shortCue: '🦁 Lion Roar',
    tongue: 'Curl the tip of your tongue upward and slightly backward like a spoon, without touching the roof.',
    lips: 'Slightly flared outward in a neutral shape (avoid rounding into a "w" circle).',
    airflow: 'Steady, open resonant airflow over the curled tongue.',
    voice: 'Voiced ⚡ — Vocal cords humming with strong vocal resonance.',
    tip: 'Curl your tongue back like a little spoon and growl softly like a friendly lion: rrrrr! 🦁',
    isolatedSound: 'rrr',
    svgType: 'retroflex'
  },
  'l': {
    place: 'Alveolar Lateral Liquid',
    placeLabel: 'Tongue Tip Raised',
    shortCue: '👅 Tongue Ridge Tap',
    tongue: 'Touch the tip of your tongue firmly against the bumpy ridge behind your upper front teeth.',
    lips: 'Relaxed and open.',
    airflow: 'Air flows freely around both sides of your tongue.',
    voice: 'Voiced ⚡ — Strong vocal cord vibration.',
    tip: 'Touch the tip of your tongue to the roof behind your teeth and sing: llll-ion! 🦁',
    isolatedSound: 'lll',
    svgType: 'alveolar_liquid'
  },
  'k': {
    place: 'Velar Stop',
    placeLabel: 'Back of Tongue',
    shortCue: '🐱 Velar Pop',
    tongue: 'Front of tongue stays resting down; the back of your tongue raises to touch the soft palate and drops.',
    lips: 'Open and neutral.',
    airflow: 'A crisp, clean burst of air released from the back of the mouth.',
    voice: 'Voiceless 🤫 — Clean air pop from the throat.',
    tip: 'Push the back of your tongue up against the roof and let it pop: k-k-clock! 🐱',
    isolatedSound: 'kuh',
    svgType: 'velar_stop'
  },
  'g': {
    place: 'Velar Stop (Voiced)',
    placeLabel: 'Back of Tongue',
    shortCue: '🎮 Throat Rumble',
    tongue: 'Back of tongue presses against soft roof of mouth, front tongue stays low.',
    lips: 'Parted naturally.',
    airflow: 'Burst of air with vocal cord vibration.',
    voice: 'Voiced ⚡ — Feel your throat rumble.',
    tip: 'Make a gentle "guh" sound from the back of your throat: g-g-game! 🎮',
    isolatedSound: 'guh',
    svgType: 'velar_stop'
  },
  'e': {
    place: 'Front-Mid Vowel',
    placeLabel: 'Mouth Half-Open',
    shortCue: '🗣️ Vocal Smile',
    tongue: 'Tongue body rests in the middle-front of the mouth, tongue tip behind lower teeth.',
    lips: 'Mouth half-open in a relaxed gentle smile.',
    airflow: 'Continuous smooth, clear vocal air release.',
    voice: 'Voiced ⚡ — Clear, open vocal cord vibration.',
    tip: 'Open your mouth halfway, smile gently, and make a clear "eh" sound: eh-elephant! 🐘',
    isolatedSound: 'eh',
    svgType: 'vowel_front'
  },
  'sh': {
    place: 'Postalveolar Fricative',
    placeLabel: 'Behind Teeth Ridge',
    shortCue: '🤫 Quiet Shush',
    tongue: 'Tongue arched just behind the alveolar ridge with sides pressed to upper molars.',
    lips: 'Pursed or rounded slightly forward.',
    airflow: 'Broad, quiet, rushing stream of air.',
    voice: 'Voiceless 🤫 — Gentle shushing whisper.',
    tip: 'Round your lips and make the quiet shush sound: shhhhh! 🤫',
    isolatedSound: 'shhh',
    svgType: 'postalveolar'
  },
  'th': {
    place: 'Dental / Interdental',
    placeLabel: 'Teeth & Tongue Tip',
    shortCue: '🐢 Turtle Peek',
    tongue: 'Tongue tip peeks gently between upper and lower front teeth.',
    lips: 'Parted and relaxed.',
    airflow: 'Gentle breeze escaping around the tongue tip.',
    voice: 'Voiceless 🤫 — Soft airy whisper.',
    tip: 'Let your tongue tip peek out between your teeth like a happy turtle: th-th-three! 🐢',
    isolatedSound: 'thhh',
    svgType: 'dental'
  },
  'f': {
    place: 'Labiodental Fricative',
    placeLabel: 'Top Teeth & Lower Lip',
    shortCue: '🐰 Bunny Breath',
    tongue: 'Resting flat inside the mouth.',
    lips: 'Upper front teeth rest gently on top of the lower lip.',
    airflow: 'Smooth gentle stream of air blown through teeth and lip.',
    voice: 'Voiceless 🤫 — Soft windy breath.',
    tip: 'Rest your top teeth on your bottom lip like a cute bunny and blow: fffff! 🐰',
    isolatedSound: 'ffff',
    svgType: 'labiodental'
  },
  'd': {
    place: 'Alveolar Stop',
    placeLabel: 'Tongue Ridge Tap',
    shortCue: '🥁 Drum Tap',
    tongue: 'Tongue tip taps firmly against the ridge behind upper teeth and releases with voice.',
    lips: 'Open naturally.',
    airflow: 'Quick burst of voiced air.',
    voice: 'Voiced ⚡ — Vocal cords buzz on release.',
    tip: 'Tap your tongue on the roof behind your teeth like a drum: d-d-drum! 🥁',
    isolatedSound: 'duh',
    svgType: 'alveolar_stop'
  },
  'kl': {
    place: 'Velar + Liquid Blend',
    placeLabel: 'Back Pop + Tongue Tap',
    shortCue: '🕐 Pop & Tap',
    tongue: 'Back of tongue pops against soft palate for "k", then tongue tip taps ridge for "l".',
    lips: 'Open and relaxed.',
    airflow: 'Clean velar burst smoothly transitioning to lateral flow.',
    voice: 'Voiceless into voiced: k-l! ⚡',
    tip: 'Pop from the back of your mouth then tap behind your teeth: kl-kl-clock! 🕐',
    isolatedSound: 'kluh',
    svgType: 'velar_stop'
  },
  'fr': {
    place: 'Labiodental + Liquid Blend',
    placeLabel: 'Bunny Teeth + Lion Curl',
    shortCue: '🐸 Teeth & Curl',
    tongue: 'Start flat, then curl tongue back for "r".',
    lips: 'Teeth on bottom lip for "f", then flare into "r".',
    airflow: 'Windy breeze into voiced roll.',
    voice: 'Voiceless into voiced ⚡.',
    tip: 'Blow with top teeth on lip then curl your tongue: fr-fr-frog! 🐸',
    isolatedSound: 'fruh',
    svgType: 'labiodental'
  },

  // ── Hindi Phonemes ──
  'स': {
    place: 'दंत्य/वर्त्स्य संघर्षी (Dental/Alveolar Fricative)',
    placeLabel: 'दांत और जीभ की नोक',
    shortCue: '☀️ सीटी जैसी हवा',
    tongue: 'जीभ की नोक ऊपर के सामने वाले दांतों के ठीक पीछे रखें, बिना दांतों को पूरी तरह छुए।',
    lips: 'हल्की मुस्कान के साथ होंठ खुले रखें, दांत पास-पास।',
    airflow: 'दांतों के बीच से सीटी जैसी धीमी, निरंतर हवा निकालिए।',
    voice: 'अघोष 🤫 — केवल हवा की मधुर ध्वनि, गले में कंपन नहीं।',
    tip: 'दांत पास लाकर सीटी जैसी धीमी हवा निकालिए: स-स-सूरज! ☀️',
    isolatedSound: 'स',
    svgType: 'alveolar_fricative'
  },
  'र': {
    place: 'वर्त्स्य उत्क्षिप्त/कंपित (Alveolar Tap/Trill)',
    placeLabel: 'जीभ का कंपन',
    shortCue: '🚩 जीभ का कंपन',
    tongue: 'जीभ की नोक को ऊपर के तालू/मसूड़े के पास ले जाकर हल्का सा कम्पन या झटका दें।',
    lips: 'होंठ सामान्य रूप से खुले।',
    airflow: 'हल्का झटका लेते हुए प्रवाहित हवा।',
    voice: 'सघोष ⚡ — गले के वोकल कॉर्ड में कंपन महसूस करें।',
    tip: 'जीभ की नोक को ऊपर हल्का सा कम्पित करके बोलिए: र-र-राम! 🚩',
    isolatedSound: 'र',
    svgType: 'retroflex'
  },
  'प': {
    place: 'ओष्ठ्य स्पर्श (Bilabial Stop)',
    placeLabel: 'दोनों होंठ',
    shortCue: '💧 होंठों का स्पर्श',
    tongue: 'जीभ मुंह के नीचे शांत विश्राम अवस्था में रहती है।',
    lips: 'दोनों होंठों को आपस में मिलाकर थोड़ा हवा का दबाव बनाकर खोलें।',
    airflow: 'होंठ खुलते ही हवा का हल्का फुहार जैसा निकास।',
    voice: 'अघोष 🤫 — होंठों से साफ फटने वाली आवाज।',
    tip: 'दोनों होंठों को मिलाकर प्यार से खोलिए: प-प-पानी! 💧',
    isolatedSound: 'प',
    svgType: 'bilabial_stop'
  },
  'क': {
    place: 'कंठ्य स्पर्श (Velar Stop)',
    placeLabel: 'गले/तालू का पिछला भाग',
    shortCue: '🪷 गले से साफ आवाज',
    tongue: 'जीभ की नोक नीचे रहती है, जीभ का पिछला हिस्सा कोमल तालू से मिलकर छूटता है।',
    lips: 'होंठ सामान्य खुले।',
    airflow: 'गले से साफ और त्वरित हवा का निकास।',
    voice: 'अघोष 🤫 — गले से साफ क ध्वनि।',
    tip: 'गले के पिछले हिस्से से साफ आवाज निकालिए: क-क-कमल! 🪷',
    isolatedSound: 'क',
    svgType: 'velar_stop'
  },
  'म': {
    place: 'ओष्ठ्य नासिक्य (Bilabial Nasal)',
    placeLabel: 'दोनों होंठ (नासिक्य)',
    shortCue: '👩 होंठों की गुंजन',
    tongue: 'जीभ आराम से नीचे रहती है।',
    lips: 'दोनों होंठ पूरी तरह बंद रहते हैं।',
    airflow: 'हवा नाक के रास्ते गूंजते हुए निकलती है।',
    voice: 'सघोष ⚡ — गले में मीठी गुंजन का अहसास होता है।',
    tip: 'होंठ बंद करके मीठी गुंजन कीजिए: म-म-माँ! 👩',
    isolatedSound: 'म',
    svgType: 'bilabial_nasal'
  },
  'त': {
    place: 'दंत्य स्पर्श (Dental Stop)',
    placeLabel: 'ऊपरी दांतों के पीछे',
    shortCue: '🦋 दांतों पर जीभ',
    tongue: 'जीभ की नोक ऊपरी दांतों की पिछली सतह को छूती है और फिर अलग होती है।',
    lips: 'होंठ स्वाभाविक रूप से खुले।',
    airflow: 'दांतों से जीभ हटते ही हवा निकलती है।',
    voice: 'अघोष 🤫 — साफ त ध्वनि।',
    tip: 'जीभ को दांतों से छूकर साफ बोलिए: त-त-तितली! 🦋',
    isolatedSound: 'त',
    svgType: 'dental'
  },
  'ह': {
    place: 'काकल्य संघर्षी (Glottal Fricative)',
    placeLabel: 'खुला गला',
    shortCue: '🐘 खुली गर्म सांस',
    tongue: 'जीभ विश्राम में रहती है।',
    lips: 'मुंह आराम से खुला रहता है।',
    airflow: 'गले से गहरी गर्म सांस की तरह हवा बहती है।',
    voice: 'अघोष 🤫 — खुली सांस।',
    tip: 'गले से खुली सांस छोड़ते हुए बोलिए: ह-ह-हाथी! 🐘',
    isolatedSound: 'ह',
    svgType: 'vowel_front'
  },
  'फ': {
    place: 'ओष्ठ्य/दंत्योष्ठ्य (Labiodental/Bilabial)',
    placeLabel: 'होंठ और हवा',
    shortCue: '🌸 कोमल हवा',
    tongue: 'जीभ शांत नीचे रहती है।',
    lips: 'होंठों से हल्की हवा छोड़ें।',
    airflow: 'मुलायम हवा का निकास।',
    voice: 'अघोष 🤫 — कोमल सांस।',
    tip: 'हल्की हवा के साथ बोलिए: फ-फ-फूल! 🌸',
    isolatedSound: 'फ',
    svgType: 'labiodental'
  },
  'ग': {
    place: 'कंठ्य सघोष स्पर्श (Velar Voiced)',
    placeLabel: 'गले का कंपन',
    shortCue: '⚽ गले की गूंज',
    tongue: 'जीभ का पिछला हिस्सा तालू से छूकर छूटता है।',
    lips: 'होंठ खुले।',
    airflow: 'गले से गूंजती हवा।',
    voice: 'सघोष ⚡ — गले में कंपन।',
    tip: 'गले से गूंजती आवाज निकालिए: ग-ग-गेंद! ⚽',
    isolatedSound: 'ग',
    svgType: 'velar_stop'
  },
  'न': {
    place: 'वर्त्स्य नासिक्य (Alveolar Nasal)',
    placeLabel: 'तालू और नाक',
    shortCue: '🌊 नाक से गूंज',
    tongue: 'जीभ की नोक ऊपर मसूड़े को छूती है।',
    lips: 'होंठ खुले।',
    airflow: 'हवा नाक से निकलती है।',
    voice: 'सघोष ⚡ — नाक से गूंज।',
    tip: 'जीभ ऊपर लगाकर नाक से बोलिए: न-न-नदी! 🌊',
    isolatedSound: 'न',
    svgType: 'alveolar_liquid'
  }
};

/**
 * Get posture object for a phoneme with intelligent fallback
 */
function getPostureGuide(phoneme, word = '') {
  if (!phoneme && word) {
    phoneme = word.trim().charAt(0).toLowerCase();
  }
  const cleanPh = (phoneme || '').trim().toLowerCase();
  if (POSTURE_GUIDES[cleanPh]) {
    return POSTURE_GUIDES[cleanPh];
  }

  // Check initial character or fallback
  const firstChar = cleanPh.charAt(0);
  if (POSTURE_GUIDES[firstChar]) {
    return POSTURE_GUIDES[firstChar];
  }

  // General fallback
  return {
    place: 'Speech Articulation',
    placeLabel: 'Vocal Tract',
    shortCue: '🎯 Clear Sound',
    tongue: 'Keep your tongue in a relaxed natural position and move it clearly.',
    lips: 'Shape your lips naturally according to the sound.',
    airflow: 'Smooth, steady outward breath.',
    voice: 'Voiced ⚡ — Speak with your confident natural voice!',
    tip: `Focus on pronouncing "${word || phoneme}" clearly and steadily! 🌟`,
    isolatedSound: cleanPh || 'ah',
    svgType: 'vowel_front'
  };
}

/**
 * Short badge cue for list views
 */
function getShortPostureCue(phoneme, word = '') {
  const guide = getPostureGuide(phoneme, word);
  return guide.shortCue || '👅 Tongue Guide';
}

/**
 * Generates an interactive SVG cross-section diagram showing mouth, tongue position, and airflow.
 */
function renderPostureSVG(svgType, containerId) {
  const container = document.getElementById(containerId);
  if (!container) return;

  // Visual parameters depending on articulatory posture
  let tonguePath = 'M 60 110 Q 90 95 125 105 Q 150 110 165 115'; // Default flat
  let highlightTongue = false;
  let highlightLips = false;
  let highlightRidge = false;
  let highlightVelum = false;
  let airflowArrow = 'M 90 100 L 175 100'; // Default stream

  if (svgType === 'bilabial_stop' || svgType === 'bilabial_nasal') {
    // Lips firmly pressed together, tongue flat
    tonguePath = 'M 55 110 Q 95 100 130 110 Q 155 115 168 120';
    highlightLips = true;
    airflowArrow = svgType === 'bilabial_nasal' ? 'M 65 85 Q 120 50 175 60' : 'M 140 105 L 185 105';
  } else if (svgType === 'alveolar_fricative' || svgType === 'alveolar_stop' || svgType === 'blend_sp' || svgType === 'blend_st') {
    // Tongue tip raised right behind alveolar ridge
    tonguePath = 'M 55 115 Q 85 105 120 95 Q 148 70 156 68';
    highlightRidge = true;
    highlightTongue = true;
    airflowArrow = 'M 140 68 Q 160 72 185 75';
  } else if (svgType === 'retroflex') {
    // Tongue curled up and back
    tonguePath = 'M 55 115 Q 80 100 115 90 Q 140 65 125 55';
    highlightTongue = true;
    airflowArrow = 'M 110 75 Q 145 75 185 85';
  } else if (svgType === 'alveolar_liquid') {
    // Tongue tip pressed to alveolar ridge, sides open
    tonguePath = 'M 55 115 Q 85 105 120 85 Q 146 64 154 62';
    highlightRidge = true;
    highlightTongue = true;
    airflowArrow = 'M 110 95 Q 145 95 185 98';
  } else if (svgType === 'velar_stop') {
    // Back of tongue elevated to soft palate
    tonguePath = 'M 55 115 Q 80 62 105 60 Q 135 95 165 115';
    highlightVelum = true;
    highlightTongue = true;
    airflowArrow = 'M 95 62 L 185 80';
  } else if (svgType === 'dental') {
    // Tongue tip touching teeth
    tonguePath = 'M 55 115 Q 90 105 130 92 Q 158 80 172 82';
    highlightRidge = true;
    highlightTongue = true;
    airflowArrow = 'M 150 82 L 188 84';
  } else if (svgType === 'labiodental') {
    // Top teeth on bottom lip
    tonguePath = 'M 55 115 Q 95 105 130 110 Q 155 115 168 118';
    highlightLips = true;
    airflowArrow = 'M 150 85 L 188 88';
  } else {
    // Front vowel
    tonguePath = 'M 55 115 Q 95 85 135 88 Q 155 105 165 115';
    highlightTongue = true;
    airflowArrow = 'M 75 95 Q 125 90 185 95';
  }

  const svgHTML = `
    <svg viewBox="0 0 200 140" style="width:100%; max-width:210px; height:auto; display:block; margin:0 auto;" aria-label="Mouth and Tongue Cross-Section">
      <defs>
        <linearGradient id="tongueGrad" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FF5C8A" />
          <stop offset="100%" stop-color="#DC143C" />
        </linearGradient>
        <linearGradient id="palateGrad" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stop-color="#4B5563" />
          <stop offset="100%" stop-color="#9CA3AF" />
        </linearGradient>
        <filter id="glow">
          <feGaussianBlur stdDeviation="2.5" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>
      </defs>

      <!-- Head & Palate Profile -->
      <path d="M 40 125 L 40 40 Q 90 35 130 45 Q 155 52 165 65" fill="none" stroke="var(--border-light, #333)" stroke-width="3" stroke-linecap="round"/>

      <!-- Hard Palate & Alveolar Ridge -->
      <path d="M 85 46 Q 125 48 148 58 Q 158 64 163 70" fill="none" stroke="url(#palateGrad)" stroke-width="4" stroke-linecap="round"/>

      <!-- Upper Teeth -->
      <path d="M 163 70 L 165 82" stroke="#FFF" stroke-width="4.5" stroke-linecap="round"/>

      <!-- Upper Lip -->
      <path d="M 160 55 Q 175 60 178 72" fill="none" stroke="${highlightLips ? 'var(--crimson, #DC143C)' : '#9CA3AF'}" stroke-width="${highlightLips ? '4.5' : '3'}" stroke-linecap="round" ${highlightLips ? 'filter="url(#glow)"' : ''}/>

      <!-- Lower Lip -->
      <path d="M 176 96 Q 174 110 158 116" fill="none" stroke="${highlightLips ? 'var(--crimson, #DC143C)' : '#9CA3AF'}" stroke-width="${highlightLips ? '4.5' : '3'}" stroke-linecap="round" ${highlightLips ? 'filter="url(#glow)"' : ''}/>

      <!-- Lower Teeth -->
      <path d="M 162 100 L 164 92" stroke="#FFF" stroke-width="4.5" stroke-linecap="round"/>

      <!-- Velum / Soft Palate Highlight -->
      ${highlightVelum ? '<circle cx="95" cy="50" r="7" fill="var(--warning, #F59E0B)" filter="url(#glow)" opacity="0.85"/>' : ''}

      <!-- Alveolar Ridge Target Highlight -->
      ${highlightRidge ? '<circle cx="152" cy="62" r="6" fill="var(--gold, #FFD700)" filter="url(#glow)" opacity="0.9"/>' : ''}

      <!-- Tongue Body -->
      <path d="${tonguePath}" fill="none" stroke="url(#tongueGrad)" stroke-width="8" stroke-linecap="round" ${highlightTongue ? 'filter="url(#glow)"' : ''}/>

      <!-- Airflow Arrow -->
      <path d="${airflowArrow}" fill="none" stroke="var(--success, #22C55E)" stroke-width="2.5" stroke-dasharray="4,3" stroke-linecap="round"/>
      <polygon points="186,${airflowArrow.split(' ').pop()} 180,${parseInt(airflowArrow.split(' ').pop())-3} 180,${parseInt(airflowArrow.split(' ').pop())+3}" fill="var(--success, #22C55E)"/>

      <!-- Labels -->
      <text x="14" y="125" fill="var(--text-muted, #9CA3AF)" font-size="8.5" font-weight="700">Throat</text>
      <text x="160" y="132" fill="var(--text-muted, #9CA3AF)" font-size="8.5" font-weight="700">Lips</text>
    </svg>
  `;

  container.innerHTML = svgHTML;
}
