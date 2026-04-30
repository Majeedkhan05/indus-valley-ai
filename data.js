/* =========================================================
   Static data — seals, cities, motifs, script glyphs
   ========================================================= */

window.IVA_DATA = {

  /* — 92 real seals from the Indus-Seal-Dataset (Mature Harappan corpus) — */
  seals: [
    { id: 1  , file: 'assets/seals/seal-1.jpg', label: 'Unicorn seal', tag: 'Mohenjo-daro · steatite' },
    { id: 2  , file: 'assets/seals/seal-2.jpg', label: 'Unicorn + script', tag: 'Mohenjo-daro · standard format' },
    { id: 3  , file: 'assets/seals/seal-3.jpg', label: 'Unicorn variant', tag: 'Lower town · DK area' },
    { id: 4  , file: 'assets/seals/seal-4.jpg', label: 'Unicorn with manger', tag: 'Classic five-sign register' },
    { id: 5  , file: 'assets/seals/seal-5.jpg', label: 'Zebu bull profile', tag: 'Punjab provenance' },
    { id: 6  , file: 'assets/seals/seal-6.jpg', label: 'Composite animal', tag: 'Hybrid iconography' },
    { id: 7  , file: 'assets/seals/seal-7.jpg', label: 'Composite creature', tag: 'Harappa · square seal' },
    { id: 8  , file: 'assets/seals/seal-8.jpg', label: 'Bull standard', tag: 'Cultic emblem' },
    { id: 9  , file: 'assets/seals/seal-9.jpg', label: 'Unicorn (worn)', tag: 'Heavy use-wear' },
    { id: 10 , file: 'assets/seals/seal-10.jpg', label: 'Buffalo motif', tag: 'Symbolic register' },
    { id: 11 , file: 'assets/seals/seal-11.jpg', label: 'Elephant', tag: 'Sacred fauna' },
    { id: 12 , file: 'assets/seals/seal-12.jpg', label: 'Rhinoceros', tag: 'Wetland species' },
    { id: 13 , file: 'assets/seals/seal-13.jpg', label: 'Multi-script', tag: 'Long inscription' },
    { id: 14 , file: 'assets/seals/seal-14.jpg', label: 'Zebu bull', tag: 'Civic register' },
    { id: 15 , file: 'assets/seals/seal-15.jpg', label: 'Goat / antelope', tag: 'Pastoral motif' },
    { id: 16 , file: 'assets/seals/seal-16.jpg', label: 'Two-sign tag', tag: 'Trade marker' },
    { id: 17 , file: 'assets/seals/seal-17.jpg', label: 'Tiger profile', tag: 'Predator iconography' },
    { id: 18 , file: 'assets/seals/seal-18.jpg', label: 'Three-sign tag', tag: 'Compact administrative' },
    { id: 19 , file: 'assets/seals/seal-19.jpg', label: 'Script only', tag: 'Inscription tablet' },
    { id: 20 , file: 'assets/seals/seal-20.jpg', label: 'Bull plus tree', tag: 'Sacred-tree composition' },
    { id: 21 , file: 'assets/seals/seal-21.jpg', label: 'Standard mark', tag: 'Worship apparatus' },
    { id: 22 , file: 'assets/seals/seal-22.jpg', label: 'Elephant motif', tag: 'Sacred fauna' },
    { id: 23 , file: 'assets/seals/seal-23.jpg', label: 'Goat + tree', tag: 'Cultic context' },
    { id: 24 , file: 'assets/seals/seal-24.jpg', label: 'Mythic figure', tag: 'Anthropomorphic' },
    { id: 25 , file: 'assets/seals/seal-25.jpg', label: 'Square block', tag: 'Administrative tablet' },
    { id: 26 , file: 'assets/seals/seal-26.jpg', label: 'Buffalo head', tag: 'Symbolic' },
    { id: 27 , file: 'assets/seals/seal-27.jpg', label: 'Procession', tag: 'Multi-animal scene' },
    { id: 35 , file: 'assets/seals/seal-35.jpg', label: 'Tiger / horned', tag: 'Anthropomorphic' },
    { id: 38 , file: 'assets/seals/seal-38.jpg', label: 'Composite head', tag: 'Hybrid iconography' },
    { id: 39 , file: 'assets/seals/seal-39.jpg', label: 'Pipal tree', tag: 'Sacred motif' },
    { id: 43 , file: 'assets/seals/seal-43.jpg', label: 'Six-sign seal', tag: 'Long inscription' },
    { id: 47 , file: 'assets/seals/seal-47.jpg', label: 'Hare / ibex', tag: 'Pastoral motif' },
    { id: 48 , file: 'assets/seals/seal-48.jpg', label: 'Rhinoceros', tag: 'Wetland species' },
    { id: 53 , file: 'assets/seals/seal-53.jpg', label: 'Banded bull', tag: 'Decorative cattle' },
    { id: 54 , file: 'assets/seals/seal-54.jpg', label: 'Antelope', tag: 'Wild fauna' },
    { id: 55 , file: 'assets/seals/seal-55.jpg', label: 'Geometric', tag: 'Abstract design' },
    { id: 56 , file: 'assets/seals/seal-56.jpg', label: 'Composite', tag: 'Hybrid creature' },
    { id: 57 , file: 'assets/seals/seal-57.jpg', label: 'Profile bull', tag: 'Standard motif' },
    { id: 58 , file: 'assets/seals/seal-58.jpg', label: 'Wheel sign', tag: 'Spoked emblem' },
    { id: 59 , file: 'assets/seals/seal-59.jpg', label: 'Crescent', tag: 'Lunar mark' },
    { id: 60 , file: 'assets/seals/seal-60.jpg', label: 'Buffalo head', tag: 'Symbolic register' },
    { id: 61 , file: 'assets/seals/seal-61.jpg', label: 'Triple sign', tag: 'Numeric register' },
    { id: 62 , file: 'assets/seals/seal-62.jpg', label: 'Long inscription', tag: 'Seven-sign tag' },
    { id: 63 , file: 'assets/seals/seal-63.jpg', label: 'Tiger emblem', tag: 'Predator iconography' },
    { id: 64 , file: 'assets/seals/seal-64.jpg', label: 'Tablet', tag: 'Bar-seal form' },
    { id: 65 , file: 'assets/seals/seal-65.jpg', label: 'Bull + standard', tag: 'Composite icon' },
    { id: 71 , file: 'assets/seals/seal-71.jpg', label: 'Procession', tag: 'Animal sequence' },
    { id: 72 , file: 'assets/seals/seal-72.jpg', label: 'Pashupati-style', tag: 'Yogic figure · debated' },
    { id: 73 , file: 'assets/seals/seal-73.jpg', label: 'Horned god', tag: 'Anthropomorphic' },
    { id: 74 , file: 'assets/seals/seal-74.jpg', label: 'Two-fold', tag: 'Mirrored seal' },
    { id: 76 , file: 'assets/seals/seal-76.jpg', label: 'Archer', tag: 'Mythic figure' },
    { id: 77 , file: 'assets/seals/seal-77.jpg', label: 'Boat / vessel', tag: 'Trade context' },
    { id: 78 , file: 'assets/seals/seal-78.jpg', label: 'Compound', tag: 'Multi-element' },
    { id: 79 , file: 'assets/seals/seal-79.jpg', label: 'Goat + post', tag: 'Tethered animal' },
    { id: 80 , file: 'assets/seals/seal-80.jpg', label: 'Ibex', tag: 'Highland fauna' },
    { id: 81 , file: 'assets/seals/seal-81.jpg', label: 'Bull worship', tag: 'Ritual scene' },
    { id: 82 , file: 'assets/seals/seal-82.jpg', label: 'Geometric', tag: 'Abstract' },
    { id: 83 , file: 'assets/seals/seal-83.jpg', label: 'Worship scene', tag: 'Cultic' },
    { id: 84 , file: 'assets/seals/seal-84.jpg', label: 'Markhor', tag: 'Mountain goat' },
    { id: 85 , file: 'assets/seals/seal-85.jpg', label: 'Worship + tree', tag: 'Sacred tableau' },
    { id: 86 , file: 'assets/seals/seal-86.jpg', label: 'Fish sign', tag: 'Most frequent sign' },
    { id: 87 , file: 'assets/seals/seal-87.jpg', label: 'Mother goddess', tag: 'Female figure' },
    { id: 89 , file: 'assets/seals/seal-89.jpg', label: 'Multi-animal', tag: 'Procession seal' },
    { id: 90 , file: 'assets/seals/seal-90.jpg', label: 'Long inscription', tag: 'Eight-sign' },
    { id: 91 , file: 'assets/seals/seal-91.jpg', label: 'Composite', tag: 'Hybrid creature' },
    { id: 92 , file: 'assets/seals/seal-92.jpg', label: 'Bull profile', tag: 'Classic motif' },
    { id: 93 , file: 'assets/seals/seal-93.jpg', label: 'Antelope', tag: 'Pastoral' },
    { id: 94 , file: 'assets/seals/seal-94.jpg', label: 'Tiger', tag: 'Predator' },
    { id: 95 , file: 'assets/seals/seal-95.jpg', label: 'Compound seal', tag: 'Multi-register' },
    { id: 96 , file: 'assets/seals/seal-96.jpg', label: 'Worship', tag: 'Ritual scene' },
    { id: 97 , file: 'assets/seals/seal-97.jpg', label: 'Geometric', tag: 'Abstract' },
    { id: 98 , file: 'assets/seals/seal-98.jpg', label: 'Standard', tag: 'Cultic emblem' },
    { id: 99 , file: 'assets/seals/seal-99.jpg', label: 'Jar suffix sign', tag: 'Most frequent terminal' },
    { id: 100, file: 'assets/seals/seal-100.jpg', label: 'Script-only', tag: 'Inscription tag' },
    { id: 101, file: 'assets/seals/seal-101.jpg', label: 'Bull + man', tag: 'Composite scene' },
    { id: 102, file: 'assets/seals/seal-102.jpg', label: 'Crescent', tag: 'Lunar' },
    { id: 103, file: 'assets/seals/seal-103.jpg', label: 'Multi-sign', tag: 'Long register' },
    { id: 104, file: 'assets/seals/seal-104.jpg', label: 'Bull worship', tag: 'Ritual' },
    { id: 105, file: 'assets/seals/seal-105.jpg', label: 'Hand sign', tag: 'Anthropomorphic mark' },
    { id: 106, file: 'assets/seals/seal-106.jpg', label: 'Compound', tag: 'Multi-element' },
    { id: 107, file: 'assets/seals/seal-107.jpg', label: 'Tiger', tag: 'Predator' },
    { id: 108, file: 'assets/seals/seal-108.jpg', label: 'Procession', tag: 'Animal sequence' },
    { id: 109, file: 'assets/seals/seal-109.jpg', label: 'Tree + bull', tag: 'Sacred tableau' },
    { id: 110, file: 'assets/seals/seal-110.jpg', label: 'Geometric', tag: 'Abstract' },
    { id: 111, file: 'assets/seals/seal-111.jpg', label: 'Inscription', tag: 'Script tag' },
    { id: 112, file: 'assets/seals/seal-112.jpg', label: 'Composite', tag: 'Hybrid' },
    { id: 113, file: 'assets/seals/seal-113.jpg', label: 'Worship', tag: 'Ritual' },
    { id: 114, file: 'assets/seals/seal-114.jpg', label: 'Long sign-row', tag: 'Extended inscription' },
    { id: 115, file: 'assets/seals/seal-115.jpg', label: 'Tablet form', tag: 'Trade marker' },
    { id: 116, file: 'assets/seals/seal-116.jpg', label: 'Bull', tag: 'Standard' },
    { id: 117, file: 'assets/seals/seal-117.jpg', label: 'Compound', tag: 'Multi-register' },
    { id: 130, file: 'assets/seals/seal-130.jpg', label: 'Bull standard', tag: 'Cultic emblem' }
  ],

  /* — major cities — */
  cities: [
    {
      name: 'Mohenjo-daro',
      loc: 'Sindh · Pakistan',
      summary: 'The largest excavated Indus city. The Great Bath, granary, citadel & lower town, and dense civic drainage — the archetype of Mature Harappan urbanism.',
      stats: ['c. 250+ ha', 'pop. ~40,000', 'discovered 1922'],
      detail: [
        'Identified in 1922 by R. D. Banerji of the Archaeological Survey of India.',
        'Layout: a fortified citadel mound (west) with the Great Bath, granary, and assembly hall; and a sprawling lower town on a strict grid.',
        'The Great Bath (c. 12 × 7 × 2.4 m) is the earliest known public water tank — waterproofed with bitumen. Likely ritual, not utilitarian.',
        'Standardized fired-brick ratios (1 : 2 : 4), covered drains, soak pits, and wells in nearly every house.',
        'Famous artefacts: the Priest-King statuette, the Dancing Girl bronze, hundreds of unicorn seals.'
      ]
    },
    {
      name: 'Harappa',
      loc: 'Punjab · Pakistan',
      summary: 'The eponymous site of the civilization. Excavated since 1921 and still the longest-running Harappan dig — sequencing pre-urban Ravi through Late Harappan transitions.',
      stats: ['c. 150 ha', 'first excavated 1921', 'multi-period'],
      detail: [
        'First reported by Charles Masson in 1829; excavated by Daya Ram Sahni from 1920–21 — the type-site after which the civilization is named.',
        'Continuous occupation from Ravi phase (c. 3700 BCE) through Late Harappan (~1300 BCE) — the deepest cultural sequence.',
        'Granary, working platforms, and barracks of the citadel mound; cemetery R-37 yields the longest series of mature-Harappan burials.',
        'Major centre for shell-bangle production, copper/tin alloys, and seal manufacture.'
      ]
    },
    {
      name: 'Dholavira',
      loc: 'Gujarat · India',
      summary: 'A masterpiece of stone urbanism and water engineering. Three-tier division, 16 reservoirs, and the world\'s earliest known signboard.',
      stats: ['c. 100 ha', 'UNESCO 2021', 'three-tier plan'],
      detail: [
        'Excavated by R. S. Bisht (ASI) from 1989–2005. UNESCO World Heritage inscribed in 2021.',
        'Layout: citadel · middle town · lower town — a tripartite division unique in the Harappan world.',
        'Built almost entirely of dressed stone (not just brick), with massive defensive walls.',
        '16 reservoirs harvested every drop of seasonal monsoon water — one of the earliest water-conservation systems known.',
        'The "Dholavira Signboard": ten large gypsum-inlaid signs, 37 cm tall each, mounted over the north citadel gate. The largest known Indus inscription.'
      ]
    },
    {
      name: 'Lothal',
      loc: 'Gujarat · India',
      summary: 'A planned port-town with the world\'s oldest known dock, bead workshops, and direct evidence of Persian Gulf trade.',
      stats: ['c. 2400 BCE', 'dockyard 218 × 37 m', 'bead workshop'],
      detail: [
        'Excavated by S. R. Rao (ASI) from 1955–62.',
        'The trapezoidal dockyard — 218 × 37 m, with a regulated water inlet — is widely considered the earliest known artificial dock.',
        'Bead-making industry: carnelian, agate, steatite — finished beads exported to Mesopotamia.',
        'A separate "fire altar" complex; debated as ritual or industrial.',
        'Cemetery yields paired burials and grave goods of trade-class artefacts.'
      ]
    },
    {
      name: 'Rakhigarhi',
      loc: 'Haryana · India',
      summary: 'Possibly the largest Harappan site by area. Source of the 2018 ancient-DNA study reframing the Aryan migration debate.',
      stats: ['c. 350 ha', 'aDNA 2018', '7 mounds'],
      detail: [
        'Spread across seven mounds in Hisar district, Haryana — recent surveys suggest the site may exceed 300 ha, potentially the largest known Harappan settlement.',
        'Excavations by A. Nath (ASI), then Vasant Shinde (Deccan College).',
        '2018: Shinde et al. extracted ancient DNA from a Rakhigarhi female skeleton — the only successful aDNA from mature Harappan remains. The genome shows Iranian-related farmer + South Asian hunter-gatherer ancestry, with no detectable Steppe component.',
        'This finding reframed the Indo-Aryan migration debate — Steppe ancestry enters the gene pool only later, post-Harappan.'
      ]
    },
    {
      name: 'Kalibangan',
      loc: 'Rajasthan · India',
      summary: '"Black bangles." The first ploughed field in human archaeology, fire-altars, and a distinctive citadel-and-lower-town plan.',
      stats: ['c. 11.5 ha', 'on dry Ghaggar', 'fire-altars'],
      detail: [
        'Excavated by B. B. Lal and B. K. Thapar (ASI), 1960–69.',
        'The earliest ploughed field in the world: a furrowed surface in the Early Harappan layer, with two plough directions at 90° — identical to traditional Indian agriculture today.',
        'Distinctive "fire altars" with ash, bones, and terracotta cakes — interpreted by some as ritual hearths.',
        'Twin-mound plan: small citadel (west) and lower town (east), separated and individually fortified.',
        'The drying of the Ghaggar-Hakra channel correlates with site abandonment c. 1900 BCE.'
      ]
    },
    {
      name: 'Banawali',
      loc: 'Haryana · India',
      summary: 'Pre-Harappan to Harappan continuity, distinctive plan, and a famous toy plough that confirmed agricultural practice.',
      stats: ['c. 16 ha', 'plough toy', 'three phases'],
      detail: [
        'Excavated by R. S. Bisht (ASI), 1973–84.',
        'Three cultural phases: Pre-Harappan, Harappan, and Late Harappan.',
        'A terracotta toy plough — direct evidence of the bullock-drawn plough in everyday use.',
        'Apsidal plan: roughly semi-circular fortification, distinct from the rectilinear plans of Mohenjo-daro / Harappa.',
        'Earliest evidence of barley, wheat, sesame, and mustard.'
      ]
    },
    {
      name: 'Surkotada',
      loc: 'Kutch · India',
      summary: 'A small fortified outpost. Centre of the long-running "horse bones" debate — possibly evidence of equine presence in mature Harappan layers.',
      stats: ['c. 1.4 ha', '~2300 BCE', 'fortified'],
      detail: [
        'Excavated by J. P. Joshi (ASI), 1964–68.',
        'Small fortified citadel-and-residential plan in the seasonal Rann of Kutch — likely a regional administrative or defensive outpost.',
        'Bones initially identified as Equus caballus (true horse) by Sándor Bökönyi in 1991; later contested by Richard Meadow and Ajita Patel as Equus hemionus (Asian wild ass).',
        'The debate is unresolved — it matters because the horse is central to the Indo-Aryan linguistic question.'
      ]
    },
    {
      name: 'Chanhudaro',
      loc: 'Sindh · Pakistan',
      summary: 'A craft-specialist town. Beadmaking, seal-cutting, and bone-working at industrial precision.',
      stats: ['c. 7 ha', 'bead workshop', 'no citadel'],
      detail: [
        'Excavated by Ernest Mackay, 1935–36.',
        'Unusually, no clear citadel — the entire site appears to be a craft-production settlement.',
        'Long-barrel carnelian beads — extraordinary precision drilling, with bow-drill marks visible. Identical beads excavated at Royal Tombs of Ur (Mesopotamia).',
        'Late Harappan layers (Jhukar phase) overlay the mature occupation — a rare in-situ transition.'
      ]
    },
    {
      name: 'Mehrgarh',
      loc: 'Balochistan · Pakistan',
      summary: 'The seedbed of the civilization — Neolithic farming, dentistry, and cotton, four millennia before the cities rose.',
      stats: ['c. 7000 BCE', 'farming origin', 'dentistry'],
      detail: [
        'Excavated by Jean-François Jarrige and Catherine Jarrige, 1974 onwards.',
        'The earliest known Neolithic settlement in South Asia — c. 7000 BCE.',
        'Earliest evidence in the world of dentistry: drilled molars on adult skulls, c. 7500 years old.',
        'Earliest South Asian cotton (c. 5000 BCE), domesticated barley, wheat, zebu cattle, and humped sheep.',
        'Provides the cultural depth from which Early Harappan and then Mature Harappan urbanism emerged.'
      ]
    }
  ],

  /* — animal & symbolic motifs — */
  motifs: [
    {
      name: 'Unicorn (one-horned bull)',
      freq: '~60% of figured seals',
      summary: 'The most common animal motif on Indus seals. Always shown in profile with a single curving horn and a "feeding manger" or "standard" before its face.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 42 Q14 34 22 36 L40 38 L48 32 L52 22 L48 26 L42 30 L40 38" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/><path d="M22 36 L18 50 M30 38 L26 50 M40 38 L42 50" stroke="#C2A878" stroke-width="1.4"/><circle cx="46" cy="34" r="1.4" fill="#D4AF37"/></svg>',
      detail: [
        'Despite the popular "unicorn" name, this is almost certainly a stylized one-horned bull rendered in strict profile — the second horn hidden behind the first.',
        'Almost always paired with a vertical "ritual standard" or "feeding trough" — possibly a censer, an incense holder, or a filtering device.',
        'Likely a clan or guild emblem rather than a deity per se. The most administratively significant motif.',
        'Yajnadevam treats the unicorn as the canonical "subject" of the inscription it carries.'
      ]
    },
    {
      name: 'Zebu bull',
      freq: '~5–7%',
      summary: 'The humped Indian cattle (Bos indicus). Realistically rendered, often massive, with prominent dewlap and high hump.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 44 Q12 32 24 30 Q26 22 32 24 Q34 28 36 32 L48 32 L52 28 L56 36 L52 44 L46 44 L42 50 L36 50 L32 44 L24 50 L18 50 L14 44 Z" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/></svg>',
      detail: [
        'Bos indicus — the indigenous humped cattle, still common in South Asia today.',
        'Renderings emphasize the muscular hump and dewlap — naturalistic, not stylized.',
        'Tend to appear on larger, often more elaborate seals — possibly indicating elite-status owners.',
        'Distinct from the unicorn in iconography and probable function.'
      ]
    },
    {
      name: 'Elephant',
      freq: '~3%',
      summary: 'The Asian elephant, often shown solo without standard. Realistic, with hatched body texture suggesting a draped cloth.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 44 Q12 26 28 24 Q44 24 50 32 L54 30 L52 38 L48 44 Q42 50 36 50 L20 50 Q12 50 10 46 Z M14 44 L16 52 M28 50 L28 56 M44 50 L44 56" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/></svg>',
      detail: [
        'Always solitary, never paired with a standard or trough.',
        'Often shown with hatched body markings — likely a draped cloth or harness, suggesting domestication.',
        'May indicate an elephant-keeping clan or a regional-power emblem.',
        'Striking in absence: in later South Asian iconography elephants are everywhere — but in Indus seals, far rarer than the unicorn.'
      ]
    },
    {
      name: 'Tiger / feline',
      freq: '~2%',
      summary: 'Aggressive striped felines, often interacting with anthropomorphic figures — a distinct iconographic register.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M10 42 Q16 34 26 34 L44 36 Q52 36 54 30 L52 40 L48 46 L40 48 L36 50 L26 48 L20 50 L14 46 Z M22 36 L20 30 M30 36 L30 28 M38 36 L40 30" stroke="#D4AF37" stroke-width="1.6" fill="none"/><circle cx="22" cy="38" r="1" fill="#D4AF37"/><circle cx="30" cy="38" r="1" fill="#D4AF37"/><circle cx="38" cy="38" r="1" fill="#D4AF37"/></svg>',
      detail: [
        'Tigers appear in tense narrative scenes — humans on trees with tigers below, or tigers facing horned figures.',
        'May represent the wild "outside" world — danger that the seal-bearer\'s authority controls.',
        'Some scholars connect tiger-with-human-headdress iconography to later goddess traditions.'
      ]
    },
    {
      name: 'Rhinoceros',
      freq: '~1.5%',
      summary: 'The single-horned Indian rhinoceros (Rhinoceros unicornis), shown realistically without standard.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 44 Q14 30 28 30 L40 32 Q50 32 52 26 L54 36 L48 44 L42 50 L34 50 L28 50 L18 50 L12 46 Z M44 30 L48 22 M44 36 L40 32" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/></svg>',
      detail: [
        'Confirms the wetter, more forested environment of the mature Harappan era — rhinos require lush riverine grassland.',
        'Always solitary, often muscular and bulky in render — emphasizing power.',
        'Appears at sites near old river-channels — Mohenjo-daro especially.'
      ]
    },
    {
      name: 'Water buffalo',
      freq: '~2%',
      summary: 'Curved-horn bovid, often paired with worshipping figures or shown alone.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 42 Q14 32 28 32 L40 34 Q50 34 52 28 L48 38 L44 44 L36 48 L26 48 L18 48 L12 44 Z M30 32 L24 22 L26 22 L32 32 M40 34 L46 24 L44 24 L38 34" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/></svg>',
      detail: [
        'The Indian water buffalo — a riverine wetland animal, also fitting the wetter Harappan environment.',
        'Famously appears on the "Pashupati" seal (M-304), under the seated horned figure.',
        'Possibly carried sacrificial connotations — buffalo sacrifice survives in later South Asian rural religion.'
      ]
    },
    {
      name: 'Composite / fantastic creatures',
      freq: '~1%',
      summary: 'Hybrids — multi-headed beasts, human-bodied animals, animals with human heads. The seal-makers\' imaginative register.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M8 44 Q12 32 26 32 L34 30 Q40 26 42 32 L42 18 L48 28 L54 34 L50 42 L42 48 L34 50 L24 50 L14 48 Z" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linejoin="round"/><circle cx="44" cy="22" r="1.5" fill="#D4AF37"/></svg>',
      detail: [
        'Includes the "tiger-headed-buffalo," "antelope-bull-elephant," and seals where one creature has features of three.',
        'Usually on larger, more carefully cut seals — suggesting non-utilitarian, mythic content.',
        'Possible parallels with later South Asian dream-fauna — though direct continuity is unproven.'
      ]
    },
    {
      name: 'Seated horned figure ("Pashupati")',
      freq: '~0.1% (singular)',
      summary: 'Seal M-304 from Mohenjo-daro: a horned, seated, possibly tri-faced figure surrounded by animals. Iconic and contested.',
      glyph: '<svg viewBox="0 0 64 64"><path d="M22 12 L32 20 L42 12 M32 20 L32 30 M22 30 Q32 36 42 30 L46 36 L42 44 L34 50 L30 50 L22 44 L18 36 Z" stroke="#D4AF37" stroke-width="1.6" fill="none"/><path d="M14 38 H8 M50 38 H56 M14 46 L8 50 M50 46 L56 50" stroke="#C2A878" stroke-width="1.4"/></svg>',
      detail: [
        'Often called the "Pashupati" or "proto-Shiva" seal — but this is interpretation, not consensus.',
        'A horned figure (possibly three-faced) seated in what looks like a yogic posture, surrounded by tiger, elephant, rhinoceros, water buffalo.',
        'Sir John Marshall (1931) read it as a "Lord of Beasts." Later scholars — Doris Srinivasan, Asko Parpola — have argued for alternatives.',
        'A foundational artefact in any discussion of Indus religion and its possible relation to later Hindu traditions.'
      ]
    }
  ],

  /* — Indus script signs (visual approximations for the strip) — */
  scriptGlyphs: [
    'M10 6 V42 M10 6 L26 22 L10 38',
    'M6 24 H42 M24 6 V42',
    'M6 12 H42 M6 24 H42 M6 36 H42',
    'M24 6 L6 42 H42 Z',
    'M8 8 H40 V40 H8 Z M14 14 H34 V34 H14 Z',
    'M24 6 V42 M14 14 H34 M14 30 H34',
    'M6 24 Q24 6 42 24 Q24 42 6 24',
    'M10 10 L38 10 L24 38 Z',
    'M8 8 L40 40 M40 8 L8 40 M24 8 V40',
    'M6 24 H42 M14 14 L24 24 L14 34 M34 14 L24 24 L34 34',
    'M24 6 V42 M10 12 L24 24 L38 12 M10 36 L24 24 L38 36',
    'M14 8 H34 V40 H14 Z M14 24 H34 M22 8 V24 M26 24 V40',
    'M10 24 Q24 10 38 24 Q24 38 10 24 M24 18 V30',
    'M6 8 V40 H42 M6 24 H30 M30 8 V24',
    'M24 6 L40 24 L24 42 L8 24 Z',
    'M12 12 H36 V36 H12 Z M16 16 H32 V32 H16 Z M22 22 H26 V26 H22 Z'
  ]
};
