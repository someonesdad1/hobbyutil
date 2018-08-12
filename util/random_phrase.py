'''
Generate random phrases of words; the words and their counts are:
    Noun                967
    Verb                1037
    Adjective           1856
    Adverb              329
    Preposition         89
    Pronoun             80

Note this gives large sample spaces if the words are selected randomly.
For example, suppose you chose to use three words as a passphrase.
You used the following command line invocation:

    python phrase.py -s 0 v a n

and you'd get the output
    rob billowy walk
    meddle healthy cover
    cheat brilliant treatment
    bare endearing test
    select dynamic dock
    brake jovial step
    repair engaging throat
    normalize volatile partner
    push demonic coast
    cycle brilliant swing

For this case, there are 1037*1856*967 = 1.9e9 combinations of 
such words.  While this isn't proof against a modern brute-force search, it
can result in reasonable secure pass phrases, especially if you include
puntuation marks.  An advantage is that such phrases are easier for humans
to memorize.

'''

from __future__ import division, print_function
import sys
import getopt
import random

nl = "\n"

#----------------------------------------------------------------------
# Lists of words
wordstrings = {

    "adjective" : '''
    aback abaft abandoned abashed aberrant abhorrent abiding abject
    ablaze able abnormal aboard aboriginal abortive abounding aboveboard
    abrasive abrupt absent absorbed absorbing abstracted absurd abundant
    abusive acceptable accepting accessible accidental acclaimed
    accommodating accomplished accountable accurate aces achieving acid
    acidic acoustic acrid active actual actualized actually ad hoc
    adamant adaptable addicted adept adhesive adjoining adjusted
    admirable adorable adroit advanced advantaged adventuresome
    adventurous advocative aesthetic affable affecting affectionate
    affirming affluent afraid ageless aggressive agile agonizing
    agreeable ahead ajar alacritous alcoholic alert alike alive alleged
    alluring aloof altruistic amazing ambiguous ambitious ameliorative
    amenable amiable ample amuck amused amusing ancient angelic angry
    animated annoyed annoying anxious apathetic appealing appeasing
    appetizing appreciated appreciative approachable appropriate
    approving aquatic ardent aromatic arresting arrogant articulate
    artistic ascending ashamed aspiring assertive assiduous assorted
    assured astonishing astounding astute attentive attractive atypical
    august auspicious authentic authoritative automatic autonomous
    available average awake aware awesome awful axiomatic bad balanced
    barbarous baronial bashful bawdy beautiful befitting believable
    belligerent beloved benefactor beneficent beneficial benevolent
    benign bent berserk best better bewildered big billowy bite-sized
    bitter bizarre black black-and-white blazing blessed blessing
    blissful bloody blooming blossoming blue blue-eyed blushing boiling
    boisterous bold bona bonny boorish bored boring bouncy bounding
    boundless bounteous bountiful brainy brash brave brawny breakable
    breezy brief bright brilliant broad broadminded broken brotherly
    brown bumpy buoyant burly business-like bustling busy cagey
    calculating caliber callous calm canny capable capital capricious
    captivating carefree careful careless caring casual causative
    cautious ceaseless celebrated celeritous celestial centered cerebral
    certain changeable charismatic charitable charming cheap cheerful
    chemical cherished chic chief childlike chilly chivalrous choice
    chubby chummy chunky civil civilized clairvoyant clammy classy clean
    clear clement clever climbing cloistered closed cloudy clumsy
    cluttered cogent cognizant coherent cold colorful colossal combative
    comely comfortable comforting comical commanding commendable
    commiserative committed common communicative companionable
    compassionate compatible compelling competent complete complex
    complimentary composed concerned concise conclusive condemned
    confident confused congenial congruous conquering conscientious
    conscious consensual considerable considerate consonant constructive
    contemplative contemporary content contributive convenient
    conversant convincing cooing cool cooperative coordinated cordial
    correct cosmic courageous courteous courtly cowardly cozy crabby
    craven crazy creamy creative credible creepy crooked crowded cruel
    cuddly cultured cumbersome curious curly curved curvy cut cute
    cynical daffy daily damaged damaging damp dangerous dapper daring
    dark dashing dazzling dead deadpan deafening dear debonair decent
    decisive decorous dedicated deep deeply defeated defective defiant
    definite deft delectable deliberate delicate delicious delighted
    delightful delirious demonic dependable dependent depressed deranged
    descriptive deserted deserving destined detailed determined
    developed developing devilish devoted devout dexterous didactic
    different difficult dignified diligent diplomatic direct direful
    dirty disagreeable disarming disastrous discerning disciplined
    discreet discrete discriminating disgusted disgusting disillusioned
    dispensable disporting distinct distinctive distinguished disturbed
    divergent diverse divine dizzy domineering doubtful down-to-earth
    drab draconian dramatic dreamy dreary driven drunk dry dull durable
    dusty dynamic dynamite dysfunctional eager early earnest
    earsplitting earthy ease easy easygoing eatable ebullient economic
    ecstatic educated educational effective effectual effervescent
    efficacious efficient eight elastic elated elderly electric
    electrifying elegant elfin eligible elite embarrassed emerging
    eminent empathetic empowered empty enamored enamoring enchanted
    enchanting encouraging endearing endeavoring endurable enduring
    energetic energy engaging enjoyable enjoyed enjoying enlightened
    enlightening enormous enterprising entertaining enthusiastic
    enticing entrancing entrepreneurial envious equable equal
    equanimitous equitable erect erratic erudite essential esteemed
    ethereal ethical euphoric evanescent evasive even evenhanded
    evolving exact excellent exceptional excited exciting exclusive
    executive exemplary exotic expansive expectant expeditious expensive
    experienced explorative expressive exquisite extra-large extra-small
    extraordinary exuberant exultant fabulous faded faint fair faithful
    fallacious false familial familiar famous fanatical fancy fantastic
    far far-flung farsighted fascinated fascinating fast fat faulty
    favorable favored fearful fearless feeble feigned felicitous female
    fertile fervent festive fetching few fierce fiery filthy fine
    finicky first fit fitting five fixed flagrant flaky flamboyant
    flashy flat flavorful flawless fleet flexible flimsy flippant
    flourishing flowery fluent fluffy fluttering foamy focused foolish
    forceful foregoing foresighted forgetful forgiving forthcoming
    forthright fortified fortuitous fortunate four fragile frail frank
    frantic fraternal free freethinking freezing frequent fresh fretful
    friendly frightened frightening frolicsome fruitful fulfilled
    fulfilling full fumbling fun functional funny furry furtive future
    futuristic fuzzy gabby gainful gallant gamesome gamy gaping
    garrulous gaudy gay general generous genial gentle gentlemanly
    genuine giant giddy gifted gigantic giving glad glamorous gleaming
    gleeful glib glistening glorious glossy glowing godly golden good
    good-humored good-looking good-natured goodhearted goofy gorgeous
    graced graceful gracious grand grandiose grateful gratified
    gratifying gratis gray greasy great greedy green grey grieving
    groovy grotesque grouchy grounded growing grubby gruesome grumpy
    guarded guiding guiltless gullible gusty gutsy guttural gymnastic
    habitual hale half hallowed halting handsome handsomely handy
    hanging hapless happening happy happy-go-lucky hard hard-to-find
    hard-working hardy harmless harmonious harsh hateful heady healing
    healthy heartbreaking hearty heavenly heavy hellish helpful helpless
    heralded heroic hesitant hideous high high-dbccc1 high-pitched
    high-spirited highfalutin hilarious hissing historical holistic
    hollow holy homeless homely honest honorable honored hopeful
    horrible hospitable hot huge huggable hulking humane humanitarian
    humble humdrum humorous hungry hurried hurt hushed husky hygienic
    hypnotic hysterical icky icy ideal idealistic idiotic ignorant ill
    ill-fated ill-informed illegal illuminated illuminating illustrious
    imaginary imaginative immaculate immense imminent immune impartial
    impeccable imperfect impish impolite important imported impossible
    impressive improved improving improvisational incandescent incisive
    incompetent inconclusive incredible indefatigable independent
    indestructible indispensable individualistic indomitable industrious
    inexpensive infamous influential informative informed ingenious
    innate innocent innovative inquisitive insidious insightful inspired
    inspiring inspiriting instinctive instructive instrumental
    integrated intellectual intelligent intense intent interactive
    interconnected interested interesting internal intertwined intimate
    inventive invincible inviolable inviting irate irreplaceable
    irrepressible irreproachable irresistible irritating itchy jaded
    jagged jaunty jazzy jealous jester jittery jobless jocose jocular
    joker jolly jovial joy joyful joyous jubilant judicious juicy
    jumbled jumpy just juvenile kaput keen key kind kindhearted kindly
    kissable knightly knotty knowing knowledgeable known labored
    lackadaisical lacking ladylike laid-back lame lamentable languid
    large last late laudable laughable lavish law-abiding lazy leader
    leading lean learned left legal legendary legitimate leisurely
    lenient leonine lethal level levelheaded lewd liberal liberated
    liberating light light-hearted likable like likeable limber limping
    lionhearted literate lithesome little live lively living lonely long
    long-term longing loose lopsided lordly loud loutish lovable love
    lovely loving low lowly lucid lucky ludicrous luminous lumpy
    luscious lush lustrous lusty luxuriant lying lyrical macabre macho
    maddening madly magenta magical magnanimous magnetic magnificent
    majestic major makeshift male malicious malleable mammoth managerial
    maniacal manly mannerly many marked married marvel marvelous
    masculine massagable massive masterful masterly material
    materialistic maternal matter-of-fact mature mean meaningful measly
    meaty medical meditative meek mellow melodic melodious melted
    merciful mere meritorious merry mesmerizing messy metaphysical
    meteoric methodical meticulous mettlesome mighty military milky
    mindful mindless miniature ministerial minor mint miraculous
    mirthful mischievous miscreant misty mixed moaning modern modest
    moldy momentous moneyed moral motionless motivated motivating
    mountainous moving muddled multidimensional multidisciplined
    multifaceted mundane munificent murky muscular mushy musical mute
    mysterious naive nappy narrow nasty natural naughty nauseating near
    neat nebulous necessary needed needless needy neighborly nervous new
    next nice nifty nimble nine nippy noble noiseless noisy nonchalant
    nondescript nonstop normal nostalgic nosy notable noteworthy
    nourishing noxious nubile null numberless numerous nurturing
    nutritious nutty oafish obedient obeisant obese objective obliging
    obnoxious obscene obsequious observant obsolete obtainable oceanic
    odd offbeat old old-fashioned olympian omniscient one onerous open
    open-hearted open-minded openhanded opposite optimal optimistic
    opulent orange ordinary organic organized oriented original ossified
    out-of-sight outgoing outrageous outstanding oval overconfident
    overjoyed overrated overt overwrought pacifistic painful painstaking
    pale paltry panicky panoramic parallel paramount parched parental
    parsimonious participative particular passionate past pastoral
    paternal pathetic patient peaceful penitent penultimate peppy
    perceptive perfect periodic perky permissible permissive perpetual
    persistent personable perspicacious perspicuous persuasive pert
    petite phenomenal philanthropic philosophical phobic physical
    picayune picturesque pink pioneering pious piquant placid plain
    plant plastic plausible playful pleasant pleased pleasing
    pleasurable pliable plucky poetic pointless poised polished polite
    political poor popular positive possessive possible powerful
    practical pragmatic praiseworthy prayerful precious precise
    preferred premium prepared present prestigious pretty prevalent
    previous pricey prickly prime princely principled pristine private
    privileged probable prodigious productive professional proficient
    profitable profound profuse progressive prolific prominent promising
    prompt proper prophetic propitious prosperous protective proud
    provocative prudent psychedelic psychotic public public-spirited
    puffy pulchritudinous pumped punctual puny pure purple purposeful
    purring pushy puzzled puzzling quack quaint qualified qualitative
    quality quarrelsome questionable quick quick-witted quickest quiet
    quintessential quirky quixotic quizzical rabid racial racy radiant
    ragged rainy rambunctious rampant rapid rare rascally raspy rational
    ratty ravishing razor-sharp ready real realistic realized reasonable
    rebel receptive recommendable recondite recuperative red redundant
    refined reflective refreshing regal regular rejoicing rejuvenated
    rejuvenating relaxed relaxing reliable relieved relished relishing
    remarkable reminiscent renewed renowned repulsive reputable
    resilient resolute resonant resounding resourceful respectable
    respected respectful resplendent responsible responsive restive
    restorative retentive revered reverent rewarded rewarding rhapsodic
    rhetorical rich right righteous rightful rigid ripe risible ritzy
    roasted robust rollicking romantic roomy rosy rotten rough round
    rousing royal ruddy rude rugged rural rustic ruthless sable sad safe
    sagacious saintly salty same sanguine sapient sassy satisfied
    satisfying saucy savory savvy scandalous scarce scared scary
    scattered scholarly scientific scintillating scrawny screeching
    scrumptious scrupulous seasoned second second-hand secret secretive
    secure sedate sedulous seemly selective self-accepting self-made
    self-sufficient selfish selfless sensational sensible sensitive
    sensuous sentimental separate serendipitous serene serious
    service-minded sexy shaggy shaky shallow sharp sheltering shining
    shiny shipshape shivering shocking short shrewd shrill shut shy sick
    significant silent silky silly simple simplistic sincere sisterly
    six skillful skinny sleek sleepy slim slimy slippery sloppy slow
    small smart smelly smiley smiling smoggy smooth snazzy sneaky
    snobbish snotty snugly soaring sociable social soft softhearted
    soggy solid solomon-like somber soothing sophisticated sordid sore
    soulful sound sour sparkling special spectacular spellbinding spicy
    spiffy spiky spirited spiritual spiteful splendid spontaneous spooky
    sporting spotless spotted spotty sprightly spunky spurious squalid
    square squealing squeamish stable staking stale stalwart standing
    stately statuesque steadfast steady steep stellar stereotyped
    sterling stick-to-itive sticky stiff stimulating stingy stirring
    stormy straight straightforward strange striking striped striving
    strong studious stunning stupendous stupid sturdy stylish suave
    subdued sublime subsequent substantial successful succinct sudden
    sulky sunny super superabundant superangelic superb supercivilized
    supereminent superethical superexcellent superficial supple
    supportive supreme sure sure-footed sure-handed sustaining swanky
    sweet sweltering swift sympathetic symptomatic synergistic
    synonymous taboo tacit tacky tactful talented tall tame tan tangible
    tangy tart tasteful tasteless tasty tawdry tearful tedious teeny
    teeny-tiny telling temporary ten tender tense tenuous terrible
    terrific tested testy thankful therapeutic thick thin thinkable
    third thirsty thorough thoughtful thoughtless threatening three
    thrilled thrilling thriving thundering tidy tight tightfisted tiny
    tired tireless tiresome together tolerant toothsome torpid
    totally-tubular touching tough towering trailblazing tranquil
    transcendent transcendental transnormal trashy treasured tremendous
    tricky trite triumphant troubled truculent true true-blue trusting
    trustworthy truthful two tympanic typical ubiquitous ugliest ugly
    ultra unable unaccountable unadvised unaffected unarmed unbecoming
    unbiased uncovered understanding understood undesirable unencumbered
    unequal unequaled uneven unhealthy uninterested unique unkempt
    unknown unlimited unnatural unruly unsightly unstoppable unsuitable
    untidy unused unusual unwieldy unwritten up-and-coming upbeat
    uplifting uppity upright upset upstanding uptight urbane used useful
    useless utopian utter uttermost vacuous vagabond vague valiant
    valorous valuable various vast venerable venerated vengeful venomous
    venturesome veracious verdant versatile versed vibrant victorious
    vigilant vigorous violent violet virtuous visionary vital vivacious
    vocal vogue voiceless volatile volitional voluptuous voracious
    vulgar wacky waggish waiting wakeful wandering wanted wanting
    warlike warm warmhearted wary wasteful watery weak wealthy weary
    well well-disposed well-groomed well-made well-off well-read
    well-spoken well-to-do wet whimsical whispering white whole
    wholehearted wholesale wholesome wicked wide wide-eyed wiggly wild
    willful willing windy winning winsome wiry wise wistful witty
    wizardly woebegone womanly wonderful wondrous wooden woozy workable
    worldly worried worthless worthy wrathful wretched wrong wry
    xen(o)ial yellow yielding young young-at-heart youthful yummy zany
    zealous zesty zippy zonked
''',

    "adverb" : '''
    abnormally absentmindedly accidentally acidly actually adventurously
    afterwards almost always angrily annually anxiously arrogantly
    awkwardly badly bashfully beautifully bitterly bleakly blindly
    blissfully boastfully boldly bravely briefly brightly briskly
    broadly busily calmly carefully carelessly cautiously certainly
    cheerfully clearly cleverly closely coaxingly colorfully commonly
    continually coolly correctly courageously crossly cruelly curiously
    daily daintily dearly deceivingly deeply defiantly deliberately
    delightfully diligently dimly doubtfully dreamily easily elegantly
    energetically enormously enthusiastically equally especially even
    evenly eventually exactly excitedly extremely fairly faithfully
    famously far fast fatally ferociously fervently fiercely fondly
    foolishly fortunately frankly frantically freely frenetically
    frightfully fully furiously generally generously gently gladly
    gleefully gracefully gratefully greatly greedily happily hastily
    healthily heavily helpfully helplessly highly honestly hopelessly
    hourly hungrily immediately innocently inquisitively instantly
    intensely intently interestingly inwardly irritably jaggedly
    jealously joshingly jovially joyfully joyously jubilantly
    judgementally justly keenly kiddingly kindheartedly kindly kissingly
    knavishly knottily knowingly knowledgeably kookily lazily less
    lightly likely limply lively loftily longingly loosely loudly
    lovingly loyally madly majestically meaningfully mechanically
    merrily miserably mockingly monthly more mortally mostly
    mysteriously naturally nearly neatly needily nervously never nicely
    noisily not obediently obnoxiously oddly offensively officially
    often only openly optimistically overconfidently owlishly painfully
    partially patiently perfectly physically playfully politely poorly
    positively potentially powerfully promptly properly punctually
    quaintly quarrelsomely queasily queerly questionably questioningly
    quicker quickly quietly quirkily quizzically rapidly rarely readily
    really reassuringly recklessly regularly reluctantly repeatedly
    reproachfully restfully righteously rightfully rigidly roughly
    rudely sadly safely scarcely scarily searchingly sedately seemingly
    seldom selfishly separately seriously shakily sharply sheepishly
    shrilly shyly silently sleepily slowly smoothly softly solemnly
    solidly sometimes soon speedily stealthily sternly strictly
    successfully suddenly surprisingly suspiciously sweetly swiftly
    sympathetically tenderly tensely terribly thankfully thoroughly
    thoughtfully tightly tomorrow too tremendously triumphantly truly
    truthfully ultimately unabashedly unaccountably unbearably
    unethically unexpectedly unfortunately unimpressively unnaturally
    unnecessarily upbeat upliftingly upright upside-down upward upwardly
    urgently usefully uselessly usually utterly vacantly vaguely vainly
    valiantly vastly verbally very viciously victoriously violently
    vivaciously voluntarily warmly weakly wearily well wetly wholly
    wildly willfully wisely woefully wonderfully worriedly wrongly
    yawningly yearly yearningly yesterday yieldingly youthfully
    zealously zestfully zestily
''',

    "noun" : '''
    account achiever acoustics act action activity actor addition
    adjustment advertisement advice aftermath afternoon afterthought
    agreement air airplane airport alarm alley amount amusement anger
    angle animal answer ant ants apparatus apparel apple apples
    appliance approval arch argument arithmetic arm army art attack
    attempt attention attraction aunt authority babies baby back badge
    bag bait balance ball balloon balls banana band base baseball basin
    basket basketball bat bath battle bead beam bean bear bears beast
    bed bedroom beds bee beef beetle beggar beginner behavior belief
    believe bell bells berry bike bikes bird birds birth birthday bit
    bite blade blood blow board boat boats body bomb bone book books
    boot border bottle boundary box boy boys brain brake branch brass
    bread breakfast breath brick bridge brother brothers brush bubble
    bucket building bulb bun burn burst bushes business butter button
    cabbage cable cactus cake cakes calculator calendar camera camp can
    cannon canvas cap caption car card care carpenter carriage cars cart
    cast cat cats cattle cause cave celery cellar cemetery cent chain
    chair chairs chalk chance change channel cheese cherries cherry
    chess chicken chickens children chin church circle clam class clock
    clocks cloth cloud clouds clover club coach coal coast coat cobweb
    coil collar color comb comfort committee company comparison
    competition condition connection control cook copper copy cord cork
    corn cough country cover cow cows crack cracker crate crayon cream
    creator creature credit crib crime crook crow crowd crown crush cry
    cub cup current curtain curve cushion dad daughter day death debt
    decision deer degree design desire desk destruction detail
    development digestion dime dinner dinosaurs direction dirt discovery
    discussion disease disgust distance distribution division dock
    doctor dog dogs doll dolls donkey door downtown drain drawer dress
    drink driving drop drug drum duck ducks dust ear earth earthquake
    edge education effect egg eggnog eggs elbow end engine error event
    example exchange existence expansion experience expert eye eyes face
    fact fairies fall family fan fang farm farmer father faucet fear
    feast feather feeling feet fiction field fifth fight finger fire
    fireman fish flag flame flavor flesh flight flock floor flower
    flowers fly fog fold food foot force fork form fowl frame friction
    friend friends frog frogs front fruit fuel furniture game garden
    gate geese ghost giants giraffe girl girls glass glove glue goat
    gold goldfish good-bye goose government governor grade grain
    grandfather grandmother grape grass grip ground group growth guide
    guitar gun hair haircut hall hammer hand hands harbor harmony hat
    hate head health hearing heart heat help hen hill history hobbies
    hole holiday home honey hook hope horn horse horses hose hospital
    hot hour house houses humor hydrant ice icicle idea impulse income
    increase industry ink insect instrument insurance interest invention
    iron island jail jam jar jeans jelly jellyfish jewel join joke
    journey judge juice jump kettle key kick kiss kite kitten kittens
    kitty knee knife knot knowledge laborer lace ladybug lake lamp land
    language laugh lawyer lead leaf learning leather leg legs letter
    letters lettuce level library lift light limit line linen lip liquid
    list lizards loaf lock locket look loss love low lumber lunch
    lunchroom machine magic maid mailbox man manager map marble mark
    market mask mass match meal measure meat meeting memory men metal
    mice middle milk mind mine minister mint minute mist mitten mom
    money monkey month moon morning mother motion mountain mouth move
    muscle music nail name nation neck need needle nerve nest net news
    night noise north nose note notebook number nut oatmeal observation
    ocean offer office oil operation opinion orange oranges order
    organization ornament oven owl owner page pail pain paint pan
    pancake paper parcel parent park part partner party passenger paste
    patch payment peace pear pen pencil person pest pet pets pickle
    picture pie pies pig pigs pin pipe pizzas place plane planes plant
    plantation plants plastic plate play playground pleasure plot plough
    pocket point poison police polish pollution popcorn porter position
    pot potato powder power price print prison process produce profit
    property prose protest pull pump punishment purpose push quarter
    quartz queen question quicksand quiet quill quilt quince quiver
    rabbit rabbits rail railway rain rainstorm rake range rat rate ray
    reaction reading reason receipt recess record regret relation
    religion representative request respect rest reward rhythm rice
    riddle rifle ring rings river road robin rock rod roll roof room
    root rose route rub rule run sack sail salt sand scale scarecrow
    scarf scene scent school science scissors screw sea seashore seat
    secretary seed selection self sense servant shade shake shame shape
    sheep sheet shelf ship shirt shock shoe shoes shop show side
    sidewalk sign silk silver sink sister sisters size skate skin skirt
    sky slave sleep sleet slip slope smash smell smile smoke snail
    snails snake snakes sneeze snow soap society sock soda sofa son song
    songs sort sound soup space spade spark spiders sponge spoon spot
    spring spy square squirrel stage stamp star start statement station
    steam steel stem step stew stick sticks stitch stocking stomach
    stone stop store story stove stranger straw stream street stretch
    string structure substance sugar suggestion suit summer sun support
    surprise sweater swim swing system table tail talk tank taste tax
    teaching team teeth temper tendency tent territory test texture
    theory thing things thought thread thrill throat throne thumb
    thunder ticket tiger time tin title toad toe toes tomatoes tongue
    tooth toothbrush toothpaste top touch town toy toys trade trail
    train trains tramp transport tray treatment tree trees trick trip
    trouble trousers truck trucks tub turkey turn twig twist umbrella
    uncle underwear unit use vacation value van vase vegetable veil vein
    verse vessel vest view visitor voice volcano volleyball voyage walk
    wall war wash waste watch water wave waves wax way wealth weather
    week weight wheel whip whistle wilderness wind window wine wing
    winter wire wish woman women wood wool word work worm wound wren
    wrench wrist writer writing
''',

    "preposition" : '''
    about above absent across after against along alongside amid amidst
    among anti around as at atop before behind below beneath beside
    besides between beyond but by concerning considering despite down
    during except excepting excluding following for from in in front of
    inside instead of into like mid minus near next of off on on top of
    onto opposite out out of outside over past per plus regarding round
    save since than through till times to toward towards under
    underneath unlike until up upon versus via with withaboard within
    without
''',

    "pronoun" : '''
    all another any anybody anyone anything both each each other either
    everybody everyone everything few he her hers herself him himself
    his I it its itself little many me mine more most much my myself
    neither no one nobody none nothing one one another other others our
    ours ourselves several she some somebody someone something that
    their theirs them themselves these they this those us we what
    whatever which whichever who whoever whom whomever whose you your
    yours yourself yourselves
''',

    "verb" : '''
    abide accelerate accept accomplish achieve acquire acted activate adapt
    add address administer admire admit adopt advise afford agree alert
    alight allow altered amuse analyze announce annoy answer anticipate
    apologize appear applaud applied appoint appraise appreciate approve
    arbitrate argue arise arrange arrest arrive ascertain ask assemble
    assess assist assure attach attack attain attempt attend attract
    audited avoid awake back bake balance ban bang bare bat bathe battle be
    beam bear beat become beg begin behave behold belong bend beset bet bid
    bind bite bleach bleed bless blind blink blot blow blush boast boil
    bolt bomb book bore borrow bounce bow box brake branch break breathe
    breed brief bring broadcast bruise brush bubble budget build bump burn
    burst bury bust buy buzz calculate call camp care carry carve cast
    catalog catch cause challenge change charge chart chase cheat check
    cheer chew choke choose chop claim clap clarify classify clean clear
    cling clip close clothe coach coil collect color comb come command
    communicate compare compete compile complain complete compose compute
    conceive concentrate conceptualize concern conclude conduct confess
    confront confuse connect conserve consider consist consolidate
    construct consult contain continue contract control convert coordinate
    copy correct correlate cost cough counsel count cover crack crash crawl
    create creep critique cross crush cry cure curl curve cut cycle dam
    damage dance dare deal decay deceive decide decorate define delay
    delegate delight deliver demonstrate depend describe desert deserve
    design destroy detail detect determine develop devise diagnose dig
    direct disagree disappear disapprove disarm discover dislike dispense
    display disprove dissect distribute dive divert divide do double doubt
    draft drag drain dramatize draw dream dress drink drip drive drop drown
    drum dry dust dwell earn eat edited educate eliminate embarrass employ
    empty enacted encourage end endure enforce engineer enhance enjoy
    enlist ensure enter entertain escape establish estimate evaluate
    examine exceed excite excuse execute exercise exhibit exist expand
    expect expedite experiment explain explode express extend extract face
    facilitate fade fail fancy fasten fax fear feed feel fence fetch fight
    file fill film finalize finance find fire fit fix flap flash flee fling
    float flood flow flower fly fold follow fool forbid force forecast
    forego foresee foretell forget forgive form formulate forsake frame
    freeze frighten fry gather gaze generate get give glow glue go govern
    grab graduate grate grease greet grin grind grip groan grow guarantee
    guard guess guide hammer hand handle handwrite hang happen harass harm
    hate haunt head heal heap hear heat help hide hit hold hook hop hope
    hover hug hum hunt hurry hurt hypothesize identify ignore illustrate
    imagine implement impress improve improvise include increase induce
    influence inform initiate inject injure inlay innovate input inspect
    inspire install institute instruct insure integrate intend intensify
    interest interfere interlay interpret interrupt interview introduce
    invent inventory investigate invite irritate itch jail jam jog join
    joke judge juggle jump justify keep kept kick kill kiss kneel knit
    knock knot know label land last laugh launch lay lead lean leap learn
    leave lecture led lend let level license lick lie lifted light lighten
    like list listen live load locate lock log long look lose love maintain
    make man manage manipulate manufacture map march mark market marry
    match mate matter mean measure meddle mediate meet melt melt memorize
    mend mentor milk mine mislead miss misspell mistake misunderstand mix
    moan model modify monitor moor motivate mourn move mow muddle mug
    multiply murder nail name navigate need negotiate nest nod nominate
    normalize note notice number obey object observe obtain occur offend
    offer officiate open operate order organize oriented originate overcome
    overdo overdraw overflow overhear overtake overthrow owe own pack
    paddle paint park part participate pass paste pat pause pay peck pedal
    peel peep perceive perfect perform permit persuade phone photograph
    pick pilot pinch pine pinpoint pioneer place plan plant play plead
    please plug point poke polish pop possess post pour practice praised
    pray preach precede predict prefer prepare prescribe present preserve
    preset preside press pretend prevent prick print process procure
    produce profess program progress project promise promote proofread
    propose protect prove provide publicize pull pump punch puncture punish
    purchase push put qualify question queue quit race radiate rain raise
    rank rate reach read realign realize reason receive recognize recommend
    reconcile record recruit reduce refer reflect refuse regret regulate
    rehabilitate reign reinforce reject rejoice relate relax release rely
    remain remember remind remove render reorganize repair repeat replace
    reply report represent reproduce request rescue research resolve
    respond restored restructure retire retrieve return review revise rhyme
    rid ride ring rinse rise risk rob rock roll rot rub ruin rule run rush
    sack sail satisfy save saw say scare scatter schedule scold scorch
    scrape scratch scream screw scribble scrub seal search secure see seek
    select sell send sense separate serve service set settle sew shade
    shake shape share shave shear shed shelter shine shiver shock shoe
    shoot shop show shrink shrug shut sigh sign signal simplify sin sing
    sink sip sit sketch ski skip slap slay sleep slide sling slink slip
    slit slow smash smell smile smite smoke snatch sneak sneeze sniff snore
    snow soak solve soothe soothsay sort sound sow spare spark sparkle
    speak specify speed spell spend spill spin spit split spoil spot spray
    spread spring sprout squash squeak squeal squeeze stain stamp stand
    stare start stay steal steer step stick stimulate sting stink stir
    stitch stop store strap streamline strengthen stretch stride strike
    string strip strive stroke structure study stuff sublet subtract
    succeed suck suffer suggest suit summarize supervise supply support
    suppose surprise surround suspect suspend swear sweat sweep swell swim
    swing switch symbolize synthesize systemize tabulate take talk tame tap
    target taste teach tear tease telephone tell tempt terrify test thank
    thaw think thrive throw thrust tick tickle tie time tip tire touch tour
    tow trace trade train transcribe transfer transform translate transport
    trap travel tread treat tremble trick trip trot trouble troubleshoot
    trust try tug tumble turn tutor twist type undergo understand undertake
    undress unfasten unify unite unlock unpack untidy update upgrade uphold
    upset use vanish verbalize verify vex visit wail wait wake walk wander
    want warm warn wash waste watch water wave wear weave wed weep weigh
    welcome wend wet whine whip whirl whisper whistle win wind wink wipe
    wish withdraw withhold withstand wobble wonder work worry wrap wreck
    wrestle wriggle wring write

'''
}

# Convert strings to lists
words = {}
for key in wordstrings:
    s = []
    for i in wordstrings[key].split(nl):
        s.extend(i.split())
    words[key] = s

# Translates wordtype abbreviation to dictionary key
keys = {
    "n": "noun",
    "v": "verb",
    "a": "adjective",
    "ad": "adverb",
    "p": "preposition",
    "pr": "pronoun",
}

ikeys = dict([(j, i) for i, j in keys.items()])

# Build a dictionary of abbrev:count items to calculate total number of
# combinations.
wordcounts = dict([(ikeys[i], len(words[i])) for i in words])

def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)

def Usage(d, status=1):
    name = sys.argv[0]
    nouns = len(words["noun"])
    verbs = len(words["verb"])
    adjectives = len(words["adjective"])
    adverbs = len(words["adverb"])
    prepositions = len(words["preposition"])
    pronouns = len(words["pronoun"])
    num = d["-n"]
    s = '''
Usage:  {name} [options] descr1 [descr2 ...]
  Generate random phrases of words.  descr1, etc. are (numbers are word
  counts):
    n       Noun                {nouns}
    v       Verb                {verbs}
    a       Adjective           {adjectives}
    ad      Adverb              {adverbs}
    p       Preposition         {prepositions}
    pr      Pronoun             {pronouns}

Example:        {name} -s 0 -n 3 v a n
  prints 3 lines of a verb, followed by an adjective, followed by a
  noun.  The results were:
        rob billowy walk
        meddle healthy cover
        cheat brilliant treatment
        Possible combinations = 1859363072 = 1.9e+09

Options:
    -s seed
        Seed the random number generator.  Normally, it is seeded by the
        clock and is unpredictable.
    -l
        Print out the counts of each type of word.
    -n num
        How many lines to print out (defaults to {num}).
    -p
        Print the list of words in each category given on the command line.
'''[1:-1]
    print(s.format(**locals()))
    exit(status)

def CheckWordtypes(words):
    '''words is a list of wordtype abbreviations.  See that they
    uniquely identify one of the indicated types.
    '''
    allowed = set("n v a ad p pr".split())
    for i in words:
        if i.lower() not in allowed:
            Error("'{}' is not an allowed word type abbreviation".format(i))

def PrintWordCounts():
    print("Counts of the different types of words:")
    for wordtype in words:
        count = len(words[wordtype])
        key = ikeys[wordtype]
        print("    {:15s} {:2s} {}".format(wordtype, key, count))
    exit()

def ParseCommandLine(d):
    d["-s"] = None      # If not None, its hash is the RNG seed
    d["-n"] = 20        # How many lines to print
    d["-p"] = False     # If True, print the lists of words
    if len(sys.argv) < 2:
        Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ln:ps:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-l",):
            PrintWordCounts()
        elif o in ("-n",):
            try:
                d["-n"] = int(a)
            except Exception:
                Error("'{}' is not a valid integer".format(a))
            if d["-n"] < 1:
                Error("-n option must be > 0")
        elif o in ("-p",):
            d["-p"] = not d["-p"]
        elif o in ("-s",):
            d["-s"] = a
            random.seed(a)
    if not args:
        Usage(d)
    # Check that the indicated wordtypes are valid
    CheckWordtypes(args)
    return args

def GetWord(wordtype):
    '''Given the abbreviation wordtype, return a random word from the
    associated list.
    '''
    wordlist = words[keys[wordtype]]
    return random.choice(wordlist)

def PrintExpansion(wordtypes):
    '''wordtypes is a list of desired wordtype abbreviations.  Print one
    word randomly for each type.
    '''
    s = []
    for wordtype in wordtypes:
        word = GetWord(wordtype)
        s.append(word)
    print(' '.join(s))

def PrintWords(wordtypes):
    '''Print the wordlist for each of the given types of words in
    wordtypes.
    '''
    for wordtype in wordtypes:
        print(keys[wordtype] + ":")
        s = " "*4 + wordstrings[keys[wordtype]].strip()
        print(s)
        print()

def CalculateCombinations(wordtypes):
    count = 1
    for i in wordtypes:
        count *= wordcounts[i]
    print("Possible combinations =", count, "= {:.1e}".format(count))

if __name__ == "__main__":
    d = {}      # Options dictionary
    wordtypes = ParseCommandLine(d)
    if d["-p"]:
        PrintWords(wordtypes)
    else:
        for i in range(d["-n"]):
            PrintExpansion(wordtypes)
        CalculateCombinations(wordtypes)
