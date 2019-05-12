import sys
import os
import re
import json
import fnmatch
import math
import random

index = {"POSITIVE":0,"NEGATIVE":1,"TRUTHFUL":2,"DECEPTIVE":3}
termCounter = {}
vanillaPerceptron = [{},{}]
vBias = [0]*2
averagePerceptron = [{},{}]
aBias = [0]*2
cumulativePerceptron = [{},{}]
cBias = [0]*2
docCounter = [0]*4
ignoreList = {'ve': 1, 'very': 1, 'dont': 1, 'nor': 1, "shan't": 1, 'such': 1, 'again': 1, 'here': 1, 'hasn': 1, 'his': 1, "won't": 1, "couldn't": 1, 'so': 1, 'on': 1, 'y': 1, 'during': 1, 'this': 1, 'a': 1, 'she': 1, 'into': 1, 'didn': 1, 'can': 1, 'doesnt': 1, "needn't": 1, "mustn't": 1, 'doing': 1, 'mustnt': 1, 'both': 1, "mightn't": 1, "hasn't": 1, 'couldnt': 1, 'whom': 1, 'mustn': 1, 'your': 1, 'each': 1, 'wont': 1, 'what': 1, 'down': 1, 'up': 1, 'our': 1, 'isnt': 1, 'having': 1, 'were': 1, 'just': 1, 'and': 1, 'ours': 1, 'there': 1, 'before': 1, 'above': 1, 'about': 1, 'o': 1, 'should': 1, 'other': 1, 'more': 1, "it's": 1, 'have': 1, "weren't": 1, 'himself': 1, 'to': 1, 'of': 1, "you've": 1, 'do': 1, 'are': 1, 'her': 1, 'an': 1, 't': 1, 'weren': 1, 'no': 1, "that'll": 1, 'themselves': 1, 'isn': 1, 'has': 1, 'when': 1, 'then': 1, 'than': 1, 'because': 1, 'wouldn': 1, 'neednt': 1, 'they': 1, 'me': 1, "wouldn't": 1, 'itself': 1, "didn't": 1, 'not': 1, 'arent': 1, 'between': 1, 'wouldnt': 1, 'ma': 1, 'if': 1, 'ourselves': 1, 'shouldnt': 1, 'hasnt': 1, 're': 1, "you'll": 1, 'against': 1, 'm': 1, 'mightnt': 1, 'shant': 1, 'them': 1, "you're": 1, 'wasnt': 1, "aren't": 1, 'does': 1, 'at': 1, 'until': 1, 'only': 1, 'the': 1, 'their': 1, 'you': 1, 'few': 1, 'havent': 1, 's': 1, 'shouldn': 1, 'am': 1, 'did': 1, 'too': 1, 'wasn': 1, 'won': 1, 'be': 1, 'off': 1, 'had': 1, 'but': 1, 'myself': 1, 'some': 1, 'theirs': 1, 'my': 1, 'with': 1, 'those': 1, 'these': 1, 'by': 1, "don't": 1, 'is': 1, 'over': 1, 'who': 1, 'out': 1, 'while': 1, 'hers': 1, 'will': 1, 'didnt': 1, 'being': 1, 'shan': 1, 'for': 1, 'doesn': 1, 'he': 1, 'him': 1, "you'd": 1, 'own': 1, 'below': 1, 'its': 1, 'once': 1, 'mightn': 1, "she's": 1, 'where': 1, "hadn't": 1, 'couldn': 1, 'aren': 1, 'don': 1, 'further': 1, "wasn't": 1, "doesn't": 1, 'werent': 1, 'or': 1, 'as': 1, 'why': 1, "haven't": 1, 'most': 1, 'yourself': 1, 'needn': 1, 'd': 1, 'any': 1, 'we': 1, 'herself': 1, 'yourselves': 1, "isn't": 1, 'that': 1, 'yours': 1, 'from': 1, 'was': 1, 'in': 1, 'how': 1, 'haven': 1, 'same': 1, 'hadn': 1, 'which': 1, "shouldn't": 1, 'under': 1, 'll': 1, 'all': 1, 'hadnt': 1, 'after': 1, 'it': 1, 'ain': 1, 'been': 1, "should've": 1, 'now': 1, 'through': 1, 'i': 1}
vocabulary = {}
synonyms = {}
synonymList = [('doors', 'door'), ('markets', 'market'), ('screeches', 'screech'), ('displays', 'display'), ('bowls', 'bowl'), ('conventions', 'convention'), ('spaces', 'space'), ('reviews', 'review'), ('canopies', 'canopy'), ('troubles', 'trouble'), ('lures', 'lure'), ('hammers', 'hammer'), ('glitches', 'glitch'), ('districts', 'district'), ('toiletries', 'toiletry'), ('appeals', 'appeal'), ('brands', 'brand'), ('belongings', 'belonging'), ('treats', 'treat'), ('fronts', 'front'), ('drunks', 'drunk'), ('sensitivities', 'sensitivity'), ('sheratons', 'sheraton'), ('guests', 'guest'), ('dishes', 'dish'), ('kinds', 'kind'), ('stains', 'stain'), ('pillowcases', 'pillowcase'), ('touches', 'touch'), ('folks', 'folk'), ('heads', 'head'), ('fans', 'fan'), ('points', 'point'), ('bartenders', 'bartender'), ('difficulties', 'difficulty'), ('gives', 'give'), ('sensibilities', 'sensibility'), ('machines', 'machine'), ('houses', 'house'), ('notches', 'notch'), ('ages', 'age'), ('misses', 'miss'), ('smears', 'smear'), ('superlatives', 'superlative'), ('treatments', 'treatment'), ('pajamas', 'pajama'), ('dumpsters', 'dumpster'), ('choices', 'choice'), ('islands', 'island'), ('starters', 'starter'), ('scarves', 'scarf'), ('wonders', 'wonder'), ('brochures', 'brochure'), ('meets', 'meet'), ('detectors', 'detector'), ('lakes', 'lake'), ('flags', 'flag'), ('residents', 'resident'), ('spans', 'span'), ('flowers', 'flower'), ('chefs', 'chef'), ('meetings', 'meeting'), ('attendants', 'attendant'), ('artists', 'artist'), ('taxes', 'tax'), ('embraces', 'embrace'), ('sells', 'sell'), ('properties', 'property'), ('leaves', 'leaf'), ('suburbs', 'suburb'), ('directions', 'direction'), ('patios', 'patio'), ('corners', 'corner'), ('eyes', 'eye'), ('muffins', 'muffin'), ('mornings', 'morning'), ('ps', 'p'), ('strawberries', 'strawberry'), ('pizzas', 'pizza'), ('applications', 'application'), ('distances', 'distance'), ('inns', 'inn'), ('facilities', 'facility'), ('stations', 'station'), ('catches', 'catch'), ('opinions', 'opinion'), ('weddings', 'wedding'), ('needs', 'need'), ('servers', 'server'), ('trims', 'trim'), ('centers', 'center'), ('ants', 'ant'), ('animals', 'animal'), ('vacuums', 'vacuum'), ('duties', 'duty'), ('futons', 'futon'), ('sucks', 'suck'), ('theatres', 'theatre'), ('services', 'service'), ('developments', 'development'), ('finishes', 'finish'), ('donuts', 'donut'), ('tabletops', 'tabletop'), ('sorts', 'sort'), ('hires', 'hire'), ('casts', 'cast'), ('walls', 'wall'), ('davies', 'davy'), ('las', 'la'), ('shoulders', 'shoulder'), ('ballrooms', 'ballroom'), ('speakers', 'speaker'), ('extras', 'extra'), ('peanuts', 'peanut'), ('options', 'option'), ('sinuses', 'sinus'), ('megaphones', 'megaphone'), ('cities', 'city'), ('wans', 'wan'), ('cans', 'can'), ('negatives', 'negative'), ('roses', 'rose'), ('lanes', 'lane'), ('cigarettes', 'cigarette'), ('tastes', 'taste'), ('bagels', 'bagel'), ('knows', 'know'), ('strangers', 'stranger'), ('damages', 'damage'), ('workings', 'working'), ('tones', 'tone'), ('sessions', 'session'), ('adults', 'adult'), ('bonuses', 'bonus'), ('dollars', 'dollar'), ('commitments', 'commitment'), ('delays', 'delay'), ('rocks', 'rock'), ('comments', 'comment'), ('questions', 'question'), ('swipes', 'swipe'), ('alternatives', 'alternative'), ('takes', 'take'), ('shells', 'shell'), ('settings', 'setting'), ('babies', 'baby'), ('glasses', 'glass'), ('dots', 'dot'), ('slippers', 'slipper'), ('influences', 'influence'), ('lengths', 'length'), ('languages', 'language'), ('bucks', 'buck'), ('nieces', 'niece'), ('drops', 'drop'), ('scratches', 'scratch'), ('daughters', 'daughter'), ('controls', 'control'), ('theres', 'there'), ('treasures', 'treasure'), ('apartments', 'apartment'), ('patterns', 'pattern'), ('moments', 'moment'), ('loads', 'load'), ('events', 'event'), ('reviewers', 'reviewer'), ('memories', 'memory'), ('angels', 'angel'), ('boardrooms', 'boardroom'), ('germs', 'germ'), ('surgeries', 'surgery'), ('programs', 'program'), ('washcloths', 'washcloth'), ('requests', 'request'), ('threads', 'thread'), ('honors', 'honor'), ('results', 'result'), ('maids', 'maid'), ('chances', 'chance'), ('suggestions', 'suggestion'), ('ers', 'er'), ('aesthetics', 'aesthetic'), ('concierges', 'concierge'), ('swimmers', 'swimmer'), ('waiters', 'waiter'), ('us', 'u'), ('enemies', 'enemy'), ('groupings', 'grouping'), ('profanities', 'profanity'), ('professionals', 'professional'), ('quotes', 'quote'), ('attacks', 'attack'), ('specials', 'special'), ('nightspots', 'nightspot'), ('sisters', 'sister'), ('configurations', 'configuration'), ('compares', 'compare'), ('boxes', 'box'), ('resorts', 'resort'), ('breaks', 'break'), ('bathrobes', 'bathrobe'), ('waits', 'wait'), ('reassurances', 'reassurance'), ('crisps', 'crisp'), ('upgrades', 'upgrade'), ('parts', 'part'), ('excuses', 'excuse'), ('needless', 'needle'), ('snippets', 'snippet'), ('sculptures', 'sculpture'), ('features', 'feature'), ('regards', 'regard'), ('insults', 'insult'), ('mumbles', 'mumble'), ('salads', 'salad'), ('diapers', 'diaper'), ('bathrooms', 'bathroom'), ('spots', 'spot'), ('monitors', 'monitor'), ('levies', 'levy'), ('places', 'place'), ('reservations', 'reservation'), ('essentials', 'essential'), ('delights', 'delight'), ('bulbs', 'bulb'), ('stirrers', 'stirrer'), ('decades', 'decade'), ('times', 'time'), ('conveniences', 'convenience'), ('uses', 'us'), ('offices', 'office'), ('crepes', 'crepe'), ('credits', 'credit'), ('boasts', 'boast'), ('frames', 'frame'), ('floorboards', 'floorboard'), ('pays', 'pay'), ('activities', 'activity'), ('cancellations', 'cancellation'), ('teams', 'team'), ('towels', 'towel'), ('valets', 'valet'), ('hrs', 'hr'), ('steps', 'step'), ('croissants', 'croissant'), ('grinds', 'grind'), ('marks', 'mark'), ('pluses', 'plus'), ('bills', 'bill'), ('singles', 'single'), ('taxis', 'taxi'), ('repairs', 'repair'), ('appearances', 'appearance'), ('ashtrays', 'ashtray'), ('locations', 'location'), ('serves', 'serf'), ('grays', 'gray'), ('bits', 'bit'), ('friends', 'friend'), ('californians', 'californian'), ('individuals', 'individual'), ('responses', 'response'), ('slices', 'slice'), ('drips', 'drip'), ('pipes', 'pipe'), ('intentions', 'intention'), ('charities', 'charity'), ('cords', 'cord'), ('cereals', 'cereal'), ('rugs', 'rug'), ('baths', 'bath'), ('mugs', 'mug'), ('suites', 'suite'), ('claims', 'claim'), ('aunts', 'aunt'), ('switches', 'switch'), ('les', 'le'), ('sacrifices', 'sacrifice'), ('duvets', 'duvet'), ('reads', 'read'), ('dips', 'dip'), ('wells', 'well'), ('biscuits', 'biscuit'), ('vents', 'vent'), ('headphones', 'headphone'), ('beds', 'bed'), ('regrets', 'regret'), ('indicators', 'indicator'), ('signs', 'sign'), ('roaches', 'roach'), ('families', 'family'), ('hopes', 'hope'), ('clients', 'client'), ('desserts', 'dessert'), ('venues', 'venue'), ('caps', 'cap'), ('veggies', 'veggie'), ('shuttles', 'shuttle'), ('standards', 'standard'), ('fillings', 'filling'), ('orders', 'order'), ('minds', 'mind'), ('teenagers', 'teenager'), ('sirens', 'siren'), ('advances', 'advance'), ('conversations', 'conversation'), ('creams', 'cream'), ('decks', 'deck'), ('vistas', 'vista'), ('screens', 'screen'), ('attractions', 'attraction'), ('accoutrements', 'accoutrement'), ('benefits', 'benefit'), ('boats', 'boat'), ('quilts', 'quilt'), ('hits', 'hit'), ('cards', 'card'), ('turtles', 'turtle'), ('systems', 'system'), ('closets', 'closet'), ('connections', 'connection'), ('admissions', 'admission'), ('gowns', 'gown'), ('carpets', 'carpet'), ('countertops', 'countertop'), ('wires', 'wire'), ('boards', 'board'), ('queens', 'queen'), ('husbands', 'husband'), ('mins', 'min'), ('vs', 'v'), ('contents', 'content'), ('hairballs', 'hairball'), ('sinks', 'sink'), ('runs', 'run'), ('kiosks', 'kiosk'), ('roofs', 'roof'), ('apples', 'apple'), ('girls', 'girl'), ('shambles', 'shamble'), ('dealers', 'dealer'), ('mats', 'mat'), ('seats', 'seat'), ('lobbies', 'lobby'), ('promises', 'promise'), ('ribs', 'rib'), ('periods', 'period'), ('patches', 'patch'), ('bedspreads', 'bedspread'), ('sweets', 'sweet'), ('sheets', 'sheet'), ('cleaners', 'cleaner'), ('pieces', 'piece'), ('brioches', 'brioche'), ('pads', 'pad'), ('efforts', 'effort'), ('reaches', 'reach'), ('jeans', 'jean'), ('organizations', 'organization'), ('lets', 'let'), ('complaints', 'complaint'), ('ramps', 'ramp'), ('blocks', 'block'), ('communications', 'communication'), ('ads', 'ad'), ('calories', 'calorie'), ('outlets', 'outlet'), ('likes', 'like'), ('reams', 'ream'), ('hips', 'hip'), ('matthews', 'matthew'), ('hallways', 'hallway'), ('persons', 'person'), ('discounts', 'discount'), ('answers', 'answer'), ('hotels', 'hotel'), ('faucets', 'faucet'), ('lowers', 'lower'), ('impressions', 'impression'), ('stands', 'stand'), ('splinters', 'splinter'), ('cocktails', 'cocktail'), ('flashes', 'flash'), ('omelettes', 'omelette'), ('senses', 'sens'), ('matches', 'match'), ('meals', 'meal'), ('fireplaces', 'fireplace'), ('cares', 'care'), ('grandchildren', 'grandchild'), ('presents', 'present'), ('photos', 'photo'), ('planes', 'plane'), ('fingerprints', 'fingerprint'), ('melds', 'meld'), ('attempts', 'attempt'), ('games', 'game'), ('trimmings', 'trimming'), ('docks', 'dock'), ('vacancies', 'vacancy'), ('motels', 'motel'), ('dents', 'dent'), ('drapes', 'drape'), ('earrings', 'earring'), ('olds', 'old'), ('stares', 'stare'), ('corridors', 'corridor'), ('devices', 'device'), ('weeks', 'week'), ('sparkles', 'sparkle'), ('qualities', 'quality'), ('says', 'say'), ('numbers', 'number'), ('tabs', 'tab'), ('bars', 'bar'), ('representations', 'representation'), ('comes', 'come'), ('starts', 'start'), ('odors', 'odor'), ('gimmicks', 'gimmick'), ('sills', 'sill'), ('months', 'month'), ('hands', 'hand'), ('lamps', 'lamp'), ('prices', 'price'), ('murals', 'mural'), ('flaws', 'flaw'), ('trays', 'tray'), ('shops', 'shop'), ('arms', 'arm'), ('ladies', 'lady'), ('stalls', 'stall'), ('falls', 'fall'), ('scores', 'score'), ('showplaces', 'showplace'), ('bulldozers', 'bulldozer'), ('styles', 'style'), ('feathers', 'feather'), ('headaches', 'headache'), ('projects', 'project'), ('fumes', 'fume'), ('cubes', 'cube'), ('plans', 'plan'), ('alleyways', 'alleyway'), ('helps', 'help'), ('mixes', 'mix'), ('descriptions', 'description'), ('mrs', 'mr'), ('copies', 'copy'), ('legs', 'leg'), ('cousins', 'cousin'), ('soaps', 'soap'), ('perks', 'perk'), ('scraps', 'scrap'), ('showers', 'shower'), ('associates', 'associate'), ('stickers', 'sticker'), ('pets', 'pet'), ('strollers', 'stroller'), ('procedures', 'procedure'), ('owners', 'owner'), ('guys', 'guy'), ('bikes', 'bike'), ('specifics', 'specific'), ('relatives', 'relative'), ('shelves', 'shelf'), ('des', 'de'), ('fountains', 'fountain'), ('acquaintances', 'acquaintance'), ('brownies', 'brownie'), ('breasts', 'breast'), ('cars', 'car'), ('laps', 'lap'), ('leftovers', 'leftover'), ('beaches', 'beach'), ('smokes', 'smoke'), ('borders', 'border'), ('ends', 'end'), ('salts', 'salt'), ('candles', 'candle'), ('museums', 'museum'), ('indentations', 'indentation'), ('quarters', 'quarter'), ('items', 'item'), ('necks', 'neck'), ('rooms', 'room'), ('chips', 'chip'), ('trucks', 'truck'), ('leads', 'lead'), ('hawks', 'hawk'), ('roots', 'root'), ('curtains', 'curtain'), ('shampoos', 'shampoo'), ('basics', 'basic'), ('toys', 'toy'), ('heaters', 'heater'), ('sales', 'sale'), ('bellhops', 'bellhop'), ('neighbors', 'neighbor'), ('footsteps', 'footstep'), ('doorways', 'doorway'), ('amounts', 'amount'), ('funds', 'fund'), ('buds', 'bud'), ('accommodations', 'accommodation'), ('valuables', 'valuable'), ('tunes', 'tune'), ('vacations', 'vacation'), ('adds', 'add'), ('actors', 'actor'), ('cabs', 'cab'), ('engineers', 'engineer'), ('papers', 'paper'), ('channels', 'channel'), ('showerheads', 'showerhead'), ('cloths', 'cloth'), ('burns', 'burn'), ('rolls', 'roll'), ('newspapers', 'newspaper'), ('stores', 'store'), ('loves', 'love'), ('dreams', 'dream'), ('receptionists', 'receptionist'), ('crutches', 'crutch'), ('views', 'view'), ('mirrors', 'mirror'), ('travelers', 'traveler'), ('condos', 'condo'), ('peoples', 'people'), ('maps', 'map'), ('lives', 'life'), ('condominiums', 'condominium'), ('smiles', 'smile'), ('ranks', 'rank'), ('cases', 'case'), ('passengers', 'passenger'), ('disappointments', 'disappointment'), ('valences', 'valence'), ('overlooks', 'overlook'), ('chains', 'chain'), ('accessories', 'accessory'), ('issues', 'issue'), ('travels', 'travel'), ('gentlemen', 'gentleman'), ('staffs', 'staff'), ('expectations', 'expectation'), ('parks', 'park'), ('bears', 'bear'), ('recommendations', 'recommendation'), ('thieves', 'thief'), ('rats', 'rat'), ('mimosas', 'mimosa'), ('hangers', 'hanger'), ('rewards', 'reward'), ('pedestrians', 'pedestrian'), ('preferences', 'preference'), ('names', 'name'), ('towers', 'tower'), ('tours', 'tour'), ('lists', 'list'), ('looks', 'look'), ('days', 'day'), ('aides', 'aide'), ('afternoons', 'afternoon'), ('necessities', 'necessity'), ('browns', 'brown'), ('steaks', 'steak'), ('ratings', 'rating'), ('receptions', 'reception'), ('touts', 'tout'), ('shirts', 'shirt'), ('chops', 'chop'), ('refunds', 'refund'), ('holes', 'hole'), ('terms', 'term'), ('drinks', 'drink'), ('movies', 'movie'), ('tags', 'tag'), ('shades', 'shade'), ('burritos', 'burrito'), ('twins', 'twin'), ('palms', 'palm'), ('piddles', 'piddle'), ('wits', 'wit'), ('sodas', 'soda'), ('bugs', 'bug'), ('pimps', 'pimp'), ('actions', 'action'), ('groups', 'group'), ('uniforms', 'uniform'), ('hairs', 'hair'), ('sports', 'sport'), ('means', 'mean'), ('vips', 'vip'), ('wifes', 'wife'), ('girlfriends', 'girlfriend'), ('lines', 'line'), ('sights', 'sight'), ('massages', 'massage'), ('lounges', 'lounge'), ('stairwells', 'stairwell'), ('clerks', 'clerk'), ('souvenirs', 'souvenir'), ('tears', 'tear'), ('boys', 'boy'), ('waffles', 'waffle'), ('ones', 'one'), ('flights', 'flight'), ('paintings', 'painting'), ('remarks', 'remark'), ('interests', 'interest'), ('colleges', 'college'), ('injuries', 'injury'), ('gibsons', 'gibson'), ('edges', 'edge'), ('halls', 'hall'), ('carmines', 'carmine'), ('perfumes', 'perfume'), ('messages', 'message'), ('weekdays', 'weekday'), ('scouts', 'scout'), ('fixtures', 'fixture'), ('surprises', 'surprise'), ('children', 'child'), ('sunglasses', 'sunglass'), ('employees', 'employee'), ('cents', 'cent'), ('buses', 'bus'), ('dinners', 'dinner'), ('prostitutes', 'prostitute'), ('blisters', 'blister'), ('phones', 'phone'), ('colleagues', 'colleague'), ('passes', 'pass'), ('pastries', 'pastry'), ('chaperones', 'chaperone'), ('associations', 'association'), ('establishments', 'establishment'), ('fireworks', 'firework'), ('dumbbells', 'dumbbell'), ('reasons', 'reason'), ('fathers', 'father'), ('focuses', 'focus'), ('generations', 'generation'), ('outfittings', 'outfitting'), ('steppers', 'stepper'), ('pass', 'pas'), ('lungs', 'lung'), ('projections', 'projection'), ('warrants', 'warrant'), ('laws', 'law'), ('sites', 'site'), ('sofas', 'sofa'), ('feels', 'feel'), ('pages', 'page'), ('luxuries', 'luxury'), ('canes', 'cane'), ('decorations', 'decoration'), ('snacks', 'snack'), ('tastings', 'tasting'), ('closes', 'close'), ('stops', 'stop'), ('muscles', 'muscle'), ('lovelies', 'lovely'), ('minuets', 'minuet'), ('beats', 'beat'), ('suits', 'suit'), ('samples', 'sample'), ('brides', 'bride'), ('lots', 'lot'), ('bellmen', 'bellman'), ('covers', 'cover'), ('airlines', 'airline'), ('dogs', 'dog'), ('colors', 'color'), ('interactions', 'interaction'), ('kisses', 'kiss'), ('ideas', 'idea'), ('coffees', 'coffee'), ('chocolates', 'chocolate'), ('bedrooms', 'bedroom'), ('eaters', 'eater'), ('frowns', 'frown'), ('legends', 'legend'), ('rituals', 'ritual'), ('packers', 'packer'), ('wakes', 'wake'), ('panties', 'panty'), ('handlers', 'handler'), ('pools', 'pool'), ('drivers', 'driver'), ('women', 'woman'), ('furnishings', 'furnishing'), ('res', 're'), ('attendees', 'attendee'), ('arts', 'art'), ('leaks', 'leak'), ('chemicals', 'chemical'), ('cakes', 'cake'), ('alas', 'ala'), ('offers', 'offer'), ('desks', 'desk'), ('greetings', 'greeting'), ('stays', 'stay'), ('mints', 'mint'), ('amenities', 'amenity'), ('areas', 'area'), ('weekends', 'weekend'), ('teens', 'teen'), ('furnitures', 'furniture'), ('towners', 'towner'), ('tells', 'tell'), ('heels', 'heel'), ('measures', 'measure'), ('clubs', 'club'), ('gets', 'get'), ('forks', 'fork'), ('floors', 'floor'), ('tables', 'table'), ('workers', 'worker'), ('elevators', 'elevator'), ('replacements', 'replacement'), ('footprints', 'footprint'), ('particles', 'particle'), ('kids', 'kid'), ('manners', 'manner'), ('rivers', 'river'), ('tails', 'tail'), ('instructions', 'instruction'), ('grandparents', 'grandparent'), ('lights', 'light'), ('chairs', 'chair'), ('nachos', 'nacho'), ('doormen', 'doorman'), ('entrees', 'entree'), ('posts', 'post'), ('opportunities', 'opportunity'), ('ears', 'ear'), ('gates', 'gate'), ('swims', 'swim'), ('trains', 'train'), ('blinds', 'blind'), ('benjamins', 'benjamin'), ('guarantees', 'guarantee'), ('tubs', 'tub'), ('housekeepers', 'housekeeper'), ('singers', 'singer'), ('thinks', 'think'), ('gusts', 'gust'), ('sees', 'see'), ('lows', 'low'), ('windows', 'window'), ('rows', 'row'), ('downs', 'down'), ('shows', 'show'), ('minutes', 'minute'), ('trees', 'tree'), ('snickers', 'snicker'), ('lugs', 'lug'), ('products', 'product'), ('limes', 'lime'), ('tips', 'tip'), ('allergies', 'allergy'), ('hops', 'hop'), ('levels', 'level'), ('grounds', 'ground'), ('rates', 'rate'), ('jobs', 'job'), ('keys', 'key'), ('cubs', 'cub'), ('beggars', 'beggar'), ('arrangements', 'arrangement'), ('costs', 'cost'), ('pcs', 'pc'), ('awards', 'award'), ('incidentals', 'incidental'), ('menus', 'menu'), ('works', 'work'), ('members', 'member'), ('origins', 'origin'), ('emergencies', 'emergency'), ('details', 'detail'), ('sufferers', 'sufferer'), ('neighborhoods', 'neighborhood'), ('cookies', 'cooky'), ('couches', 'couch'), ('pictures', 'picture'), ('offerings', 'offering'), ('bubbles', 'bubble'), ('swisses', 'swiss'), ('tons', 'ton'), ('layouts', 'layout'), ('whims', 'whim'), ('fires', 'fire'), ('watts', 'watt'), ('millions', 'million'), ('headboards', 'headboard'), ('schemes', 'scheme'), ('bothers', 'bother'), ('bottles', 'bottle'), ('miles', 'mile'), ('yards', 'yard'), ('finds', 'find'), ('stories', 'story'), ('beverages', 'beverage'), ('danishes', 'danish'), ('greats', 'great'), ('tries', 'try'), ('mansions', 'mansion'), ('travellers', 'traveller'), ('stars', 'star'), ('lotions', 'lotion'), ('westerns', 'western'), ('horns', 'horn'), ('hundreds', 'hundred'), ('comforts', 'comfort'), ('kits', 'kit'), ('theaters', 'theater'), ('hairdressers', 'hairdresser'), ('racks', 'rack'), ('selections', 'selection'), ('batteries', 'battery'), ('cons', 'con'), ('managers', 'manager'), ('photographs', 'photograph'), ('crowds', 'crowd'), ('downfalls', 'downfall'), ('resources', 'resource'), ('ranges', 'range'), ('mattresses', 'mattress'), ('utensils', 'utensil'), ('martinis', 'martini'), ('parents', 'parent'), ('brags', 'brag'), ('credentials', 'credential'), ('states', 'state'), ('clouds', 'cloud'), ('sets', 'set'), ('tools', 'tool'), ('wares', 'ware'), ('plays', 'play'), ('conditions', 'condition'), ('downgrades', 'downgrade'), ('functions', 'function'), ('authors', 'author'), ('remnants', 'remnant'), ('limits', 'limit'), ('wines', 'wine'), ('types', 'type'), ('victims', 'victim'), ('symptoms', 'symptom'), ('illusions', 'illusion'), ('attitudes', 'attitude'), ('computers', 'computer'), ('dates', 'date'), ('ceilings', 'ceiling'), ('performers', 'performer'), ('conventioneers', 'conventioneer'), ('blankets', 'blanket'), ('hours', 'hour'), ('arguments', 'argument'), ('drawbacks', 'drawback'), ('potatoes', 'potato'), ('stringers', 'stringer'), ('welcomes', 'welcome'), ('weeknights', 'weeknight'), ('plasmas', 'plasma'), ('treadmills', 'treadmill'), ('checks', 'check'), ('initials', 'initial'), ('taps', 'tap'), ('governors', 'governor'), ('butts', 'butt'), ('customers', 'customer'), ('concentrates', 'concentrate'), ('fries', 'fry'), ('blasts', 'blast'), ('buildings', 'building'), ('pops', 'pop'), ('ashes', 'ash'), ('renovations', 'renovation'), ('desires', 'desire'), ('gripes', 'gripe'), ('walks', 'walk'), ('talkies', 'talkie'), ('appliances', 'appliance'), ('shards', 'shard'), ('backaches', 'backache'), ('itches', 'itch'), ('blemishes', 'blemish'), ('trainers', 'trainer'), ('presidents', 'president'), ('shifts', 'shift'), ('freebies', 'freebie'), ('routes', 'route'), ('images', 'image'), ('charges', 'charge'), ('evenings', 'evening'), ('highlights', 'highlight'), ('valentines', 'valentine'), ('records', 'record'), ('tiles', 'tile'), ('boils', 'boil'), ('picks', 'pick'), ('occasions', 'occasion'), ('keeps', 'keep'), ('affects', 'affect'), ('expenses', 'expense'), ('seasons', 'season'), ('tenants', 'tenant'), ('plants', 'plant'), ('robes', 'robe'), ('apologies', 'apology'), ('positives', 'positive'), ('appetizers', 'appetizer'), ('ambulances', 'ambulance'), ('aches', 'ache'), ('cups', 'cup'), ('bicycles', 'bicycle'), ('agents', 'agent'), ('kings', 'king'), ('groceries', 'grocery'), ('pedals', 'pedal'), ('matters', 'matter'), ('goodies', 'goody'), ('vouchers', 'voucher'), ('garages', 'garage'), ('ports', 'port'), ('cupcakes', 'cupcake'), ('permits', 'permit'), ('insects', 'insect'), ('turns', 'turn'), ('lifts', 'lift'), ('grapes', 'grape'), ('shoes', 'shoe'), ('portions', 'portion'), ('dancers', 'dancer'), ('tvs', 'tv'), ('waitresses', 'waitress'), ('celebrities', 'celebrity'), ('doubles', 'double'), ('boots', 'boot'), ('tops', 'top'), ('classes', 'class'), ('sticks', 'stick'), ('strikes', 'strike'), ('words', 'word'), ('tickets', 'ticket'), ('years', 'year'), ('counters', 'counter'), ('goes', 'go'), ('materials', 'material'), ('tourists', 'tourist'), ('circumstances', 'circumstance'), ('plates', 'plate'), ('mistakes', 'mistake'), ('petals', 'petal'), ('cockroaches', 'cockroach'), ('lids', 'lid'), ('situations', 'situation'), ('gifts', 'gift'), ('hostesses', 'hostess'), ('ways', 'way'), ('vegas', 'vega'), ('couples', 'couple'), ('traits', 'trait'), ('voicemails', 'voicemail'), ('chandeliers', 'chandelier'), ('wives', 'wife'), ('things', 'thing'), ('welts', 'welt'), ('stadiums', 'stadium'), ('errors', 'error'), ('outcomes', 'outcome'), ('webcams', 'webcam'), ('doubts', 'doubt'), ('websites', 'website'), ('stairs', 'stair'), ('props', 'prop'), ('voices', 'voice'), ('smokers', 'smoker'), ('sounds', 'sound'), ('feet', 'foot'), ('foods', 'food'), ('sons', 'son'), ('tracks', 'track'), ('visitors', 'visitor'), ('calls', 'call'), ('scales', 'scale'), ('emails', 'email'), ('students', 'student'), ('visits', 'visit'), ('nightclubs', 'nightclub'), ('sidewalks', 'sidewalk'), ('detours', 'detour'), ('televisions', 'television'), ('aspects', 'aspect'), ('rockers', 'rocker'), ('critters', 'critter'), ('departments', 'department'), ('shepards', 'shepard'), ('pumps', 'pump'), ('compliments', 'compliment'), ('gadgets', 'gadget'), ('washrags', 'washrag'), ('balls', 'ball'), ('pleas', 'plea'), ('bedbugs', 'bedbug'), ('martens', 'marten'), ('burgers', 'burger'), ('pointers', 'pointer'), ('sides', 'side'), ('noises', 'noise'), ('patrons', 'patron'), ('skills', 'skill'), ('wants', 'want'), ('bites', 'bite'), ('accounts', 'account'), ('idiots', 'idiot'), ('minuses', 'minus'), ('articles', 'article'), ('lacks', 'lack'), ('deals', 'deal'), ('earplugs', 'earplug'), ('omelets', 'omelet'), ('towns', 'town'), ('granddaughters', 'granddaughter'), ('makes', 'make'), ('bets', 'bet'), ('invitations', 'invitation'), ('restaurants', 'restaurant'), ('forms', 'form'), ('monstrosities', 'monstrosity'), ('shoppers', 'shopper'), ('jackets', 'jacket'), ('inches', 'inch'), ('cracks', 'crack'), ('pits', 'pit'), ('crumbs', 'crumb'), ('musicians', 'musician'), ('shortcomings', 'shortcoming'), ('elements', 'element'), ('speeds', 'speed'), ('locals', 'local'), ('problems', 'problem'), ('yrs', 'yr'), ('posters', 'poster'), ('changes', 'change'), ('patients', 'patient'), ('squeals', 'squeal'), ('premises', 'premise'), ('frustrations', 'frustration'), ('hives', 'hive'), ('letters', 'letter'), ('plusses', 'plus'), ('fees', 'fee'), ('bags', 'bag'), ('breakfasts', 'breakfast'), ('favorites', 'favorite'), ('drawers', 'drawer'), ('degrees', 'degree'), ('wastebaskets', 'wastebasket'), ('thumbs', 'thumb'), ('destinations', 'destination'), ('screams', 'scream'), ('safes', 'safe'), ('inclusions', 'inclusion'), ('gags', 'gag'), ('airports', 'airport'), ('smudges', 'smudge'), ('neighbours', 'neighbour'), ('employers', 'employer'), ('blues', 'blue'), ('chimes', 'chime'), ('trips', 'trip'), ('bumps', 'bump'), ('recalls', 'recall'), ('discuss', 'discus'), ('parties', 'party'), ('overcoats', 'overcoat'), ('thoughts', 'thought'), ('noodles', 'noodle'), ('diamonds', 'diamond'), ('smells', 'smell'), ('linens', 'linen'), ('conferences', 'conference'), ('coupons', 'coupon'), ('streets', 'street'), ('hides', 'hide'), ('cruises', 'cruise'), ('less', 'le'), ('supplies', 'supply'), ('characters', 'character'), ('techniques', 'technique'), ('practices', 'practice'), ('occupants', 'occupant'), ('puts', 'put'), ('pillows', 'pillow'), ('seconds', 'second'), ('concerns', 'concern'), ('mouths', 'mouth'), ('boutiques', 'boutique'), ('fins', 'fin'), ('fingertips', 'fingertip'), ('nights', 'night'), ('sensors', 'sensor'), ('guts', 'gut'), ('packages', 'package'), ('businesses', 'business'), ('weights', 'weight'), ('authorizations', 'authorization'), ('notes', 'note'), ('overflows', 'overflow'), ('transformers', 'transformer'), ('guestrooms', 'guestroom'), ('comparisons', 'comparison'), ('advertisements', 'advertisement'), ('eggs', 'egg'), ('corporations', 'corporation'), ('designs', 'design'), ('experiences', 'experience'), ('pros', 'pro'), ('inconveniences', 'inconvenience')]

for x,y in synonymList:
    synonyms[x] = y
synonymList = None
docData = {}
maxIter = 50
if __name__ == '__main__':
    model_file = "vanillamodel.txt"
    avg_model_file = "averagemodel.txt"
    input_path = str(sys.argv[1])
    uniqueCounter = 0
    for path,_,fileList in os.walk(input_path):
        for file in fileList:
            if fnmatch.fnmatch(file.lower(), '*.txt'):
                if fnmatch.fnmatch(file.lower(),'readme.txt'):
                    continue
                fptr = open(''.join([path,'/',file]),'r')
                text = fptr.read()
                fptr.close()
                text = re.sub(r'[^ a-zA-Z]', r' ', text)
                text = re.sub(r'\s+', r' ', text)
                text = text.strip().split(' ')
                if path.lower().find('positive') != -1:
                    classA = 'POSITIVE'
                else:
                    classA = 'NEGATIVE'

                if path.lower().find('truthful') != -1:
                    classB = 'TRUTHFUL'
                else:
                    classB = 'DECEPTIVE'

                check_repeat = {}
                for word in text:
                    if len(word)<3:
                        continue
                    word = word.lower()
                    if word in synonyms:
                        word = synonyms[word]
                    if (word not in ignoreList):
                        vocabulary[word] = 1
                        if word in check_repeat:
                        	check_repeat[word] = check_repeat[word]+1
                        	continue
                        check_repeat[word] = 1
                        if word not in termCounter:
                            termCounter[word] = {"POSITIVE":float(0),"NEGATIVE":float(0),"TRUTHFUL":float(0),"DECEPTIVE":float(0)}
                        
                        termCounter[word][classA]+= 1
                        termCounter[word][classB]+= 1

                docCounter[index[classA]]+= 1
                docCounter[index[classB]]+= 1
                docData[uniqueCounter] = [classA,classB,check_repeat]
                uniqueCounter+= 1
    wordList1 = []
    wordList2 = []
    infoList1 = []
    infoList2 = []
    
    for word in vocabulary.keys():
    	if termCounter[word]["POSITIVE"]>0 or termCounter[word]["NEGATIVE"]>0:
    		matrix = [[2,2,0],[float(termCounter[word]["NEGATIVE"]+1),float(termCounter[word]["POSITIVE"]+1),0],[0,0,0]]
    		matrix[0][0] += -matrix[1][0]+docCounter[index["NEGATIVE"]]
    		matrix[0][1] += -matrix[1][1]+docCounter[index["POSITIVE"]]
    		#print matrix[1][1],matrix[1][0],matrix[0][1],matrix[0][0]
    		#exit()
    		matrix[0][2] = matrix[0][0] + matrix[0][1]
    		matrix[1][2] = matrix[1][0] + matrix[1][1]
    		matrix[2][0] = matrix[0][0] + matrix[1][0]
    		matrix[2][1] = matrix[0][1] + matrix[1][1]
    		matrix[2][2] = matrix[2][0] + matrix[2][1]
    		info = 0
    		for i in range(2):
    			for j in range(2):
    				info += (matrix[i][j]/matrix[2][2])*math.log((matrix[2][2]*matrix[i][j])/(matrix[i][2]*matrix[2][j]),2)
    		
    		wordList1.append(word)
    		infoList1.append(info)

    	if termCounter[word]["TRUTHFUL"]>0 or termCounter[word]["DECEPTIVE"]>0:
    		matrix = [[2,2,0],[float(termCounter[word]["DECEPTIVE"]+1),float(termCounter[word]["TRUTHFUL"]+1),0],[0,0,0]]
    		matrix[0][0] += -matrix[1][0]+docCounter[index["DECEPTIVE"]]
    		matrix[0][1] += -matrix[1][1]+docCounter[index["TRUTHFUL"]]
    		matrix[0][2] = matrix[0][0] + matrix[0][1]
    		matrix[1][2] = matrix[1][0] + matrix[1][1]
    		matrix[2][0] = matrix[0][0] + matrix[1][0]
    		matrix[2][1] = matrix[0][1] + matrix[1][1]
    		matrix[2][2] = matrix[2][0] + matrix[2][1]
    		info = 0
    		for i in range(2):
    			for j in range(2):
    				info += (matrix[i][j]/matrix[2][2])*math.log((matrix[2][2]*matrix[i][j])/(matrix[i][2]*matrix[2][j]),2)

    		wordList2.append(word)
    		infoList2.append(info)

    termCounter = docCounter = None
    infoList1, wordList1 = zip(*sorted(zip(infoList1, wordList1)))
    infoList2, wordList2 = zip(*sorted(zip(infoList2, wordList2)))
    PN_info = {}
    TD_info = {}
    for i in range(0,int((6/10.0)*len(wordList1))):
    	PN_info[wordList1[i]] = 1
    for i in range(0,int((6/10.0)*len(wordList2))):
    	TD_info[wordList2[i]] = 1
    wordList1 = infoList1 = wordList2 = infoList2 = None
    C = 1
    index = {"POSITIVE":1,"NEGATIVE":-1,"TRUTHFUL":1,"DECEPTIVE":-1}
    for word in vocabulary.keys():
    	if word in PN_info:
    		pass
    	else:
    		vanillaPerceptron[0][word] = 0
    		averagePerceptron[0][word] = 0
    		cumulativePerceptron[0][word] = 0
    	if word in TD_info:
    		pass
    	else:
    		vanillaPerceptron[1][word] = 0
    		averagePerceptron[1][word] = 0
    		cumulativePerceptron[1][word] = 0
    C = float(1)
    Convergence = False
    for i in range(0,maxIter):
    	if not Convergence:
    		Convergence = True
    	else:
    		break
    	for j in random.sample(range(uniqueCounter),uniqueCounter):
    		A = [[vBias[0],vBias[1]],[aBias[0],aBias[1]]]
    		classA,classB,wordCounter = docData[j]
    		for word,wordCount in wordCounter.items():
    			if word in PN_info:
    				pass
    			else:
    				A[0][0] = A[0][0]+wordCount*vanillaPerceptron[0][word]
    				A[1][0] = A[1][0]+wordCount*averagePerceptron[0][word]

    			if word in TD_info:
    				pass
    			else:
    				A[0][1] = A[0][1]+wordCount*vanillaPerceptron[1][word]
    				A[1][1] = A[1][1]+wordCount*averagePerceptron[1][word]

    		if A[0][0]*index[classA]>0:
    			pass
    		else:
    			vBias[0] = vBias[0]+index[classA] 
    			for word,wordCount in wordCounter.items():
    				if word in PN_info:
    					pass
    				else:
    					vanillaPerceptron[0][word] += index[classA]*wordCount
    			Convergence = False

    		if A[1][0]*index[classA]>0:
    			pass
    		else:
    			aBias[0] = aBias[0]+index[classA] 
    			cBias[0] = cBias[0]+C*index[classA] 
    			for word,wordCount in wordCounter.items():
    				if word in PN_info:
    					pass
    				else:
    					averagePerceptron[0][word] += index[classA]*wordCount
    					cumulativePerceptron[0][word] += index[classA]*C*wordCount
    			Convergence = False

    		if A[0][1]*index[classB]>0:
    			pass
    		else:
    			vBias[1] = vBias[1]+index[classB]
    			for word,wordCount in wordCounter.items():
    				if word in TD_info:
    					pass
    				else:
    					vanillaPerceptron[1][word] += index[classB]*wordCount
    			Convergence = False

    		if A[1][1]*index[classB]>0:
    			pass
    		else:
    			aBias[1] = aBias[1]+index[classB] 
    			cBias[1] = cBias[1]+C*index[classB] 
    			for word,wordCount in wordCounter.items():
    				if word in TD_info:
    					pass
    				else:
    					averagePerceptron[1][word] += index[classB]*wordCount
    					cumulativePerceptron[1][word] += index[classB]*C*wordCount
    			Convergence = False

    		C = C+1.0

    for word,weight in averagePerceptron[0].items():
    	averagePerceptron[0][word] = -(cumulativePerceptron[0][word]/C) + averagePerceptron[0][word]
    for word,weight in averagePerceptron[1].items():
    	averagePerceptron[1][word] = -(cumulativePerceptron[1][word]/C) + averagePerceptron[1][word]
    aBias[0] = (-cBias[0]/C)+aBias[0]
    aBias[1] = (-cBias[1]/C)+aBias[1]
    cumulativePerceptron = cBias = None

    fptr = open(model_file,'w')
    fptr.write(json.dumps({'Parameters':vanillaPerceptron,'Bias':vBias},indent=4))
    fptr.close()
    fptr = open(avg_model_file,'w')
    fptr.write(json.dumps({'Parameters':averagePerceptron,'Bias':aBias},indent=4))
    fptr.close()