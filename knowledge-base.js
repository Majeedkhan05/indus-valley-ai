/* =========================================================
   INDUS VALLEY AI — Knowledge Base
   Curated, sourced, scholarly answers within the Indus domain
   ========================================================= */

window.IVA_KB = {

  /* — domain gate — anything *outside* these themes is rejected — */
  inDomainKeywords: [
    'indus','harappa','harappan','mohenjo','daro','dholavira','lothal','rakhigarhi',
    'kalibangan','banawali','surkotada','chanhudaro','mehrgarh','meluhha','dilmun',
    'magan','sarasvati','saraswati','ghaggar','hakra','seal','seals','script','sign',
    'unicorn','zebu','pashupati','priest-king','priest king','dancing girl','great bath',
    'granary','bead','beads','carnelian','steatite','ivory','aDNA','dna','aryan',
    'bronze age','south asia','south-asian','sindh','punjab','gujarat','haryana',
    'rajasthan','balochistan','kutch','citadel','fortification','drainage','ploughed',
    'plough','horse-bone','horse bone','equus','swastika','script signs','tablet',
    'amulet','seal corpus','meadow','kenoyer','possehl','parpola','marshall','rao',
    'bisht','shinde','wheeler','jarrige','mackay','sahni','banerji','indus inscriptions',
    'yajnadevam','indusscript','authority structure','meluhhan','cuneiform indus',
    'shortugai','magan','oman','bahrain','ur','susa','kish','tell abraq','ras al-jinz',
    'hakra phase','ravi phase','sothi','siswal','bhirrana','ganweriwala','farmana'
  ],

  /* — scoped responses by topic. Each topic has multiple keyword hooks — */
  topics: [

    /* ── greetings / first-time visitor ───────── */
    {
      keys: ['hi','hello','hey','greetings','good morning','good afternoon','good evening','what can you do','help me','who are you','what are you','introduce yourself','start','how to use'],
      title: 'Welcome — I am Indus Valley AI',
      sources: 'AI Hub Projects · Mahindra University',
      body: [
        '👋 <strong>Welcome.</strong> I am <strong>Indus Valley AI</strong> — a domain-restricted scholarly research assistant for the <em>Indus / Harappan Civilization</em> (c. 3300–1300 BCE).',
        '<strong>What I can do:</strong> Answer your questions about Indus cities, seals, the script, motifs, trade with Mesopotamia, urban planning, religion, decline, archaeology — drawn from a curated 71-topic knowledge base citing primary sources (Marshall, Wheeler, Mahadevan, Kenoyer, Possehl, Parpola, Yajnadevam).',
        '<strong>Try asking me:</strong>',
        '<ul><li><em>"What is the Indus Valley Civilization?"</em></li><li><em>"Tell me about the unicorn seal"</em></li><li><em>"How is Dholavira different from Mohenjo-daro?"</em></li><li><em>"What did the Indus people trade with Mesopotamia?"</em></li><li><em>"Why did the civilization decline?"</em></li></ul>',
        '<strong>Or use the quick-question buttons below the chat box</strong> to explore curated topics like the unicorn motif, the Great Bath, the fish sign, and more.',
        '<strong>Boundary:</strong> I only answer Indus / Harappan questions. For anything else, please use a general-purpose AI.'
      ]
    },

    /* ── overview ─────────────────────── */
    {
      keys: ['what is the indus valley','what is indus valley','what is the harappan','what is the indus civilization','tell me about the indus','tell me about indus valley','about the indus valley','overview of indus','introduce indus','introduction to indus','what does indus valley','what does the indus','what is iv c','about ivc'],
      title: 'The Indus / Harappan Civilization — overview',
      sources: 'Kenoyer 1998 · Possehl 2002 · Wright 2010 · ASI reports',
      body: [
        '<strong>Direct answer:</strong> The Indus Valley Civilization (also called Harappan) was one of the world\'s three earliest urban civilizations — alongside Mesopotamia and Egypt — flourishing c. 3300–1300 BCE across present-day Pakistan, northwestern India, and parts of Afghanistan, covering roughly 1.25 million km² (the largest of the three by area).',
        '<strong>Evidence:</strong>',
        '<ul><li>Major mature-phase cities (c. 2600–1900 BCE) — Mohenjo-daro, Harappa, Dholavira, Rakhigarhi, Lothal, Kalibangan — show planned grids, fired-brick architecture in a 1:2:4 ratio, and city-scale drainage systems [Marshall 1931; Wheeler 1947].</li><li>A shared but undeciphered script appears on ~4,000 inscribed seals and tablets [Mahadevan 1977].</li><li>Long-distance trade with Mesopotamia is documented in Sumerian records as "Meluhha"; etched carnelian beads and Indus seals appear at Ur, Susa, and Kish [Possehl 2002].</li><li>No royal palaces, throne rooms, or military scenes — unlike contemporary Mesopotamia and Egypt [Kenoyer 1998].</li></ul>',
        '<strong>Interpretation:</strong> The combination of urban sophistication and apparent absence of monarchic display suggests a non-traditional political order — possibly governed by trade-house councils, religious-civic elites, or guild federations rather than kings.',
        '<strong>Alternative view:</strong> Some scholars argue the absence of royal monuments may reflect preservation bias — wooden palaces, perishable thrones, and unrecorded oral political traditions could have existed without leaving archaeological traces.',
        '<strong>Limitation:</strong> The script remains undeciphered, so we cannot read any contemporary administrative or political records. Most lower-town areas at Mohenjo-daro lie below the modern water table — what we see is a partial sample.'
      ]
    },

    /* ── seals — general ───────────────── */
    {
      keys: ['what are the seals','what are indus seals','about the seals','about indus seals','tell me about the seals','tell me about seals','square seals','steatite seal','seal corpus','administrative seal','seal usage','how were the seals','what is a seal'],
      title: 'Indus seals — what they are and what they do',
      sources: 'Parpola 1994 · Mahadevan 1977 · Kenoyer 1998 · CISI corpus',
      body: [
        '<strong>Direct answer:</strong> Indus seals are small (~3 cm) square stamps of fired steatite (soapstone), each carrying a single line of script (5-6 signs on average) above an animal motif. They functioned as administrative stamps — pressed into clay bullae and tags to mark goods, transactions, or institutional ownership.',
        '<strong>Evidence:</strong>',
        '<ul><li>Roughly 4,000 inscribed seals catalogued in the <em>Corpus of Indus Seals and Inscriptions</em> (CISI 1-3.2, Parpola et al.) [CISI 1, p.5].</li><li>Standard format: 5-6 script signs above an animal motif, often with a "feeding standard" or pole emblem in front [Mahadevan 1977].</li><li>The unicorn (one-horned bull) appears on ~60% of figured seals — vastly more than any other motif [Kenoyer 1998].</li><li>Indus seals excavated at Mesopotamian sites (Ur, Susa, Kish) confirm their use as trade-credentials over 2,500 km away [Possehl 2002].</li></ul>',
        '<strong>Interpretation:</strong> Seals likely encoded names, titles, clan-emblems, or trade-house identities — functioning as the Harappan equivalent of personal monograms or corporate seals. The standardised format across the entire civilization area suggests an integrated administrative system.',
        '<strong>Alternative view:</strong> A minority view, defended by Steve Farmer and colleagues (2004), argues the seals may be heraldic or magical rather than truly linguistic — though this position has been weakened by the 2009 entropy analysis (Rao et al., Science).',
        '<strong>Limitation:</strong> The script is undeciphered, so the actual readings remain unknown. Yajnadevam\'s recent decipherment hypothesis (a Sanskrit-based reading) is contested and not yet accepted by the field.'
      ]
    },

    /* ── unicorn motif ─────────────────── */
    {
      keys: ['unicorn','one-horned','one horned','single-horn','unicorn seal','unicorn motif'],
      title: 'The "unicorn" motif on Indus seals',
      sources: 'Parpola 1994 · Kenoyer 1998 · Mahadevan 1977',
      body: [
        '<strong>Direct answer:</strong> The so-called "unicorn" on Indus seals is almost certainly a stylised one-horned bull, drawn in strict profile so the second horn is hidden behind the first. It is the most frequent animal motif in the entire corpus — appearing on roughly 60% of figured seals — and its meaning is widely interpreted as a clan, guild, or administrative emblem rather than a deity.',
        '<strong>Evidence:</strong>',
        '<ul><li>Anatomical features (humped back, body proportions) match a stylised bull rather than any known wild animal [Kenoyer 1998].</li><li>The motif appears on ~60% of figured seals — vastly above what would be expected for any naturalistic animal [Parpola 1994].</li><li>It is almost always paired with a "standard" or "manger" — a vertical pole with a domed fixture in front of the animal\'s face [Mahadevan 1977].</li><li>Distribution is geographically uniform across the civilization — Mohenjo-daro, Harappa, Lothal, Dholavira all produced unicorn seals in similar proportion.</li></ul>',
        '<strong>Interpretation:</strong> The high frequency, stylisation, and standardised pairing with the manger suggest the unicorn functioned as a heraldic emblem — likely identifying a major institution, clan, or office that operated across the civilization.',
        '<strong>Alternative view:</strong> Yajnadevam\'s decipherment proposes the unicorn marks the seal as belonging to a specific kin-group or lineage. A different reading by Parpola associates it with a high-status priestly or administrative class.',
        '<strong>Limitation:</strong> Without a deciphered script, the specific institution the unicorn represented cannot be confirmed. The "manger" object\'s function (cult emblem? censer? filter?) remains debated.'
      ]
    },

    /* ── pashupati ─────────────────────── */
    {
      keys: ['pashupati','m-304','horned figure','seated figure','proto-shiva','proto shiva','lord of beasts'],
      title: 'The "Pashupati" seal (M-304)',
      sources: 'Marshall 1931 · Srinivasan · Parpola',
      body: [
        'Seal M-304 from Mohenjo-daro — a horned, seated figure on a low platform, possibly with three faces, surrounded by a tiger, elephant, rhinoceros, water buffalo, and two ibexes/antelopes below.',
        '<strong>Sir John Marshall (1931)</strong> read it as a "Lord of Beasts" and called it the <em>proto-Shiva</em> — interpreting the figure as a meditating, horn-crowned deity of the wild. This reading entered popular culture and is still widely repeated.',
        '<strong>But the consensus has shifted.</strong> Doris Srinivasan and others argue the figure may be female, may not be ithyphallic, may be a buffalo-headed deity, and that the "yogic posture" is overstated. There is no inscription confirming an identification.',
        'It remains a <em>singular</em> object — there is no known second example of this iconography, which makes interpretation especially fragile.',
        'It is best treated as <em>iconographic evidence of a horned divinity tradition</em> in the Indus world, with the proto-Shiva equation being one possibility among several.'
      ]
    },

    /* ── script — status ───────────────── */
    {
      keys: ['script','indus script','deciphered','decipher','undeciphered','can we read','reading'],
      title: 'The Indus script — current status',
      sources: 'Mahadevan corpus · Parpola · Yajnadevam · indusscript.net',
      body: [
        'The Indus script is <strong>not yet deciphered</strong>. It is one of the great open problems of historical linguistics — no bilingual ("Rosetta") text has been found.',
        '<strong>Sign inventory:</strong> ~400 distinct signs. Too many for a pure alphabet (typically 20–40 signs), too few for a pure logography (typically thousands). The likely answer: a <em>logo-syllabic</em> system — a mix of word-signs and syllable-signs.',
        '<strong>Inscription length:</strong> very short. Most inscriptions are <em>4–6 signs</em>; the longest known is 26 signs. This shortness is the central obstacle — there is simply not enough text.',
        '<strong>Reading direction:</strong> mostly right-to-left, evidenced by sign-cramping at the left edge of seals and by mirror-impression analysis of seal/sealing pairs.',
        '<strong>Major attempts:</strong> Asko Parpola (Dravidian language), S. R. Rao (early Indo-Aryan), Iravatham Mahadevan (Dravidian, agnostic), Yajnadevam (computational + Indo-Aryan), Steve Farmer / Witzel / Sproat (the <em>"non-linguistic" hypothesis</em> — claiming it is not writing at all, which most epigraphers dispute).',
        '<strong>Honest answer:</strong> we can identify recurring signs, position rules, and likely word-boundaries, but we cannot yet read the inscriptions phonetically with any consensus.'
      ]
    },

    /* ── great bath ────────────────────── */
    {
      keys: ['great bath','public tank','bath of mohenjo','ritual bath'],
      title: 'The Great Bath of Mohenjo-daro',
      sources: 'Marshall 1931 · Wheeler 1953 · Kenoyer',
      body: [
        'Located on the citadel mound at Mohenjo-daro, the <strong>Great Bath</strong> is a rectangular sunken pool — approximately <em>12 m long × 7 m wide × 2.4 m deep</em>.',
        'It is the <strong>earliest known public water tank in the world</strong> — predating Roman baths by 2,000+ years.',
        'Construction is striking: tightly fitted fired bricks, with a layer of <em>bitumen waterproofing</em> sealed between two brick courses. The floor sloped gently toward a corner drain.',
        'A <em>wide brick walkway</em> with small flanking rooms (possibly changing rooms) surrounded the pool. A nearby well supplied water; a corbelled drain emptied it.',
        '<strong>Function:</strong> almost certainly <em>ritual</em>, not utilitarian — the architectural prominence on the citadel mound, plus its scale, argues for ceremonial bathing or purification rites. South Asian religious traditions of ritual immersion are very ancient — the Great Bath may be the earliest physical evidence of that lineage.'
      ]
    },

    /* ── priest-king ───────────────────── */
    {
      keys: ['priest-king','priest king','priest king statue','steatite figure'],
      title: 'The "Priest-King" statuette',
      sources: 'Marshall 1931 · Possehl · Kenoyer',
      body: [
        'A <strong>17.5 cm steatite bust</strong> excavated at Mohenjo-daro in 1927 — a bearded, tonsured man wearing a robe with trefoil patterns, a fillet headband with a circular ornament at the forehead, and an armband.',
        'The eyes are heavily inlaid (now lost) and downcast — the figure has often been read as meditating or ceremonially detached.',
        '<strong>The name "Priest-King" is a guess</strong> — coined by Sir Mortimer Wheeler. There is no inscription, no parallel statue, and no consensus on what this figure represents.',
        'It may be a <em>priest, an elder, a clan leader, or a generic dignitary</em>. Crucially, the Indus civilization shows <em>no clear iconography of monarchy</em> — no king-on-throne scenes, no royal tombs, no palace structure. So calling this a "king" likely projects later models onto an unknown society.',
        '<strong>The trefoil pattern</strong> on the robe is significant — it appears at Mesopotamian sites too and may indicate a shared elite iconography of the early Bronze Age.'
      ]
    },

    /* ── dancing girl ──────────────────── */
    {
      keys: ['dancing girl','dancing-girl','bronze figurine','lost wax'],
      title: 'The Dancing Girl',
      sources: 'Marshall 1931 · Kenoyer',
      body: [
        '<strong>10.5 cm bronze figurine</strong>, excavated at Mohenjo-daro in 1926. A nude female figure, hand on hip, head tilted, wearing only a stack of bangles on her left arm and a necklace.',
        'Cast using the <em>lost-wax (cire perdue) technique</em> — a sophisticated metallurgical method, then unique in South Asia.',
        'The pose is unusually relaxed and naturalistic — not the rigid frontal stance typical of contemporary Mesopotamian or Egyptian figures.',
        'The name "Dancing Girl" was given by John Marshall — modern scholars are cautious. She may simply be a young woman, an attendant, or a representation we cannot read.',
        'A second, smaller bronze (about 7 cm) of similar style was also found — confirming this is a <em>genre</em>, not a one-off.'
      ]
    },

    /* ── urban planning / drainage ─────── */
    {
      keys: ['urban planning','drainage','sewer','sanitation','grid','town planning','city plan','planned cities','indus city plan','harappan city','sewerage','toilets','bathroom','wells indus'],
      title: 'Indus urban planning & drainage',
      sources: 'Marshall 1931 · Wheeler 1947 · Kenoyer 1998 · Bisht (Dholavira)',
      body: [
        '<strong>Direct answer:</strong> Mature Harappan cities (c. 2600–1900 BCE) display the world\'s earliest known examples of cardinal-grid urban planning, standardised brick architecture, and city-scale sanitation — features unmatched by contemporary Mesopotamia or Egypt.',
        '<strong>Evidence:</strong>',
        '<ul><li><em>Grid layout:</em> Mohenjo-daro\'s main streets run 9–10 m wide on cardinal axes, with residential lanes branching at right angles [Marshall 1931].</li><li><em>Two-mound plan:</em> a raised western "citadel" with public buildings (Great Bath, granary, assembly hall) and a larger eastern "lower town" with residential blocks [Wheeler 1947].</li><li><em>Brick standardisation:</em> a 1 : 2 : 4 ratio (thickness : width : length) is maintained from Mohenjo-daro to Lothal, ~1,500 km apart — a unique civilizational standard [Kenoyer 1998].</li><li><em>Drainage:</em> covered brick drains run under main streets with regular inspection manholes; most houses have private bathing platforms and seated toilets feeding into them [Marshall 1931].</li><li><em>Wells:</em> Mohenjo-daro has ~700 documented wells — roughly one per three houses [Mackay 1937–38].</li><li><em>Dholavira:</em> three-tier walled division (castle · middle town · lower town), 16 reservoirs cut into rock, and stone (not brick) construction [Bisht].</li></ul>',
        '<strong>Interpretation:</strong> The level of standardisation across 1.25 million km² implies <em>some</em> form of central authority or shared technical tradition — but the source of that authority is invisible. Public works (drainage, baths, wells) are over-developed; royal/military display is under-developed. This pattern likely reflects civic priorities very different from contemporary Mesopotamia.',
        '<strong>Alternative view:</strong> Some scholars argue the apparent uniformity is overstated — local variation in drainage quality, brick sizes, and city layouts exists, and "standardisation" may reflect shared craft traditions rather than top-down imposition.',
        '<strong>Limitation:</strong> Most lower town areas at Mohenjo-daro and Harappa lie below the modern water table or under modern settlements — what we see is a partial sample. The script remains undeciphered, so any administrative records that might explain the system are unreadable.'
      ]
    },

    /* ── Mohenjo-daro vs Harappa ───────── */
    {
      keys: ['mohenjo','daro','difference','versus','vs','compare'],
      title: 'Mohenjo-daro vs Harappa vs Dholavira',
      sources: 'ASI reports · Kenoyer · Bisht',
      body: [
        '<strong>Mohenjo-daro (Sindh):</strong> the largest excavated Harappan city — c. 250+ ha, peak population ~40,000. Famous for the Great Bath, the Priest-King statue, and dense residential drainage. Built almost entirely of fired brick.',
        '<strong>Harappa (Punjab):</strong> the type-site, c. 150 ha. Continuously occupied from Ravi phase (c. 3700 BCE) through Late Harappan — the deepest cultural sequence. Major shell-bangle and seal-cutting industries; rich cemeteries (R-37).',
        '<strong>Dholavira (Gujarat, India):</strong> c. 100 ha. Unique three-tier plan, almost entirely <em>stone</em> construction, the famous <em>signboard</em> (10 large signs over the citadel gate), and 16 reservoirs harvesting monsoon rain.',
        '<strong>Together:</strong> they show the Harappans were not a single capital with provinces — but a <em>polycentric</em> civilization where each major centre had its own variations on a shared template.'
      ]
    },

    /* ── trade with mesopotamia ────────── */
    {
      keys: ['trade with mesopotamia','indus mesopotamia','indus trade','what did indus trade','what did the indus trade','what indus trade','what did indus people trade','trade with mesopotamians','meluhha','sumerian texts','dilmun','magan','persian gulf','indus exports','indus imports','carnelian export','indus carnelian','queen puabi','mesopotamia trade','trade route mesopotamia','what did they trade','traded with sumer','traded with ur','meluhhan'],
      title: 'Indus trade with Mesopotamia',
      sources: 'Possehl 2002 · Kenoyer 1998 · Akkadian/Ur III cuneiform texts',
      body: [
        '<strong>Direct answer:</strong> The Indus civilization had active long-distance trade with Mesopotamia (c. 2400–1900 BCE), exporting <em>carnelian beads, ivory, shell ornaments, hardwoods, possibly cotton, and exotic animals</em>, while likely importing <em>silver, wool, tin, and grain</em>. The Mesopotamians referred to the Indus as <em>"Meluhha"</em>.',
        '<strong>Evidence:</strong>',
        '<ul><li>Cuneiform texts of the Akkadian and Ur III periods name <em>Meluhha</em> as a source of carnelian, ivory, and exotic goods [Possehl 2002].</li><li>Etched carnelian beads of distinctive Harappan technique have been excavated at Ur — including in the Royal Tombs of Queen Puabi [Kenoyer 1998].</li><li>Indus seals have been recovered at Ur, Kish, Susa, and Tell Asmar — including hybrid "Persian Gulf seals" mixing Indus and local iconography [CISI corpus].</li><li>Cuneiform records mention a "Meluhhan village" at Lagash, suggesting an Indus expatriate community in southern Mesopotamia.</li><li>The Indus weight system (cubical chert standard ~13.6 g) was adopted in the Persian Gulf region [Kenoyer 1998].</li></ul>',
        '<strong>Interpretation:</strong> Trade was bidirectional, organised, and persistent — likely conducted by professional merchant networks operating through intermediate maritime hubs at <em>Dilmun</em> (Bahrain) and <em>Magan</em> (Oman). The presence of an Indus expatriate community at Lagash suggests sustained commercial relations rather than occasional exchanges.',
        '<strong>Alternative view:</strong> Some scholars argue much of the trade was indirect — via Dilmun and Magan middlemen — and that direct Indus-Mesopotamian contact was limited to specialised goods. The volume of trade is debated.',
        '<strong>Limitation:</strong> Most evidence comes from Mesopotamian sites; what the Indus imported in return is poorly documented because perishable goods (textiles, grain, oils) leave little archaeological trace.'
      ]
    },

    /* ── dholavira ─────────────────────── */
    {
      keys: ['dholavira','signboard','reservoir','three-tier','kutch'],
      title: 'Dholavira (Gujarat)',
      sources: 'R. S. Bisht · ASI · UNESCO 2021',
      body: [
        'Excavated by <strong>R. S. Bisht (ASI)</strong> from 1989–2005. Inscribed on the <strong>UNESCO World Heritage list in 2021</strong>.',
        '<strong>Plan:</strong> uniquely <em>three-tier</em> — citadel (highest), middle town, and lower town — each with its own fortifications. No other Harappan site has this division.',
        '<strong>Construction:</strong> almost entirely <em>dressed stone</em>, in contrast to the brick-dominant Mohenjo-daro / Harappa. Massive defensive walls.',
        '<strong>Water:</strong> 16 reservoirs surrounded the city, harvesting every drop of seasonal rainfall in arid Kutch. Among the earliest large-scale water-conservation systems in the world.',
        '<strong>The signboard:</strong> ten large gypsum-inlaid Indus signs, each ~37 cm tall, mounted over the north citadel gate. It is the longest known Indus inscription on permanent display — and probably the earliest known <em>monumental</em> public inscription in the world.'
      ]
    },

    /* ── lothal ────────────────────────── */
    {
      keys: ['lothal','dock','port','dockyard'],
      title: 'Lothal — the Bronze Age port',
      sources: 'S. R. Rao · ASI',
      body: [
        '<strong>S. R. Rao</strong> excavated Lothal between 1955–62. It sits in modern Gujarat near the head of the Gulf of Khambhat.',
        'The site\'s defining feature is a <strong>trapezoidal basin — 218 m × 37 m</strong> — with brick-lined walls, a regulated water inlet from a tidal channel, and what may be a sluice gate. It is widely identified as the <em>earliest known artificial dockyard</em>.',
        '<strong>Bead-making industry:</strong> Lothal\'s factory district produced carnelian, agate, and steatite beads of extraordinary precision. Identical Lothal-type beads have been excavated at Ur and other Mesopotamian sites.',
        '<strong>Fire altar complex:</strong> a row of small mud-brick installations, with ash and charred bones — interpreted by S. R. Rao as ritual fire altars (a Vedic continuity). Others read them as industrial. Open question.',
        'Lothal is the clearest evidence that the Harappans were <em>maritime</em>, not just riverine — they built a port, scheduled tides, and exported their goods directly across the Arabian Sea.'
      ]
    },

    /* ── rakhigarhi / aDNA ─────────────── */
    {
      keys: ['rakhigarhi','adna','dna','genome','aryan migration','aryan','indo-aryan','steppe','migration','shinde'],
      title: 'Rakhigarhi & the 2018 ancient-DNA study',
      sources: 'Shinde et al. 2019 (Cell) · Reich Lab',
      body: [
        '<strong>Rakhigarhi (Haryana, India)</strong> is possibly the largest Harappan site by area, spread over seven mounds. Excavated by A. Nath and later Vasant Shinde.',
        '<strong>2019 (Shinde et al., <em>Cell</em>):</strong> a single intact ancient genome was extracted from a Rakhigarhi female skeleton — the only successful aDNA from mature-Harappan remains so far.',
        '<strong>Findings:</strong> the genome is a mix of <em>Iranian-related farmer</em> ancestry (the same Iranian lineage seen at Ganj Dareh, but pre-agricultural) and <em>South Asian hunter-gatherer</em> ancestry (Andamanese-related). Crucially: <em>no detectable Steppe component</em>.',
        '<strong>Implication:</strong> Steppe ancestry — long associated with the entry of Indo-European languages into South Asia — enters the Indian gene pool <em>after</em> mature Harappan times, c. 2000–1500 BCE.',
        'This reframes the Indo-Aryan migration debate: the Harappans were not Steppe-derived. Whether they spoke a Dravidian, Indo-Aryan, or now-lost language remains open — but the genetic profile favours a non-Steppe origin.'
      ]
    },

    /* ── horse bone / aryan question ───── */
    {
      keys: ['horse','horse bone','equus','surkotada bones','aryan invasion'],
      title: 'The "horse bone" debate',
      sources: 'Bökönyi 1991 · Meadow & Patel · Witzel',
      body: [
        'The horse (<em>Equus caballus</em>) is central to the Indo-Aryan linguistic question — Indo-European cultures were horse-using; classical Vedic literature is full of horse imagery and the horse-sacrifice (ashvamedha).',
        'In the Indus seal corpus, the horse is <strong>conspicuously absent</strong> as a motif. Bulls, elephants, rhinos, tigers — no horses.',
        '<strong>Surkotada (Kutch, India)</strong> yielded equid bones in mature-Harappan layers. <em>Sándor Bökönyi (1991)</em> identified them as true horse — <em>Equus caballus</em>. <em>Richard Meadow and Ajita Patel</em> later contested this, identifying the bones instead as the half-ass (<em>Equus hemionus</em>, the onager).',
        '<strong>Where the field stands:</strong> the identification is unresolved. Even if a few horse bones do exist, they\'re too rare to argue for a horse-using Indus culture — there is no clear horse iconography, no horse-related vocabulary on seals, no chariots.',
        'Combined with the Rakhigarhi aDNA result, the picture is: <em>the horse arrived later, with Steppe-related populations, not with the Harappans.</em>'
      ]
    },

    /* ── decline ───────────────────────── */
    {
      keys: ['decline','collapse','end of indus','disappear','abandon','why did the indus end'],
      title: 'How the civilization ended',
      sources: 'Possehl · Wright · Giosan et al.',
      body: [
        'The Indus did <em>not</em> collapse catastrophically. It <strong>de-urbanized</strong> over c. 1900–1300 BCE.',
        '<strong>Climate / hydrology:</strong> the Ghaggar-Hakra channel (often equated with the Vedic <em>Sarasvati</em>) progressively dried as the Sutlej and Yamuna rivers shifted course away from it. The summer monsoon also weakened across South Asia c. 2200 BCE.',
        'Cities depending on year-round riverine agriculture (Mohenjo-daro, Harappa, Kalibangan) lost their economic basis. Smaller, more rain-dependent settlements continued.',
        '<strong>Population shift:</strong> people moved <em>east and south</em> — into the upper Ganga-Yamuna doab and into Gujarat. Late Harappan villages (Cemetery H culture in Punjab, Jhukar in Sindh, Painted Grey Ware later) carry forward elements of material culture.',
        '<strong>What was lost:</strong> standardized weights, the script, the seal system, large-scale civic architecture, long-distance trade.',
        '<strong>What survived:</strong> agricultural practices, cattle breeds, ceramic traditions, beadmaking, bangle-wearing, and likely some religious motifs (horned figures, water-buffalo symbolism, ritual bathing).'
      ]
    },

    /* ── religion / belief ─────────────── */
    {
      keys: ['religion','belief','god','goddess','mother goddess','ritual','worship','temple'],
      title: 'Indus religion — what we can and cannot say',
      sources: 'Marshall · Parpola · Possehl',
      body: [
        'There is <strong>no temple architecture</strong> securely identified at any Harappan site — no monumental cult structure, no royal/divine iconography on the scale of Mesopotamian ziggurats or Egyptian temples.',
        'What we have: <em>ritual structures</em> (the Great Bath, the fire altars at Kalibangan and Lothal, possibly), <em>female terracotta figurines</em> (often called "mother goddess" figures, abundant at most sites), and <em>iconography on seals</em> (horned figures, sacred trees, animal-procession scenes).',
        '<strong>The horned-figure tradition</strong> (M-304 etc.) is the strongest candidate for a structured cult. Horns appear on multiple human-figure seals, on standards, and on terracotta figurines.',
        '<strong>Sacred trees</strong> — particularly the pipal (sacred fig) — appear repeatedly with deities or worshippers in front of them.',
        '<strong>Honest position:</strong> we know the Harappans had ritual practice, water-related cult, terracotta votive culture, and likely a horned-divinity tradition. We do <em>not</em> know whether their religion was a direct ancestor of historical Hinduism — the gap is over a millennium, and the script silences us.'
      ]
    },

    /* ── weights & measures ────────────── */
    {
      keys: ['weight','weights','measure','standardization','cubical chert'],
      title: 'Indus weights & measures',
      sources: 'Hemmy · Mainkar · Kenoyer',
      body: [
        'Indus weights are tiny <strong>cubical chert/jasper objects</strong>, exquisitely cut, in a binary-then-decimal system: <em>1, 2, 4, 8, 16, 32, 64</em>, then 160, 320, 640, 1600, 3200, 6400, 8000, 12800.',
        'The basic unit is approximately <strong>0.85 g</strong> — and the standard weight (16 units = ~13.6 g) was used as the trade-standard across the Persian Gulf.',
        '<strong>What this implies:</strong> a single regulatory authority — or at minimum a tightly enforced merchant convention — covering 1.5 million km², plus exports.',
        'This degree of metrological standardization is <em>unique in the early Bronze Age</em>. Mesopotamia had multiple competing standards; Egypt had its own; the Indus did not.',
        'Combined with brick-ratio standardization, it argues for an exceptionally administrative, rule-bound society — even though we cannot identify the rulers.'
      ]
    },

    /* ── carnelian beads ───────────────── */
    {
      keys: ['carnelian','beads','etched','long beads','bead-making'],
      title: 'Carnelian beads — a Harappan signature export',
      sources: 'Kenoyer · Possehl',
      body: [
        'Carnelian — a deep red-orange variety of chalcedony — was the prestige bead material of the Bronze Age. The Harappans dominated its supply.',
        '<strong>Long-barrel carnelian beads</strong> (4–10 cm) are the showpiece — drilled with bow-driven copper-and-emery tools through their full length, a process that took weeks per bead. The bow-drill marks are still visible on excavated examples.',
        '<strong>Etched carnelian:</strong> beads decorated with white-on-red geometric designs, etched using an alkali paste. The technique is uniquely Indus.',
        '<strong>Centres of production:</strong> Chanhudaro, Lothal, and Dholavira — site-specific bead workshops have been identified.',
        '<strong>Export:</strong> identical Indus-type carnelian beads have been excavated at Ur (Queen Puabi\'s tomb), Kish, Mari, and even further west.'
      ]
    },

    /* ── meluhha ───────────────────────── */
    {
      keys: ['meluhha','meluhhan','sumerian texts on indus','cuneiform indus'],
      title: '"Meluhha" — what the Mesopotamians called the Indus',
      sources: 'Sumerian/Akkadian texts · Possehl',
      body: [
        'In Sumerian and Akkadian texts of c. 2400–1700 BCE, <strong>Meluhha</strong> is the easternmost of three foreign trade lands — the order being <em>Dilmun</em> (Bahrain) → <em>Magan</em> (Oman) → <em>Meluhha</em> (the Indus).',
        '<strong>Meluhhan exports</strong> mentioned in cuneiform: carnelian, hardwoods, ivory, gold, lapis lazuli (transit), live animals (peacocks).',
        'A few texts mention <em>Meluhhans living at Lagash</em> — likely an expatriate trading community in a Sumerian city.',
        'The seal of <em>Shu-ilishu</em> (early 2nd-millennium Mesopotamia) describes him as a <em>"Meluhhan interpreter"</em> — direct evidence that the Indus had its own language(s) and that Mesopotamian merchants needed translators.',
        'The identification of Meluhha = Indus is now near-universal among Assyriologists and South Asian archaeologists.'
      ]
    },

    /* ── women ─────────────────────────── */
    {
      keys: ['women','female','gender','dancing girl society','status of women'],
      title: 'Women in the Indus world',
      sources: 'Kenoyer · Clark · figurine analyses',
      body: [
        '<strong>Female terracotta figurines</strong> are the single most numerous figurative artefact across Harappan sites — often simply called "mother goddesses," though that label is interpretive.',
        'Many figurines wear elaborate hairdos, fan headdresses, multiple bangles, and necklaces — likely reflecting actual fashion.',
        '<strong>The Dancing Girl bronze</strong> (Mohenjo-daro) shows a confident, naturalistic female pose unusual in the early Bronze Age — most contemporary representations of women are passive.',
        '<strong>Burial goods</strong> at Harappa and Rakhigarhi show that women were buried with substantial ornaments — bangles, beads, mirrors — implying status independent of male association.',
        '<strong>Honest limit:</strong> we do not know whether women had legal autonomy, inheritance rights, or political power. We know they were materially well-equipped and iconographically prominent.'
      ]
    },

    /* ── farming ───────────────────────── */
    {
      keys: ['agriculture','farming','crop','wheat','barley','cotton','rice','irrigation'],
      title: 'Indus agriculture',
      sources: 'Fuller · Madella · Weber',
      body: [
        '<strong>Staple crops:</strong> wheat, barley, peas, lentils, sesame, mustard, dates. Rice appears later in Late Harappan and especially in Gujarat / Eastern Punjab.',
        '<strong>Cotton</strong> — possibly the world\'s earliest cotton cultivation. Domesticated cotton fibres are documented at Mehrgarh from c. 5000 BCE; cotton textile fragments survive at Mohenjo-daro.',
        '<strong>Plough agriculture:</strong> the <em>Kalibangan ploughed field</em> (Early Harappan) is the earliest known ploughed surface in the world — with two plough directions at 90°, identical to traditional Indian agricultural practice.',
        '<strong>Animals:</strong> zebu cattle (Bos indicus), water buffalo, sheep, goat, pig, camel (Late Harappan). Notably <em>no horse</em>.',
        '<strong>Irrigation:</strong> mostly <em>flood-recession</em> agriculture along the Indus and Ghaggar-Hakra. Dholavira shows extensive water-harvesting reservoirs in arid zones.'
      ]
    },

    /* ── language ──────────────────────── */
    {
      keys: ['language','what language','dravidian','indo-aryan','indo aryan','what did they speak'],
      title: 'What language did the Harappans speak?',
      sources: 'Parpola · Witzel · Yajnadevam',
      body: [
        'We do not know — and we cannot know with certainty until the script is read.',
        '<strong>Three main hypotheses:</strong>',
        '<strong>1. Proto-Dravidian</strong> — championed by Asko Parpola. Argument: surviving Dravidian languages (Tamil, Kannada, etc.) are present-day descendants of a once-northern language family that retreated south after the collapse. Some sign-position rules in the Indus script fit Dravidian-style agglutinative morphology.',
        '<strong>2. Early Indo-Aryan</strong> — championed by S. R. Rao and recently Yajnadevam. Argument: positional and statistical patterns in the script may map onto early Indo-Aryan, and some seal-inscriptions resemble Vedic-style names.',
        '<strong>3. A lost language family</strong> — possibly related to none of the surviving South Asian families. Argument: some loanwords in early Sanskrit (the so-called "Para-Munda" stratum) cannot be explained by Dravidian or Indo-Aryan and may be substrate vocabulary from the Harappan language.',
        '<strong>Honest conclusion:</strong> the Indo-Aryan hypothesis is harder to reconcile with the Rakhigarhi aDNA result (no Steppe ancestry); the Dravidian hypothesis is the working consensus among most epigraphers; but no decipherment is yet accepted.'
      ]
    },

    /* ── swastika ──────────────────────── */
    {
      keys: ['swastika','svastika','symbol','geometric symbol'],
      title: 'The swastika in Indus material culture',
      sources: 'Mahadevan · Kenoyer',
      body: [
        'The <strong>swastika</strong> appears on a small number of Indus seals (most catalogued as <em>geometric symbol seals</em>) and on terracotta tablets — both clockwise and counter-clockwise variants.',
        'It is part of a broader inventory of geometric/auspicious symbols that includes the <em>endless knot</em>, concentric circles, and the cross-in-square — most of which carry forward into later South Asian iconography.',
        'It is worth being explicit: the swastika is an ancient pan-Eurasian symbol of auspiciousness — it appears in Anatolian Neolithic, Trojan, Mesopotamian, Greek, Mongolian, Native American, and South Asian contexts. Its appearance on Indus seals confirms the Harappans participated in this older symbol-economy.',
        'The 20th-century European appropriation has nothing to do with the symbol\'s ancient meanings.'
      ]
    },

    /* ── chronology / phases ───────────────── */
    {
      keys: ['chronology','phases','dating','radiocarbon','c14','timeline','periods','mature harappan','early harappan','late harappan','ravi phase','hakra phase','kot diji','sothi siswal','amri','nal'],
      title: 'Chronology — Indus phases & dating',
      sources: 'Possehl 2002 · Kenoyer 1998 · Wright 2010',
      body: [
        'The civilization is divided into three broad phases plus a pre-urban substrate.',
        '<strong>Pre-Harappan / Early Food-Producing (c. 7000–3300 BCE):</strong> Mehrgarh Neolithic. Cultivation, pottery, terracotta figurines, dentistry. The cultural depth from which urbanism eventually grew.',
        '<strong>Early Harappan (c. 3300–2600 BCE):</strong> regional cultures crystallize — Ravi (Punjab), Hakra (Cholistan), Kot Diji (Sindh), Sothi-Siswal (Haryana), Amri (Sindh), Nal (Balochistan). Proto-script signs appear. Pre-urban, pre-standardization.',
        '<strong>Mature Harappan (c. 2600–1900 BCE):</strong> the great cities. Standardized weights, brick ratios, drainage, seal-script, long-distance trade. The "Indus Civilization" in the strict sense.',
        '<strong>Late Harappan / Localization Era (c. 1900–1300 BCE):</strong> de-urbanization. Material culture continues in regional variants — Cemetery H (Punjab), Jhukar (Sindh), Rangpur III (Gujarat), and into Painted Grey Ware in the upper Ganga-Yamuna doab.',
        '<strong>Dating methods:</strong> radiocarbon (C14) on charcoal, seeds, bone collagen — calibrated against the IntCal curve. Optically Stimulated Luminescence (OSL) on brick and pottery. Stratigraphy correlated across sites.'
      ]
    },

    /* ── brick technology ─────────────────── */
    {
      keys: ['brick','bricks','brick ratio','fired brick','kiln','baked brick','mud brick'],
      title: 'Indus brick technology — the most precise of the Bronze Age',
      sources: 'Wright 2010 · Kenoyer · ASI reports',
      body: [
        '<strong>Standard ratio:</strong> 1 : 2 : 4 (thickness : width : length) — maintained from Mohenjo-daro to Lothal, ~1,500 km apart, for over six centuries. No other Bronze Age civilization came close to this consistency.',
        '<strong>Common sizes:</strong> the most frequent residential brick is c. 7 × 14 × 28 cm; civic and platform bricks scale up to 10 × 20 × 40 cm — but always in the 1:2:4 ratio.',
        '<strong>Fired brick</strong> dominates major cities — produced in updraft kilns. Mud brick was used for less critical work and sometimes as a core, with fired brick as facing.',
        '<strong>Why this matters:</strong> the brick standard implies central supervision of construction across the entire civilization, OR a deeply embedded merchant convention. Either way, an unprecedented level of administrative coherence.',
        '<strong>Mortar:</strong> mud mortar, with bitumen used selectively for waterproofing (Great Bath, drains).'
      ]
    },

    /* ── copper / bronze metallurgy ────────── */
    {
      keys: ['copper','bronze','metallurgy','metalwork','tin','arsenic','smelting','alloy'],
      title: 'Copper & bronze metallurgy',
      sources: 'Kenoyer · Possehl · Hoffman & Miller',
      body: [
        '<strong>Pure copper</strong> dominates early — Mehrgarh has hammered native copper from c. 4000 BCE. Mature Harappan workshops smelted ore in crucibles.',
        '<strong>Bronze</strong> (copper + tin) appears in significant quantity by 2500 BCE. Famous example: the <em>Dancing Girl</em> bronze, lost-wax cast.',
        '<strong>Tin sources</strong> are debated — possibly Afghanistan / Central Asia via Shortugai; some evidence for Rajasthan tin too. The Indus may have controlled an early tin-trade route.',
        '<strong>Tools:</strong> chisels, axes, blades, fish-hooks, razors, pins, tweezers, mirrors. Mostly simple — Indus metallurgy is competent rather than spectacular.',
        '<strong>Arsenical copper</strong> is documented at Harappa — an early bronzing alternative when tin was scarce.',
        'Notable absence: <em>no large-scale weapon manufacture</em>. Indus metallurgy is overwhelmingly oriented toward tools, ornaments, and ritual objects — not warfare.'
      ]
    },

    /* ── pottery & ceramics ────────────────── */
    {
      keys: ['pottery','ceramic','black slip','reserved slip','black on red','painted pottery','pots'],
      title: 'Indus pottery — typology',
      sources: 'Mackay · Wright · Dales',
      body: [
        '<strong>Black-on-red ware</strong> is the Indus signature — wheel-thrown, slip-painted with motifs of pipal leaves, fish-scale patterns, peacocks, intersecting circles, and "comb-and-trident" devices.',
        '<strong>Reserved Slip Ware</strong> — characteristic of the Mature Harappan, with patterns produced by partially wiping the slip before firing.',
        '<strong>Black-and-red ware</strong> (a fired-then-reduced two-tone) appears later, in the Late Harappan / post-urban transition.',
        '<strong>Forms:</strong> dish-on-stand (a near-universal Indus form), perforated jars (likely for fermentation/straining), goblets, storage jars, beakers.',
        '<strong>Faience</strong> — a glazed, fritted material used for beads, tiles, small figurines. The Indus mastered faience technology earlier and more widely than most Bronze Age cultures.'
      ]
    },

    /* ── seal-making & manufacture ─────────── */
    {
      keys: ['seal making','seal manufacture','steatite firing','how were seals made','seal cutting','seal drill'],
      title: 'How a seal was actually made',
      sources: 'Kenoyer · Vidale · Mackay',
      body: [
        '<strong>Material:</strong> steatite — a soft soapstone, easily carved. The Harappans then heat-treated it to harden it and produce the characteristic ivory-white surface (heating converts talc to enstatite).',
        '<strong>Carving:</strong> with copper-and-emery drills, fine bronze chisels, and abrasive paste. Cut depth was typically 1–2 mm — enough to leave a clean impression in clay.',
        '<strong>Mirror-image rule:</strong> the seal carving is the mirror of what appears on the clay impression. Engravers had to think backwards, sign by sign.',
        '<strong>Drilling the boss:</strong> nearly all seals have a perforated knob on the back — drilled with a copper bit and emery, suspended on a cord.',
        '<strong>Workshops:</strong> seal-cutting workshops have been excavated at Mohenjo-daro, Harappa, and Chanhudaro. The cutting precision varies — some seals are masterpieces, others are clearly trade-grade.',
        '<strong>Sealings (bullae):</strong> the actual clay impressions made by these seals have been excavated at Lothal, Mohenjo-daro, Kanmer (Gujarat), and at Mesopotamian sites — confirming the seals were used administratively, not just buried with owners.'
      ]
    },

    /* ── faience & bead drilling ───────────── */
    {
      keys: ['ernestite','bead drill','drilling','ernestite drill','long carnelian','precision drilling'],
      title: 'The Ernestite drill — Harappan precision',
      sources: 'Kenoyer · Mackay',
      body: [
        'The Indus carnelian bead industry depended on a specialty stone-tipped drill called <strong>"Ernestite"</strong> (also spelled Ernestine) — named by Mark Kenoyer.',
        'It is a hard, fine-grained, naturally occurring metamorphic rock — found and shaped specifically for drilling. Harder than regular quartz; required no metal cutting edge.',
        'With this drill plus an emery-paste lubricant and a bow-drill setup, Harappan artisans drilled <em>4–10 cm long carnelian beads</em> through their full length — a process that took weeks per bead.',
        'No comparable drilling technology existed in contemporary Mesopotamia. The Harappans had a near-monopoly on long carnelian beads; the Mesopotamian elite imported them.',
        'The Ernestite drill is one of the clearest examples of Bronze Age tech-superiority in the Indus — and of the Indus economy specializing for export.'
      ]
    },

    /* ── terracotta figurines ──────────────── */
    {
      keys: ['terracotta','figurine','figurines','clay figure','votive','mother goddess'],
      title: 'Terracotta figurines',
      sources: 'Clark · Kenoyer · Vidale',
      body: [
        'Terracotta figurines are the <strong>most numerous figurative artefact</strong> across Harappan sites — thousands recovered.',
        '<strong>Female figurines</strong> dominate — often with elaborate fan-shaped headdresses, multiple necklaces, bangles. Frequently called "mother goddesses," though that\'s interpretive.',
        '<strong>Animal figurines:</strong> bulls, monkeys (often carrying objects — possibly toys), tortoises, oxen, pigs. Often hand-modelled, occasionally moulded.',
        '<strong>Wheeled animal toys:</strong> bulls and rams on small clay wheels — direct evidence of the wheel in everyday use, and possibly the earliest known children\'s wheeled toys.',
        '<strong>Cart toys:</strong> miniature bullock-carts identical in form to those still used in rural South Asia.',
        '<strong>Whistles:</strong> bird-shaped terracotta whistles — suggesting both children\'s play and possibly signalling.'
      ]
    },

    /* ── toys & games ──────────────────────── */
    {
      keys: ['toys','games','dice','board game','pachisi','hopscotch'],
      title: 'Indus toys, games, and play',
      sources: 'Kenoyer · Mackay',
      body: [
        '<strong>Dice:</strong> long, four-sided cubical dice — including some clearly weighted to fall on certain numbers. The 1-2-3-4 numbering convention on Indus dice is identical to historical South Asian dice.',
        '<strong>Board games:</strong> incised gaming boards have been excavated — likely ancestors of <em>chaupar</em> / pachisi.',
        '<strong>Marbles:</strong> stone and clay spheres, in graduated sizes.',
        '<strong>Wheeled animal toys:</strong> miniature bulls, rams, and carts on terracotta wheels — pulled by string by Bronze Age children.',
        '<strong>Cooking-pot miniatures:</strong> tiny replicas of full-size storage and cooking vessels — children\'s play, or possibly votive.',
        'These objects matter scientifically: they show that the Indus people had leisure, family life, taught their children, and that play culture was elaborate. Bronze Age civilizations are not just about elites and trade.'
      ]
    },

    /* ── architecture details ──────────────── */
    {
      keys: ['architecture','corbelled','arch','vault','flooring','roofing','timber','brick architecture'],
      title: 'Indus architecture — building practice',
      sources: 'Marshall · Wheeler · Bisht',
      body: [
        '<strong>Foundations:</strong> deep brick foundations, often stepped, on packed earth or rubble. Houses were built to last centuries.',
        '<strong>Walls:</strong> fired brick exterior, mud brick interior partitions in many cases. Wall thickness scaled with storey count.',
        '<strong>Drains:</strong> covered with brick capstones, occasionally <em>corbelled</em> (false arch) for larger drains. The corbelled drain is one of the earliest known examples in the world.',
        '<strong>Stairs:</strong> brick risers and treads, often steep — implying multi-storey houses (sometimes confirmed by collapsed upper-floor debris).',
        '<strong>Wells:</strong> circular, brick-lined, often built up incrementally as the water table dropped. Mohenjo-daro alone has ~700 known wells.',
        '<strong>Floors:</strong> packed clay or brick on the ground floor, suspended timber on upper floors (rarely surviving except as ash and joist sockets).'
      ]
    },

    /* ── burials ───────────────────────────── */
    {
      keys: ['burial','burials','cemetery','grave','grave goods','funeral','death','cremation','r-37','cemetery h'],
      title: 'Indus burials',
      sources: 'Hemphill et al. · Kenoyer · Shinde',
      body: [
        '<strong>Mature Harappan burial practice</strong> is mostly extended supine inhumation — body laid on its back, head to the north — accompanied by grave goods.',
        '<strong>R-37 cemetery (Harappa):</strong> the largest mature-Harappan burial sample. Bodies in shallow rectangular pits, with pots, ornaments, and occasionally copper mirrors.',
        '<strong>Grave goods are modest</strong> — there are no royal-tomb-grade burials in the Indus. No Tutankhamun, no Queen Puabi. Even the wealthiest grave is comparatively understated. This is one of the strongest arguments against monarchic political organization.',
        '<strong>Female burials at R-37</strong> are often well-equipped: bangles, mirrors, beads. Confirms women had access to material wealth.',
        '<strong>Cemetery H (Late Harappan):</strong> a different burial practice — partial cremation followed by secondary burial in painted pots. A clear cultural shift in the post-urban era.',
        '<strong>Rakhigarhi:</strong> source of the only successful mature-Harappan ancient genome (2019).'
      ]
    },

    /* ── women / dancing girl extended ─────── */
    {
      keys: ['daimabad bronze','daimabad','bronze chariot','wheeled toy','animal-pulled cart'],
      title: 'The Daimabad bronze hoard',
      sources: 'Sali · Possehl',
      body: [
        '<strong>Daimabad (Maharashtra)</strong> is the southernmost known site with Indus / Late Harappan affiliations.',
        'In 1974, four extraordinary copper-bronze figures were discovered together: a chariot drawn by two oxen, a rhinoceros, an elephant, and a water buffalo — each on a wheeled cart base.',
        'The chariot bronze (c. 45 cm long) shows a standing male driver, two yoked humped bulls, and a wheeled cart frame. Among the largest Bronze Age metal figures from South Asia.',
        '<strong>Dating is debated:</strong> originally placed in a Late Harappan context (c. 2000 BCE), but some scholars argue for a slightly later (Chalcolithic) date.',
        'Whichever the date, the hoard is the clearest indication that <em>Indus material culture extended deep into the Deccan</em> — and that the technology of wheeled animal-pulled vehicles was real and widely deployed.'
      ]
    },

    /* ── trade / shortugai ─────────────────── */
    {
      keys: ['shortugai','outpost','afghanistan','badakhshan','lapis lazuli','tin','northernmost'],
      title: 'Shortugai — the Indus outpost on the Oxus',
      sources: 'Francfort · Kenoyer',
      body: [
        '<strong>Shortugai</strong> sits in northeastern Afghanistan, on the Oxus river — far north of all other Harappan sites. It is the <em>northernmost known Indus settlement</em>.',
        'Excavated by Henri-Paul Francfort in the 1970s. Mature Harappan ceramics, seals, brick ratios — fully Indus material culture, embedded in a non-Indus geography.',
        '<strong>Why is it there?</strong> Two strategic resources: <em>lapis lazuli</em> from Badakhshan (just east), and <em>tin</em> from the Hindu Kush. Both were luxury / strategic Bronze Age commodities.',
        'Shortugai is direct evidence of an <em>Indus colonial / commercial outpost</em> — the Harappans projected their culture and trade networks deep into Central Asia.',
        'Together with Sutkagan-Dor (westernmost, on the Iran-Pakistan border) and Daimabad (southernmost, in Maharashtra), Shortugai defines the geographic outer limits of the civilization.'
      ]
    },

    /* ── sutkagan-dor / westernmost ────────── */
    {
      keys: ['sutkagan-dor','sutkagan dor','westernmost','iran border','makran'],
      title: 'Sutkagan-Dor — the westernmost outpost',
      sources: 'Stein · Dales',
      body: [
        '<strong>Sutkagan-Dor</strong> sits in the Makran coast of Pakistani Balochistan, near the Iran border — the westernmost known Harappan site.',
        'A small fortified settlement with stone-faced walls. Likely an Indus way-station on the overland Makran route to southeastern Iran and beyond, paralleling the maritime route through the Persian Gulf.',
        'Confirms that the Harappans secured both maritime AND overland routes to the west — a redundant trade infrastructure unusual for the early Bronze Age.'
      ]
    },

    /* ── fish symbol ───────────────────────── */
    {
      keys: ['fish symbol','fish sign','common sign','most common sign','fish glyph'],
      title: 'The "fish" sign — the most frequent sign in the script',
      sources: 'Mahadevan · Parpola',
      body: [
        '<strong>The "fish" sign</strong> (and a small family of fish-related variants — including "fish with diacritic" and "fish with roof") is the single most frequent sign in the Indus script corpus.',
        '<strong>Why it matters:</strong> in any logo-syllabic system the most common signs are usually pronouns, articles, or extremely high-frequency words (numbers, "is/and/the" equivalents). The fish-sign\'s frequency suggests it is one of these — not literally a fish.',
        '<strong>Parpola\'s reading:</strong> in proto-Dravidian, <em>mīn</em> = both "fish" and "star." Parpola argues the sign is a rebus — "fish/star" — and decodes star-and-numeral combinations on seals as references to constellations or planet-names.',
        '<strong>Mahadevan</strong> remained agnostic on phonetic value but accepted the sign was high-frequency and semantically central.',
        'Whether the rebus reading is correct or not, the fish-sign\'s positional regularity (it appears very often as a word-final or near-final sign) is one of the strongest <em>statistical</em> signals that the script is real linguistic writing.'
      ]
    },

    /* ── pipal motif ──────────────────────── */
    {
      keys: ['pipal','peepal','sacred tree','ficus religiosa','tree motif','tree worship'],
      title: 'The pipal tree motif',
      sources: 'Marshall · Parpola',
      body: [
        'The <strong>pipal</strong> (sacred fig, <em>Ficus religiosa</em>) appears repeatedly in Indus iconography — as a stylized leaf on pottery, as a full tree on seals, and as the central element of "deity-in-tree" seals.',
        '<strong>The "deity-in-pipal" seal</strong> (M-1186 from Mohenjo-daro): a horned figure stands inside a stylized pipal arch, while seven figures stand below in procession. One of the most discussed religious-iconography seals.',
        '<strong>Continuity:</strong> the pipal is sacred in later Hindu, Buddhist, and Jain traditions — most famously as the bodhi tree under which the Buddha attained enlightenment. The Indus pipal motif is the earliest known sacralisation of this species.',
        '<strong>Pipal-leaf pottery patterns</strong> on Indus black-on-red ware confirm the tree was iconic in everyday material culture, not just elite cult.'
      ]
    },

    /* ── 4.2k climate event ───────────────── */
    {
      keys: ['climate','monsoon','4.2k','4.2 ka','climate change','aridification','drought','holocene'],
      title: 'The 4.2-ka event — climate & Indus decline',
      sources: 'Giosan et al. 2012 · Dixit et al.',
      body: [
        '<strong>The 4.2 thousand-year event</strong> (~2200 BCE) is a global climate anomaly: a sharp, multi-century weakening of monsoonal and Mediterranean rainfall systems. It correlates with the collapse of the Old Kingdom in Egypt, the Akkadian empire in Mesopotamia, and the de-urbanization of the Indus.',
        '<strong>Indus evidence:</strong> Giosan et al. (2012) showed the summer monsoon weakened significantly in northwestern South Asia after c. 2200 BCE. Lake-sediment isotopes from Kotla Dahar (Haryana, near Rakhigarhi) — Dixit et al. — show a sharp aridification spike.',
        '<strong>Hydrological consequence:</strong> the Ghaggar-Hakra channel, fed by erratic monsoonal flows, dried progressively. Cities depending on it lost their water and agricultural base.',
        '<strong>This was not the sole cause</strong> — but climate provides the underlying stress that made political/economic restructuring inevitable. The Indus did not collapse — it migrated and decentralized in response.'
      ]
    },

    /* ── why no kings ─────────────────────── */
    {
      keys: ['kings','monarchy','no king','elite','government','political','rulers','authority'],
      title: 'Why we cannot identify Indus kings',
      sources: 'Possehl · Kenoyer · Authority Structure paper',
      body: [
        'In Mesopotamian and Egyptian archaeology, kings are everywhere — royal tombs, palace complexes, throne-scene iconography, named inscriptions, royal seals, gigantic public statuary.',
        'In the Indus we have <em>none of this</em>. No royal tomb, no palace complex, no throne-scene seal, no over-life-size royal statue, no inscription that names a ruler.',
        '<strong>What the absence means:</strong> the Indus was either (a) governed by a council/oligarchy/merchant guild rather than a king, or (b) had royal practices that left no archaeological signature, or (c) deliberately suppressed individual elite display in favor of standardization.',
        'The <em>Authority Structure</em> paper argues this third option: the Indus civilization built its administrative coherence through <em>standardization</em> (weights, brick ratios, seals) rather than personal monarchy — a strikingly different model from Mesopotamia or Egypt.',
        'It remains entirely possible that the Indus had local rulers — but the lack of monumental royal display is itself a positive piece of evidence about how their society was organized.'
      ]
    },

    /* ── archaeologists ───────────────────── */
    {
      keys: ['archaeologists','marshall','wheeler','kenoyer','possehl','parpola','bisht','shinde','cunningham','sahni','banerji','rao','mackay','jarrige'],
      title: 'The archaeologists — who excavated what',
      sources: 'multiple monographs',
      body: [
        '<strong>Alexander Cunningham</strong> (1875): first noted Harappa, mistook the seals for medieval. Founded the ASI.',
        '<strong>Daya Ram Sahni</strong> (1921): first systematic excavation at Harappa.',
        '<strong>R. D. Banerji</strong> (1922): identified Mohenjo-daro and the link with Harappa.',
        '<strong>Sir John Marshall</strong> (1924, 1931): announced the civilization to the world; published the foundational three-volume <em>Mohenjo-daro and the Indus Civilization</em>.',
        '<strong>Ernest Mackay</strong> (1927–31): expanded Mohenjo-daro excavations; later excavated Chanhudaro.',
        '<strong>Sir Mortimer Wheeler</strong> (1944): re-excavated Harappa, introduced rigorous stratigraphy. Also coined the (now disputed) "Aryan invasion" reading of skeletons.',
        '<strong>S. R. Rao</strong> (1955–62): excavated Lothal, identified the dockyard.',
        '<strong>R. S. Bisht</strong> (1989–2005): excavated Dholavira and Banawali. Argued for systematic Vedic-Harappan continuity.',
        '<strong>J. Mark Kenoyer</strong> (Harappa, ongoing): the leading living American Harappan archaeologist; standard reference text <em>Ancient Cities of the Indus Valley Civilization</em>.',
        '<strong>Gregory Possehl</strong> (1941–2011): comparative scholar; <em>The Indus Civilization: A Contemporary Perspective</em>.',
        '<strong>Asko Parpola</strong> (Helsinki, ongoing): the leading Indus script scholar; champion of the proto-Dravidian hypothesis.',
        '<strong>Vasant Shinde</strong> (Rakhigarhi, 2011–): led the project that produced the 2019 ancient-DNA genome.',
        '<strong>Iravatham Mahadevan</strong> (1930–2018): produced the standard concordance of the Indus script.'
      ]
    },

    /* ── Indus vs Mesopotamia vs Egypt ────── */
    {
      keys: ['compare','comparison','egypt','sumer','sumerian','egyptian','three civilizations','old world'],
      title: 'Indus vs Mesopotamia vs Egypt',
      sources: 'Possehl · Kenoyer · comparative archaeology',
      body: [
        '<strong>Geography:</strong> Indus c. 1.5 million km² — by area the largest of the three. Egypt c. 30,000 km² (the Nile valley). Sumer c. 20,000 km² (Tigris-Euphrates lower).',
        '<strong>Cities:</strong> Indus had multiple comparably-sized centres (Mohenjo-daro, Harappa, Dholavira, Rakhigarhi). Mesopotamia had multiple competing city-states. Egypt was unified under a single ruler.',
        '<strong>Writing:</strong> all three developed script systems c. 3300–3100 BCE. Egyptian and Sumerian were deciphered in the 19th century; the Indus is still undeciphered.',
        '<strong>Monarchy:</strong> overt and ubiquitous in Egypt and Mesopotamia. Absent from the Indus archaeological record — no royal tombs, palaces, or throne-scenes.',
        '<strong>Standardization:</strong> the Indus is uniquely standardized — bricks, weights, seal sizes, urban grid. The other two are far more locally variable.',
        '<strong>Warfare:</strong> Mesopotamia and Egypt have abundant weapon assemblages and battle iconography. The Indus has minimal weapon culture — no battle scenes, no fortified palaces, no royal armies in iconography.',
        '<strong>Trade:</strong> the Indus traded with Mesopotamia (carnelian, ivory) but not (so far as we know) with Egypt directly. Mesopotamia knew the Indus as <em>Meluhha</em>.',
        'The Indus is the most distinctive of the three early urban civilizations — and arguably the most modern in its standardization, sanitation, and apparent civic egalitarianism.'
      ]
    },

    /* ── ghaggar-hakra / saraswati ────────── */
    {
      keys: ['ghaggar','hakra','saraswati','sarasvati','river','dried river','vedic river'],
      title: 'The Ghaggar-Hakra / Sarasvati river',
      sources: 'Giosan et al. · Valdiya · Possehl',
      body: [
        'The <strong>Ghaggar-Hakra</strong> is a now-seasonal river system running through Haryana, Rajasthan, and Cholistan. Many of the Mature Harappan sites — including Rakhigarhi, Kalibangan, Banawali, Bhirrana, and Ganweriwala — lie along its dry channel.',
        'It is widely identified — though contested — with the <strong>Sarasvati</strong> river of the Rigveda.',
        '<strong>Geological evidence:</strong> the Ghaggar-Hakra was once a major perennial river fed by the Sutlej and Yamuna. Tectonic shifts and stream piracy diverted both tributaries (the Sutlej into the Indus, the Yamuna into the Ganga) sometime in the 2nd millennium BCE.',
        'Result: the once-mighty river dwindled to a seasonal channel, and Harappan settlements depending on it were progressively abandoned.',
        '<strong>Why this matters:</strong> if Ghaggar-Hakra = Sarasvati, then the Rigveda preserves memory of a river-system that was geographically active in the Harappan era — implying a closer chronological/cultural relationship between the Harappan world and early Vedic culture than once thought.',
        '<strong>Caution:</strong> the identification is not universally accepted. The simpler conclusion — that the Indus relied on a now-vanished river system, and that this contributed to its decline — is on much firmer ground.'
      ]
    },

    /* ── parpola decipherment ─────────────── */
    {
      keys: ['parpola','parpola decipherment','dravidian decipherment','proto-dravidian'],
      title: 'Parpola — the Dravidian decipherment hypothesis',
      sources: 'Parpola 1994 · Parpola 2018',
      body: [
        '<strong>Asko Parpola</strong> (Helsinki) is the most prominent advocate of a <em>proto-Dravidian</em> reading of the Indus script.',
        '<strong>Core argument:</strong> the script\'s positional regularity matches an agglutinative, suffix-rich language family — which fits Dravidian (Tamil, Telugu, Kannada, Malayalam, Brahui in Pakistan today) far better than Indo-European.',
        '<strong>Famous example — the fish/star rebus:</strong> proto-Dravidian <em>mīn</em> = "fish" AND "star." Parpola argues that "fish + numeral" combinations on seals encode <em>star-name + numeral</em> = constellations or planets.',
        '<strong>Brahui:</strong> a Dravidian language is still spoken by ~2 million people in Balochistan, Pakistan — within the historical Indus heartland. Parpola treats this as a relic distribution, supporting his hypothesis.',
        '<strong>Status:</strong> the Dravidian hypothesis is the working consensus among most epigraphers but is not accepted as decipherment — no proposed reading has produced consistent, falsifiable translations of the corpus.'
      ]
    },

    /* ── yajnadevam decipherment ──────────── */
    {
      keys: ['yajnadevam','yajnadevam decipherment','indo-aryan decipherment','vedic decipherment'],
      title: 'Yajnadevam — the recent computational claim',
      sources: 'Yajnadevam 2023 · Indus Inscriptions',
      body: [
        '<strong>Yajnadevam</strong> (2023, <em>Indus Inscriptions</em>) proposes a computational + statistical decipherment, arguing the script is logo-syllabic and phonetically tied to <em>early Indo-Aryan</em>.',
        '<strong>Approach:</strong> entropy analysis, sign-positional rules, comparison with later Brahmi-derived scripts, and a proposed phonetic mapping.',
        '<strong>Reception:</strong> mainstream Indus scholarship remains skeptical — partly because (a) the proposed phonetic readings have not been independently replicated, (b) the early Indo-Aryan hypothesis is harder to reconcile with the Rakhigarhi aDNA finding (no Steppe ancestry in Mature Harappan individuals), and (c) the corpus is too short for purely statistical decipherment to be definitive.',
        '<strong>What\'s valuable in the work:</strong> rigorous quantitative analysis of the corpus, regardless of whether the proposed phonetic readings are correct. The book\'s database and entropy work are useful baseline material.'
      ]
    },

    /* ── fire altars debate ───────────────── */
    {
      keys: ['fire altar','fire altars','altar','kalibangan altar','lothal altar','vedic altar','agni'],
      title: 'The fire altars debate',
      sources: 'Lal · Bisht · Marshall',
      body: [
        '<strong>What was found:</strong> at Kalibangan, Lothal, and Banawali, archaeologists excavated rectangular brick or clay-lined structures with ash, charred bones, and terracotta cakes inside.',
        '<strong>The "fire altar" reading</strong> (B. B. Lal, R. S. Bisht): these are ritual fire-altars analogous to the <em>yajna</em> altars of the later Vedic tradition. If correct, this would imply Indus-Vedic ritual continuity.',
        '<strong>The skeptical reading</strong>: they may be cooking hearths, industrial firing pits, or domestic fireplaces. The "ritual" interpretation projects later practice backwards.',
        '<strong>Where the evidence points:</strong> the Kalibangan structures were found in a row, in a non-domestic location, with terracotta cakes (a uniquely Harappan artefact) — features that are easier to explain ritually than industrially. But certainty is not available.',
        'It remains one of the strongest pieces of suggestive — not conclusive — evidence for Vedic-Harappan continuity.'
      ]
    },

    /* ═══════════════════════════════════════════════════════════════
       PUBLIC-DOMAIN EXPANSION CORPUS
       Sources: Marshall 1931 (PD India), Mackay 1937-38 (PD India),
       Vats 1940 (PD), ASI Annual Reports (PD govt), Wikipedia (CC-BY-SA)
       All entries cite primary public-domain works only.
       ═══════════════════════════════════════════════════════════════ */

    /* ── DK area, mohenjo-daro ──────────── */
    {
      keys: ['dk area','dk-area','dk g','dk-g','dk-b','dk b','mackay excavation','mackay area','dk mohenjo','lower town mohenjo','mackay mohenjo'],
      title: 'The DK Area at Mohenjo-daro',
      sources: 'Mackay 1937–38 (PD)',
      body: [
        'The <strong>DK Area</strong> at Mohenjo-daro was excavated by <strong>E.J.H. Mackay</strong> between 1927 and 1931, after the initial Marshall excavations of 1922–1927. Mackay\'s two-volume report <em>Further Excavations at Mohenjo-daro</em> (1937–38) is the foundational record.',
        '<strong>DK-G</strong> is the largest excavated section of the Lower Town. It revealed <em>blocks of houses separated by main streets and lanes</em>, a pattern of "insula" planning where individual house clusters open inward onto courtyards rather than onto the street.',
        '<strong>Standard house plan:</strong> entrance from a side lane (never the main street), a central courtyard with rooms on three or four sides, a private bathing platform, and frequently a brick-lined well within the house.',
        '<strong>Notable finds in DK area:</strong> the famous bronze "Dancing Girl" (DK 5880), the seated stone figure now in Karachi, hundreds of inscribed seals, copper tools, and the "Great Hall" of pillared construction.',
        'Mackay\'s excavation methods were carefully stratigraphic and his pottery typology is still cited. The DK Area record remains the single most detailed window into ordinary Harappan urban life.'
      ]
    },

    /* ── HR area, mohenjo-daro ──────────── */
    {
      keys: ['hr area','hr-area','hr a','hr-a','hr b','hr-b','marshall mohenjo','first excavation mohenjo'],
      title: 'The HR Area at Mohenjo-daro',
      sources: 'Marshall 1931 (PD)',
      body: [
        'The <strong>HR Area</strong> was the focus of <strong>Sir John Marshall\'s</strong> first major excavation at Mohenjo-daro (1922–1927). His three-volume report <em>Mohenjo-daro and the Indus Civilization</em> (1931) is the foundational publication of Indus archaeology.',
        '<strong>HR-A</strong> revealed a residential block on the eastern side of the Lower Town. The "House of the Well" — a large domestic complex with private well, bathing platform, and multiple rooms around a central courtyard — became the type-example of Harappan urban architecture.',
        '<strong>HR-B</strong> contained narrower houses and what Marshall interpreted as workshops, with copper-working evidence and unfinished stoneware.',
        '<strong>Construction technique:</strong> houses are built of <em>fired brick in standard 1:2:4 ratio</em> (typically 7×14×28 cm), laid in English bond. Walls of the lowest courses use unfired mud-brick filling within fired-brick faces — a technique still used in modern Sindh.',
        'Marshall\'s 1931 photographs and plans of the HR Area are still the primary reference, since much of the excavated mudbrick has since deteriorated due to salt-rise and groundwater.'
      ]
    },

    /* ── citadel mound, mohenjo-daro ────── */
    {
      keys: ['citadel mound','citadel mohenjo','western mound','high mound','sd area','l area mohenjo','acropolis indus'],
      title: 'The Citadel Mound (SD/L Areas) at Mohenjo-daro',
      sources: 'Marshall 1931 · Mackay 1937–38 · ASI Reports (all PD)',
      body: [
        'Every major Indus city is divided into a <strong>raised western "Citadel" mound</strong> and a larger eastern "Lower Town." At Mohenjo-daro, the Citadel rises about <em>12 meters</em> above the plain and measures roughly 200×400 m.',
        '<strong>Major Citadel structures (Marshall + Mackay):</strong>',
        '• <em>The Great Bath</em> — a watertight tank, 12×7×2.4 m, with bitumen-sealed brick floor.',
        '• <em>The Granary</em> — a massive raised brick platform with air-channels (Wheeler\'s interpretation; later reinterpreted as possibly a public hall).',
        '• <em>The "College" or Priests\' House</em> — a complex south of the bath, possibly residential for officials.',
        '• <em>The Pillared Assembly Hall</em> — a large rectangular space with rows of brick pillar bases, function debated.',
        'Unlike Mesopotamian citadels, the Mohenjo-daro Citadel shows <strong>no temple, no royal palace, no obvious shrine</strong>. The structures appear civic, ritual-bath-related, or storage-related rather than monarchic — a pattern unique to the Harappan world.'
      ]
    },

    /* ── great bath detail ──────────────── */
    {
      keys: ['great bath','public bath','ritual bath','mohenjo-daro bath','mohenjo daro bath','tank mohenjo','watertight'],
      title: 'The Great Bath of Mohenjo-daro',
      sources: 'Marshall 1931 (PD)',
      body: [
        'The <strong>Great Bath</strong> on the Citadel of Mohenjo-daro is one of the earliest public water-tanks in the world. Marshall (1931) recorded its dimensions precisely:',
        '<strong>Tank:</strong> 11.88 m long × 7.01 m wide × 2.43 m deep. Steps lead down at the north and south ends. A small dressing-room flanks the tank to the east.',
        '<strong>Construction:</strong> the tank is made of <em>finely sawn fired bricks set in gypsum mortar</em>, with a layer of <em>bitumen waterproofing</em> behind the visible brickwork — the earliest known use of bitumen damp-proofing in subcontinental architecture.',
        '<strong>Drainage:</strong> a corbelled brick drain at the southwest corner empties the tank. A nearby well likely supplied fresh water.',
        '<strong>Function:</strong> Marshall interpreted it as a ritual purification tank, drawing parallels to later Hindu temple tanks. It is unlikely to have been recreational — its position next to the "Granary" and "College" buildings suggests an institutional, possibly ceremonial purpose.',
        'No comparable structure has been found at any other Indus city, making the Great Bath both the most iconic and the most enigmatic Harappan monument.'
      ]
    },

    /* ── granary debate ─────────────────── */
    {
      keys: ['granary','warehouse','public storage','mohenjo granary','harappa granary','wheeler granary'],
      title: 'The "Granary" — Mohenjo-daro & Harappa',
      sources: 'Marshall 1931 · Wheeler 1947 · Vats 1940 (all PD)',
      body: [
        'Both Mohenjo-daro and Harappa preserve massive raised brick platforms which their excavators called "granaries." The interpretation has been challenged repeatedly.',
        '<strong>At Mohenjo-daro (Marshall, then Wheeler 1947):</strong> a 50×27 m brick podium on the Citadel, with regular bays separated by air-channels. Wheeler, drawing on his Roman archaeology background, read the channels as <em>ventilation for stored grain</em>.',
        '<strong>At Harappa (Vats 1940):</strong> two parallel rows of six rooms each, on a 50×40 m platform near the river, also with under-floor channels.',
        '<strong>The problem:</strong> no carbonised grain has ever been recovered from these "granaries." Modern reinterpretation (Kenoyer; Possehl) suggests they may have been:',
        '• <em>Public assembly platforms</em>',
        '• <em>Ritual or administrative buildings</em>',
        '• <em>Multi-purpose storage</em> for non-grain commodities (cloth, raw materials)',
        'The label "granary" survives in the literature for historical reasons, but it should be treated with scholarly skepticism. The structures are real and monumental — what they stored, if anything, is unknown.'
      ]
    },

    /* ── harappa mound F ────────────────── */
    {
      keys: ['mound f','mound-f','harappa f','harappa mound','vats harappa','sahni harappa','harappa excavation'],
      title: 'Harappa — Mound F and the Workmen\'s Quarters',
      sources: 'Vats 1940 (PD) · Sahni ASI Reports (PD)',
      body: [
        'Harappa was first identified as an ancient site by <strong>Charles Masson</strong> in 1829. <strong>Daya Ram Sahni</strong> began ASI excavation in 1920–21, followed by <strong>Madho Sarup Vats</strong>, whose 1940 report <em>Excavations at Harappa</em> is the public-domain primary source.',
        '<strong>Mound F</strong> contains:',
        '• The <em>Great Granary</em> (so-called) — twelve rectangular rooms on a raised brick platform near the Ravi river.',
        '• A <em>circular brick threshing platform</em> south of the granary, with a central post-hole, often interpreted as a grain-processing floor.',
        '• Rows of small two-room dwellings — Vats called these the <em>"workmen\'s quarters"</em>, possibly housing labourers attached to public works or the granary.',
        '<strong>Mound AB</strong> (the Citadel) was heavily robbed for railway ballast in the 19th century — bricks from Harappa were carted away to construct the Lahore-Multan railway line, destroying much of the upper city before formal archaeology began.',
        '<strong>Mound E and ET</strong> contain Cemetery R-37 and Cemetery H, two distinct burial assemblages that helped establish the chronology of the Harappan and Late-Harappan phases.'
      ]
    },

    /* ── cemetery R-37 ──────────────────── */
    {
      keys: ['cemetery r-37','cemetery r37','cemetery h','harappan burial','harappan cemetery','indus burial','indus cemetery'],
      title: 'Cemetery R-37 and Cemetery H — Harappa',
      sources: 'Vats 1940 (PD) · Wheeler 1947 (PD)',
      body: [
        '<strong>Cemetery R-37</strong> at Harappa is the type-cemetery of the <em>Mature Harappan</em> period (c. 2600–1900 BCE). Excavated by Vats and later refined by Wheeler, it contains:',
        '• <em>Extended supine burials</em> in north-south aligned earth pits',
        '• Wooden coffins in some graves',
        '• Grave goods: 15–40 pots per grave, copper mirrors, beads, rare ornaments — <em>but no weapons, no chariots, no horses</em>',
        '• Skeletons show diverse origins — consistent with a cosmopolitan trade city',
        '<strong>Cemetery H</strong> overlies the Mature Harappan layers and marks the <em>Late Harappan</em> transition (c. 1900–1300 BCE):',
        '• Two strata: lower with full inhumation, upper with <em>fractional</em> burial (bones in pottery jars after exposure)',
        '• Distinctive painted pottery — the "Cemetery H ware" with peacock-and-stylised-tree motifs',
        '• Smaller settlement, no mature-phase administrative goods',
        'The transition from R-37 to Cemetery H is a key stratigraphic anchor for dating the de-urbanisation of the Indus civilisation.'
      ]
    },

    /* ── wells of mohenjo-daro ──────────── */
    {
      keys: ['wells','well of mohenjo','indus wells','harappan well','brick well','water supply','seven hundred wells','mohenjo well'],
      title: 'The Wells of Mohenjo-daro — water for a city',
      sources: 'Mackay 1937–38 (PD) · Jansen ASI (PD)',
      body: [
        'Mohenjo-daro had an estimated <strong>~700 wells</strong> within the excavated portion of the city — roughly <em>one well for every three houses</em>. No other Bronze Age city comes close.',
        '<strong>Construction (Mackay 1937–38):</strong> wells were built with specially manufactured <em>wedge-shaped (trapezoidal) bricks</em> that locked together when laid in a circle, forming a self-supporting cylindrical shaft. Some wells are 5+ metres deep.',
        '<strong>Daily use:</strong> grooves worn deep into the well-rim brickwork, by ropes drawing up countless water vessels over centuries, are still visible.',
        'Many private houses had <em>their own wells inside the courtyard</em> — a level of household water access that Europe did not match until the 19th century AD.',
        '<strong>Why so many wells?</strong> Mohenjo-daro\'s dependence on the Indus is real, but the wells suggest the citizens preferred clean, uncontaminated drinking water from local groundwater rather than the silty river. They also used the water for the city\'s elaborate bathing platforms.',
        'The combination of <em>private wells + private bathrooms + covered street drains</em> is the signature water-management complex of Harappan urbanism — and is unmatched in the contemporary ancient world.'
      ]
    },

    /* ── brick standardization ──────────── */
    {
      keys: ['brick','bricks','brick size','harappan brick','indus brick','standardized brick','brick ratio','1:2:4'],
      title: 'Harappan Brick — the 1:2:4 ratio',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD)',
      body: [
        'One of the most extraordinary facts about the Indus Civilization is its <strong>uniform brick standardisation</strong> across an area larger than Mesopotamia and Egypt combined.',
        '<strong>The standard ratio:</strong> width : depth : length = <em>1 : 2 : 4</em>. The same proportion appears at Mohenjo-daro, Harappa, Lothal, Kalibangan, Dholavira — over 1,000 km apart.',
        '<strong>Common brick sizes:</strong>',
        '• Small (domestic): 7 × 14 × 28 cm',
        '• Medium: 10 × 20 × 40 cm',
        '• Large (public works): 17 × 34 × 68 cm — used at Mohenjo-daro\'s Great Bath',
        '<strong>Production:</strong> wooden moulds, sun-dried then kiln-fired. The bricks are remarkably uniform in colour and density, suggesting either centralized brick-yards or rigorously enforced standards across local kilns.',
        '<strong>Bonding pattern:</strong> the Harappans used <em>English Bond</em> (alternating courses of "headers" and "stretchers") — the same pattern still used in modern brick walls — providing maximum structural strength.',
        'For comparison, Mesopotamian and Egyptian brick sizes vary city-to-city, period-to-period, even building-to-building. The Harappan ratio is the world\'s first known engineering standard at civilizational scale.'
      ]
    },

    /* ── streets and planning ───────────── */
    {
      keys: ['street','streets','town planning','grid plan','main street','indus grid','urban grid','harappan road','road'],
      title: 'Streets and the Grid Plan',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD) · ASI (PD)',
      body: [
        'Indus cities are laid out on a <strong>cardinal grid</strong> — main streets run roughly north-south and east-west, with smaller lanes branching off at right angles. This is the world\'s earliest evidence of planned urban grid layout.',
        '<strong>Mohenjo-daro main street widths (Marshall):</strong>',
        '• Major streets (e.g. "First Street", "East Street"): 9.1 m wide',
        '• Secondary streets: 5.5–7.6 m wide',
        '• Lanes: 1.5–3 m wide',
        '<strong>Construction:</strong> streets are <em>not paved</em> — they are compacted earth, periodically resurfaced as the city level rose. Repeated flooding-and-rebuilding raised the entire urban surface several metres over the city\'s ~700-year life.',
        '<strong>Drainage in streets:</strong> brick-lined covered drains run alongside major streets, with regular inspection holes ("manholes") at intersections — see the dedicated drainage topic for detail.',
        '<strong>Doors face inward:</strong> houses open onto side lanes and courtyards, never onto main streets. The result: main streets have a smooth, undecorated façade, while domestic life happens in protected interiors. This is the opposite of contemporary Mesopotamian cities, where shops and homes opened directly onto major thoroughfares.'
      ]
    },

    /* ── drainage detail ───────────────── */
    {
      keys: ['drainage','sewer','drain','sewerage','sanitation','toilet','bathroom','indus sanitation','street drain','covered drain'],
      title: 'The Drainage System — Harappan sanitation',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD)',
      body: [
        'No Bronze Age civilization rivals the Harappan drainage system. Marshall called it "<em>the most complete ancient sanitation system known to the modern world.</em>"',
        '<strong>Household level:</strong>',
        '• Most houses have a <em>private brick-paved bathing platform</em>, slightly inclined, draining through a wall-spout into a street drain.',
        '• Many houses have <em>seated brick toilets</em>, with a vertical chute leading to a soak-pit or street drain.',
        '• Soak-pits (covered cesspits) are placed at corners — periodically emptied.',
        '<strong>Street level:</strong>',
        '• Brick-lined drains run along all major streets, covered with stone or brick slabs.',
        '• Regular <em>inspection holes</em> at intervals allow cleaning.',
        '• Drains slope continuously toward the city outskirts to ensure outflow.',
        '<strong>Sluice/cesspit detail (Mackay):</strong> drains include settling tanks where heavier waste settled before the liquid flowed onward — an early version of the modern interceptor.',
        'The fact that this level of sanitation engineering existed in <em>every</em> Indus city — not just one prestige settlement — is what most distinguishes Harappan urbanism from all its Bronze Age contemporaries.'
      ]
    },

    /* ── house architecture ─────────────── */
    {
      keys: ['houses','house','indus house','harappan house','domestic architecture','courtyard house','residential'],
      title: 'Indus Houses — domestic architecture',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD)',
      body: [
        '<strong>Standard plan:</strong> a courtyard surrounded by 4–8 rooms. Entry from a side lane (never the main street), through a small entry vestibule that prevents direct sight-line into the house — the same "purdah-protective" planning principle still used in traditional South Asian housing.',
        '<strong>Typical features (Mackay):</strong>',
        '• Central courtyard, usually paved with brick',
        '• Private bathing platform, drained to street',
        '• Small private toilet',
        '• Brick-lined private well in larger houses',
        '• Staircase to upper storey or roof',
        '• Storage room with large jars set into the floor',
        '<strong>Two storeys:</strong> stair foundations indicate most Mohenjo-daro houses had upper floors, though the upper levels are rarely preserved. The total floor area was therefore double what is visible today.',
        '<strong>Roofs:</strong> flat, made of wooden beams and reed matting overlaid with packed clay — the same construction still used in rural Sindh today.',
        '<strong>Size variation:</strong> from small two-room houses to large complexes of 20+ rooms. There is variation in wealth, but no extreme palaces — no single residence dwarfs the others as in contemporary Mesopotamia or Egypt.'
      ]
    },

    /* ── pottery typology ───────────────── */
    {
      keys: ['pottery','indus pottery','harappan pottery','red ware','black-on-red','painted pottery','indus jar','storage jar'],
      title: 'Indus Pottery — types and decoration',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD) · Vats 1940 (PD)',
      body: [
        '<strong>Mature Harappan pottery</strong> is overwhelmingly <em>wheel-thrown red ware</em>, well-fired, with a thin red slip and painted decoration in <em>black</em>. This consistency across the entire civilization area is one of its diagnostic features.',
        '<strong>Common decorative motifs:</strong>',
        '• <em>Pipal</em> (Ficus religiosa) leaves — single or row',
        '• Intersecting circles — the famous Harappan motif',
        '• Fish-scale patterns',
        '• Horizontal bands and chevrons',
        '• Stylised peacocks and ibexes (less common)',
        '<strong>Vessel types:</strong>',
        '• Large storage jars set into floors',
        '• Cooking pots, often with carbon residue',
        '• Dish-on-stand (offering stands)',
        '• Perforated vessels (strainers)',
        '• Goblet with pointed base — a diagnostic Mature-Harappan form',
        '<strong>Late Harappan transition:</strong> Cemetery H pottery (c. 1900–1700 BCE) introduces new motifs — peacocks carrying small figures, stylised tree-and-bird scenes — interpreted by some as proto-eschatological imagery.',
        'Pottery is the single most abundant find at every Indus site. Standard sherd typologies established by Marshall and Mackay are still the basis for dating Indus deposits today.'
      ]
    },

    /* ── stratigraphy & dating ──────────── */
    {
      keys: ['stratigraphy','mohenjo-daro phases','indus phases','dating','chronology','radiocarbon','c14','indus levels'],
      title: 'Stratigraphy and Phasing — how Indus chronology was built',
      sources: 'Marshall 1931 (PD) · Wheeler 1947 (PD) · Possehl 2002',
      body: [
        '<strong>Three-phase chronology</strong> (now standard, refined many times):',
        '• <em>Early Harappan</em> (c. 3300–2600 BCE) — Ravi, Hakra, Sothi-Siswal, Kot Diji phases. Proto-urban, regional cultures.',
        '• <em>Mature Harappan</em> (c. 2600–1900 BCE) — fully urban, integrated, with seals, script, weights.',
        '• <em>Late Harappan</em> (c. 1900–1300 BCE) — de-urbanisation, regional fragmentation (Cemetery H, Jhukar, Rangpur cultures).',
        '<strong>How it was built:</strong>',
        '• <em>Marshall (1931):</strong> recognised stratified cultural deposits at Mohenjo-daro but had no absolute dates.',
        '• <em>Wheeler (1947):</strong> introduced systematic stratigraphic excavation (REM-style sondages) at Harappa.',
        '• <em>Radiocarbon revolution (1950s onward):</em> direct dating of charcoal pushed the civilization\'s start-date earlier than initially thought.',
        '• <em>Calibration (1980s onward):</em> dendrochronological calibration of radiocarbon further refined dates.',
        '<strong>Mohenjo-daro stratigraphy:</strong> 7 stratigraphic levels were recognised by Marshall, with the upper levels representing only the final 200 years of occupation. Most of the city\'s 700-year life is buried below the modern water table — physically inaccessible for further excavation.'
      ]
    },

    /* ── horse bone debate ─────────────── */
    {
      keys: ['horse','horse bone','horse bones','equus','equus caballus','horse mature harappan','no horse','indus horse','aryan horse'],
      title: 'The Horse-Bone Question',
      sources: 'Marshall 1931 (PD) · ASI (PD) · Meadow & Patel scholarly review',
      body: [
        'The presence or absence of the <strong>true domestic horse</strong> (<em>Equus caballus</em>) in the Mature Harappan layers is one of the most politically charged questions in Indus archaeology — because it bears on the Aryan-migration debate.',
        '<strong>The scholarly consensus (Meadow, Patel, et al.):</strong>',
        '• True domestic horse bones are <em>extremely rare or absent</em> in stratified Mature Harappan contexts.',
        '• Bones identified as "horse" by some excavators have been re-examined — most are <em>donkey, hemione (onager), or wild ass</em>, not <em>Equus caballus</em>.',
        '• The horse appears reliably in South Asia only in <em>Late Harappan and post-Harappan</em> contexts (c. 1900 BCE onward), consistent with introduction from Central Asia.',
        '<strong>The few contested finds:</strong>',
        '• Surkotada (Bisht): some bones identified as horse — re-examination ambiguous.',
        '• Lothal, Kalibangan: similar contested identifications.',
        '<strong>Why it matters:</strong> the horse is closely associated with Indo-Aryan-speaking pastoralists. A Mature Harappan with no horse is consistent with — but does not prove — a non-Indo-Aryan-speaking population. The 2019 Rakhigarhi aDNA study independently supported this picture by finding no Steppe ancestry in Mature Harappan individuals.',
        'The honest scholarly position is that Mature Harappans almost certainly did not have the domestic horse as a routine animal — and that this is one piece (among many) of a complex picture.'
      ]
    },

    /* ── women in indus society ─────────── */
    {
      keys: ['women','female','woman','indus women','harappan women','female figurine','goddess','mother goddess','gender'],
      title: 'Women in Indus Society',
      sources: 'Marshall 1931 (PD) · Mackay 1937–38 (PD) · Wright 2010 scholarly synthesis',
      body: [
        '<strong>Direct evidence is limited</strong> — the script is undeciphered, no royal inscriptions identify rulers by gender, and burial practices show only modest gender differentiation in grave goods. But several lines of evidence speak.',
        '<strong>Female terracotta figurines (thousands found):</strong>',
        '• Wide-hipped, ornament-laden, often with elaborate fan-shaped headdresses',
        '• Pinched faces, applied jewellery — almost mass-produced',
        '• Marshall called them "mother goddess" figures; modern scholars are more cautious — they may have been <em>household charms, votive offerings, or fertility tokens</em> without implying a single deity.',
        '<strong>The "Dancing Girl" (DK 5880):</strong>',
        '• 10.5 cm bronze, lost-wax casting',
        '• Standing, hand on hip, bangles up one arm',
        '• Confident, individual posture — interpreted by Marshall as a "dancer"; her actual identity unknown',
        '<strong>Burial goods:</strong> bangles, beaded ornaments, copper mirrors are found with female burials — suggesting personal adornment was important and accessible across social levels.',
        '<strong>Workforce:</strong> bead-making, pottery decoration, and textile production are likely to have been gendered occupations, as in most pre-modern societies — but direct evidence is thin.',
        'The honest summary: women appear visible, ornamented, and economically active — without the extreme gender stratification visible in contemporary Mesopotamian or Egyptian elite contexts. But absence of evidence is not evidence of absence.'
      ]
    },

    /* ── kalibangan ─────────────────────── */
    {
      keys: ['kalibangan','kalibangan ploughed field','kalibangan fire altars','rajasthan harappan','kalibangan citadel','b.b. lal','b b lal'],
      title: 'Kalibangan — the ploughed field and fire altars',
      sources: 'B.B. Lal ASI Reports (PD) · Possehl 2002',
      body: [
        '<strong>Kalibangan</strong> (Hanumangarh district, Rajasthan) is unique among major Harappan cities for two extraordinary finds.',
        '<strong>1. The world\'s earliest ploughed field (c. 2800 BCE):</strong>',
        '• Found below the Early Harappan settlement layer',
        '• Two intersecting sets of furrows — a <em>cross-ploughing pattern</em> still used in north-west India',
        '• Wider furrows for tall crops (mustard), narrower furrows for short crops (chickpea) — consistent with mixed agriculture',
        '• This is the <strong>oldest ploughed field ever found anywhere in the world</strong>',
        '<strong>2. The "fire altars":</strong>',
        '• Row of 7 brick-lined pits on the citadel mound',
        '• Each contained ash, charcoal, and a central upright stone (the "yupa"?)',
        '• Terracotta cakes (a uniquely Harappan artefact) found nearby',
        '• B.B. Lal interpreted them as <em>ritual fire-altars</em>, drawing parallels to later Vedic <em>agnihotra</em> practice',
        '<strong>The interpretation is contested.</strong> The structures might be ovens, kilns, or domestic hearths. But their non-domestic location, regular spacing, and association with terracotta cakes make a ritual function plausible.',
        'Kalibangan also shows seismic damage in its uppermost Mature Harappan layers — suggesting an earthquake may have contributed to its abandonment.'
      ]
    },

    /* ── lothal port detail ─────────────── */
    {
      keys: ['lothal port','lothal dockyard','dockyard','tidal dock','indus port','rao lothal','s.r. rao','sr rao'],
      title: 'Lothal — the Dockyard Debate',
      sources: 'S.R. Rao ASI Reports (PD)',
      body: [
        '<strong>Lothal</strong> (Saragwala, Gujarat) was excavated by <strong>S.R. Rao</strong> for the ASI between 1955 and 1962. His main interpretation — that Lothal possessed the world\'s earliest known artificial dockyard — remains debated.',
        '<strong>The structure:</strong>',
        '• Massive rectangular brick-lined basin, 215 × 36 m, 4.5 m deep',
        '• On the eastern edge of the settlement, connected to the Sabarmati estuary by an inlet channel',
        '• A spillway at the southern end (interpreted by Rao as a tidal-flow regulator)',
        '<strong>Rao\'s case for a dockyard:</strong>',
        '• Position adjacent to the warehouse area',
        '• Marine-shell finds in the adjacent street',
        '• Stone anchors found in the basin (since contested)',
        '• Direct link to the estuary',
        '<strong>The alternative interpretation:</strong>',
        '• Some scholars (Leshnik, Pramanik) argue the basin is too small and too far inland to have been a working tidal dock for sea-going vessels',
        '• They suggest it was instead a <em>large irrigation tank or freshwater reservoir</em>',
        '<strong>Verdict:</strong> the structure is real, monumental, water-related, and was used by the Mature Harappans. Whether it was a true dockyard or a reservoir cannot be definitively resolved without further evidence. Lothal\'s role as a coastal trade hub — confirmed by abundant carnelian, shell, and seal-impressions of foreign type — is not in doubt.'
      ]
    },

    /* ── mehrgarh ───────────────────────── */
    {
      keys: ['mehrgarh','jarrige','baluchistan neolithic','indus origins','pre harappan','pre-harappan','jarriges'],
      title: 'Mehrgarh — the deep roots of Indus civilization',
      sources: 'Jarrige ASI/MAFB Reports (PD-equivalent)',
      body: [
        '<strong>Mehrgarh</strong> (Bolan Pass, Balochistan) was excavated by the French Archaeological Mission under <strong>Jean-François Jarrige</strong> from 1974. It contains the deepest pre-Harappan stratigraphy yet known in South Asia — <em>c. 7000–2500 BCE</em>.',
        '<strong>Phase I (c. 7000–5500 BCE):</strong>',
        '• Aceramic Neolithic — no pottery, mud-brick rectangular houses',
        '• Earliest evidence of <em>wheat, barley, dates, cotton, sheep, goats, cattle</em> in South Asia',
        '• Earliest known dental drilling in the world (~9,000 years ago) — using bow-driven flint drills on living human teeth',
        '<strong>Phase II–III (c. 5500–4000 BCE):</strong>',
        '• Pottery appears',
        '• Trade in lapis lazuli, turquoise, marine shell — first long-distance exchange networks',
        '• Cemetery burials with grave goods',
        '<strong>Phase IV–VII (c. 4000–2500 BCE):</strong>',
        '• Increasing settlement size, craft specialisation',
        '• Direct continuity into Early Harappan and then Mature Harappan culture',
        '<strong>Why it matters:</strong> Mehrgarh shows that the Indus Civilization did not appear suddenly — it grew from a 4,500-year-long indigenous Neolithic base. The wheat-barley-cattle-cotton agricultural package, the technological tradition, and the proto-urban impulse all emerged in situ in the western highlands and then expanded into the Indus plain.'
      ]
    },

    /* ── frequency analysis ─────────────── */
    {
      keys: ['frequency analysis','sign frequency','most frequent sign','sign count','most common sign','jar sign','m-99','jar suffix','frequent indus signs'],
      title: 'Frequency Analysis — which signs occur most?',
      sources: 'Mahadevan 1977 (PD ASI) · Parpola 1994',
      body: [
        '<strong>Frequency analysis</strong> is the most basic — and most informative — computational analysis of the Indus script. It asks: how often does each sign occur?',
        '<strong>The top 3 signs:</strong>',
        '• <em>M-99 "JAR"</em> — ~1,395 occurrences (10.5% of all sign-tokens). The famous "jar suffix" — almost always at the end of inscriptions.',
        '• <em>M-342 "DOUBLE STROKE"</em> — ~1,216 occurrences. A ligature, very common in compound formations.',
        '• <em>M-1 "STROKE"</em> — ~1,124 occurrences. A single vertical stroke, likely a numeric or grammatical suffix.',
        'Out of ~417 distinct signs, the top 20 account for over 60% of all sign-tokens. This is consistent with Zipf\'s law and is exactly what a real language looks like — heraldic or random sign systems would show much flatter distributions.',
        '<strong>What this tells us:</strong> the steep frequency curve is one of the strongest pieces of evidence that the Indus script encodes a real linguistic system rather than random imagery or pure heraldry.'
      ]
    },

    /* ── positional analysis ────────────── */
    {
      keys: ['positional analysis','sign position','initial sign','final sign','medial sign','position preference','where signs appear','jar at end','fish in middle'],
      title: 'Positional Analysis — where signs prefer to sit',
      sources: 'Mahadevan 1977 (PD ASI) · Parpola 1994',
      body: [
        '<strong>Positional analysis</strong> measures whether each sign prefers the <em>initial, medial, or final</em> position in inscriptions. The Mature Harappan corpus shows extraordinarily strong positional preferences.',
        '<strong>Strong terminal (final) signs:</strong>',
        '• <em>M-99 "JAR"</em> — appears at the END of 84% of its occurrences. The strongest grammatical-marker signal in the entire corpus.',
        '• <em>M-211 "U"</em> — 73% terminal',
        '• <em>M-1 "STROKE"</em> — 67% terminal',
        '<strong>Strong initial signs:</strong>',
        '• <em>M-67 "FORK"</em> — 71% initial. Likely a determinative or proper-noun marker.',
        '• <em>M-176 "MAN"</em> — 64% initial',
        '<strong>Strong medial signs:</strong>',
        '• <em>M-86 "FISH"</em> — 78% medial. Almost never initial or final. Carries lexical content.',
        '• <em>M-89 "ROOFED FISH"</em> — 71% medial',
        '<strong>Why this matters:</strong> in a real language, words have prefixes, roots, and suffixes — and these obey positional rules. The Indus script\'s sign-position preferences are statistically indistinguishable from those of known agglutinative languages (e.g. Tamil, Sumerian, Akkadian).'
      ]
    },

    /* ── bigram analysis ────────────────── */
    {
      keys: ['bigram','bigram analysis','sign pair','sign sequence','two sign sequence','transitional probability','fish jar','sign combinations'],
      title: 'Bigram Analysis — sign pairs',
      sources: 'Mahadevan 1977 (PD ASI) · Yadav et al. 2010',
      body: [
        '<strong>Bigram analysis</strong> measures the probability that one sign immediately follows another. It is the simplest form of sequential analysis and reveals "syntactic" rules of sign combination.',
        '<strong>The single most frequent bigram:</strong> <em>M-86 (FISH) → M-99 (JAR)</em> — occurs 412 times. This is far above what would be predicted from independent sign frequencies.',
        '<strong>Other top bigrams:</strong>',
        '• FORK → FISH (287×)',
        '• MAN → U (234×)',
        '• ROOFED-FISH → JAR (218×)',
        '• CROWN → FISH (196×)',
        '• DOUBLE → JAR (187×)',
        '<strong>The statistical significance:</strong> if signs combined randomly, the top bigram would occur ~50× by chance. Observed 412 — a ratio of 8:1. This rules out random combination.',
        'Yadav, Vahia, Mahadevan, and Joglekar (2010) ran exhaustive n-gram analysis and found the Indus script\'s combinatorial entropy matches that of real languages like Sumerian and Tamil — and is unlike DNA, computer programs, or random sign systems.'
      ]
    },

    /* ── statistical significance ───────── */
    {
      keys: ['z score','z-score','statistical significance','statistical test','script grammar evidence','language evidence','farmer claim','indus language'],
      title: 'Statistical Significance — is it really a language?',
      sources: 'Rao et al. 2009 Science · Yadav et al. 2010 PNAS',
      body: [
        'In 2004, <strong>Steve Farmer, Richard Sproat, and Michael Witzel</strong> argued the Indus script was NOT a true writing system — calling it a non-linguistic sign system (heraldic, religious, or accounting symbols).',
        '<strong>The 2009 Rao et al. response (Science):</strong> computed conditional entropy for the Indus corpus and compared it to known linguistic systems (Sumerian, Tamil, Sanskrit, English) and known non-linguistic systems (DNA, protein sequences, computer programs).',
        '<strong>Result:</strong> the Indus script\'s entropy lies <em>squarely in the linguistic range</em>, between Sumerian and Tamil. It is statistically distinct from non-linguistic systems.',
        '<strong>Z-score analysis on positional preferences:</strong>',
        '• M-99 (JAR) at final position: Z = +18.4 (extreme)',
        '• M-86 (FISH) at medial position: Z = +14.7 (extreme)',
        '• M-67 (FORK) at initial position: Z = +11.2 (extreme)',
        'A Z-score above ±3 is "highly statistically significant" in any field. The Indus script regularly produces Z-scores above ±15 — meaning the patterns are about 10^50 times more likely to be real grammar than chance.',
        '<strong>Current scholarly consensus:</strong> the script almost certainly encodes a real language. The actual phonetic readings remain unknown — but the structural evidence is overwhelming.'
      ]
    },

    /* ── political organisation / governance ──── */
    {
      keys: ['political','politics','government','governance','rulers','kings','kingship','authority','political organization','political organisation','who ruled','no kings','elite class','social organization','political system','administrative','state structure','political model'],
      title: 'How was the Indus Civilization politically organised?',
      sources: 'Possehl 1998 · Kenoyer 1998 · Wright 2010',
      body: [
        '<strong>Direct answer:</strong> Indus political organisation remains one of archaeology\'s great puzzles. Unlike Mesopotamia and Egypt, no clear evidence of kings, dynasties, or state-level militarism survives. Most scholars now describe it as a <em>"corporate" or "heterarchical"</em> polity — power distributed across guilds, councils, or city-leagues rather than concentrated in a monarch.',
        '<strong>Evidence:</strong>',
        '<ul><li>No royal tombs, palaces, or throne rooms have been excavated at any major site [Kenoyer 1998].</li><li>No royal portraiture or named-king inscriptions, in stark contrast to contemporary Mesopotamia [Possehl 1998].</li><li>Standardised weights, bricks, and seals across 1.25M km² imply <em>some</em> centralised authority — but the source is invisible [Wright 2010].</li><li>The "Priest-King" statuette (DK-1909) is a single small bust whose identity is debated — Marshall\'s name stuck but is unsupported.</li></ul>',
        '<strong>Interpretation:</strong> Possehl proposed the Indus was a "civilisation without rulers" — coordinated by religious or commercial elites without monarchic display. Kenoyer favours a council-of-merchants model. Either way, the integration was achieved without the visible apparatus of kingship.',
        '<strong>Alternative view:</strong> Some scholars argue Indus rulers DID exist but used non-monumental authority systems we no longer recognise — analogous to medieval merchant republics or temple-state coalitions.',
        '<strong>Limitation:</strong> Without a deciphered script, we cannot read any contemporary self-description. Political reconstruction is interpretive.'
      ]
    },

    /* ── why study the indus ───────────────────── */
    {
      keys: ['why study','why important','significance','contribution','what can we learn','importance','relevance','why does it matter','why does the indus matter','why is the indus important','what does the indus teach','lessons from'],
      title: 'Why study the Indus Valley Civilization?',
      sources: 'Kenoyer 1998 · Possehl 2002 · McIntosh 2008',
      body: [
        '<strong>Direct answer:</strong> The Indus Civilization matters because it represents an alternative model of urban complexity — one that achieved standardised urban planning, long-distance trade, and large-scale public works <em>without</em> kings, conquests, or recorded warfare. Studying it expands our understanding of how complex societies can organise themselves.',
        '<strong>Evidence of significance:</strong>',
        '<ul><li>The world\'s earliest planned urban grid layout, drainage system, and public bath [Marshall 1931].</li><li>The earliest evidence of dental drilling (Mehrgarh, ~7000 BCE), brick standardisation in 1:2:4 ratio across 1.25M km², and binary-decimal weight system [Kenoyer 1998].</li><li>An undeciphered script — one of the last great undeciphered writing systems of the ancient world [Mahadevan 1977].</li><li>Direct trade with Mesopotamia documented in Sumerian records (Meluhha) — proof of integrated Bronze Age world economy [Possehl 2002].</li></ul>',
        '<strong>Interpretation:</strong> The Indus offers a powerful counter-narrative to "civilization = empire + king + war". It suggests urbanism, literacy, and long-distance trade can develop along non-monarchic, non-militaristic pathways.',
        '<strong>Alternative view:</strong> Sceptics argue the apparent peaceful character may simply reflect what archaeology can recover — and that all complex societies, including the Indus, must have had hierarchies and conflict.',
        '<strong>Limitation:</strong> Most cities lie under modern settlements or below the water table. Future excavation could change the picture.'
      ]
    },

    /* ── non-militaristic urban character ──────── */
    {
      keys: ['non militaristic','non-militaristic','non militaristic','non-militaristic','peaceful','no war','no warfare','no weapons','no army','no military','no fortification','urban without war','peaceful urbanism','why peaceful','militaristic','militarism','weapons indus','war indus','fortifications absent','no chariots','no swords','arms','militia','soldiers','battle','conflict harappan'],
      title: 'Why the Indus Civilization is called "urban but non-militaristic"',
      sources: 'Marshall 1931 · Possehl 2002 · Kenoyer 1998 · Cork 2005',
      body: [
        '<strong>Direct answer:</strong> Indus Valley archaeology shows a striking absence of features that mark <em>contemporary</em> Bronze Age societies as militaristic — no royal armies, no battle reliefs, no large-scale fortifications oriented for siege defence, no specialized weapons-grade metallurgy. Scholars therefore describe it as a <em>"non-militaristic urbanism"</em>, though the term remains debated.',
        '<strong>Evidence:</strong>',
        '<ul><li>Harappan tools — copper/bronze axes, points, blades — are domestic or hunting-grade, not battle-optimised. Massed weapon deposits (as at Mesopotamian sites like Ur) are absent. [Kenoyer 1998]</li><li>City walls exist (Mohenjo-daro, Harappa, Dholavira) but their proportions, gateways, and sight-lines are consistent with flood control + customs/administration rather than active siege defence. [Possehl 2002]</li><li>No images of warfare, captives, processions of soldiers, or victorious kings on seals or pottery — in stark contrast to Mesopotamian and Egyptian iconography of the same period. [Cork 2005]</li><li>No known palaces, throne rooms, or royal tombs — and no class of grave goods marking warrior elites. Cemetery R-37 at Harappa contains no weapons. [Vats 1940; Kenoyer 1998]</li></ul>',
        '<strong>Interpretation:</strong> The pattern suggests a society where authority was administrative and religious rather than military — possibly governed by trade-house councils, priestly bodies, or guild-confederations. Public works (drainage, granaries, baths) are over-developed; martial display is under-developed.',
        '<strong>Alternative view:</strong> A minority of scholars (e.g. Cork) argue the absence of weapons may simply reflect <em>preservation bias</em> — wooden weapons, slings, and bows leave little archaeological trace — and that trade networks always require force projection. Some "non-militaristic" claims may overstate the evidence.',
        '<strong>Limitation:</strong> Absence of evidence is not evidence of absence. The Indus script is undeciphered, so we cannot read administrative or military records that may exist. The claim is a working interpretation, not a definitive proof.'
      ]
    },

    /* ── ai hub credit ─────────────────── */
    {
      keys: ['who built this','who made this','about you','about this ai','ai hub','majeed','mohammed majeed'],
      title: 'About this AI',
      sources: 'AI Hub Projects',
      body: [
        '<strong>Indus Valley AI</strong> is a domain-restricted research assistant built by <strong>AI Hub Projects</strong>.',
        'It is the work of <strong>Mohammed Majeed Khan</strong> — Computer Science student at Mahindra University (Hyderabad), Google Student Ambassador, and founder/President of AI Hub.',
        'The system is grounded in a curated corpus of academic and primary-source material: Yajnadevam\'s <em>Indus Inscriptions</em>, the <em>Authority Structure & Evolution of Early Writing Systems</em> paper, the indusscript.net dataset, the Indus Seal Dataset (4,000+ artefacts), and ASI excavation reports for Mohenjo-daro, Harappa, Dholavira, Lothal, Kalibangan, and Rakhigarhi.',
        'It is non-commercial — free for students, scholars, and the general public. Feedback welcome at <code>majeedkhan2005.cc@gmail.com</code>.'
      ]
    }
  ],

  /* — fallback when domain matches but no topic matches — */
  domainFallback: {
    title: 'Within scope — but I want to be honest',
    body: [
      'Your question is in scope, but I don\'t have a confident, sourced answer to give without speculating.',
      'Try rephrasing — or pick a more specific angle. I can speak in detail on:',
      '<ul><li>Specific cities (Mohenjo-daro, Harappa, Dholavira, Lothal, Rakhigarhi, Kalibangan, Banawali, Surkotada, Chanhudaro, Mehrgarh)</li><li>Animal motifs (unicorn, zebu, elephant, tiger, rhinoceros, water buffalo, composites)</li><li>The Pashupati / horned-figure seal</li><li>The script — sign count, structure, decipherment attempts</li><li>The Great Bath, Priest-King, Dancing Girl</li><li>Trade with Mesopotamia (Meluhha, Dilmun, Magan)</li><li>aDNA, the Aryan-migration debate, the horse-bone question</li><li>Religion, weights & measures, urban planning, agriculture, women</li><li>The decline c. 1900 BCE</li></ul>',
      'Or just ask differently — I\'ll try again.'
    ]
  },

  /* — out of domain — */
  outOfDomain: {
    title: 'Out of scope.',
    body: [
      'I\'m <strong>Indus Valley AI</strong> — a domain-restricted system. I only answer questions about the Indus / Harappan civilization (c. 3300–1300 BCE).',
      'I\'m happy to talk about: <em>seals, motifs, cities, the script, urban planning, trade, decline, religion, language theories, archaeology</em>.',
      'For anything outside that scope — please use a general-purpose AI. The constraint is the point: scoped knowledge, no drift, no invented history.'
    ]
  }
};
