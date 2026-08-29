**OLMo 3 Stage-One: Landmark–Country–Capital Compositional Queries**

All queries were answered correctly. Composition has RR ≥ 0.5; shortcut candidates have RR ≤ 0.2; values between the thresholds are ambiguous.

**Part 1: Queries and In-Context Examples**

**Compositional (370)**

- **Query 1 — Context:** British Library → London | Sultan Ahmed Mosque → Ankara | Radcliffe Camera → London | Bad Lobenstein → Berlin | Bad Kleinkirchheim → Vienna | Tokyo Disney Resort → Tokyo | Książ Castle and park complex → Warsaw | Fujian Tulou → Beijing | Bad Königshofen im Grabfeld → Berlin | Galleria Borghese → Rome || **Final:** Palace of Versailles → Paris

- **Query 8 — Context:** Big Ben → London | Scharinska villa → Stockholm | Hirschhorn → Berlin | Bad Lobenstein → Berlin | Gochang, Hwasun and Ganghwa Dolmen Sites → Seoul | War of Independence Victory Column → Tallinn | Cumalıkızık → Ankara | Hamburger Kunsthalle → Berlin | M. H. de Young Memorial Museum → Washington, D.C. | Monument Valley → Washington, D.C. || **Final:** Persepolis → Tehran

- **Query 11 — Context:** Kreuth → Berlin | Fingal&#x27;s Cave → London | National Library of Wales → London | Dallas Museum of Art → Washington, D.C. | Shrine of the Báb → Jerusalem | Bad Aussee → Vienna | Bryn Celli Ddu → London | Malente → Berlin | Bad Wörishofen → Berlin | Macau Tower → Beijing || **Final:** Tabernas Desert → Madrid

- **Query 21 — Context:** Nümbrecht → Berlin | Champaner-Pavagadh Archaeological Park → New Delhi | Nesebar → Sofia | Trinity Lavra of St. Sergius → Moscow | Grasellenbach → Berlin | Royal Palace of Milan → Rome | Bad Liebenzell → Berlin | Bad Teinach-Zavelstein → Berlin | Palazzo Barberini → Rome | Naumburg → Berlin || **Final:** Rök Runestone → Stockholm

- **Query 24 — Context:** Ta&#x27; Ħaġrat → Valletta | Ludlow Castle → London | Fifth Avenue → Washington, D.C. | Jinggang Mountains → Beijing | tomb of Tutankhamun → Cairo | Teide → Madrid | Mount Vesuvius → Rome | Bad Kissingen → Berlin | Musée Fabre → Paris | Oberstaufen → Berlin || **Final:** Solovetsky Monastery → Moscow

- **Query 35 — Context:** Petra → Amman | Wrocław Cathedral → Warsaw | Stadium MK → London | Fitzwilliam Museum → London | Madinat Al-Zahra → Madrid | Anichkov Bridge → Moscow | Poulnabrone dolmen → Dublin | Porta San Sebastiano → Rome | Mevlâna Museum → Ankara | Luxor → Cairo || **Final:** Thien Duong Cave → Hanoi

- **Query 37 — Context:** Canyon de Chelly National Monument → Washington, D.C. | Green Mosque → Kabul | National Portrait Gallery → London | Hagia Sophia → Ankara | Odesa Fine Arts Museum → Kyiv | Althorp → London | Baabe → Berlin | Rialto Bridge → Rome | Spa → City of Brussels | Osborne House → London || **Final:** Luxor → Cairo

- **Query 46 — Context:** Terracotta Army → Beijing | Rök Runestone → Stockholm | National Archaeological Museum → Rome | The Wallace Collection → London | Solovetsky Monastery → Moscow | Kronberg im Taunus → Berlin | Pennsylvania Academy of the Fine Arts → Washington, D.C. | St. Nicholas Naval Cathedral, St. Petersburg → Moscow | British Library → London | Brooklyn Bridge → Washington, D.C. || **Final:** Susa → Tehran

- **Query 55 — Context:** J. Paul Getty Museum → Washington, D.C. | Urquhart Castle → London | Borobudur → Jakarta | The Cloisters → Washington, D.C. | Château de Malmaison → Paris | Bad Friedrichshall → Berlin | The Huntington Library, Art Museum, and Botanical Gardens → Washington, D.C. | Wild Wadi Water Park → Abu Dhabi | Lake Tuz → Ankara | Hollywood Walk of Fame → Washington, D.C. || **Final:** Mausoleum of Theodoric → Rome

- **Query 56 — Context:** Ale&#x27;s Stones → Stockholm | Disneyland → Washington, D.C. | Church of All Saints → Moscow | Font-de-Gaume → Paris | Mount Wutai → Beijing | Buckingham Palace → London | Montreal Museum of Fine Arts → Ottawa | Ehlscheid → Berlin | Polanica-Zdrój → Warsaw | Korela Fortress → Moscow || **Final:** Las Médulas → Madrid

- **Query 66 — Context:** Summer Garden → Moscow | Al-Masjid Al-Haram → Riyadh | Kołobrzeg → Warsaw | Galapagos Islands → Quito | Düden Waterfalls → Ankara | Dikteon Andron → Athens | Kailasa Temple, Ellora → New Delhi | Mamayev Kurgan → Moscow | Qazan Kremlin → Moscow | Tel Aviv Museum of Art → Jerusalem || **Final:** Bad Lauterberg im Harz → Berlin

- **Query 73 — Context:** Benaki Museum → Athens | Abbadia Lariana → Rome | Brancacci Chapel → Rome | Bodrum Castle → Ankara | Kyoto Tower → Tokyo | Christ the King statue → Warsaw | Angel Falls → Caracas | Metropolitan Museum of Art → Washington, D.C. | Călimănești → Bucharest | Behistun Inscription → Tehran || **Final:** Sachsenhausen concentration camp → Berlin

- **Query 77 — Context:** Cueva de Nerja → Madrid | MACBA Barcelona Museum of Contemporary Art → Madrid | Falkirk Wheel → London | Poverty Point → Washington, D.C. | Mount Sanqing → Beijing | 30 St Mary Axe → London | Rumelihisarı → Ankara | Spodek → Warsaw | Piešťany → Bratislava | Detroit Institute of Arts → Washington, D.C. || **Final:** Bad Marienberg → Berlin

- **Query 80 — Context:** Euromast → Amsterdam | Ali Qapu → Tehran | Terracotta Army → Beijing | Triumphal Arch of Orange → Paris | Pelion → Athens | KV10 → Cairo | Fifth Avenue → Washington, D.C. | Humayun&#x27;s Tomb → New Delhi | Grossglockner High Alpine Road → Vienna | Chilean National Museum of Fine Arts → Santiago || **Final:** Bad Wünnenberg → Berlin

- **Query 96 — Context:** Gur-e Amir → Tashkent | Kobe Port Tower → Tokyo | Aljafería → Madrid | Wuyi Mountains → Beijing | Eisriesenwelt → Vienna | Ahrenshoop → Berlin | Shah Mosque → Tehran | Nieheim → Berlin | Bad Windsheim → Berlin | Ani → Ankara || **Final:** Château de Montsoreau-Museum of Contemporary Art → Paris

- **Query 98 — Context:** Moskovsky railway station → Moscow | Qiandao Lake → Beijing | Fountains Abbey → London | Tian Tan Buddha → Beijing | Downing Street → London | Museum of Bad Art → Washington, D.C. | Vindolanda → London | Metropolitan Cathedral Basilica of St. James the Apostle → Madrid | Trump Tower → Washington, D.C. | Glastonbury Tor → London || **Final:** Heringsdorf → Berlin

- **Query 101 — Context:** Bad Fallingbostel → Berlin | Bayrischzell → Berlin | National Archaeological Museum of Athens → Athens | Yuriev Monastery → Moscow | Antwerp City Hall → City of Brussels | Trinity Cathedral → Moscow | Sasbachwalden → Berlin | Colossus of Rhodes → Athens | Füssen → Berlin | Natzweiler-Struthof concentration camp → Paris || **Final:** Arlington National Cemetery → Washington, D.C.

- **Query 106 — Context:** British Museum → London | Alcazaba of Málaga → Madrid | Golden Gate Park → Washington, D.C. | Pelion → Athens | Kreuth → Berlin | Heimbach → Berlin | Buckow → Berlin | Ben Nevis → London | Peggy Guggenheim Collection → Rome | Disney&#x27;s Hollywood Studios → Washington, D.C. || **Final:** Sverd i fjell → Oslo

- **Query 107 — Context:** İstanbul Modern → Ankara | Sayyidah Zaynab Mosque → Damascus | Persepolis → Tehran | Bad Steben → Berlin | Chelyabinsk Airport → Moscow | Knowth → Dublin | Lascaux → Paris | Choragic Monument of Lysicrates → Athens | Cappadocia → Ankara | KV3 → Cairo || **Final:** Pombia Safari Park → Rome

- **Query 108 — Context:** New Athos Cave → Tbilisi | Brooklyn Bridge → Washington, D.C. | Bad Birnbach → Berlin | Euromast → Amsterdam | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Wuppertal Schwebebahn → Berlin | Murcia&#x27;s Cathedral → Madrid | Omonoia Square → Athens | Naval Cathedral in Kronstadt → Moscow | Gammelstad Church Town → Stockholm || **Final:** KV15 → Cairo

- **Query 115 — Context:** Pompey&#x27;s Pillar → Cairo | Tamme-Lauri oak → Tallinn | Wissen → Berlin | Wuyi Mountains → Beijing | Hever Castle → London | Bad Kleinkirchheim → Vienna | The Little Mermaid → Copenhagen | Tropaeum Traiani → Bucharest | Düden Waterfalls → Ankara | Bad Klosterlausnitz → Berlin || **Final:** Dervio → Rome

- **Query 116 — Context:** Majuli → New Delhi | KV57 → Cairo | Al Abbas Mosque → Baghdad | Călimănești → Bucharest | Arch of Trajan → Rome | Charminar → New Delhi | Queen&#x27;s House → London | Cathedral of the Savior in his Epiphany of Zaragoza → Madrid | The Stone of Million → Ankara | War of Independence Victory Column → Tallinn || **Final:** Bad Sassendorf → Berlin

- **Query 118 — Context:** Lugnaquilla → Dublin | Horse Cave → Washington, D.C. | Alcazaba y Murallas del Cerro de San Cristóbal → Madrid | Dobšinská Ice Cave → Bratislava | Mount Wutai → Beijing | Dubino → Rome | Tamme-Lauri oak → Tallinn | Piskaryovskoye Memorial Cemetery → Moscow | Mount Longonot → Nairobi | İstanbul Modern → Ankara || **Final:** Wittdün auf Amrum → Berlin

- **Query 122 — Context:** Treasury of Atreus → Athens | Peggy Guggenheim Collection → Rome | Centennial Hall → Warsaw | Museum of Fine Arts Ghent (MSK) → City of Brussels | Château de Montsoreau-Museum of Contemporary Art → Paris | Uffizi Gallery → Rome | Tann → Berlin | KV34 → Cairo | Bad Schwartau → Berlin | Stonehenge → London || **Final:** Lia Fáil → Dublin

- **Query 123 — Context:** Bodrum Castle → Ankara | Wissen → Berlin | Sklené Teplice → Bratislava | Tomb of Hafez → Tehran | Metropolitan Museum of Art → Washington, D.C. | Brooklyn Museum → Washington, D.C. | Galleria Nazionale d&#x27;Arte Moderna e Contemporanea di Roma → Rome | Bad Brückenau → Berlin | Isabella Stewart Gardner Museum → Washington, D.C. | St Mark&#x27;s Clocktower → Rome || **Final:** Olympia → Athens

- **Query 135 — Context:** Freud Museum London → London | Sklené Teplice → Bratislava | Raj Ghat and associated memorials → New Delhi | Wrocław Cathedral → Warsaw | Panathenaic Stadium → Athens | Shah Mosque → Tehran | Château de Montsoreau → Paris | Zhouzhuang Town → Beijing | Ferapontov Monastery → Moscow | Marine Corps War Memorial → Washington, D.C. || **Final:** Circus Maximus → Rome

- **Query 136 — Context:** KV35 → Cairo | Dulwich Picture Gallery → London | Madinat Al-Zahra → Madrid | Hohwacht → Berlin | Museo Correr → Rome | Anadoluhisarı → Ankara | Disneyland → Washington, D.C. | Old Faithful → Washington, D.C. | Feldherrnhalle → Berlin | Forchtenstein Castle → Vienna || **Final:** Petralona cave → Athens

- **Query 139 — Context:** Bad Aibling → Berlin | Dadiani Palaces Museum → Tbilisi | Baltimore Museum of Art → Washington, D.C. | Brancacci Chapel → Rome | Lugnaquilla → Dublin | Banqueting House → London | Cathedral of Valladolid → Madrid | Valle dei Templi → Rome | Alcazaba y Murallas del Cerro de San Cristóbal → Madrid | Gothenburg Museum of Art → Stockholm || **Final:** Merneptah Stele → Cairo

- **Query 143 — Context:** Althorp → London | Goa Gajah → Jakarta | Hamburger Kunsthalle → Berlin | National Gallery → London | Norton Simon Museum → Washington, D.C. | Ming Xiaoling → Beijing | Multnomah Falls → Washington, D.C. | Kneiff → Luxembourg | Höchenschwand → Berlin | Serengeti National Park → Dodoma || **Final:** KV12 → Cairo

- **Query 144 — Context:** Truskavets → Kyiv | Rosa Khutor Alpine Resort → Moscow | Wallraf–Richartz Museum → Berlin | Centennial Hall → Warsaw | Jedlina-Zdrój → Warsaw | Bad Schwalbach → Berlin | Wustrow → Berlin | Reformation Wall → Bern | Śniardwy → Warsaw | Walhalla memorial → Berlin || **Final:** Cascata delle Marmore → Rome

- **Query 147 — Context:** Coit Tower → Washington, D.C. | Meteor Crater → Washington, D.C. | Piton des Neiges → Paris | Laykyun Sekkya → Naypyidaw | Dobšinská Ice Cave → Bratislava | Niterói Contemporary Art Museum → Brasília | Osun-Osogbo Grove → Abuja | Catacombs of Kom el Shoqafa → Cairo | Hearst Castle → Washington, D.C. | Royal Academy of Arts → London || **Final:** Deidesheim → Berlin

- **Query 150 — Context:** Perledo → Rome | Burghley House → London | Edinburgh Castle → London | Thorvaldsen Museum → Copenhagen | Pickford&#x27;s House → London | Glory&#x27;s Portico → Madrid | Graceland → Washington, D.C. | Pyramid of Userkaf → Cairo | Charing Cross → London | Cueva de los Verdes → Madrid || **Final:** Dahme → Berlin

- **Query 151 — Context:** Gołdap → Warsaw | Glasgow Cathedral → London | Ninth Fort → Vilnius | Zhouzhuang Town → Beijing | Mount Tai → Beijing | Fatih Sultan Mehmet Bridge → Ankara | Detroit Institute of Arts → Washington, D.C. | Tate Modern → London | Font-de-Gaume → Paris | Dune of Pilat → Paris || **Final:** Great Pyramid of Giza → Cairo

- **Query 155 — Context:** KV19 → Cairo | Skansen → Stockholm | Aqueduct of Segovia → Madrid | Weilburg → Berlin | Museu Picasso → Madrid | Goa Gajah → Jakarta | Church of the Savior on Blood → Moscow | Indianapolis Museum of Art → Washington, D.C. | Bad Freienwalde → Berlin | M. H. de Young Memorial Museum → Washington, D.C. || **Final:** Mount Longonot → Nairobi

- **Query 157 — Context:** Spannagel Cave → Vienna | Circus Maximus → Rome | Lion Monument Lucerne → Bern | Walibi Holland → Amsterdam | iron pillar of Delhi → New Delhi | Imam Ali Mosque → Baghdad | Szczawnica → Warsaw | Korela Fortress → Moscow | Pinacoteca di Brera → Rome | Gulangyu → Beijing || **Final:** Neuharlingersiel → Berlin

- **Query 158 — Context:** Soltau → Berlin | Cathedral Basilica of the Virgin of Incarnation → Madrid | Wallraf–Richartz Museum → Berlin | Bad Lausick → Berlin | Rumelihisarı → Ankara | Windsor Castle → London | Fountains Abbey → London | Gol Gumbaz → New Delhi | Newgrounds → Washington, D.C. | Borkum → Berlin || **Final:** Bad Gastein → Vienna

- **Query 160 — Context:** Shanghai Disneyland Park → Beijing | Pombia Safari Park → Rome | KV13 → Cairo | Sandringham House → London | Fountains Abbey → London | Ladonia → Stockholm | KV14 → Cairo | Osmangazi Bridge → Ankara | Osborne House → London | Lombard Street → Washington, D.C. || **Final:** Heilbad Heiligenstadt → Berlin

- **Query 166 — Context:** Tropaeum Alpium → Paris | Alexander Nevsky Lavra → Moscow | Murtala Muhammed International Airport → Abuja | Lake Van → Ankara | Disneyland → Washington, D.C. | Thien Duong Cave → Hanoi | Bad Kleinkirchheim → Vienna | Vadstena Castle → Stockholm | St. Mary&#x27;s Basilica in Gdańsk → Warsaw | Death Valley → Washington, D.C. || **Final:** Bad Saarow → Berlin

- **Query 167 — Context:** Dahme → Berlin | Tomb of Hafez → Tehran | Museum of Fine Arts of Lyon → Paris | Bad Breisig → Berlin | Reales Alcázares → Madrid | Kresty Prison → Moscow | Fundació Joan Miró → Madrid | Wallraf–Richartz Museum → Berlin | Bursa Grand Mosque → Ankara | The Nelson-Atkins Museum of Art → Washington, D.C. || **Final:** Rijksmuseum → Amsterdam

- **Query 169 — Context:** Château de Malmaison → Paris | Hiroshima Peace Memorial → Tokyo | Shah Cheragh shrine → Tehran | Bad Lauterberg im Harz → Berlin | Choragic Monument of Lysicrates → Athens | Tierradentro → Bogotá | Imbros → Ankara | Federal Hall → Washington, D.C. | Benaki Museum → Athens | Bad Freienwalde → Berlin || **Final:** Riddarholm Church → Stockholm

- **Query 174 — Context:** Kneiff → Luxembourg | Einsiedeln Abbey → Bern | Ny Carlsberg Glyptotek → Copenhagen | Epcot → Washington, D.C. | Tomb of Hafez → Tehran | Mount Fuji → Tokyo | West Bali National Park → Jakarta | Bad Orb → Berlin | Warwick Castle → London | Gröna Lund → Stockholm || **Final:** Rembrandt House Museum → Amsterdam

- **Query 177 — Context:** Moderna Museet → Stockholm | Hiroshima Peace Memorial → Tokyo | Mycenae → Athens | KV10 → Cairo | Arch of Galerius and Rotunda → Athens | Oriental Pearl Tower → Beijing | Rialto Bridge → Rome | Reales Alcázares → Madrid | Lugo Cathedral → Madrid | Kykkos Monastery → Nicosia || **Final:** Scharbeutz → Berlin

- **Query 178 — Context:** Củ Chi tunnels → Hanoi | National Museum in Wrocław → Warsaw | Circus Maximus → Rome | Munch Museum → Oslo | Arch of the Sergii → Zagreb | Cathedral Basilica of St. Ann → Madrid | Zhouzhuang Town → Beijing | War of Independence Victory Column → Tallinn | Castello Estense → Rome | Lugnaquilla → Dublin || **Final:** Bad Schandau → Berlin

- **Query 179 — Context:** Sukiennice → Warsaw | Arch of Galerius and Rotunda → Athens | KV6 → Cairo | Monument to the Sun → Zagreb | Statue of Liberty → Washington, D.C. | Lion of Belfort → Paris | Mobility Resort Motegi → Tokyo | Fujian Tulou → Beijing | Museo di Capodimonte → Rome | Varshets → Sofia || **Final:** Ahrenshoop → Berlin

- **Query 185 — Context:** Rabka-Zdrój → Warsaw | Ninth Fort → Vilnius | Hadrian&#x27;s Villa → Rome | Blenheim Palace → London | Ortaköy → Ankara | Wat Arun → Bangkok | Zhouzhuang Town → Beijing | Grand Central Terminal → Washington, D.C. | Tomb of Askia → Bamako | Bargello National Museum → Rome || **Final:** Bad Iburg → Berlin

- **Query 186 — Context:** Chilean National Museum of Fine Arts → Santiago | Glory&#x27;s Portico → Madrid | Lincoln Castle → London | Novocherkassk Cathedral → Moscow | Wild Wadi Water Park → Abu Dhabi | KV9 → Cairo | Coves del Drach → Madrid | Walters Art Museum → Washington, D.C. | Catacombs of Kom el Shoqafa → Cairo | Catholic Church of St. Catherine → Moscow || **Final:** Todtmoos → Berlin

- **Query 190 — Context:** Ninth Fort → Vilnius | Lake Tuz → Ankara | Ladonia → Stockholm | Millau Viaduct → Paris | Grand Egyptian Museum → Cairo | Zhangjiajie Glass Bridge → Beijing | Church of the Savior on Blood → Moscow | Thracian Tomb of Sveshtari → Sofia | Shah Mosque → Tehran | Tate Britain → London || **Final:** Bad Bertrich → Berlin

- **Query 203 — Context:** Malente → Berlin | iron pillar of Delhi → New Delhi | Ramsau bei Berchtesgaden → Berlin | Lion of Belfort → Paris | Sandanski → Sofia | Niterói Contemporary Art Museum → Brasília | ArcelorMittal Orbit → London | Lugo Cathedral → Madrid | Children&#x27;s Peace Monument → Tokyo | Freiburg im Breisgau → Berlin || **Final:** Veliky Ustyug → Moscow

- **Query 205 — Context:** Moderna Museet → Stockholm | Stockholm City Hall → Stockholm | St Martin-in-the-Fields → London | Kunstkamera → Moscow | Gonbad-e Qabus → Tehran | Kalmar Castle → Stockholm | Qazan Kremlin → Moscow | Mobility Resort Motegi → Tokyo | Cueva de las Manos → Buenos Aires | Everland → Seoul || **Final:** Buckow → Berlin

- **Query 214 — Context:** Zuma Rock → Abuja | Trinity Lavra of St. Sergius → Moscow | Uraniborg → Stockholm | Mariinsky Theatre → Moscow | Niagara Falls → Ottawa | Mesha Stele → Amman | Akbar&#x27;s Tomb → New Delhi | Dolmen of Viera → Madrid | City of Space → Paris | Masuleh → Tehran || **Final:** Kellenhusen → Berlin

- **Query 216 — Context:** Museum of Cycladic Art → Athens | Woburn Abbey → London | Galapagos Islands → Quito | National Museum of Beirut → Beirut | 15 July Martyrs Bridge → Ankara | Falkirk Wheel → London | Batu Caves → Kuala Lumpur | Maes Howe → London | Whitney Museum of American Art → Washington, D.C. | Teylers Museum → Amsterdam || **Final:** Bad Grönenbach → Berlin

- **Query 217 — Context:** Umedalens Skulpturpark → Stockholm | Guggenheim Museum → Madrid | St. Mary&#x27;s Basilica in Gdańsk → Warsaw | Serengeti National Park → Dodoma | Yosemite National Park → Washington, D.C. | Swiss Alps → Bern | Palais des Papes → Paris | Choragic Monument of Lysicrates → Athens | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Wawel Cathedral → Warsaw || **Final:** Bad Sulza → Berlin

- **Query 220 — Context:** Alnwick Castle → London | Museum Ludwig → Berlin | Nizhny Novgorod Kremlin → Moscow | Stadium MK → London | Maes Howe → London | Thien Duong Cave → Hanoi | Persepolis → Tehran | Chesme Church → Moscow | Polanica-Zdrój → Warsaw | Yamunotri → New Delhi || **Final:** KV11 → Cairo

- **Query 223 — Context:** Piskaryovskoye Memorial Cemetery → Moscow | Colossi of Memnon → Cairo | Yusupov Palace on Moika → Moscow | Hypogeum of Ħal Saflieni → Valletta | Everglades National Park → Washington, D.C. | Oslo Opera House → Oslo | Jallianwala Bagh → New Delhi | Ramoji Film City → New Delhi | Imam Reza Shrine → Tehran | Miniatürk → Ankara || **Final:** Warnemünde → Berlin

- **Query 225 — Context:** Templin → Berlin | Kunsthaus Zürich → Bern | Bad Waldsee → Berlin | Świnoujście → Warsaw | Bad Fallingbostel → Berlin | Oy-Mittelberg → Berlin | İzmir Clock Tower → Ankara | Serdobsk → Moscow | Museum of Fine Arts, Houston → Washington, D.C. | National Archaeological Museum → Rome || **Final:** Kalmar Castle → Stockholm

- **Query 235 — Context:** Christ the King statue → Warsaw | Wings of Tatev → Yerevan | Derby Museum and Art Gallery → London | Disneyland Park → Paris | Batu Caves → Kuala Lumpur | Sozopol → Sofia | Amélie-les-Bains-Palalda → Paris | Hong Kong Disneyland → Beijing | Shrine of the Báb → Jerusalem | Imam Ali Mosque → Baghdad || **Final:** Zingst → Berlin

- **Query 238 — Context:** Royal Museum of Fine Arts Antwerp → City of Brussels | Field Museum of Natural History → Washington, D.C. | Luxor Museum → Cairo | Hoover Dam → Washington, D.C. | Basilica of Our Lady of the Pillar → Madrid | Czocha Castle → Warsaw | Guggenheim Museum → Madrid | Jaraba → Madrid | Putuoshan → Beijing | Ancient Theatre of Epidaurus → Athens || **Final:** Kyllburg → Berlin

- **Query 239 — Context:** Natzweiler-Struthof concentration camp → Paris | The Stone of Million → Ankara | Pamplona Cathedral → Madrid | Inveraray Castle → London | Walibi Holland → Amsterdam | Philopappos Monument → Athens | Field of Mars → Moscow | Cathedral of Valladolid → Madrid | Villa Tugendhat → Prague | Ale&#x27;s Stones → Stockholm || **Final:** Gersfeld → Berlin

- **Query 248 — Context:** Reales Alcázares → Madrid | Gemäldegalerie Alte Meister → Berlin | Hollywood Sign → Washington, D.C. | Museum of Fine Arts Boston → Washington, D.C. | Kykkos Monastery → Nicosia | Schotten → Berlin | Torre del Oro → Madrid | Columbus Monument → Madrid | KV14 → Cairo | Duszniki-Zdrój → Warsaw || **Final:** Statue of Zeus at Olympia → Athens

- **Query 249 — Context:** KV18 → Cairo | BMW Welt → Berlin | KV2 → Cairo | Ölüdeniz → Ankara | Gateway Arch → Washington, D.C. | Bad Salzdetfurth → Berlin | İzmir Clock Tower → Ankara | Balatonfüred → Budapest | Düden Waterfalls → Ankara | Leshan Giant Buddha → Beijing || **Final:** Sozopol → Sofia

- **Query 251 — Context:** Taq-i Kisra → Baghdad | Turkish and Islamic Arts Museum → Ankara | Inveraray Castle → London | Sklené Teplice → Bratislava | Statue of Liberty → Washington, D.C. | Groeningemuseum → City of Brussels | Lahnstein → Berlin | Segovia Cathedral → Madrid | Hitzacker → Berlin | Sammallahdenmäki → Helsinki || **Final:** KV10 → Cairo

- **Query 261 — Context:** Ali Qapu → Tehran | Archaeological Museum of Thessaloniki → Athens | KV5 → Cairo | Bargello National Museum → Rome | Petrie Museum of Egyptian Archaeology → London | Charing Cross → London | Harrods → London | Marble Palace → Moscow | One World Trade Center → Washington, D.C. | Pera Museum → Ankara || **Final:** Brühl&#x27;s Terrace → Berlin

- **Query 263 — Context:** Freudenstadt → Berlin | Antequera Dolmens Site → Madrid | Talyllyn Railway → London | Jaén Cathedral → Madrid | Khaju Bridge → Tehran | Alte Pinakothek → Berlin | Friedrichroda → Berlin | Pelion → Athens | Bad Sachsa → Berlin | Bad Tölz → Berlin || **Final:** Museum of Anatolian Civilizations → Ankara

- **Query 268 — Context:** Bletchley Park → London | Mausoleum of Maussollos → Ankara | Castello Estense → Rome | Mount Etna → Rome | Novocherkassk Cathedral → Moscow | Wyk auf Föhr → Berlin | Tanah Lot → Jakarta | Hitzacker → Berlin | National September 11 Memorial &amp; Museum → Washington, D.C. | Roman Baths → London || **Final:** Mount Fuji → Tokyo

- **Query 269 — Context:** Royal Palace of Milan → Rome | Ahrenshoop → Berlin | Mesha Stele → Amman | Cleveland Museum of Art → Washington, D.C. | Mount Longonot → Nairobi | Kreuth → Berlin | Bodrum Castle → Ankara | Cumalıkızık → Ankara | Ca&#x27; d&#x27;Oro → Rome | National Garden of Athens → Athens || **Final:** Batu Caves → Kuala Lumpur

- **Query 274 — Context:** Brick Lane → London | Ferapontov Monastery → Moscow | Peter and Paul Fortress → Moscow | Shah Mosque → Tehran | Ani → Ankara | KV6 → Cairo | Sümela Monastery → Ankara | Heiligendamm → Berlin | Juventus Stadium → Rome | Royal Palace of La Granja de San Ildefonso → Madrid || **Final:** Raj Ghat and associated memorials → New Delhi

- **Query 277 — Context:** Amélie-les-Bains-Palalda → Paris | Acropolis Museum → Athens | Ballabio → Rome | Gonio → Tbilisi | Bad Vöslau → Vienna | Hong Kong Museum of Art → Beijing | Bridge of Sighs → Rome | Golden Gate Bridge → Washington, D.C. | Alaçatı → Ankara | Balatonfüred → Budapest || **Final:** Tecklenburg → Berlin

- **Query 278 — Context:** Oberstdorf → Berlin | Pompey&#x27;s Pillar → Cairo | Glasgow Cathedral → London | Los Angeles County Museum of Art → Washington, D.C. | Yellowstone National Park → Washington, D.C. | Gemäldegalerie Alte Meister → Berlin | Kelvingrove Art Gallery and Museum → London | Disney Adventure World → Paris | Galleria dell&#x27;Accademia → Rome | Al Abbas Mosque → Baghdad || **Final:** Kudowa-Zdrój → Warsaw

- **Query 280 — Context:** Grasellenbach → Berlin | KV26 → Cairo | Topkapı Palace → Ankara | Ancient Agora of Athens → Athens | Kenilworth Castle → London | Centennial Hall → Warsaw | Liberty Bell → Washington, D.C. | Gaztelugatxe → Madrid | Rumelihisarı → Ankara | The Stone of Million → Ankara || **Final:** Gardaland → Rome

- **Query 282 — Context:** Novate Mezzola → Rome | Dorio → Rome | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Rundetaarn → Copenhagen | Basilica of Candelaria → Madrid | Astorga Cathedral → Madrid | Gülhane Park → Ankara | Lake Van → Ankara | Topkapı Palace → Ankara | Krynica-Zdrój → Warsaw || **Final:** Schömberg → Berlin

- **Query 284 — Context:** Caernarfon Castle → London | Baltrum → Berlin | Aulendorf → Berlin | Blue Mosque → Kabul | Russian Museum → Moscow | Banqueting House → London | Szczawnica → Warsaw | Rietveld Schröder House → Amsterdam | Kungur Ice Cave → Moscow | St. Nicholas’ Church, Hamburg → Berlin || **Final:** KV18 → Cairo

- **Query 285 — Context:** Skull Tower → Belgrade | Spannagel Cave → Vienna | Kalmar Cathedral → Stockholm | Lincoln Castle → London | Novocherkassk Cathedral → Moscow | Mausoleum of the First Qin Emperor → Beijing | Trump Tower → Washington, D.C. | Bridge of Sighs → Rome | Murtala Muhammed International Airport → Abuja | Ben Nevis → London || **Final:** Bad König → Berlin

- **Query 288 — Context:** Gur-e Amir → Tashkent | Warwick Castle → London | Side → Ankara | Nikkō Tōshō-gū → Tokyo | Aqueduct of Valens → Ankara | Aqueduct of Segovia → Madrid | Rembrandt House Museum → Amsterdam | Al-Masjid Al-Haram → Riyadh | Galapagos Islands → Quito | Fort Jesus Museum → Nairobi || **Final:** Bad Pyrmont → Berlin

- **Query 293 — Context:** Uraniborg → Stockholm | Cathedral of Valladolid → Madrid | Fallingwater → Washington, D.C. | Bamburgh Castle → London | The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. | Catacombs of Kom el Shoqafa → Cairo | Alnwick Castle → London | Cathedral Basilica of the Virgin of Incarnation → Madrid | Charminar → New Delhi | Museo dell&#x27;Opera del Duomo → Rome || **Final:** Wustrow → Berlin

- **Query 294 — Context:** Schönwald im Schwarzwald → Berlin | Pulkovo Observatory → Moscow | Ancient Theatre of Epidaurus → Athens | Pripyat amusement park → Kyiv | Mariánské Lázně → Prague | Isny im Allgäu → Berlin | Smrdáky → Bratislava | Gol Gumbaz → New Delhi | Ambras Castle → Vienna | Mausoleum of Galla Placidia → Rome || **Final:** Świeradów-Zdrój → Warsaw

- **Query 313 — Context:** Baabe → Berlin | Old Faithful → Washington, D.C. | Natzweiler-Struthof concentration camp → Paris | Putuoshan → Beijing | KV17 → Cairo | Bad Klosterlausnitz → Berlin | Oscar Niemeyer International Cultural Centre → Madrid | Heringsdorf → Berlin | Canyon de Chelly National Monument → Washington, D.C. | Jasna Góra Monastery → Warsaw || **Final:** Ferapontov Monastery → Moscow

- **Query 315 — Context:** Bad Wildungen → Berlin | Imam Reza Shrine → Tehran | Bad Berneck im Fichtelgebirge → Berlin | Tatranská Lomnica → Bratislava | Pellworm → Berlin | Tann → Berlin | Aiguille du Midi → Paris | Dallas Museum of Art → Washington, D.C. | Las Médulas → Madrid | Tierradentro → Bogotá || **Final:** KV34 → Cairo

- **Query 316 — Context:** Mobility Resort Motegi → Tokyo | Mount Fuji → Tokyo | Yavuz Sultan Selim Bridge → Ankara | Borobudur → Jakarta | Luxor → Cairo | Mausoleum of Theodoric → Rome | The Little Mermaid → Copenhagen | Westerbork Transit Camp → Amsterdam | Wikipedia Monument → Warsaw | Hatfield House → London || **Final:** Bad Schwartau → Berlin

- **Query 317 — Context:** Lascaux → Paris | Angel Falls → Caracas | Hagia Irene → Ankara | Riddarholm Church → Stockholm | Cathedral of Zamora → Madrid | Murtala Muhammed International Airport → Abuja | Qutb complex → New Delhi | Tomb of Absalom → Jerusalem | Eutin → Berlin | Kobe Port Tower → Tokyo || **Final:** Pelion → Athens

- **Query 325 — Context:** Wat Arun → Bangkok | Hong Kong Disneyland → Beijing | Bardejov → Bratislava | Grande Arche → Paris | Alaçatı → Ankara | Wild Wadi Water Park → Abu Dhabi | Magura Cave → Sofia | Mount Wutai → Beijing | Mystery Play of Elche → Madrid | Doge&#x27;s Palace, Genoa → Rome || **Final:** Soltaniyeh Dome → Tehran

- **Query 330 — Context:** Children&#x27;s Peace Monument → Tokyo | Efteling → Amsterdam | Amber Mountain National Park → Antananarivo | Spodek → Warsaw | Mulholland Drive → Washington, D.C. | Taq-i Kisra → Baghdad | Milwaukee Art Museum → Washington, D.C. | Canyon de Chelly National Monument → Washington, D.C. | Admiralty building in Saint Petersburg → Moscow | Rialto Bridge → Rome || **Final:** Pompey&#x27;s Pillar → Cairo

- **Query 331 — Context:** Dubino → Rome | Gonio → Tbilisi | KV35 → Cairo | Miniatürk → Ankara | Sukur → Abuja | Statue of Liberty → Washington, D.C. | Serpentine Galleries → London | Giant&#x27;s Causeway → London | Eyüp Sultan Mosque → Ankara | Tatranská Lomnica → Bratislava || **Final:** Templin → Berlin

- **Query 344 — Context:** The Little Mermaid → Copenhagen | Chehel Sotun → Tehran | Grossglockner High Alpine Road → Vienna | Mount Vesuvius → Rome | Torre del Oro → Madrid | Kykkos Monastery → Nicosia | National Museum in Wrocław → Warsaw | Zhangjiajie Glass Bridge → Beijing | Banya → Sofia | Vigeland installation → Oslo || **Final:** Spiekeroog → Berlin

- **Query 346 — Context:** The Pentagon → Washington, D.C. | Walt Disney Studios → Washington, D.C. | Euthanasia Coaster → London | Friedrichskoog → Berlin | BMW Welt → Berlin | Walled Obelisk → Ankara | Church of the Savior on Blood → Moscow | Putuoshan → Beijing | Rothenburg ob der Tauber → Berlin | The Great Sphinx → Cairo || **Final:** Dolmen of Viera → Madrid

- **Query 349 — Context:** Green Mosque → Kabul | Grūtas Park → Vilnius | KV34 → Cairo | Smrdáky → Bratislava | Wallace Monument → London | Museum of Anatolian Civilizations → Ankara | Troldhaugen → Oslo | Bad Wilsnack → Berlin | Cleveland Museum of Art → Washington, D.C. | Bertha Benz Memorial Route → Berlin || **Final:** Gołdap → Warsaw

- **Query 350 — Context:** Bacho Kiro cave → Sofia | Monument to the Great Fire of London → London | Fallingwater → Washington, D.C. | Taj Mahal → New Delhi | Osmangazi Bridge → Ankara | Belfry of Bruges → City of Brussels | Falkirk Wheel → London | Ben Nevis → London | Saihō-ji → Tokyo | KV8 → Cairo || **Final:** Mölln → Berlin

- **Query 352 — Context:** Willingen (Upland) → Berlin | Bad Pyrmont → Berlin | Megara Hyblaea → Rome | Spannagel Cave → Vienna | Edinburgh Castle → London | Tokyo Disneyland → Tokyo | St. Florian&#x27;s Gate → Warsaw | Chichen Itza → Mexico City | Orkhon inscriptions → Ulaanbaatar | KV6 → Cairo || **Final:** Athena Parthenos → Athens

- **Query 353 — Context:** Mount Erciyes → Ankara | Christ the Redeemer → Brasília | Amber Mountain National Park → Antananarivo | Ourense Cathedral → Madrid | Fortifications of Kotor → Podgorica | Royal Palace of La Granja de San Ildefonso → Madrid | Ca&#x27; Rezzonico → Rome | Big Sur → Washington, D.C. | Roman Baths → London | Column of Constantine → Ankara || **Final:** Bad Homburg vor der Höhe → Berlin

- **Query 355 — Context:** Alaçatı → Ankara | Cabo San Lucas → Mexico City | Alcázar of Toledo → Madrid | Ponte Vecchio → Rome | Columbus Monument → Madrid | Rijksmuseum → Amsterdam | Covent Garden → London | Disneyland Paris → Paris | Laykyun Sekkya → Naypyidaw | Jaén Cathedral → Madrid || **Final:** Baltrum → Berlin

- **Query 358 — Context:** Parc Astérix → Paris | Groeningemuseum → City of Brussels | Pombia Safari Park → Rome | Perledo → Rome | Burj Khalifa → Abu Dhabi | Antelope Canyon → Washington, D.C. | Koporye → Moscow | Uludağ → Ankara | Mount Kumgang Tourist Region → Pyongyang | Bad Salzungen → Berlin || **Final:** Szczawnica → Warsaw

- **Query 359 — Context:** Columbus Monument → Madrid | Kingda Ka → Washington, D.C. | Cueva de las Manos → Buenos Aires | Disneyland Park → Paris | Muszyna → Warsaw | Kunstkamera → Moscow | Roman Walls of Lugo → Madrid | Tomb of Absalom → Jerusalem | Röbel → Berlin | Condé Museum → Paris || **Final:** Rietveld Schröder House → Amsterdam

- **Query 360 — Context:** Sklené Teplice → Bratislava | Mandello del Lario → Rome | Bad Marienberg → Berlin | Ponte Vecchio → Rome | Perledo → Rome | Hagia Irene → Ankara | Antelope Canyon → Washington, D.C. | Disneyland → Washington, D.C. | Carrow Road → London | Brancacci Chapel → Rome || **Final:** Kungur Ice Cave → Moscow

- **Query 363 — Context:** Newgrange → Dublin | Frasassi Caves → Rome | Monument Valley → Washington, D.C. | Cathedral of Saint Demetrius → Moscow | Ambras Castle → Vienna | Canyon de Chelly National Monument → Washington, D.C. | Pyramid of Cestius → Rome | Yıldız Palace → Ankara | Maes Howe → London | Yungang Grottoes → Beijing || **Final:** Mastabet el-Fara&#x27;un → Cairo

- **Query 367 — Context:** Baltimore Museum of Art → Washington, D.C. | Westerbork Transit Camp → Amsterdam | Vittskövle Church → Stockholm | The Museum of Innocence → Ankara | Qutb complex → New Delhi | Mount Kumgang Tourist Region → Pyongyang | Călimănești → Bucharest | Sukiennice → Warsaw | Spannagel Cave → Vienna | Istanbul Archaeology Museums → Ankara || **Final:** Bad Freienwalde → Berlin

- **Query 369 — Context:** Läckö Castle → Stockholm | Oscar Niemeyer International Cultural Centre → Madrid | Georgia Guidestones → Washington, D.C. | Jedlina-Zdrój → Warsaw | Tsūtenkaku → Tokyo | Gateway Arch → Washington, D.C. | Sir John Soane&#x27;s Museum → London | Morskie Oko → Warsaw | Chehel Sotun → Tehran | Jaraba → Madrid || **Final:** Graal-Müritz → Berlin

- **Query 372 — Context:** Thien Duong Cave → Hanoi | Belfry of Bruges → City of Brussels | Spa → City of Brussels | Arch of the Sergii → Zagreb | Roman Baths → London | Sultan Ahmed Mosque → Ankara | Hong Kong Disneyland → Beijing | Anne Frank House → Amsterdam | KV13 → Cairo | Tower Bridge → London || **Final:** Bad Dürrheim → Berlin

- **Query 377 — Context:** Spa → City of Brussels | Rietveld Schröder House → Amsterdam | Roman Walls of Lugo → Madrid | Pinacoteca di Brera → Rome | Statue of Liberty → Washington, D.C. | Yumen Pass → Beijing | Istanbul Archaeology Museums → Ankara | Euthanasia Coaster → London | Doge&#x27;s Palace → Rome | Gaztelugatxe → Madrid || **Final:** Tarxien Temples → Valletta

- **Query 378 — Context:** Peggy Guggenheim Collection → Rome | Veliky Ustyug → Moscow | The Cloisters → Washington, D.C. | Glory&#x27;s Portico → Madrid | Teylers Museum → Amsterdam | Jasna Góra Monastery → Warsaw | Munch Museum → Oslo | Tower of the Winds → Athens | Shanghai Disneyland Park → Beijing | Świnoujście → Warsaw || **Final:** Sandanski → Sofia

- **Query 379 — Context:** Al-Askari Shrine → Baghdad | Rothenburg ob der Tauber → Berlin | Brest Fortress → Minsk | Świeradów-Zdrój → Warsaw | Narva Triumphal Arch → Moscow | Alnwick Castle → London | Stockholm Palace → Stockholm | Oslo Opera House → Oslo | Saint Michael&#x27;s Castle → Moscow | Neue Pinakothek → Berlin || **Final:** Monastery of Saint John of Rila → Sofia

- **Query 381 — Context:** Momine Khatun Mausoleum → Baku | Obelisk of Axum → Addis Ababa | Zhouzhuang Town → Beijing | Trafalgar Square → London | Wild Wadi Water Park → Abu Dhabi | Mulholland Drive → Washington, D.C. | Serengeti National Park → Dodoma | Yıldız Hamidi Mosque → Ankara | Federal Hall → Washington, D.C. | Fort Jesus Museum → Nairobi || **Final:** Dikteon Andron → Athens

- **Query 382 — Context:** Bad Schlema → Berlin | Musée Fabre → Paris | Canyon de Chelly National Monument → Washington, D.C. | Gothenburg Museum of Art → Stockholm | Ferapontov Monastery → Moscow | National Gallery → London | Cathedral Basilica of St. Ann → Madrid | Ca&#x27; d&#x27;Oro → Rome | Druskininkai → Vilnius | Euthanasia Coaster → London || **Final:** Morskie Oko → Warsaw

- **Query 386 — Context:** Mazar-e-Quaid → Islamabad | Petershagen → Berlin | Pingyao → Beijing | Willingen (Upland) → Berlin | Kizhi Pogost → Moscow | Chilean National Museum of Fine Arts → Santiago | Mamayev Kurgan → Moscow | Ortaköy Mosque → Ankara | Läckö Castle → Stockholm | Torre del Oro → Madrid || **Final:** Van Gogh Museum → Amsterdam

- **Query 390 — Context:** Banqueting House → London | Monument to the Sun → Zagreb | Schönau am Königsee → Berlin | Mazar-e-Quaid → Islamabad | Benaki Museum → Athens | Scharbeutz → Berlin | Bad Neustadt an der Saale → Berlin | Osun-Osogbo Grove → Abuja | Wikipedia Monument → Warsaw | Great Smoky Mountains → Washington, D.C. || **Final:** Vulci → Rome

- **Query 392 — Context:** Fitzwilliam Museum → London | War of Independence Victory Column → Tallinn | Besakih → Jakarta | Luxor → Cairo | Kykkos Monastery → Nicosia | Naval Cathedral in Kronstadt → Moscow | Bargello National Museum → Rome | Ming Xiaoling → Beijing | Gothenburg Museum of Art → Stockholm | Zolotoy Rog → Moscow || **Final:** Hohwacht → Berlin

- **Query 394 — Context:** Sontra → Berlin | Carlsbad Caverns National Park → Washington, D.C. | Behistun Inscription → Tehran | Walled Obelisk → Ankara | Willingen (Upland) → Berlin | Wustrow → Berlin | Walt Disney World Resort → Washington, D.C. | Newgrounds → Washington, D.C. | Acropolis Museum → Athens | Château de Montsoreau → Paris || **Final:** Vittskövle Church → Stockholm

- **Query 396 — Context:** Bad Staffelstein → Berlin | iron pillar of Delhi → New Delhi | Wiesbaden → Berlin | Moderna Museet → Stockholm | Four Corners Monument → Washington, D.C. | Wuyi Mountains → Beijing | Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar | Olsberg → Berlin | Golden Circle → Reykjavík | Martigny-les-Bains → Paris || **Final:** Munch Museum → Oslo

- **Query 398 — Context:** Bad Dürrheim → Berlin | Kelvingrove Art Gallery and Museum → London | Jelling stones → Copenhagen | Scharbeutz → Berlin | Huangshan → Beijing | Timmendorfer Strand → Berlin | Maiden&#x27;s Tower → Ankara | Baiersbronn → Berlin | Mount Vesuvius → Rome | National Library of Wales → London || **Final:** KV1 → Cairo

- **Query 400 — Context:** Newgrange → Dublin | Gdańsk Main Town Hall → Warsaw | Reformation Wall → Bern | Mount Song → Beijing | Uffizi Gallery → Rome | Alexander Column → Moscow | Tian Tan Buddha → Beijing | Bridge of Sighs → Rome | Bara Imambara → New Delhi | Millau Viaduct → Paris || **Final:** Bad Düben → Berlin

- **Query 401 — Context:** Brick Lane → London | Jastrzębie-Zdrój → Warsaw | Besakih → Jakarta | Zhangjiajie Glass Bridge → Beijing | Akbar&#x27;s Tomb → New Delhi | Vindolanda → London | Serpentine Galleries → London | Château de Montsoreau-Museum of Contemporary Art → Paris | Roman Baths → London | Star of Nanchang → Beijing || **Final:** Bad Liebenwerda → Berlin

- **Query 402 — Context:** The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. | Old Faithful → Washington, D.C. | Sinan Pasha Mosque → Prishtina | Ca&#x27; d&#x27;Oro → Rome | Disney&#x27;s Animal Kingdom → Washington, D.C. | Alamo Mission in San Antonio → Washington, D.C. | Peter and Paul Fortress → Moscow | Nanjing Museum → Beijing | New Mosque → Ankara | Trump Tower → Washington, D.C. || **Final:** Kreuth → Berlin

- **Query 405 — Context:** Kew Palace → London | Rothenburg ob der Tauber → Berlin | Ölüdeniz → Ankara | The Wallace Collection → London | Gateway Arch → Washington, D.C. | Millau Viaduct → Paris | National Portrait Gallery → London | Disney Adventure World → Paris | São Paulo Museum of Art → Brasília | Saint Michael&#x27;s Castle → Moscow || **Final:** Mandello del Lario → Rome

- **Query 408 — Context:** The Great Sphinx → Cairo | Tower of London → London | J. Paul Getty Museum → Washington, D.C. | Marktschellenberg → Berlin | Neukirchen → Berlin | Niterói Contemporary Art Museum → Brasília | Villa Tugendhat → Prague | Heiligendamm → Berlin | Bad Urach → Berlin | Alhambra → Madrid || **Final:** Mount Kumgang Tourist Region → Pyongyang

- **Query 409 — Context:** Epcot → Washington, D.C. | Ha Long Bay → Hanoi | Ivolginsky Datsan → Moscow | Museum of Contemporary Art Australia → Canberra | Uraniborg → Stockholm | The Motherland Calls → Moscow | Alexander Column → Moscow | Yavuz Sultan Selim Bridge → Ankara | Ancient Theatre of Epidaurus → Athens | Topkapı Palace → Ankara || **Final:** Bad Soden-Salmünster → Berlin

- **Query 414 — Context:** Cathedral Basilica of St. Ann → Madrid | Champaner-Pavagadh Archaeological Park → New Delhi | Museum of Contemporary Art, Los Angeles → Washington, D.C. | Piccadilly Circus → London | Nanjing Museum → Beijing | Skansen → Stockholm | Downing Street → London | Golden Circle → Reykjavík | Treasury of Atreus → Athens | Śniardwy → Warsaw || **Final:** Bad Lippspringe → Berlin

- **Query 418 — Context:** Benaki Museum → Athens | São Paulo Museum of Art → Brasília | Monastery of Saint John of Rila → Sofia | Bad Sülze → Berlin | Euromast → Amsterdam | National Portrait Gallery → London | Bavaria → Berlin | Aachen → Berlin | Bad Wünnenberg → Berlin | Ming Xiaoling → Beijing || **Final:** KV3 → Cairo

- **Query 429 — Context:** Ancient Theatre of Epidaurus → Athens | Heilbad Heiligenstadt → Berlin | Graal-Müritz → Berlin | Aachen → Berlin | Guédelon Castle → Paris | Osmangazi Bridge → Ankara | Chehel Sotun → Tehran | Bayrischzell → Berlin | Bad Buchau → Berlin | Monument to the Sun → Zagreb || **Final:** Sigüenza Cathedral → Madrid

- **Query 434 — Context:** Palazzo Rosso → Rome | Bridge of Sighs → Rome | Dune of Pilat → Paris | Băile Herculane → Bucharest | Verona Arena → Rome | Nestorian Stele → Beijing | Atakule → Ankara | Mount Sanqing → Beijing | Mnajdra → Valletta | Reformation Wall → Bern || **Final:** Church of the Intercession on the Nerl → Moscow

- **Query 438 — Context:** Copenhagen Zoo → Copenhagen | Maiden&#x27;s Tower → Ankara | Patriarchate of Peja → Belgrade | Jaén Cathedral → Madrid | Hong Kong Disneyland → Beijing | Vigeland installation → Oslo | Republic Monument → Ankara | Jallianwala Bagh → New Delhi | Jamkaran Mosque → Tehran | Shanghai Disneyland Park → Beijing || **Final:** Hitzacker → Berlin

- **Query 448 — Context:** Tomb of Jahangir → Islamabad | Metropolitan Cathedral Basilica of the Holy Saviour, Oviedo → Madrid | Petralona cave → Athens | Golden Circle → Reykjavík | St. Andrew&#x27;s Church → Warsaw | Ushiku Daibutsu → Tokyo | Merneptah Stele → Cairo | Atakule → Ankara | Rock and Roll Hall of Fame → Washington, D.C. | Popeye Village → Valletta || **Final:** Bad Schwalbach → Berlin

- **Query 454 — Context:** St. Nicholas’ Church, Hamburg → Berlin | Ale&#x27;s Stones → Stockholm | Alcázar of Toledo → Madrid | Bellano → Rome | Museu Picasso → Madrid | Cappadocia → Ankara | Bad Staffelstein → Berlin | Igel Column → Berlin | Bad Orb → Berlin | Eisriesenwelt → Vienna || **Final:** Blagaj, Mostar → Sarajevo

- **Query 456 — Context:** Roman Walls of Lugo → Madrid | Hiroshima Peace Memorial → Tokyo | Zolotoy Rog → Moscow | Fifth Avenue → Washington, D.C. | Cueva de Nerja → Madrid | Fatih Istanbul Mosque → Ankara | São Paulo Museum of Art → Brasília | Shah Cheragh shrine → Tehran | Ancient Agora of Athens → Athens | Mamayev Kurgan → Moscow || **Final:** Manderscheid → Berlin

- **Query 459 — Context:** Tabriz Bazaar → Tehran | Banya → Sofia | Conch Republic → Washington, D.C. | Şehzade Mosque → Ankara | Dierhagen → Berlin | Wikipedia Monument → Warsaw | Arlington National Cemetery → Washington, D.C. | Star of Nanchang → Beijing | Cumalıkızık → Ankara | Derby Museum and Art Gallery → London || **Final:** KV6 → Cairo

- **Query 461 — Context:** Badajoz Cathedral → Madrid | Scottish National Gallery → London | Otrar → Astana | Kalyan Minaret → Tashkent | Vigeland installation → Oslo | KV12 → Cairo | Ta&#x27; Ħaġrat → Valletta | Segesta → Rome | Detroit Institute of Arts → Washington, D.C. | Great Ocean Road → Canberra || **Final:** Wiesbaden → Berlin

- **Query 462 — Context:** Scharbeutz → Berlin | Arch of Galerius and Rotunda → Athens | Zingst → Berlin | Murnau am Staffelsee → Berlin | Wuppertal Schwebebahn → Berlin | Dikteon Andron → Athens | Naqsh-e Jahan Square → Tehran | Damavand → Tehran | Bad Kissingen → Berlin | Tecklenburg → Berlin || **Final:** Valaam Monastery → Moscow

- **Query 467 — Context:** Mount Kumgang Tourist Region → Pyongyang | Otrar → Astana | Zinnowitz → Berlin | One World Trade Center → Washington, D.C. | Centennial Hall → Warsaw | National Gallery of Victoria → Canberra | Yavuz Sultan Selim Bridge → Ankara | Euromast → Amsterdam | Museo Egizio In Turin (IT) → Rome | Mölln → Berlin || **Final:** Yuste → Madrid

- **Query 470 — Context:** Yosemite National Park → Washington, D.C. | Museum of Modern Art of Republika Srpska → Sarajevo | Bryn Celli Ddu → London | Champaner-Pavagadh Archaeological Park → New Delhi | KV13 → Cairo | Kenilworth Castle → London | Urquhart Castle → London | Bad Füssing → Berlin | Museum of Fine Arts, Houston → Washington, D.C. | Carisbrooke Castle → London || **Final:** Church of the Savior on Blood → Moscow

- **Query 478 — Context:** National Library of Australia → Canberra | Potala Palace → Beijing | Ortaköy → Ankara | Neubulach → Berlin | Grand Bazaar → Ankara | Great Geysir → Reykjavík | Nonnweiler → Berlin | Tatranská Lomnica → Bratislava | Roman Walls of Lugo → Madrid | Juventus Stadium → Rome || **Final:** Chehel Sotun → Tehran

- **Query 482 — Context:** Museu Picasso → Madrid | Kyoto Tower → Tokyo | Munch Museum → Oslo | Jallianwala Bagh → New Delhi | Kailasa Temple, Ellora → New Delhi | Sir John Soane&#x27;s Museum → London | Van Gogh Museum → Amsterdam | Athena Promachos → Athens | Museo Egizio In Turin (IT) → Rome | Brooklyn Museum → Washington, D.C. || **Final:** Bad Harzburg → Berlin

- **Query 484 — Context:** Mecca → Riyadh | Design Museum Holon → Jerusalem | KV17 → Cairo | Teide → Madrid | Liberty Bell → Washington, D.C. | Krynica-Zdrój → Warsaw | Maes Howe → London | Galapagos Islands → Quito | Peter and Paul Fortress → Moscow | İstiklal Avenue → Ankara || **Final:** Schönwald im Schwarzwald → Berlin

- **Query 488 — Context:** Mole Antonelliana → Rome | Bad Bertrich → Berlin | Villa Tugendhat → Prague | Groeningemuseum → City of Brussels | Old Town of Lijiang → Beijing | Tokyo Disney Resort → Tokyo | St. Blasien → Berlin | Bad Rothenfelde → Berlin | Bodrum Castle → Ankara | St. Nicholas’ Church, Hamburg → Berlin || **Final:** Palacio Episcopal de Astorga → Madrid

- **Query 493 — Context:** Bad Grönenbach → Berlin | Ballabio → Rome | Champaner-Pavagadh Archaeological Park → New Delhi | Thien Duong Cave → Hanoi | Wissen → Berlin | Bad Wiessee → Berlin | Bad Waldsee → Berlin | Kelvingrove Art Gallery and Museum → London | Tomb of Suleyman Shah → Damascus | Al-Masjid Al-Haram → Riyadh || **Final:** Athena Promachos → Athens

- **Query 495 — Context:** Langeoog → Berlin | türbe → Constantinople | Yungang Grottoes → Beijing | Treblinka extermination camp → Warsaw | Belfry of Bruges → City of Brussels | Rundetaarn → Copenhagen | Bavarian National Museum → Berlin | Bad Langensalza → Berlin | Chełmno extermination camp → Warsaw | Hong Kong Disneyland → Beijing || **Final:** Château de Montsoreau → Paris

- **Query 505 — Context:** Sirius Arena → Moscow | Bad Tennstedt → Berlin | Marble Arch → London | Bad Staffelstein → Berlin | Hospital of Innocents → Rome | Bad Hönningen → Berlin | Maya Ruins of Tulum → Mexico City | Kraków Barbican → Warsaw | Denver Art Museum → Washington, D.C. | German Federal Archives → Berlin || **Final:** Bad Ischl → Vienna

- **Query 514 — Context:** Lake Retba → Dakar | Bad Wimpfen → Berlin | Valle dei Templi → Rome | Museo Poldi Pezzoli → Rome | Batu Caves → Kuala Lumpur | Carlsbad Caverns National Park → Washington, D.C. | Anne Frank House → Amsterdam | Bad Reichenhall → Berlin | KV14 → Cairo | Tower of London → London || **Final:** Mobility Resort Motegi → Tokyo

- **Query 515 — Context:** Linköping Cathedral → Stockholm | Disneyland Paris → Paris | Athena Parthenos → Athens | Oslo Opera House → Oslo | Solomon R. Guggenheim Museum → Washington, D.C. | Silesian Stadium → Warsaw | KV8 → Cairo | Natzweiler-Struthof concentration camp → Paris | Museum of San Marco → Rome | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid || **Final:** Biedenkopf → Berlin

- **Query 521 — Context:** Barbican Centre → London | Rundetaarn → Copenhagen | Spodek → Warsaw | Si-o-se Pol → Tehran | Walhalla memorial → Berlin | Museum of Contemporary Art Australia → Canberra | Pura Ulun Danu Bratan → Jakarta | Grand Egyptian Museum → Cairo | Bad Frankenhausen → Berlin | Empire State Building → Washington, D.C. || **Final:** Dadiani Palaces Museum → Tbilisi

- **Query 522 — Context:** Conch Republic → Washington, D.C. | Treblinka extermination camp → Warsaw | Burj Khalifa → Abu Dhabi | Peter the Great Saint Petersburg State Polytechnical University → Moscow | Batu Caves → Kuala Lumpur | Diamond Head → Washington, D.C. | Popeye Village → Valletta | Kelvingrove Art Gallery and Museum → London | Arch of Galerius and Rotunda → Athens | Holy Trinity Column in Olomouc → Prague || **Final:** Ytterby mine → Stockholm

- **Query 527 — Context:** Puy de Dôme → Paris | Bertha Benz Memorial Route → Berlin | Ipatiev House → Moscow | Colossus of Rhodes → Athens | São Paulo Museum of Art → Brasília | Grand Bazaar → Ankara | Cave of El Castillo → Madrid | Damavand → Tehran | German Wine Route → Berlin | Königsfeld im Schwarzwald → Berlin || **Final:** Książ Castle and park complex → Warsaw

- **Query 533 — Context:** Bad Aibling → Berlin | Bad Freienwalde → Berlin | Alexander Nevsky Lavra → Moscow | Tamme-Lauri oak → Tallinn | Nabi Habeel Mosque → Damascus | Rothenburg ob der Tauber → Berlin | Marmurova Pechera → Kyiv | Nieheim → Berlin | Amber Mountain National Park → Antananarivo | Viñales Valley → Havana || **Final:** Catacombs of Kom el Shoqafa → Cairo

- **Query 534 — Context:** Kraków Barbican → Warsaw | Mount Jiuhua → Beijing | National Portrait Gallery → London | Ourense Cathedral → Madrid | Museo Egizio In Turin (IT) → Rome | Gochang, Hwasun and Ganghwa Dolmen Sites → Seoul | Serdobsk → Moscow | Uffizi Gallery → Rome | Serengeti National Park → Dodoma | Majuli → New Delhi || **Final:** Bad Belzig → Berlin

- **Query 535 — Context:** Bad Oeynhausen → Berlin | Hisarya → Sofia | Times Square → Washington, D.C. | Kühlungsborn → Berlin | Petra → Amman | Cave of Swallows → Mexico City | Seiffen/Erzgeb. → Berlin | Bad Buchau → Berlin | Imam Husayn Mausoleum → Baghdad | Bibi Ka Maqbara → New Delhi || **Final:** Puy de Dôme → Paris

- **Query 542 — Context:** Bad Fallingbostel → Berlin | The Little Mermaid → Copenhagen | Tabriz Bazaar → Tehran | Romantic Road → Berlin | Dikteon Andron → Athens | Bad Hindelang → Berlin | Luxor → Cairo | Old House of Bank → Stockholm | Mount Vernon → Washington, D.C. | Barbican Centre → London || **Final:** Bad Aussee → Vienna

- **Query 548 — Context:** Old House of Bank → Stockholm | Al-Rifa&#x27;i Mosque → Cairo | Masuleh → Tehran | Zolotoy Rog → Moscow | Sydney Tower → Canberra | Al Abbas Mosque → Baghdad | Thien Duong Cave → Hanoi | Segovia Cathedral → Madrid | Fitzwilliam Museum → London | Salar Jung Museum → New Delhi || **Final:** Blankenburg → Berlin

- **Query 551 — Context:** Antelope Canyon → Washington, D.C. | The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. | Winterberg → Berlin | Bad König → Berlin | Hadrian&#x27;s Villa → Rome | Conch Republic → Washington, D.C. | Ploshchad Vosstaniya → Moscow | İstiklal Avenue → Ankara | Megara Hyblaea → Rome | Lublin-Majdanek concentration camp → Warsaw || **Final:** Newgrange → Dublin

- **Query 553 — Context:** Ming Xiaoling → Beijing | Hever Castle → London | Admiralty building in Saint Petersburg → Moscow | Huangshan → Beijing | Che Guevara Mausoleum → Havana | National Gallery of Norway → Oslo | Kresty Prison → Moscow | Tropaeum Traiani → Bucharest | Niagara Falls → Ottawa | Lion of Belfort → Paris || **Final:** Bad Neuenahr-Ahrweiler → Berlin

- **Query 554 — Context:** Marine Corps War Memorial → Washington, D.C. | Hollywood Sign → Washington, D.C. | Sayyidah Zaynab Mosque → Damascus | Bargello National Museum → Rome | Viñales Valley → Havana | Heligoland → Berlin | Mevlâna Museum → Ankara | Bad Füssing → Berlin | St. Blasien → Berlin | Krakus Mound → Warsaw || **Final:** Nikkō Tōshō-gū → Tokyo

- **Query 561 — Context:** Benaki Museum → Athens | Soluntum → Rome | Norderney → Berlin | Gołdap → Warsaw | Zhouzhuang Town → Beijing | Euromast → Amsterdam | Varshets → Sofia | The Little Mermaid → Copenhagen | Empire State Building → Washington, D.C. | Detroit Institute of Arts → Washington, D.C. || **Final:** tomb of Tutankhamun → Cairo

- **Query 564 — Context:** Buddha Park → Vientiane | St. Nicholas Naval Cathedral, St. Petersburg → Moscow | Teide → Madrid | Rijksmuseum → Amsterdam | Seiffen/Erzgeb. → Berlin | Tropical Islands → Berlin | Lahnstein → Berlin | Naracoorte Caves National Park → Canberra | Bad Bentheim → Berlin | Wiesbaden → Berlin || **Final:** Frasassi Caves → Rome

- **Query 566 — Context:** Serpentine Galleries → London | Varshets → Sofia | Luxor Museum → Cairo | Ancient Theatre of Epidaurus → Athens | Al-Askari Shrine → Baghdad | Spannagel Cave → Vienna | National Museum of Pakistan → Islamabad | Museu Picasso → Madrid | Verona Arena → Rome | Ephesus → Ankara || **Final:** Vallendar → Berlin

- **Query 571 — Context:** Iglesia de la Concepción → Madrid | Alamo Mission in San Antonio → Washington, D.C. | Tomb of Caecilia Metella → Rome | KV1 → Cairo | Borobudur → Jakarta | Alhambra → Madrid | Milan Cathedral → Rome | Christ the King statue → Warsaw | Basilica of San Francesco d&#x27;Assisi → Rome | Niagara Falls → Ottawa || **Final:** Eutin → Berlin

- **Query 572 — Context:** Wallace Monument → London | Hampton Court Palace → London | Cabo San Lucas → Mexico City | Yusupov Palace on Moika → Moscow | Akbar&#x27;s Tomb → New Delhi | Naxos → Rome | St. Andrew&#x27;s Church → Warsaw | Aiguille du Midi → Paris | West Lake → Beijing | Poulnabrone dolmen → Dublin || **Final:** Bad Rothenfelde → Berlin

- **Query 574 — Context:** Zhangjiajie Glass Bridge → Beijing | Seikilos epitaph → Athens | Laykyun Sekkya → Naypyidaw | Detroit Institute of Arts → Washington, D.C. | Disneyland → Washington, D.C. | Vijećnica → Sarajevo | Walibi Holland → Amsterdam | Benaki Museum → Athens | Thracian Tomb of Kazanlak → Sofia | Örebro Castle → Stockholm || **Final:** Bad Segeberg → Berlin

- **Query 575 — Context:** Ani → Ankara | Cueva de Nerja → Madrid | Doge&#x27;s Palace, Genoa → Rome | Fatih Sultan Mehmet Bridge → Ankara | Kensington Palace → London | Yıldız Hamidi Mosque → Ankara | Basilica of Our Lady of the Pillar → Madrid | Hong Kong Museum of Art → Beijing | Crazy Horse Memorial → Washington, D.C. | Königsfeld im Schwarzwald → Berlin || **Final:** Madurodam → Amsterdam

- **Query 580 — Context:** Gaztelugatxe → Madrid | Al-Rifa&#x27;i Mosque → Cairo | KV16 → Cairo | Bad Endorf → Berlin | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing | Mount Lu → Beijing | İstiklal Avenue → Ankara | Frasassi Caves → Rome | Tegernsee → Berlin | Forest of the Martyrs → Jerusalem || **Final:** Kizhi Pogost → Moscow

- **Query 585 — Context:** Tomb of Hafez → Tehran | Naracoorte Caves National Park → Canberra | Hoover Dam → Washington, D.C. | Chillon Castle → Bern | Inveraray Castle → London | Tabriz Bazaar → Tehran | Liberty Bell → Washington, D.C. | Stirling Castle → London | Novocherkassk Cathedral → Moscow | Doge&#x27;s Palace, Genoa → Rome || **Final:** Nümbrecht → Berlin

- **Query 587 — Context:** Basilica of San Francesco d&#x27;Assisi → Rome | Baden → Vienna | MAXXI → Rome | Chillon Castle → Bern | Märcani Mosque → Moscow | Mystery Play of Elche → Madrid | Martigny-les-Bains → Paris | Fountains Abbey → London | Krakus Mound → Warsaw | Dolmen of Viera → Madrid || **Final:** Wangerooge → Berlin

- **Query 590 — Context:** Saint Michael&#x27;s Castle → Moscow | Divriği Great Mosque and Hospital → Ankara | Pombia Safari Park → Rome | Wellington Arch → London | National Museum in Kraków → Warsaw | Fort Jesus Museum → Nairobi | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing | Great Buddha of Thailand → Bangkok | Old Faithful → Washington, D.C. | Hatfield House → London || **Final:** Parc Astérix → Paris

- **Query 597 — Context:** Blackpool Tower → London | Zuma Rock → Abuja | Winchester Mystery House → Washington, D.C. | Centennial Hall → Warsaw | Vjetrenica → Sarajevo | KV26 → Cairo | Kobe Port Tower → Tokyo | Denver Art Museum → Washington, D.C. | Peggy Guggenheim Collection → Rome | Orkhon inscriptions → Ulaanbaatar || **Final:** Bad Soden am Taunus → Berlin

- **Query 599 — Context:** Canadian Museum of History → Ottawa | Melsungen → Berlin | Tower of London → London | Apsley House → London | The Pentagon → Washington, D.C. | Läckö Castle → Stockholm | Tomb of I&#x27;timād-ud-Daulah → New Delhi | Garmisch-Partenkirchen → Berlin | Gernsbach → Berlin | Ale&#x27;s Stones → Stockholm || **Final:** Balatonfüred → Budapest

- **Query 602 — Context:** Antwerp City Hall → City of Brussels | M. H. de Young Memorial Museum → Washington, D.C. | Lake Retba → Dakar | Bischofswiesen → Berlin | Doge&#x27;s Palace, Genoa → Rome | Beylerbeyi Palace → Ankara | Wrocław Cathedral → Warsaw | Windsor Castle → London | Bad Harzburg → Berlin | Bad Wiessee → Berlin || **Final:** KV21 → Cairo

- **Query 604 — Context:** Museum of Fine Arts Boston → Washington, D.C. | Zolotoy Rog → Moscow | Tower Bridge → London | Cedar Point → Washington, D.C. | Drottningholm Palace → Stockholm | Son Doong Cave → Hanoi | Glasgow Cathedral → London | Coves del Drach → Madrid | Topkapı Palace → Ankara | Brooklyn Bridge → Washington, D.C. || **Final:** Bad Salzuflen → Berlin

- **Query 605 — Context:** Yosemite National Park → Washington, D.C. | Goa Gajah → Jakarta | Rainbow Bridge National Monument → Washington, D.C. | Rengsdorf → Berlin | Bad Urach → Berlin | Horse Cave → Washington, D.C. | Disneyland Park → Paris | Freiburg im Breisgau → Berlin | Westerbork Transit Camp → Amsterdam | Niagara Falls → Ottawa || **Final:** Zolotoy Rog → Moscow

- **Query 606 — Context:** Hospital of Innocents → Rome | Multnomah Falls → Washington, D.C. | Fountains Abbey → London | Naples National Archaeological Museum → Rome | Canyon de Chelly National Monument → Washington, D.C. | Nuruosmaniye Mosque → Ankara | Knossos → Athens | Dolmen of Viera → Madrid | Märcani Mosque → Moscow | Newgrounds → Washington, D.C. || **Final:** Ny Carlsberg Glyptotek → Copenhagen

- **Query 608 — Context:** Turkish and Islamic Arts Museum → Ankara | Kyllburg → Berlin | Trinity Cathedral → Moscow | Wittdün auf Amrum → Berlin | West Bali National Park → Jakarta | Cueva de las Manos → Buenos Aires | iron pillar of Delhi → New Delhi | Lublin-Majdanek concentration camp → Warsaw | Great Smoky Mountains → Washington, D.C. | Divriği Great Mosque and Hospital → Ankara || **Final:** Kenilworth Castle → London

- **Query 613 — Context:** Bad Mergentheim → Berlin | West Lake → Beijing | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Canton Tower → Beijing | Grand Canal → Rome | Bad Füssing → Berlin | Bad Waldsee → Berlin | Mount Ararat → Ankara | Gülhane Park → Ankara | Mount Song → Beijing || **Final:** KV57 → Cairo

- **Query 614 — Context:** Moskovsky railway station → Moscow | Al Khazneh → Amman | Bad Salzuflen → Berlin | Guggenheim Museum → Madrid | Piton des Neiges → Paris | Catacombs of Kom el Shoqafa → Cairo | Anne Frank House → Amsterdam | Dubino → Rome | Burghley House → London | The Nelson-Atkins Museum of Art → Washington, D.C. || **Final:** Benaki Museum → Athens

- **Query 616 — Context:** Aqueduct of Segovia → Madrid | Metropolitan Cathedral Basilica of St. James the Apostle → Madrid | Rietveld Schröder House → Amsterdam | Carrauntoohil → Dublin | Shah Mosque → Tehran | Bad Aussee → Vienna | Fitzwilliam Museum → London | Chelyabinsk Airport → Moscow | İstiklal Avenue → Ankara | Grand Egyptian Museum → Cairo || **Final:** Bad Elster → Berlin

- **Query 617 — Context:** Museum of San Marco → Rome | Baden-Baden → Berlin | Chesme Church → Moscow | Pickford&#x27;s House → London | Willis Tower → Washington, D.C. | Redwood National and State Parks → Washington, D.C. | Patriarchate of Peja → Belgrade | Obelisk of Axum → Addis Ababa | Catholic Church of St. Catherine → Moscow | Museum of Cycladic Art → Athens || **Final:** Spodek → Warsaw

- **Query 634 — Context:** KV7 → Cairo | Accademia Carrara → Rome | Kronberg im Taunus → Berlin | Museum of Cycladic Art → Athens | Triberg im Schwarzwald → Berlin | DeviantArt → Washington, D.C. | Cathedral Basilica of the Virgin of Incarnation → Madrid | Old Faithful → Washington, D.C. | Canton Tower → Beijing | Tomb of Absalom → Jerusalem || **Final:** Woburn Abbey → London

- **Query 638 — Context:** Mariánské Lázně → Prague | Lion of Belfort → Paris | One World Trade Center → Washington, D.C. | Big Sur → Washington, D.C. | Qutb complex → New Delhi | Fort Jesus Museum → Nairobi | Lia Fáil → Dublin | Arch of Trajan → Rome | Gołdap → Warsaw | Rialto Bridge → Rome || **Final:** Bad Bayersoien → Berlin

- **Query 645 — Context:** Dubino → Rome | Bad Salzdetfurth → Berlin | Bad Klosterlausnitz → Berlin | Bad Brückenau → Berlin | Rumelihisarı → Ankara | The Frick Collection → Washington, D.C. | Fingal&#x27;s Cave → London | Wales Coast Path → London | Groeningemuseum → City of Brussels | Waren → Berlin || **Final:** Choragic Monument of Lysicrates → Athens

- **Query 646 — Context:** Damavand → Tehran | Bad Nenndorf → Berlin | Mamayev Kurgan → Moscow | Naxos → Rome | Bad Buchau → Berlin | Luxor Museum → Cairo | Kołobrzeg → Warsaw | Metropolitan Cathedral Basilica of St. James the Apostle → Madrid | Design Museum Holon → Jerusalem | Nuruosmaniye Mosque → Ankara || **Final:** Škocjan Caves → Ljubljana

- **Query 651 — Context:** Tomb of Askia → Bamako | KV5 → Cairo | Bad König → Berlin | Banya → Sofia | Conch Republic → Washington, D.C. | KV11 → Cairo | Tian Tan Buddha → Beijing | Nesebar → Sofia | Bad Bentheim → Berlin | Skansen → Stockholm || **Final:** Museum of Cycladic Art → Athens

- **Query 652 — Context:** Newgrounds → Washington, D.C. | Big Sur → Washington, D.C. | Fountains Abbey → London | Ölüdeniz → Ankara | Obelisk of Theodosius → Ankara | Borobudur → Jakarta | Albert Memorial → London | Domica → Bratislava | Peter and Paul Fortress → Moscow | Imam Husayn Mausoleum → Baghdad || **Final:** Bad Schlema → Berlin

- **Query 654 — Context:** Lugo Cathedral → Madrid | Yıldız Palace → Ankara | Hong Kong Disneyland → Beijing | National Archaeological Museum → Rome | Gołdap → Warsaw | Astrid Lindgren&#x27;s World → Stockholm | Louisiana Museum of Modern Art → Copenhagen | KV17 → Cairo | Lychakiv Cemetery → Kyiv | Fifth Avenue → Washington, D.C. || **Final:** Naumburg → Berlin

- **Query 656 — Context:** Star of Nanchang → Beijing | Times Square → Washington, D.C. | Bad Grund → Berlin | Aflenz Kurort → Vienna | Bad Emstal → Berlin | Peggy Guggenheim Collection → Rome | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing | Dallas Museum of Art → Washington, D.C. | Famine Stela → Cairo | Dune of Pilat → Paris || **Final:** Cliffs of Moher → Dublin

- **Query 657 — Context:** Bad Segeberg → Berlin | Bankya → Sofia | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Carisbrooke Castle → London | Zinnowitz → Berlin | Gaztelugatxe → Madrid | Bad Urach → Berlin | Kobe Port Tower → Tokyo | Bamburgh Castle → London | Wittdün auf Amrum → Berlin || **Final:** Lądek-Zdrój → Warsaw

- **Query 666 — Context:** Column of Constantine → Ankara | Santa Claus Village → Helsinki | Sverd i fjell → Oslo | Pombia Safari Park → Rome | KV15 → Cairo | Bryn Celli Ddu → London | Mount Ararat → Ankara | Cloud Gate → Washington, D.C. | Bad Essen → Berlin | Son Doong Cave → Hanoi || **Final:** Serdobsk → Moscow

- **Query 668 — Context:** Piazza San Marco → Rome | Carisbrooke Castle → London | Galapagos Islands → Quito | Kraków Barbican → Warsaw | Royal Academy of Arts → London | Tomb of Jahangir → Islamabad | Dolmen of Menga → Madrid | Puy de Dôme → Paris | Porta San Sebastiano → Rome | Summer Garden → Moscow || **Final:** Röbel → Berlin

- **Query 671 — Context:** Forest of the Martyrs → Jerusalem | Kailasa Temple, Ellora → New Delhi | Bad Hönningen → Berlin | Doge&#x27;s Palace, Genoa → Rome | Urquhart Castle → London | Museum of Anatolian Civilizations → Ankara | Baltimore Museum of Art → Washington, D.C. | Bad Laasphe → Berlin | Old Faithful → Washington, D.C. | Nordic Museum → Stockholm || **Final:** Củ Chi tunnels → Hanoi

- **Query 676 — Context:** Ustroń → Warsaw | Škocjan Caves → Ljubljana | Gonio → Tbilisi | Schönwald im Schwarzwald → Berlin | Jeita Grotto → Beirut | Amélie-les-Bains-Palalda → Paris | Glamis Castle → London | Vittskövle Church → Stockholm | Bad Tölz → Berlin | Bad Griesbach im Rottal → Berlin || **Final:** Badajoz Cathedral → Madrid

- **Query 683 — Context:** Tecklenburg → Berlin | Susa → Tehran | Boltenhagen → Berlin | Bamburgh Castle → London | Spiekeroog → Berlin | Murtala Muhammed International Airport → Abuja | Wiesbaden → Berlin | Arch of Hadrian → Athens | Umedalens Skulpturpark → Stockholm | Gol Gumbaz → New Delhi || **Final:** Jeita Grotto → Beirut

- **Query 685 — Context:** Little Hagia Sophia → Ankara | Portman Road → London | Veliky Ustyug → Moscow | Palazzo Vecchio → Rome | Wrocław Cathedral → Warsaw | KV2 → Cairo | Cathedral of La Laguna → Madrid | Nemrut → Ankara | Rabka-Zdrój → Warsaw | ArcelorMittal Orbit → London || **Final:** Heimbach → Berlin

- **Query 686 — Context:** Bad Wiessee → Berlin | Grūtas Park → Vilnius | Ben Nevis → London | Catholic Church of St. Catherine → Moscow | DeviantArt → Washington, D.C. | Anichkov Palace → Moscow | Jasna Góra Monastery → Warsaw | Zinnowitz → Berlin | Kraków Barbican → Warsaw | Ponte Vecchio → Rome || **Final:** Astrid Lindgren&#x27;s World → Stockholm

- **Query 689 — Context:** KV20 → Cairo | Sorico → Rome | Uraniborg → Stockholm | Segesta → Rome | Windsor Castle → London | Doge&#x27;s Palace, Genoa → Rome | Ivolginsky Datsan → Moscow | Bletchley Park → London | Derby Museum and Art Gallery → London | Nabi Habeel Mosque → Damascus || **Final:** Königsfeld im Schwarzwald → Berlin

- **Query 691 — Context:** Weilburg → Berlin | Hadrian&#x27;s Wall → London | Kew Palace → London | Kingda Ka → Washington, D.C. | Casa Loma → Ottawa | Somerset House → London | Bingling Temple → Beijing | Colossus of Rhodes → Athens | Bad Kötzting → Berlin | Mariánské Lázně → Prague || **Final:** Tatranská Lomnica → Bratislava

- **Query 692 — Context:** Fortifications of Kotor → Podgorica | Triumphal Arch of Orange → Paris | Băile Herculane → Bucharest | Bad Teinach-Zavelstein → Berlin | Kelvingrove Art Gallery and Museum → London | Willingen (Upland) → Berlin | Friedrichroda → Berlin | St. Mary&#x27;s Basilica → Warsaw | Statue of Zeus at Olympia → Athens | Bad Nauheim → Berlin || **Final:** Tomb of Caecilia Metella → Rome

- **Query 694 — Context:** Angel Falls → Caracas | Rabka-Zdrój → Warsaw | Bad Dürkheim → Berlin | Machu Picchu → Lima | Bad Sassendorf → Berlin | Spring Temple Buddha → Beijing | Bad Kissingen → Berlin | Eisriesenwelt → Vienna | Grossglockner High Alpine Road → Vienna | Bacho Kiro cave → Sofia || **Final:** Skansen → Stockholm

- **Query 696 — Context:** Veliky Ustyug → Moscow | National Archaeological Museum of Athens → Athens | Panathenaic Stadium → Athens | Bad Münstereifel → Berlin | Yosemite National Park → Washington, D.C. | Bad Füssing → Berlin | Sandringham House → London | Hiroshima Peace Memorial → Tokyo | Iglesia de la Concepción → Madrid | Fatima Masumeh Shrine → Tehran || **Final:** Wings of Tatev → Yerevan

- **Query 698 — Context:** Galapagos Islands → Quito | Park Güell → Madrid | Terracotta Army → Beijing | Museum of Contemporary Art Australia → Canberra | Vindolanda → London | MACBA Barcelona Museum of Contemporary Art → Madrid | German Wine Route → Berlin | Museo Correr → Rome | Catacombs of Kom el Shoqafa → Cairo | Monument to the Sun → Zagreb || **Final:** Admont Abbey → Vienna

- **Query 701 — Context:** Puente Nuevo → Madrid | Pamplona Cathedral → Madrid | Anichkov Bridge → Moscow | Magic Kingdom → Washington, D.C. | Leshan Giant Buddha → Beijing | Märcani Mosque → Moscow | Wales Coast Path → London | Field of Mars → Moscow | West Bali National Park → Jakarta | KV57 → Cairo || **Final:** Stützerbach → Berlin

- **Query 703 — Context:** Sozopol → Sofia | Seiffen/Erzgeb. → Berlin | Downing Street → London | Istanbul Archaeology Museums → Ankara | Düden Waterfalls → Ankara | Admont Abbey → Vienna | Balatonfüred → Budapest | Spice Bazaar → Ankara | Bad Reichenhall → Berlin | Pripyat amusement park → Kyiv || **Final:** Uppsala Cathedral → Stockholm

- **Query 709 — Context:** Museu Picasso → Madrid | Bad Aussee → Vienna | Grande Arche → Paris | Jingpo Lake → Beijing | KV21 → Cairo | Sequoia National Park → Washington, D.C. | Mammoth Cave National Park → Washington, D.C. | The Nelson-Atkins Museum of Art → Washington, D.C. | Pulkovo Observatory → Moscow | Laykyun Sekkya → Naypyidaw || **Final:** Bad Oeynhausen → Berlin

- **Query 713 — Context:** Lake Powell → Washington, D.C. | Walt Disney Studios → Washington, D.C. | KV3 → Cairo | Besakih → Jakarta | Mask of Sorrow → Moscow | Bad Aussee → Vienna | Casa Loma → Ottawa | Yamunotri → New Delhi | Obelisk of Theodosius → Ankara | Caernarfon Castle → London || **Final:** Schönau am Königsee → Berlin

- **Query 720 — Context:** Shanhai Pass → Beijing | Cave of Altacosa → Madrid | Centennial Hall → Warsaw | Bad Aibling → Berlin | Museum of Fine Arts, Houston → Washington, D.C. | Bad Karlshafen → Berlin | KV7 → Cairo | Covent Garden → London | Forchtenstein Castle → Vienna | Momine Khatun Mausoleum → Baku || **Final:** Vintgar Gorge → Ljubljana

- **Query 722 — Context:** Bad Windsheim → Berlin | Conch Republic → Washington, D.C. | Bad Rothenfelde → Berlin | Royal Pavilion &amp; Garden → London | Bad Sobernheim → Berlin | Bad Sooden-Allendorf → Berlin | Lenzkirch → Berlin | 30 St Mary Axe → London | Castello Estense → Rome | National Gallery → London || **Final:** Ladonia → Stockholm

- **Query 729 — Context:** Detroit Institute of Arts → Washington, D.C. | Czartoryski Museum → Warsaw | Lake Powell → Washington, D.C. | Pompey&#x27;s Pillar → Cairo | La Défense → Paris | KV17 → Cairo | Hagia Sophia → Ankara | Bad Grund → Berlin | Basilica of Candelaria → Madrid | Petershagen → Berlin || **Final:** Postojna Cave → Ljubljana

- **Query 731 — Context:** Homberg (Ohm) → Berlin | KV14 → Cairo | Mammoth Cave National Park → Washington, D.C. | Getty Villa → Washington, D.C. | Nemrut → Ankara | Windsor Castle → London | Monument to the Sun → Zagreb | Château de Malmaison → Paris | Giant&#x27;s Causeway → London | Kimbell Art Museum → Washington, D.C. || **Final:** Mausoleum of Galla Placidia → Rome

- **Query 732 — Context:** Angel Falls → Caracas | Bad Vöslau → Vienna | Mount Longonot → Nairobi | Millennium of Russia → Moscow | Tivoli Gardens → Copenhagen | Marble Palace → Moscow | Vadstena Castle → Stockholm | Mount Sanqing → Beijing | Disney&#x27;s Hollywood Studios → Washington, D.C. | Hypogeum of Ħal Saflieni → Valletta || **Final:** Bad Karlshafen → Berlin

- **Query 734 — Context:** Shanhai Pass → Beijing | Peter and Paul Fortress → Moscow | Wild Wadi Water Park → Abu Dhabi | Lake Powell → Washington, D.C. | Louisiana Museum of Modern Art → Copenhagen | Universal Studios Japan → Tokyo | Ushiku Daibutsu → Tokyo | Bodrum Castle → Ankara | Walt Disney World Resort → Washington, D.C. | Thien Duong Cave → Hanoi || **Final:** Feldherrnhalle → Berlin

- **Query 746 — Context:** Buckingham Palace → London | Wallace Monument → London | Aqueduct of Segovia → Madrid | Bad Karlshafen → Berlin | German Federal Archives → Berlin | Blieskastel → Berlin | Oberstdorf → Berlin | Museum of Modern Art of Republika Srpska → Sarajevo | Sirius Arena → Moscow | Korela Fortress → Moscow || **Final:** Galleria Borghese → Rome

- **Query 748 — Context:** 30 St Mary Axe → London | Aiguille du Midi → Paris | Tomb of Hafez → Tehran | Las Vegas Strip → Washington, D.C. | Călimănești → Bucharest | Hiroshima Peace Memorial → Tokyo | Burj Khalifa → Abu Dhabi | Cleveland Museum of Art → Washington, D.C. | Euthanasia Coaster → London | Pera Museum → Ankara || **Final:** Bad Wilsnack → Berlin

- **Query 759 — Context:** KV7 → Cairo | Guédelon Castle → Paris | Lake Tuz → Ankara | Classical Gardens of Suzhou → Beijing | Nikkō Tōshō-gū → Tokyo | Hong Kong Museum of Art → Beijing | Mount Song → Beijing | Akbar&#x27;s Tomb → New Delhi | Walt Disney Studios → Washington, D.C. | Arches National Park → Washington, D.C. || **Final:** Dierhagen → Berlin

- **Query 760 — Context:** Aalen → Berlin | Santa Claus Village → Helsinki | Willis Tower → Washington, D.C. | Museo dell&#x27;Opera del Duomo → Rome | Shrine of Bahá&#x27;u&#x27;lláh → Jerusalem | Jaén Cathedral → Madrid | Friedrichskoog → Berlin | Luxor → Cairo | Drottningholm Palace → Stockholm | Glastonbury Tor → London || **Final:** Piskaryovskoye Memorial Cemetery → Moscow

- **Query 764 — Context:** Lion Monument Lucerne → Bern | Basilica of Our Lady of the Pillar → Madrid | Marble Arch → London | Bad Kleinkirchheim → Vienna | Lion of Belfort → Paris | Menshikov Palace (Saint Petersburg) → Moscow | Aqueduct of Valens → Ankara | West Bali National Park → Jakarta | Alcázar of Toledo → Madrid | Aiguille du Midi → Paris || **Final:** Schwerin Castle → Berlin

- **Query 767 — Context:** Canyon de Chelly National Monument → Washington, D.C. | Osmangazi Bridge → Ankara | Polanica-Zdrój → Warsaw | Graceland → Washington, D.C. | Topkapı Palace → Ankara | Dadiani Palaces Museum → Tbilisi | Valle dei Templi → Rome | Yıldız Palace → Ankara | Sukur → Abuja | Falkirk Wheel → London || **Final:** Bad Heilbrunn → Berlin

- **Query 771 — Context:** Machu Picchu → Lima | Kailasa Temple, Ellora → New Delhi | Little Hagia Sophia → Ankara | KV19 → Cairo | Fujian Tulou → Beijing | Mazar-e-Quaid → Islamabad | Niagara Falls → Ottawa | Tomb of Askia → Bamako | Grande Arche → Paris | Copenhagen Zoo → Copenhagen || **Final:** Büsum → Berlin

- **Query 773 — Context:** Bad Füssing → Berlin | Los Angeles County Museum of Art → Washington, D.C. | Leshan Giant Buddha → Beijing | Mount Kilimanjaro → Dodoma | Cumalıkızık → Ankara | Menshikov Palace (Saint Petersburg) → Moscow | Kazimierz → Warsaw | The Stone of Million → Ankara | Verona Arena → Rome | Heilbad Heiligenstadt → Berlin || **Final:** Vjetrenica → Sarajevo

- **Query 775 — Context:** Vistula Lagoon → Moscow | Bad Oeynhausen → Berlin | St. Mary&#x27;s Basilica in Gdańsk → Warsaw | Summer Garden → Moscow | Wuyi Mountains → Beijing | Novocherkassk Cathedral → Moscow | Badajoz Cathedral → Madrid | Frasassi Caves → Rome | Marktschellenberg → Berlin | Royal Museum for Central Africa → City of Brussels || **Final:** KV17 → Cairo

- **Query 776 — Context:** Dervio → Rome | Pyramid of Userkaf → Cairo | Tokyo Disneyland → Tokyo | Potala Palace → Beijing | Coves del Drach → Madrid | Amber Mountain National Park → Antananarivo | Ancient Theatre of Epidaurus → Athens | Soluntum → Rome | Arch of Trajan → Rome | Salar Jung Museum → New Delhi || **Final:** Altenberg → Berlin

- **Query 778 — Context:** Kizhi Pogost → Moscow | Topkapı Palace → Ankara | Kraków Barbican → Warsaw | Magic Kingdom → Washington, D.C. | Tokyo Disneyland → Tokyo | Holy Trinity Column in Olomouc → Prague | Koporye → Moscow | Marble Palace → Moscow | West Lake → Beijing | Bad Tennstedt → Berlin || **Final:** Mycenae → Athens

- **Query 783 — Context:** Bad Kreuznach → Berlin | Isny im Allgäu → Berlin | Naqsh-e Jahan Square → Tehran | Rök Runestone → Stockholm | Christ the Redeemer → Brasília | KV14 → Cairo | Villa Romana del Casale → Rome | Bad Hönningen → Berlin | Kykkos Monastery → Nicosia | Yumen Pass → Beijing || **Final:** Font-de-Gaume → Paris

- **Query 785 — Context:** Mariánské Lázně → Prague | Aulendorf → Berlin | Yıldız Hamidi Mosque → Ankara | Stadium MK → London | Bad Vöslau → Vienna | Yellowstone National Park → Washington, D.C. | Tomb of Absalom → Jerusalem | Schwerin Castle → Berlin | Accademia Carrara → Rome | Neue Pinakothek → Berlin || **Final:** Goa Gajah → Jakarta

- **Query 787 — Context:** Vigeland installation → Oslo | Tian Tan Buddha → Beijing | Topkapı Palace → Ankara | Portman Road → London | Orvieto Cathedral → Rome | Parc Astérix → Paris | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing | KV7 → Cairo | Fujian Tulou → Beijing | Vjetrenica → Sarajevo || **Final:** Blieskastel → Berlin

- **Query 791 — Context:** Sultan Ahmed Mosque → Ankara | Valaam Monastery → Moscow | Neuschwanstein Castle → Berlin | Aiguille du Midi → Paris | Mount Sanqing → Beijing | Beylerbeyi Palace → Ankara | Archaeological Museum of Thessaloniki → Athens | Deidesheim → Berlin | Bad Segeberg → Berlin | Ortaköy Mosque → Ankara || **Final:** Kraków-Płaszów concentration camp → Warsaw

- **Query 794 — Context:** Carisbrooke Castle → London | Hypogeum of Ħal Saflieni → Valletta | Polanica-Zdrój → Warsaw | Gammelstad Church Town → Stockholm | Shah Mosque → Tehran | Bacho Kiro cave → Sofia | Antelope Canyon → Washington, D.C. | Cathedral Basilica of St. Ann → Madrid | Mauritshuis → Amsterdam | Van Gogh Museum → Amsterdam || **Final:** Bad Blankenburg → Berlin

- **Query 805 — Context:** Vindolanda → London | Puente Nuevo → Madrid | Luxor Museum → Cairo | Kröller-Müller Museum → Amsterdam | Avtovo → Moscow | Fatih Sultan Mehmet Bridge → Ankara | Mauritshuis → Amsterdam | Louisiana Museum of Modern Art → Copenhagen | Miniatürk → Ankara | Puy de Dôme → Paris || **Final:** Nürburg → Berlin

- **Query 807 — Context:** Umedalens Skulpturpark → Stockholm | Museo dell&#x27;Opera del Duomo → Rome | National Portrait Gallery → London | Naples National Archaeological Museum → Rome | Doge&#x27;s Palace → Rome | Everglades National Park → Washington, D.C. | Novate Mezzola → Rome | Maes Howe → London | Millau Viaduct → Paris | Archaeological Museum of Thessaloniki → Athens || **Final:** Bad Friedrichshall → Berlin

- **Query 808 — Context:** Bad Breisig → Berlin | Ahrenshoop → Berlin | Macau Tower → Beijing | Manderscheid → Berlin | Machu Picchu → Lima | Royal Pavilion &amp; Garden → London | Admont Abbey → Vienna | Blagaj, Mostar → Sarajevo | Cave of El Castillo → Madrid | Kunstkamera → Moscow || **Final:** Galapagos Islands → Quito

- **Query 810 — Context:** Königsberg Cathedral → Moscow | Coit Tower → Washington, D.C. | Fingal&#x27;s Cave → London | Lake Powell → Washington, D.C. | Damavand → Tehran | Nordstrand → Berlin | German Federal Archives → Berlin | Schömberg → Berlin | Kungur Ice Cave → Moscow | Bad Münder am Deister → Berlin || **Final:** Sukiennice → Warsaw

- **Query 812 — Context:** Nestorian Stele → Beijing | Hong Kong Disneyland → Beijing | Mausoleum of Theodoric → Rome | Langeoog → Berlin | Blankenburg → Berlin | Badenweiler → Berlin | Heringsdorf → Berlin | Royal Pavilion &amp; Garden → London | Zaanse Schans → Amsterdam | Park Güell → Madrid || **Final:** Grand Egyptian Museum → Cairo

- **Query 813 — Context:** National Museum of Pakistan → Islamabad | St. Paul&#x27;s Church, Frankfurt am Main → Berlin | Galata Tower → Ankara | Fallingwater → Washington, D.C. | Bad Berka → Berlin | Lake Retba → Dakar | Blagaj, Mostar → Sarajevo | Mesha Stele → Amman | Vijećnica → Sarajevo | Wat Arun → Bangkok || **Final:** Jastrzębie-Zdrój → Warsaw

- **Query 814 — Context:** Conventico Caves → Madrid | Gonbad-e Qabus → Tehran | Amalienborg → Copenhagen | Pombia Safari Park → Rome | Bernkastel-Kues → Berlin | Little Hagia Sophia → Ankara | Spice Bazaar → Ankara | Treasury of Atreus → Athens | Natzweiler-Struthof concentration camp → Paris | Tomb of Caecilia Metella → Rome || **Final:** Vadstena Castle → Stockholm

- **Query 818 — Context:** Dadiani Palaces Museum → Tbilisi | Children&#x27;s Peace Monument → Tokyo | Wawel → Warsaw | Newgrange → Dublin | Great Smoky Mountains → Washington, D.C. | Our Lady of the Pillar → Madrid | Mausoleum of Theodoric → Rome | Bad Dürkheim → Berlin | The Nelson-Atkins Museum of Art → Washington, D.C. | Kimbell Art Museum → Washington, D.C. || **Final:** Louisiana Museum of Modern Art → Copenhagen

- **Query 819 — Context:** National Library of Australia → Canberra | Mole Antonelliana → Rome | Royal Palace of Milan → Rome | Westerbork Transit Camp → Amsterdam | Marine Corps War Memorial → Washington, D.C. | Basilica of Saint Nicholas → Rome | Segesta → Rome | Mammoth Cave National Park → Washington, D.C. | Dallas Museum of Art → Washington, D.C. | Forest of the Martyrs → Jerusalem || **Final:** Bad Bevensen → Berlin

- **Query 820 — Context:** Ain Dubai → Abu Dhabi | Stonehenge → London | Church of All Saints → Moscow | Tokyo Disneyland → Tokyo | Leeds Castle → London | Cappadocia → Ankara | Villa Tugendhat → Prague | Uludağ → Ankara | Hospital of Innocents → Rome | KV18 → Cairo || **Final:** Wissen → Berlin

- **Query 821 — Context:** Metropolitan Cathedral Basilica of the Holy Saviour, Oviedo → Madrid | Kensington Palace → London | Famine Stela → Cairo | Petralona cave → Athens | Czocha Castle → Warsaw | Škocjan Caves → Ljubljana | Wallace Monument → London | Euthanasia Coaster → London | Palazzo Barberini → Rome | Mecca → Riyadh || **Final:** German Federal Archives → Berlin

- **Query 827 — Context:** Masserberg → Berlin | Sontra → Berlin | Heiligendamm → Berlin | Märcani Mosque → Moscow | Gonbad-e Qabus → Tehran | Bad Schwartau → Berlin | DeviantArt → Washington, D.C. | Euromast → Amsterdam | West Lake → Beijing | Timmendorfer Strand → Berlin || **Final:** Orkhon inscriptions → Ulaanbaatar

- **Query 828 — Context:** Buddha Park → Vientiane | Mariinsky Theatre → Moscow | Kraków Barbican → Warsaw | Hohwacht → Berlin | Kronberg im Taunus → Berlin | Murcia&#x27;s Cathedral → Madrid | Lublin-Majdanek concentration camp → Warsaw | Vadstena Castle → Stockholm | Grand Canal → Rome | Royal Pavilion &amp; Garden → London || **Final:** Obelisk of Axum → Addis Ababa

- **Query 832 — Context:** Spice Bazaar → Ankara | Sukur → Abuja | Carrauntoohil → Dublin | Naxos → Rome | Dikteon Andron → Athens | Băile Herculane → Bucharest | Nemrut → Ankara | Bad Oeynhausen → Berlin | Pingyao → Beijing | Jaraba → Madrid || **Final:** Canadian Museum of History → Ottawa

- **Query 836 — Context:** Gaztelugatxe → Madrid | Dervio → Rome | Ballabio → Rome | Bad Bramstedt → Berlin | Ain Dubai → Abu Dhabi | Milan Cathedral → Rome | Laykyun Sekkya → Naypyidaw | Nordic Museum → Stockholm | Bad Essen → Berlin | Zuma Rock → Abuja || **Final:** Rundetaarn → Copenhagen

- **Query 846 — Context:** Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Bad Grund → Berlin | German Wine Route → Berlin | The Cloisters → Washington, D.C. | Homberg (Ohm) → Berlin | Juist → Berlin | Patriarchate of Peja → Belgrade | Colosseum → Rome | Casa Loma → Ottawa | City of Space → Paris || **Final:** Kalmar Cathedral → Stockholm

- **Query 850 — Context:** Colosseum → Rome | BMW Welt → Berlin | Ramoji Film City → New Delhi | Freiburg im Breisgau → Berlin | Christ the Redeemer → Brasília | Design Museum Holon → Jerusalem | Rothenburg ob der Tauber → Berlin | Urquhart Castle → London | Conventico Caves → Madrid | Chehel Sotun → Tehran || **Final:** Läckö Castle → Stockholm

- **Query 854 — Context:** Santa Claus Village → Helsinki | Sandanski → Sofia | Friedrichskoog → Berlin | Bad Camberg → Berlin | Kresty Prison → Moscow | Cathedral of La Laguna → Madrid | Norderney → Berlin | Schönwald im Schwarzwald → Berlin | Royal Pavilion &amp; Garden → London | Ehlscheid → Berlin || **Final:** Knowth → Dublin

- **Query 864 — Context:** Uppsala Cathedral → Stockholm | Roman Baths → London | Disney Adventure World → Paris | Rumelihisarı → Ankara | Tomb of Hafez → Tehran | National Library of Wales → London | Sorico → Rome | Neuharlingersiel → Berlin | Baltrum → Berlin | Archaeological Museum of Thessaloniki → Athens || **Final:** Śniardwy → Warsaw

- **Query 871 — Context:** Cueva de los Verdes → Madrid | Thien Duong Cave → Hanoi | Riddarholm Church → Stockholm | Tamme-Lauri oak → Tallinn | Taq-i Kisra → Baghdad | Pombia Safari Park → Rome | Kreuth → Berlin | KV19 → Cairo | German Wine Route → Berlin | Muzeum Miniaturowej Sztuki Profesjonalnej Henryk Jan Dominiak in Tychy → Warsaw || **Final:** The Little Mermaid → Copenhagen

- **Query 874 — Context:** Novocherkassk Cathedral → Moscow | Gammelstad Church Town → Stockholm | Palazzo Ducale Mantua → Rome | Segovia Cathedral → Madrid | Tropaeum Alpium → Paris | Empire State Building → Washington, D.C. | Frasassi Caves → Rome | Heraklion Archaeological Museum → Athens | türbe → Constantinople | Willis Tower → Washington, D.C. || **Final:** Bad Arolsen → Berlin

- **Query 879 — Context:** Nuruosmaniye Mosque → Ankara | Chehel Sotun → Tehran | Statue of Liberty → Washington, D.C. | Queen&#x27;s House → London | Majuli → New Delhi | The Stone of Million → Ankara | Vistula Lagoon → Moscow | Tatranská Lomnica → Bratislava | Thien Duong Cave → Hanoi | Woburn Abbey → London || **Final:** Bad Berleburg → Berlin

- **Query 880 — Context:** Sinan Pasha Mosque → Prishtina | Lublin-Majdanek concentration camp → Warsaw | Doge&#x27;s Palace, Genoa → Rome | Cave of Swallows → Mexico City | Tokyo DisneySea → Tokyo | Jingpo Lake → Beijing | Brooklyn Museum → Washington, D.C. | Bad Neustadt an der Saale → Berlin | Poulnabrone dolmen → Dublin | Heringsdorf → Berlin || **Final:** Cathedral of Zamora → Madrid

- **Query 888 — Context:** Nilgiri Mountain Railway → New Delhi | Astrid Lindgren&#x27;s World → Stockholm | City of Arts and Sciences → Madrid | Tian Tan Buddha → Beijing | Portman Road → London | Glasgow Cathedral → London | Gonio → Tbilisi | Susa → Tehran | Ellis Island → Washington, D.C. | Sammallahdenmäki → Helsinki || **Final:** Bad Bodenteich → Berlin

- **Query 895 — Context:** Kröller-Müller Museum → Amsterdam | KV26 → Cairo | Castello Estense → Rome | Maya Ruins of Tulum → Mexico City | Vjetrenica → Sarajevo | Jastrzębie-Zdrój → Warsaw | Classical Gardens of Suzhou → Beijing | Trinity Cathedral → Moscow | British Library → London | Tropaeum Alpium → Paris || **Final:** Bad Sachsa → Berlin

- **Query 897 — Context:** The Little Mermaid → Copenhagen | German Wine Route → Berlin | Bronze Horseman → Moscow | Luxor Museum → Cairo | Ourense Cathedral → Madrid | Everglades National Park → Washington, D.C. | Museo Poldi Pezzoli → Rome | Izium mass graves → Kyiv | Koporye → Moscow | Blagaj, Mostar → Sarajevo || **Final:** Damavand → Tehran

- **Query 899 — Context:** Spring Temple Buddha → Beijing | Tabriz Bazaar → Tehran | Yuste → Madrid | Big Sur → Washington, D.C. | Kneiff → Luxembourg | The Museum of Innocence → Ankara | Sümela Monastery → Ankara | Groeningemuseum → City of Brussels | Urquhart Castle → London | KV18 → Cairo || **Final:** Heiligenhafen → Berlin

- **Query 900 — Context:** Château de Montsoreau → Paris | Homberg (Ohm) → Berlin | Luxor → Cairo | Jedlina-Zdrój → Warsaw | Tian Tan Buddha → Beijing | Glasgow Cathedral → London | KV34 → Cairo | Bad Laasphe → Berlin | Bad Liebenzell → Berlin | Călimănești → Bucharest || **Final:** Mnajdra → Valletta

- **Query 903 — Context:** Solovetsky Monastery → Moscow | The Little Mermaid → Copenhagen | Jastrzębie-Zdrój → Warsaw | KV26 → Cairo | Serdobsk → Moscow | Homomonument → Amsterdam | Vadstena Castle → Stockholm | Kalmar Cathedral → Stockholm | Uffizi Gallery → Rome | Stonehenge → London || **Final:** Bischofswiesen → Berlin

- **Query 909 — Context:** Royal Academy of Arts → London | Field of Mars → Moscow | Cueva de las Manos → Buenos Aires | Zuma Rock → Abuja | Osun-Osogbo Grove → Abuja | Galleria Borghese → Rome | Swiss Alps → Bern | Skull Tower → Belgrade | Raj Ghat and associated memorials → New Delhi | Promenade des Anglais → Paris || **Final:** Heligoland → Berlin

- **Query 910 — Context:** Hollywood Walk of Fame → Washington, D.C. | Hadrian&#x27;s Wall → London | Wat Arun → Bangkok | Düden Waterfalls → Ankara | Cathedral Basilica of St. Ann → Madrid | Silesian Stadium → Warsaw | Choragic Monument of Lysicrates → Athens | Qiandao Lake → Beijing | Hoover Dam → Washington, D.C. | Odesa Fine Arts Museum → Kyiv || **Final:** Mausoleum of Khoja Ahmed Yasawi → Astana

- **Query 916 — Context:** Royal Armoury → Stockholm | Gur-e Amir → Tashkent | Bad Gastein → Vienna | Lascaux → Paris | St Mark&#x27;s Clocktower → Rome | Stirling Castle → London | Wawel Cathedral → Warsaw | The Motherland Calls → Moscow | Masuleh → Tehran | St. Nicholas Naval Cathedral, St. Petersburg → Moscow || **Final:** Bad Kreuznach → Berlin

- **Query 921 — Context:** Tanah Lot → Jakarta | Zaanse Schans → Amsterdam | Aljafería → Madrid | Carrauntoohil → Dublin | Bodrum Castle → Ankara | Arlington National Cemetery → Washington, D.C. | Solovetsky Monastery → Moscow | Ħaġar Qim → Valletta | Domica → Bratislava | Kelvingrove Art Gallery and Museum → London || **Final:** German Wine Route → Berlin

- **Query 926 — Context:** Neue Pinakothek → Berlin | Koporye → Moscow | Călimănești → Bucharest | Korela Fortress → Moscow | KV20 → Cairo | Hampton Court Palace → London | Fitzwilliam Museum → London | Hoover Dam → Washington, D.C. | Mount Tai → Beijing | Qiandao Lake → Beijing || **Final:** Anne Frank House → Amsterdam

- **Query 928 — Context:** Tabernas Desert → Madrid | Metropolitan Museum of Art → Washington, D.C. | Bad Bocklet → Berlin | Alcatraz Island → Washington, D.C. | Tierradentro → Bogotá | İzmir Clock Tower → Ankara | Downing Street → London | Saint Sophia Cathedral → Moscow | Düden Waterfalls → Ankara | Al-Masjid Al-Haram → Riyadh || **Final:** Abbadia Lariana → Rome

- **Query 930 — Context:** Alaçatı → Ankara | Blue Mosque → Kabul | Sequoia National Park → Washington, D.C. | Pickford&#x27;s House → London | Herbstein → Berlin | Champaner-Pavagadh Archaeological Park → New Delhi | 30 St Mary Axe → London | Bellano → Rome | Ny Carlsberg Glyptotek → Copenhagen | Jemaa el-Fnaa → Rabat || **Final:** Kumu → Tallinn

- **Query 932 — Context:** Kimbell Art Museum → Washington, D.C. | KV14 → Cairo | Le Gua → Paris | Cathedral of Saint Demetrius → Moscow | Metropolitan Museum of Art → Washington, D.C. | Albert Memorial → London | Jaraba → Madrid | Miniatürk → Ankara | Efteling → Amsterdam | Cathedral Basilica of the Virgin of Incarnation → Madrid || **Final:** Bad Berka → Berlin

- **Query 933 — Context:** Tate Modern → London | Vistula Lagoon → Moscow | Big Ben → London | Süleymaniye Mosque → Ankara | Scharinska villa → Stockholm | KV7 → Cairo | National Portrait Gallery → London | Mesha Stele → Amman | Newgrounds → Washington, D.C. | Obelisk of Theodosius → Ankara || **Final:** Niedenstein → Berlin

- **Query 935 — Context:** Carnuntum → Vienna | Cascata delle Marmore → Rome | Rüstem Pasha Mosque → Ankara | Mount Jiuhua → Beijing | İstanbul Modern → Ankara | Galapagos Islands → Quito | Dallas Museum of Art → Washington, D.C. | Kneiff → Luxembourg | Latin Bridge → Sarajevo | Bronze Horseman → Moscow || **Final:** Gripsholm Castle → Stockholm

- **Query 950 — Context:** Natzweiler-Struthof concentration camp → Paris | Bad Oeynhausen → Berlin | Bad Dürkheim → Berlin | La Défense → Paris | Bad Sassendorf → Berlin | Rundetaarn → Copenhagen | Bad Salzuflen → Berlin | Ortaköy → Ankara | Mount Vernon → Washington, D.C. | Maya Ruins of Tulum → Mexico City || **Final:** MAXXI → Rome

- **Query 951 — Context:** Cologne Cathedral → Berlin | Rüstem Pasha Mosque → Ankara | Thracian Tomb of Sveshtari → Sofia | Weilburg → Berlin | Segesta → Rome | Cliffs of Moher → Dublin | Szczawnica → Warsaw | National Gallery of Norway → Oslo | Ytterby mine → Stockholm | Waldbronn → Berlin || **Final:** Efteling → Amsterdam

- **Query 954 — Context:** Bad Rothenfelde → Berlin | Admont Abbey → Vienna | Bad Bocklet → Berlin | Bad Saarow → Berlin | Pont du Gard → Paris | KV6 → Cairo | Istanbul Archaeology Museums → Ankara | Ca&#x27; d&#x27;Oro → Rome | Rialto Bridge → Rome | Lombard Street → Washington, D.C. || **Final:** Khaju Bridge → Tehran

- **Query 958 — Context:** Bridge of Sighs → Rome | Sirius Arena → Moscow | Daun → Berlin | Pingyao → Beijing | Bad Griesbach im Rottal → Berlin | Seikilos epitaph → Athens | Galata Bridge → Ankara | Mount Kumgang Tourist Region → Pyongyang | Torre del Oro → Madrid | Shrine of Bahá&#x27;u&#x27;lláh → Jerusalem || **Final:** Racławice Panorama → Warsaw

- **Query 961 — Context:** Osun-Osogbo Grove → Abuja | Ninth Fort → Vilnius | Obelisk of Axum → Addis Ababa | Bargello National Museum → Rome | Serpentine Galleries → London | Tate Modern → London | Yumen Pass → Beijing | Laykyun Sekkya → Naypyidaw | Ca&#x27; Rezzonico → Rome | Mausoleum of Maussollos → Ankara || **Final:** Homberg (Ohm) → Berlin

- **Query 962 — Context:** Fatima Masumeh Shrine → Tehran | Forest of the Martyrs → Jerusalem | Neukirchen → Berlin | Blagaj, Mostar → Sarajevo | Isny im Allgäu → Berlin | Leeds Castle → London | Lombard Street → Washington, D.C. | Museum of Far Eastern Antiquities → Stockholm | Chatsworth House → London | Detroit Institute of Arts → Washington, D.C. || **Final:** Lion of Belfort → Paris

- **Query 967 — Context:** Lombard Street → Washington, D.C. | Vistula Lagoon → Moscow | Bad Bergzabern → Berlin | Mobility Resort Motegi → Tokyo | Persepolis → Tehran | Six Flags Magic Mountain → Washington, D.C. | Nördlingen → Berlin | Imam Reza Shrine → Tehran | Accademia Carrara → Rome | Big Ben → London || **Final:** Luxor Museum → Cairo

- **Query 972 — Context:** Kalmar Cathedral → Stockholm | Freiburg im Breisgau → Berlin | Rabka-Zdrój → Warsaw | Prophet&#x27;s Mosque → Riyadh | Schluchsee → Berlin | Tel Aviv Museum of Art → Jerusalem | Romantic Road → Berlin | Mount Lu → Beijing | St. Blasien → Berlin | Naxos → Rome || **Final:** Holy Trinity Column in Olomouc → Prague

- **Query 974 — Context:** Bad Elster → Berlin | Fatima Masumeh Shrine → Tehran | Nelson&#x27;s Column → London | Disneyland Paris → Paris | Tabriz Bazaar → Tehran | Tokyo Disney Resort → Tokyo | Norton Simon Museum → Washington, D.C. | Space Needle → Washington, D.C. | Gallerie dell&#x27;Accademia → Rome | Pamplona Cathedral → Madrid || **Final:** Wat Arun → Bangkok

- **Query 977 — Context:** Las Vegas Strip → Washington, D.C. | Church of the Savior on Blood → Moscow | Uzungöl → Ankara | Sayyidah Zaynab Mosque → Damascus | Mesha Stele → Amman | Nuruosmaniye Mosque → Ankara | Hoover Dam → Washington, D.C. | Palais des Papes → Paris | Veliky Ustyug → Moscow | Everland → Seoul || **Final:** Bad Wildungen → Berlin

- **Query 980 — Context:** Carisbrooke Castle → London | Basilica of Our Lady of the Pillar → Madrid | Fingal&#x27;s Cave → London | Bad Laer → Berlin | Philopappos Monument → Athens | Weiskirchen → Berlin | St Mark&#x27;s Basilica → Rome | Malbork Castle → Warsaw | Pura Luhur → Jakarta | Oscar Niemeyer International Cultural Centre → Madrid || **Final:** Grossglockner High Alpine Road → Vienna

- **Query 985 — Context:** Castello Estense → Rome | Georgia Guidestones → Washington, D.C. | Bad Füssing → Berlin | Wangerooge → Berlin | Segesta → Rome | Denver Art Museum → Washington, D.C. | Rengsdorf → Berlin | Medici Chapels → Rome | Alcazaba y Murallas del Cerro de San Cristóbal → Madrid | Ani → Ankara || **Final:** Grūtas Park → Vilnius

- **Query 988 — Context:** Royal Academy of Arts → London | Pompey&#x27;s Pillar → Cairo | Linköping Cathedral → Stockholm | Al-Masjid Al-Haram → Riyadh | Roman Walls of Lugo → Madrid | Bavarian National Museum → Berlin | Kelvingrove Art Gallery and Museum → London | Bad Homburg vor der Höhe → Berlin | Château de Montsoreau → Paris | Sankt Peter-Ording → Berlin || **Final:** Canaima National Park → Caracas

- **Query 999 — Context:** Stockholm Palace → Stockholm | Grand Bazaar → Ankara | Ramsau bei Berchtesgaden → Berlin | Sankt Peter-Ording → Berlin | Bad Waldsee → Berlin | Bankya → Sofia | Puente Nuevo → Madrid | Mount Jiuhua → Beijing | Crazy Horse Memorial → Washington, D.C. | Detroit Institute of Arts → Washington, D.C. || **Final:** Kalka–Shimla Railway → New Delhi

- **Query 1003 — Context:** Sequoia National Park → Washington, D.C. | Lion of Judah → Addis Ababa | Narva Triumphal Arch → Moscow | Naples National Archaeological Museum → Rome | Latin Bridge → Sarajevo | Triumphal Arch of Orange → Paris | Marine Corps War Memorial → Washington, D.C. | Goa Gajah → Jakarta | Alamo Mission in San Antonio → Washington, D.C. | Basilica of Our Lady of the Pillar → Madrid || **Final:** Gladenbach → Berlin

- **Query 1004 — Context:** Glory&#x27;s Portico → Madrid | Vittskövle Church → Stockholm | Gröna Lund → Stockholm | Peggy Guggenheim Collection → Rome | Winchester Mystery House → Washington, D.C. | Sandringham House → London | Atherton Tableland → Canberra | Osmangazi Bridge → Ankara | Ain Dubai → Abu Dhabi | Vulci → Rome || **Final:** Wenningstedt-Braderup → Berlin

- **Query 1006 — Context:** Tian Tan Buddha → Beijing | Stromberg → Berlin | Treasury of Atreus → Athens | Tatranská Lomnica → Bratislava | Darjeeling Himalayan Railway → New Delhi | Acropolis of Athens → Athens | Veliky Ustyug → Moscow | Riddarholm Church → Stockholm | Museum of Fine Arts of Lyon → Paris | Bad Mergentheim → Berlin || **Final:** Călimănești → Bucharest

- **Query 1009 — Context:** Kalmar Cathedral → Stockholm | Cave of Swallows → Mexico City | Yuste → Madrid | Balatonfüred → Budapest | Museum of Fine Arts Ghent (MSK) → City of Brussels | Acropolis of Athens → Athens | Museu Picasso → Madrid | Lia Fáil → Dublin | National Museum in Wrocław → Warsaw | Portman Road → London || **Final:** Bad Breisig → Berlin

- **Query 1011 — Context:** Royal Museum for Central Africa → City of Brussels | Grand Canal → Rome | Pripyat amusement park → Kyiv | Euromast → Amsterdam | Park Güell → Madrid | Fort Sumter → Washington, D.C. | Charing Cross → London | Malbork Castle → Warsaw | Jaén Cathedral → Madrid | Hoover Dam → Washington, D.C. || **Final:** Bad Sülze → Berlin

- **Query 1012 — Context:** Juventus Stadium → Rome | Bad Brambach → Berlin | Panathenaic Stadium → Athens | The Frick Collection → Washington, D.C. | Buddhas of Bamiyan → Kabul | Schwerin Castle → Berlin | Şehzade Mosque → Ankara | Susa → Tehran | Meteor Crater → Washington, D.C. | Six Flags Magic Mountain → Washington, D.C. || **Final:** Buziaș → Bucharest

- **Query 1014 — Context:** Bad Vöslau → Vienna | Tower of Hercules → Madrid | Alcatraz Island → Washington, D.C. | Lublin-Majdanek concentration camp → Warsaw | The Nelson-Atkins Museum of Art → Washington, D.C. | KV11 → Cairo | Shah Mosque → Tehran | Marble Arch → London | The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. | Pennsylvania Academy of the Fine Arts → Washington, D.C. || **Final:** Bad Staffelstein → Berlin

- **Query 1015 — Context:** Buddha Park → Vientiane | Gröna Lund → Stockholm | Gatchina Palace → Moscow | National Gallery of Victoria → Canberra | Osmangazi Bridge → Ankara | Bad Salzschlirf → Berlin | Osborne House → London | Bad Iburg → Berlin | Nesebar → Sofia | Bad Wildbad → Berlin || **Final:** Băile Herculane → Bucharest

- **Query 1022 — Context:** Chillon Castle → Bern | Imbros → Ankara | Puente Nuevo → Madrid | Madinat Al-Zahra → Madrid | Mamayev Kurgan → Moscow | Hoover Dam → Washington, D.C. | Hearst Castle → Washington, D.C. | Truskavets → Kyiv | Son Doong Cave → Hanoi | Admiralty Arch → London || **Final:** Wasserburg → Berlin

- **Query 1023 — Context:** Museum of San Marco → Rome | Obelisk of Axum → Addis Ababa | Troldhaugen → Oslo | Acropolis of Athens → Athens | Saint Michael&#x27;s Castle → Moscow | Jasna Góra Monastery → Warsaw | Mausoleum of Theodoric → Rome | Buziaș → Bucharest | Lake Powell → Washington, D.C. | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing || **Final:** Bad Emstal → Berlin

- **Query 1027 — Context:** The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. | Sofiyivsky Park → Kyiv | Rock and Roll Hall of Fame → Washington, D.C. | Green Mosque → Kabul | Überlingen → Berlin | Gaztelugatxe → Madrid | Sublime Porte → Ankara | Federal Hall → Washington, D.C. | Gulangyu → Beijing | Cappadocia → Ankara || **Final:** Nesebar → Sofia

- **Query 1030 — Context:** Boltenhagen → Berlin | Nieheim → Berlin | Krynica-Zdrój → Warsaw | KV1 → Cairo | Pelion → Athens | The Little Mermaid → Copenhagen | Green Mosque → Kabul | Bletchley Park → London | Monastery of Saint John of Rila → Sofia | Nordic Museum → Stockholm || **Final:** iron pillar of Delhi → New Delhi

- **Query 1041 — Context:** Bad Schmiedeberg → Berlin | Ratzeburg → Berlin | Bad Camberg → Berlin | KV60 → Cairo | Vulci → Rome | Mobility Resort Motegi → Tokyo | National Library of Wales → London | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Bad Reichenhall → Berlin | Denver Art Museum → Washington, D.C. || **Final:** Tel Aviv Museum of Art → Jerusalem

- **Query 1045 — Context:** Palazzo Ducale Mantua → Rome | Morskie Oko → Warsaw | Fountains Abbey → London | Schönau am Königsee → Berlin | KV19 → Cairo | Chilean National Museum of Fine Arts → Santiago | Chelyabinsk Airport → Moscow | Golden Gate → Moscow | Mausoleum of Theodoric → Rome | Hearst Castle → Washington, D.C. || **Final:** Moderna Museet → Stockholm

- **Query 1050 — Context:** Hearst Castle → Washington, D.C. | Sankt Englmar → Berlin | The Little Mermaid → Copenhagen | Bad Vilbel → Berlin | Odesa Fine Arts Museum → Kyiv | Jingpo Lake → Beijing | Majuli → New Delhi | Willingen (Upland) → Berlin | Cappadocia → Ankara | Crazy Horse Memorial → Washington, D.C. || **Final:** Angel Falls → Caracas

- **Query 1051 — Context:** Anne Frank House → Amsterdam | Kimbell Art Museum → Washington, D.C. | Mammoth Cave National Park → Washington, D.C. | Graceland → Washington, D.C. | Dolmen of Menga → Madrid | Blackpool Tower → London | Zuma Rock → Abuja | Blue Mosque → Kabul | KV17 → Cairo | Bad Vöslau → Vienna || **Final:** Bad Nenndorf → Berlin

- **Query 1056 — Context:** Ramoji Film City → New Delhi | Sinan Pasha Mosque → Prishtina | India Gate → New Delhi | Riddarholm Church → Stockholm | Schotten → Berlin | Royal Palace of La Granja de San Ildefonso → Madrid | Louisiana Museum of Modern Art → Copenhagen | Kingda Ka → Washington, D.C. | Monastery of Saint John of Rila → Sofia | Ellis Island → Washington, D.C. || **Final:** Philopappos Monument → Athens

- **Query 1070 — Context:** Ca&#x27; d&#x27;Oro → Rome | Imam Husayn Mausoleum → Baghdad | Bad Rodach → Berlin | 30 St Mary Axe → London | Aqueduct of Valens → Ankara | Bad Bramstedt → Berlin | Glastonbury Tor → London | Metropolitan Museum of Art → Washington, D.C. | Bletchley Park → London | Panathenaic Stadium → Athens || **Final:** Skokloster Castle → Stockholm

- **Query 1073 — Context:** Amélie-les-Bains-Palalda → Paris | Besakih → Jakarta | Aalen → Berlin | Basilica of Saint Nicholas → Rome | Traben-Trarbach → Berlin | Summer Garden → Moscow | Sun Yat-sen Mausoleum → Beijing | Columbus Monument → Madrid | Yıldız Hamidi Mosque → Ankara | Vintgar Gorge → Ljubljana || **Final:** Troldhaugen → Oslo

- **Query 1081 — Context:** Denver Art Museum → Washington, D.C. | Rengsdorf → Berlin | Lia Fáil → Dublin | Tierradentro → Bogotá | Bad Salzdetfurth → Berlin | Cappadocia → Ankara | Basilica of Our Lady of the Pillar → Madrid | Naval Cathedral in Kronstadt → Moscow | Bad Teinach-Zavelstein → Berlin | Imagine Peace Tower → Reykjavík || **Final:** Busan → Seoul

- **Query 1083 — Context:** İstanbul Modern → Ankara | Bad Schwartau → Berlin | KV15 → Cairo | Bad Wilsnack → Berlin | Archaeological Museum of Thessaloniki → Athens | Glamis Castle → London | Space Needle → Washington, D.C. | Upper German-Raetian Limes → Berlin | Soltaniyeh Dome → Tehran | Liberty Bell → Washington, D.C. || **Final:** Sammallahdenmäki → Helsinki

- **Query 1084 — Context:** Korela Fortress → Moscow | Le Gua → Paris | Novocherkassk Cathedral → Moscow | Charminar → New Delhi | St Mark&#x27;s Clocktower → Rome | Bletchley Park → London | Dahme → Berlin | Falkirk Wheel → London | Château de Montsoreau-Museum of Contemporary Art → Paris | Marmurova Pechera → Kyiv || **Final:** Everland → Seoul

- **Query 1085 — Context:** Mecca → Riyadh | Ploshchad Vosstaniya → Moscow | New Athos Cave → Tbilisi | Harrods → London | Bursa Grand Mosque → Ankara | Mystery Play of Elche → Madrid | Ludlow Castle → London | Valaam Monastery → Moscow | Goa Gajah → Jakarta | The STRAT Hotel, Casino &amp; SkyPod → Washington, D.C. || **Final:** Bad Münstereifel → Berlin

- **Query 1086 — Context:** Art Gallery of New South Wales → Canberra | Mount Kumgang Tourist Region → Pyongyang | Uppsala Cathedral → Stockholm | Chełmno extermination camp → Warsaw | Grand Egyptian Museum → Cairo | Pura Luhur → Jakarta | Peggy Guggenheim Collection → Rome | Mausoleum of Khoja Ahmed Yasawi → Astana | Basilica of Notre-Dame de Fourvière → Paris | Millau Viaduct → Paris || **Final:** Waren → Berlin

- **Query 1090 — Context:** Wiesbaden → Berlin | Casa Vicens → Madrid | Schwerin Castle → Berlin | Antequera Dolmens Site → Madrid | Nesebar → Sofia | Burghley House → London | Summer Garden → Moscow | Ramoji Film City → New Delhi | Bad Laer → Berlin | Wings of Tatev → Yerevan || **Final:** Piešťany → Bratislava

- **Query 1103 — Context:** Luxor → Cairo | Bad Karlshafen → Berlin | Choragic Monument of Lysicrates → Athens | Ali Qapu → Tehran | Parc Astérix → Paris | Bad Brambach → Berlin | Arlington National Cemetery → Washington, D.C. | Alexander Column → Moscow | Bad Heilbrunn → Berlin | Vittskövle Church → Stockholm || **Final:** Colosseum → Rome

- **Query 1115 — Context:** Anichkov Bridge → Moscow | Monastery of Saint John of Rila → Sofia | Acropolis Museum → Athens | Dune of Pilat → Paris | Osborne House → London | Lake Powell → Washington, D.C. | Uzungöl → Ankara | Pompey&#x27;s Pillar → Cairo | Golden Gate Bridge → Washington, D.C. | Museum of San Marco → Rome || **Final:** Bad Wildbad → Berlin

- **Query 1123 — Context:** Acropolis of Athens → Athens | Obelisk of Axum → Addis Ababa | Juventus Stadium → Rome | Great Ocean Road → Canberra | Cleveland Museum of Art → Washington, D.C. | Museum of Far Eastern Antiquities → Stockholm | Polanica-Zdrój → Warsaw | Château de Montsoreau → Paris | Old Town of Lijiang → Beijing | Piccadilly Circus → London || **Final:** Bad Grund → Berlin

- **Query 1130 — Context:** Dervio → Rome | Cascata delle Marmore → Rome | São Paulo Museum of Art → Brasília | Conch Republic → Washington, D.C. | Mariánské Lázně → Prague | Jemaa el-Fnaa → Rabat | Bad Belzig → Berlin | Kizhi Pogost → Moscow | Amber Mountain National Park → Antananarivo | Garmisch-Partenkirchen → Berlin || **Final:** Tsūtenkaku → Tokyo

- **Query 1139 — Context:** Igel Column → Berlin | Korela Fortress → Moscow | Mevlâna Museum → Ankara | Trafalgar Square → London | Überlingen → Berlin | Ca&#x27; d&#x27;Oro → Rome | Wales Coast Path → London | Lake Van → Ankara | Font-de-Gaume → Paris | Alnwick Castle → London || **Final:** KV14 → Cairo

- **Query 1140 — Context:** Glastonbury Tor → London | Ca&#x27; Rezzonico → Rome | Divriği Great Mosque and Hospital → Ankara | Ladonia → Stockholm | Cliffs of Moher → Dublin | Shanhai Pass → Beijing | Galata Tower → Ankara | Universal Studios Japan → Tokyo | Yellowstone National Park → Washington, D.C. | Tate Modern → London || **Final:** Travemünde → Berlin

- **Query 1145 — Context:** Tomb of Cyrus the Great → Tehran | Arc de Triomf → Madrid | Bad Belzig → Berlin | Spiekeroog → Berlin | Piskaryovskoye Memorial Cemetery → Moscow | Scottish National Gallery → London | Yellowstone National Park → Washington, D.C. | Bodrum Castle → Ankara | Menshikov Palace (Saint Petersburg) → Moscow | Koporye → Moscow || **Final:** Museum of Modern Art of Republika Srpska → Sarajevo

- **Query 1157 — Context:** S.A.I. Catedral Metropolitana de la Encarnación → Madrid | Shanghai Disneyland Park → Beijing | Sümela Monastery → Ankara | Birka → Stockholm | Ale&#x27;s Stones → Stockholm | Morskie Oko → Warsaw | Rumelihisarı → Ankara | Monument Valley → Washington, D.C. | Glastonbury Tor → London | Palazzo Vecchio → Rome || **Final:** Großenbrode → Berlin

- **Query 1158 — Context:** Monument to the Great Fire of London → London | Heraklion Archaeological Museum → Athens | Mazar-e-Quaid → Islamabad | Vjetrenica → Sarajevo | Inveraray Castle → London | Six Flags Magic Mountain → Washington, D.C. | National Portrait Gallery → London | Great Geysir → Reykjavík | Peter and Paul Fortress → Moscow | Gardens of Bomarzo → Rome || **Final:** Bad Hindelang → Berlin

- **Query 1162 — Context:** İstiklal Avenue → Ankara | Ali Qapu → Tehran | Bad Feilnbach → Berlin | Urquhart Castle → London | Willingen (Upland) → Berlin | Umedalens Skulpturpark → Stockholm | Multnomah Falls → Washington, D.C. | Naval Cathedral in Kronstadt → Moscow | Czartoryski Museum → Warsaw | Newgrange → Dublin || **Final:** Stoa Poikile → Athens

- **Query 1168 — Context:** Skansen → Stockholm | Bad Münder am Deister → Berlin | Stirling Castle → London | Bad Mergentheim → Berlin | Megara Hyblaea → Rome | Ivolginsky Datsan → Moscow | Bad Arolsen → Berlin | Museo dell&#x27;Opera del Duomo → Rome | Van Gogh Museum → Amsterdam | Sankt Englmar → Berlin || **Final:** Kunsthaus Graz → Vienna

- **Query 1169 — Context:** Alexander Nevsky Cathedral → Warsaw | Empire State Building → Washington, D.C. | Archcathedral Basilica of St. Peter and St. Paul → Warsaw | Cologne Cathedral → Berlin | Acropolis of Athens → Athens | Tegernsee → Berlin | Shah Mosque → Tehran | Mauritshuis → Amsterdam | Neptune&#x27;s Grotto → Rome | Bad Brambach → Berlin || **Final:** Moskovsky railway station → Moscow

- **Query 1170 — Context:** Castello Estense → Rome | Jinggang Mountains → Beijing | Teylers Museum → Amsterdam | Pompey&#x27;s Pillar → Cairo | Hever Castle → London | Museo Poldi Pezzoli → Rome | Rosa Khutor Alpine Resort → Moscow | Aiguille du Midi → Paris | Tomb of Suleyman Shah → Damascus | Liseberg → Stockholm || **Final:** Bad Bramstedt → Berlin

- **Query 1172 — Context:** Zolotoy Rog → Moscow | Mangla Dam → Islamabad | Tarxien Temples → Valletta | Wangerooge → Berlin | Bad Rothenfelde → Berlin | Chehel Sotun → Tehran | Victoria and Albert Museum → London | KV14 → Cairo | Banya → Sofia | Mask of Sorrow → Moscow || **Final:** Galleria Nazionale d&#x27;Arte Moderna e Contemporanea di Roma → Rome

- **Query 1174 — Context:** Ponte Vecchio → Rome | Park Güell → Madrid | Waldbronn → Berlin | Borkum → Berlin | Bad Wiessee → Berlin | Chengde Mountain Resort and its outlying temples → Beijing | Las Médulas → Madrid | Topkapı Palace → Ankara | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Grande Arche → Paris || **Final:** Gröna Lund → Stockholm

- **Query 1175 — Context:** Kalka–Shimla Railway → New Delhi | Efteling → Amsterdam | Tomb of Jahangir → Islamabad | Mevlâna Museum → Ankara | New Mosque → Ankara | Tokyo DisneySea → Tokyo | Carnuntum → Vienna | Divriği Great Mosque and Hospital → Ankara | KV34 → Cairo | Peggy Guggenheim Collection → Rome || **Final:** Bad Neustadt an der Saale → Berlin

- **Query 1177 — Context:** Amber Mountain National Park → Antananarivo | Statue of Liberty → Washington, D.C. | Banya → Sofia | Bad Segeberg → Berlin | Tower of London → London | Bad Bayersoien → Berlin | Ellis Island → Washington, D.C. | Bad Nauheim → Berlin | Niterói Contemporary Art Museum → Brasília | Fallingwater → Washington, D.C. || **Final:** Royal Palace of La Granja de San Ildefonso → Madrid

- **Query 1183 — Context:** Tivoli Gardens → Copenhagen | Yellowstone National Park → Washington, D.C. | Kew Palace → London | Uzungöl → Ankara | Grand Egyptian Museum → Cairo | West Bali National Park → Jakarta | Stirling Castle → London | Piccadilly Circus → London | Lion Monument Lucerne → Bern | KV11 → Cairo || **Final:** Gernsbach → Berlin

- **Query 1185 — Context:** Bad Reichenhall → Berlin | Smrdáky → Bratislava | Zhouzhuang Town → Beijing | Tropical Islands → Berlin | Gripsholm Castle → Stockholm | Gatchina Palace → Moscow | Design Museum Holon → Jerusalem | Baths of Caracalla → Rome | Radolfzell am Bodensee → Berlin | Omonoia Square → Athens || **Final:** Rabka-Zdrój → Warsaw

- **Query 1187 — Context:** Munch Museum → Oslo | Badajoz Cathedral → Madrid | Saadiyat Island → Abu Dhabi | Moskovsky railway station → Moscow | Hollywood Sign → Washington, D.C. | Drottningholm Palace → Stockholm | Buckingham Palace → London | Hong Kong Museum of Art → Beijing | Gaztelugatxe → Madrid | Lion of Judah → Addis Ababa || **Final:** Bad Essen → Berlin

- **Query 1191 — Context:** Nikkō Tōshō-gū → Tokyo | Gdańsk Main Town Hall → Warsaw | Garmisch-Partenkirchen → Berlin | Bad Bayersoien → Berlin | Mount Song → Beijing | St. Nicholas Naval Cathedral, St. Petersburg → Moscow | Stockholm City Hall → Stockholm | Milwaukee Art Museum → Washington, D.C. | KV8 → Cairo | Ħaġar Qim → Valletta || **Final:** Ancient Theatre of Epidaurus → Athens

- **Query 1195 — Context:** Multnomah Falls → Washington, D.C. | Bursa Grand Mosque → Ankara | Atherton Tableland → Canberra | Sydney Opera House → Canberra | Monument to the Great Fire of London → London | Westerbork Transit Camp → Amsterdam | KV35 → Cairo | Famine Stela → Cairo | Prophet&#x27;s Mosque → Riyadh | Hollywood Walk of Fame → Washington, D.C. || **Final:** Thracian Tomb of Sveshtari → Sofia

- **Query 1197 — Context:** Canyon de Chelly National Monument → Washington, D.C. | Waren → Berlin | Kreuth → Berlin | Mycenae → Athens | Oberstdorf → Berlin | National Museum in Kraków → Warsaw | Little Hagia Sophia → Ankara | Zuma Rock → Abuja | Fujian Tulou → Beijing | Mazar-e-Quaid → Islamabad || **Final:** Ha Long Bay → Hanoi

- **Query 1201 — Context:** Maes Howe → London | Imam Husayn Mausoleum → Baghdad | Blenheim Palace → London | Millau Viaduct → Paris | Ölüdeniz → Ankara | Tomb of Safdar Jang → New Delhi | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Musée Fabre → Paris | Tierradentro → Bogotá | Stockholm Palace → Stockholm || **Final:** Bad Langensalza → Berlin

- **Query 1213 — Context:** Qazan Kremlin → Moscow | Lake Retba → Dakar | Grand Canal → Rome | Fitzwilliam Museum → London | Museum of Fine Arts Ghent (MSK) → City of Brussels | Upper German-Raetian Limes → Berlin | Bad Laasphe → Berlin | J. Paul Getty Museum → Washington, D.C. | Bad Kösen → Berlin | Sun Yat-sen Mausoleum → Beijing || **Final:** Borobudur → Jakarta

- **Query 1214 — Context:** Heiligendamm → Berlin | Bad Schlema → Berlin | Museum of Modern Art of Republika Srpska → Sarajevo | Pickford&#x27;s House → London | Koporye → Moscow | Christ the King statue → Warsaw | Ottobeuren → Berlin | Museo Correr → Rome | Bad Bentheim → Berlin | Atakule → Ankara || **Final:** Mariánské Lázně → Prague

- **Query 1219 — Context:** Statue of Zeus at Olympia → Athens | Lublin-Majdanek concentration camp → Warsaw | Bargello National Museum → Rome | Peggy Guggenheim Collection → Rome | Iglesia de la Concepción → Madrid | Glory&#x27;s Portico → Madrid | Gardaland → Rome | Osborne House → London | Tomb of Suleyman Shah → Damascus | Doge&#x27;s Palace, Genoa → Rome || **Final:** Willingen (Upland) → Berlin

- **Query 1229 — Context:** Nuruosmaniye Mosque → Ankara | Gardaland → Rome | Kudowa-Zdrój → Warsaw | Diamond Head → Washington, D.C. | Ytterby mine → Stockholm | Royal Museum for Central Africa → City of Brussels | Książ Castle and park complex → Warsaw | Ladonia → Stockholm | Avtovo → Moscow | Mausoleum of Khoja Ahmed Yasawi → Astana || **Final:** The Great Sphinx → Cairo

- **Query 1232 — Context:** Bargello National Museum → Rome | Jaraba → Madrid | Świeradów-Zdrój → Warsaw | Palazzo Rosso → Rome | Palazzo Vecchio → Rome | Antwerp City Hall → City of Brussels | Basilica of San Francesco d&#x27;Assisi → Rome | Basilica of Saint Nicholas → Rome | Bad Steben → Berlin | Everland → Seoul || **Final:** Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar

- **Query 1240 — Context:** Bad Salzdetfurth → Berlin | Marble Palace → Moscow | Wieliczka Salt Mine → Warsaw | Knossos → Athens | Rockefeller Center → Washington, D.C. | Koporye → Moscow | J. Paul Getty Museum → Washington, D.C. | Canton Tower → Beijing | Borobudur → Jakarta | Valaam Monastery → Moscow || **Final:** KV13 → Cairo

- **Query 1244 — Context:** Qazan Kremlin → Moscow | Colosseum → Rome | Winchester Mystery House → Washington, D.C. | Roman Walls of Lugo → Madrid | Bad Lauterberg im Harz → Berlin | Wiesbaden → Berlin | Atakule → Ankara | Bargello National Museum → Rome | Bad Kötzting → Berlin | Murnau am Staffelsee → Berlin || **Final:** Shah Cheragh shrine → Tehran

- **Query 1245 — Context:** The Wallace Collection → London | Blenheim Palace → London | Pura Luhur → Jakarta | Otrar → Astana | Ushiku Daibutsu → Tokyo | Gateway Arch → Washington, D.C. | Marble Palace → Moscow | Museum of San Marco → Rome | Hollywood Sign → Washington, D.C. | Lincoln Castle → London || **Final:** Nonnweiler → Berlin

- **Query 1247 — Context:** Cathedral of La Laguna → Madrid | Forchtenstein Castle → Vienna | Magic Kingdom → Washington, D.C. | Hampton Court Palace → London | Umedalens Skulpturpark → Stockholm | Chehel Sotun → Tehran | Ortaköy → Ankara | Cloud Gate → Washington, D.C. | Mount Erciyes → Ankara | Royal Palace of Naples → Rome || **Final:** Bad Laasphe → Berlin

- **Query 1249 — Context:** Yıldız Palace → Ankara | National Library of Australia → Canberra | La Défense → Paris | Coves del Drach → Madrid | KV19 → Cairo | Trinity Lavra of St. Sergius → Moscow | National Archaeological Museum of Athens → Athens | Lake Powell → Washington, D.C. | Great Buddha of Thailand → Bangkok | Akbar&#x27;s Tomb → New Delhi || **Final:** Rengsdorf → Berlin

- **Query 1250 — Context:** Bad Sooden-Allendorf → Berlin | Cave of Swallows → Mexico City | St. Nicholas’ Church, Hamburg → Berlin | Schönau am Königsee → Berlin | Central Park → Washington, D.C. | Gulangyu → Beijing | Travemünde → Berlin | Garmisch-Partenkirchen → Berlin | Universal Studios Japan → Tokyo | Malmö Castle → Stockholm || **Final:** Château de Malmaison → Paris

- **Query 1251 — Context:** Schotten → Berlin | Otrar → Astana | Korela Fortress → Moscow | Durham Castle → London | Herzog Anton Ulrich Museum → Berlin | Wallace Monument → London | Oberstdorf → Berlin | Bad Nenndorf → Berlin | Wuppertal Schwebebahn → Berlin | Novate Mezzola → Rome || **Final:** Altaussee → Vienna

- **Query 1260 — Context:** Nestorian Stele → Beijing | Banya → Sofia | Pulkovo Observatory → Moscow | Gaztelugatxe → Madrid | National Museum in Kraków → Warsaw | Federal Hall → Washington, D.C. | Ölüdeniz → Ankara | türbe → Constantinople | Art Gallery of New South Wales → Canberra | Lake Retba → Dakar || **Final:** Keukenhof → Amsterdam

- **Query 1261 — Context:** Neptune&#x27;s Grotto → Rome | İstiklal Avenue → Ankara | Zuma Rock → Abuja | Pompey&#x27;s Pillar → Cairo | Szczawnica → Warsaw | Stockholm City Hall → Stockholm | Circus Maximus → Rome | Mausoleum of Galla Placidia → Rome | KV27 → Cairo | Bargello National Museum → Rome || **Final:** Bad Frankenhausen → Berlin

- **Query 1264 — Context:** Château de Montsoreau-Museum of Contemporary Art → Paris | Olympia → Athens | Four Corners Monument → Washington, D.C. | Lake Powell → Washington, D.C. | Mastabet el-Fara&#x27;un → Cairo | Ahrenshoop → Berlin | Radcliffe Camera → London | Galata Bridge → Ankara | Monument to the Great Fire of London → London | Waldbrunn → Berlin || **Final:** Zaanse Schans → Amsterdam

- **Query 1266 — Context:** Bad Ischl → Vienna | Mausoleum of Maussollos → Ankara | Linköping Cathedral → Stockholm | Otrar → Astana | Galleria dell&#x27;Accademia → Rome | S.A.I. Catedral Metropolitana de la Encarnación → Madrid | Swiss Alps → Bern | Jaén Cathedral → Madrid | Mycenae → Athens | Madurodam → Amsterdam || **Final:** Weiskirchen → Berlin

- **Query 1267 — Context:** KV35 → Cairo | Selinunte → Rome | Tokyo Disneyland → Tokyo | Bad Bertrich → Berlin | Titisee-Neustadt → Berlin | Timmendorfer Strand → Berlin | Überlingen → Berlin | Acropolis of Athens → Athens | Old House of Bank → Stockholm | West Bali National Park → Jakarta || **Final:** Muzeum Miniaturowej Sztuki Profesjonalnej Henryk Jan Dominiak in Tychy → Warsaw

- **Query 1271 — Context:** Palazzo Pitti → Rome | Druskininkai → Vilnius | Su Nuraxi di Barumini → Rome | Our Lady of the Pillar → Madrid | Tate Modern → London | Yellowstone National Park → Washington, D.C. | Luxor → Cairo | Mount Erciyes → Ankara | Cyprus Museum → Nicosia | Nemrut → Ankara || **Final:** Friedrichroda → Berlin

- **Query 1273 — Context:** Bad Driburg → Berlin | Holstentor → Berlin | Röbel → Berlin | Damavand → Tehran | CN Tower → Ottawa | Hever Castle → London | Sukiennice → Warsaw | Pripyat amusement park → Kyiv | Palazzo Rosso → Rome | Segovia Cathedral → Madrid || **Final:** Ochtinská Aragonite Cave → Bratislava

- **Query 1275 — Context:** Alte Pinakothek → Berlin | Treasury of Atreus → Athens | Kunstkamera → Moscow | Hadrian&#x27;s Villa → Rome | Salamanca New Cathedral → Madrid | Warnemünde → Berlin | Malmö Castle → Stockholm | Bridge of Sighs → Rome | Ochtinská Aragonite Cave → Bratislava | Glory&#x27;s Portico → Madrid || **Final:** Ushiku Daibutsu → Tokyo

- **Query 1278 — Context:** Admiralty Arch → London | Todtmoos → Berlin | Pont du Gard → Paris | Silesian Stadium → Warsaw | Goa Gajah → Jakarta | Zolotoy Rog → Moscow | Mask of Sorrow → Moscow | Vallendar → Berlin | Great Buddha of Thailand → Bangkok | Imam Ali Mosque → Baghdad || **Final:** Carnuntum → Vienna

- **Query 1279 — Context:** German Wine Route → Berlin | Potala Palace → Beijing | Cabo San Lucas → Mexico City | Fingal&#x27;s Cave → London | Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar | Zwinger → Berlin | Tel Aviv Museum of Art → Jerusalem | Daun → Berlin | Fitzwilliam Museum → London | Galata Tower → Ankara || **Final:** Millau Viaduct → Paris

- **Query 1280 — Context:** Fingal&#x27;s Cave → London | Green Mosque → Kabul | Bilbao Fine Arts Museum → Madrid | Promenade des Anglais → Paris | Bad Klosterlausnitz → Berlin | Château de Montsoreau → Paris | Norddorf → Berlin | KV15 → Cairo | Śniardwy → Warsaw | Bad Gastein → Vienna || **Final:** Sybaris → Rome

- **Query 1282 — Context:** Zhangjiajie Glass Bridge → Beijing | Kazimierz → Warsaw | Lublin-Majdanek concentration camp → Warsaw | One World Trade Center → Washington, D.C. | Oy-Mittelberg → Berlin | Ambras Castle → Vienna | Glory&#x27;s Portico → Madrid | Bardejov → Bratislava | Bad Königshofen im Grabfeld → Berlin | Soltau → Berlin || **Final:** Gardens of Bomarzo → Rome

- **Query 1292 — Context:** Truskavets → Kyiv | Scottish National Gallery → London | Juist → Berlin | Peter and Paul Fortress → Moscow | Sheikh Lotfollah Mosque → Tehran | Bad Bodenteich → Berlin | Athena Promachos → Athens | Lion Monument Lucerne → Bern | New Athos Cave → Tbilisi | Oy-Mittelberg → Berlin || **Final:** Nordic Museum → Stockholm

- **Query 1294 — Context:** Osmangazi Bridge → Ankara | Teide → Madrid | Bad Wilsnack → Berlin | Ramsau bei Berchtesgaden → Berlin | Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar | Puente Nuevo → Madrid | Bad Bentheim → Berlin | Mölln → Berlin | Kröller-Müller Museum → Amsterdam | Racławice Panorama → Warsaw || **Final:** KV35 → Cairo

- **Query 1295 — Context:** Christ the King statue → Warsaw | Disney&#x27;s Hollywood Studios → Washington, D.C. | Sankt Peter-Ording → Berlin | Al-Masjid Al-Haram → Riyadh | Gersfeld → Berlin | Las Vegas Strip → Washington, D.C. | Palazzo Vecchio → Rome | Bad Teinach-Zavelstein → Berlin | Museum of Modern Art of Republika Srpska → Sarajevo | Blankenburg → Berlin || **Final:** Alexander Nevsky Lavra → Moscow

- **Query 1296 — Context:** Hoover Dam → Washington, D.C. | Bellano → Rome | Tower of London → London | Vistula Lagoon → Moscow | Triumphal Arch of Orange → Paris | Merneptah Stele → Cairo | Khaju Bridge → Tehran | Niagara Falls → Ottawa | Bad Klosterlausnitz → Berlin | Imbros → Ankara || **Final:** Drottningholm Palace → Stockholm

- **Query 1300 — Context:** Nemrut → Ankara | Mausoleum of Galla Placidia → Rome | Al-Askari Shrine → Baghdad | Canyon de Chelly National Monument → Washington, D.C. | Library of Celsus → Ankara | Domica → Bratislava | Tate Britain → London | Dorio → Rome | Galata Tower → Ankara | Banqueting House → London || **Final:** Bad Fallingbostel → Berlin

- **Query 1305 — Context:** KV21 → Cairo | Villa Romana del Casale → Rome | Museum of Modern Art of Republika Srpska → Sarajevo | Bamburgh Castle → London | St. Florian&#x27;s Gate → Warsaw | Rüstem Pasha Mosque → Ankara | S.A.I. Catedral Metropolitana de la Encarnación → Madrid | Bad Segeberg → Berlin | Bad Endbach → Berlin | Glasgow Cathedral → London || **Final:** Bad Vöslau → Vienna

- **Query 1306 — Context:** Royal Museums of Fine Arts of Belgium → City of Brussels | Tierradentro → Bogotá | Ancient Agora of Athens → Athens | Bad Bayersoien → Berlin | Majuli → New Delhi | Kreuth → Berlin | Deidesheim → Berlin | Villa Tugendhat → Prague | Burj Khalifa → Abu Dhabi | Yosemite National Park → Washington, D.C. || **Final:** Salamanca New Cathedral → Madrid

- **Query 1307 — Context:** Sachsenhausen concentration camp → Berlin | Freiburg im Breisgau → Berlin | Tomb of I&#x27;timād-ud-Daulah → New Delhi | Admont Abbey → Vienna | Bad Endorf → Berlin | Poulnabrone dolmen → Dublin | Château de Malmaison → Paris | Mobility Resort Motegi → Tokyo | Times Square → Washington, D.C. | Pompey&#x27;s Pillar → Cairo || **Final:** Acropolis Museum → Athens

- **Query 1308 — Context:** Oberstdorf → Berlin | 15 July Martyrs Bridge → Ankara | Großenbrode → Berlin | Yavuz Sultan Selim Bridge → Ankara | Valle dei Templi → Rome | Mount Kilimanjaro → Dodoma | Universal Studios Japan → Tokyo | Pripyat amusement park → Kyiv | Carlsbad Caverns National Park → Washington, D.C. | Mangla Dam → Islamabad || **Final:** Si-o-se Pol → Tehran

- **Query 1322 — Context:** Burj Khalifa → Abu Dhabi | Stockholm Palace → Stockholm | Cathedral of Zamora → Madrid | Dorio → Rome | M. H. de Young Memorial Museum → Washington, D.C. | Uzungöl → Ankara | Trinity Cathedral → Moscow | Raj Ghat and associated memorials → New Delhi | Świnoujście → Warsaw | Maya Ruins of Tulum → Mexico City || **Final:** Wyk auf Föhr → Berlin

- **Query 1324 — Context:** Taj Mahal → New Delhi | ArcelorMittal Orbit → London | Canton Tower → Beijing | Bad Heilbrunn → Berlin | Tel Aviv Museum of Art → Jerusalem | Mariinsky Theatre → Moscow | Ourense Cathedral → Madrid | Empire State Building → Washington, D.C. | Stadium MK → London | M. H. de Young Memorial Museum → Washington, D.C. || **Final:** Linköping Cathedral → Stockholm

- **Query 1329 — Context:** Guggenheim Museum → Madrid | Fountains Abbey → London | Centennial Hall → Warsaw | Museo di Capodimonte → Rome | Imagine Peace Tower → Reykjavík | Badajoz Cathedral → Madrid | Hagia Sophia → Ankara | Apsley House → London | Persepolis → Tehran | KV11 → Cairo || **Final:** Kühlungsborn → Berlin

- **Query 1331 — Context:** Osmangazi Bridge → Ankara | Mandello del Lario → Rome | Bad Neustadt an der Saale → Berlin | Nelson&#x27;s Column → London | Cathedral of Saint Demetrius → Moscow | Bad Driburg → Berlin | Bad Staffelstein → Berlin | Wallraf–Richartz Museum → Berlin | Egyptian pyramids → Cairo | Royal Museum of Fine Arts Antwerp → City of Brussels || **Final:** Omonoia Square → Athens

- **Query 1343 — Context:** Circus Maximus → Rome | Wawel Cathedral → Warsaw | Norderney → Berlin | Uraniborg → Stockholm | Darjeeling Himalayan Railway → New Delhi | Waldbronn → Berlin | Avtovo → Moscow | Rialto Bridge → Rome | Guédelon Castle → Paris | Little Hagia Sophia → Ankara || **Final:** Swiss Alps → Bern

- **Query 1345 — Context:** J. Paul Getty Museum → Washington, D.C. | Alcazaba y Murallas del Cerro de San Cristóbal → Madrid | Freudenstadt → Berlin | Portman Road → London | Ratzeburg → Berlin | Friedrichskoog → Berlin | Millennium of Russia → Moscow | Bernkastel-Kues → Berlin | Bad Sobernheim → Berlin | Bad Tabarz → Berlin || **Final:** Gothenburg Museum of Art → Stockholm

- **Query 1346 — Context:** Ca&#x27; Rezzonico → Rome | Igel Column → Berlin | Kraków Barbican → Warsaw | Tomb of Hafez → Tehran | Sankt Englmar → Berlin | Triumphal Arch of Orange → Paris | Sorico → Rome | Guggenheim Museum → Madrid | Hiroshima Peace Memorial → Tokyo | Medici Chapels → Rome || **Final:** Birka → Stockholm

- **Query 1349 — Context:** Ca&#x27; Rezzonico → Rome | Oscar Niemeyer International Cultural Centre → Madrid | Kołobrzeg → Warsaw | Lombard Street → Washington, D.C. | Diamond Head → Washington, D.C. | Alexander Column → Moscow | Redwood National and State Parks → Washington, D.C. | Atherton Tableland → Canberra | Oriental Pearl Tower → Beijing | Malmö Castle → Stockholm || **Final:** Bad Schmiedeberg → Berlin

- **Query 1363 — Context:** Las Vegas Strip → Washington, D.C. | Graceland → Washington, D.C. | Bad Kissingen → Berlin | Rialto Bridge → Rome | Bad Salzuflen → Berlin | Waldbrunn → Berlin | The Cloisters → Washington, D.C. | Mask of Sorrow → Moscow | Bad Grönenbach → Berlin | Royal Museum of Fine Arts Antwerp → City of Brussels || **Final:** Pyramid of Userkaf → Cairo

- **Query 1365 — Context:** Le Gua → Paris | İstanbul Modern → Ankara | Sultan Ahmed Mosque → Ankara | Royal Museums of Fine Arts of Belgium → City of Brussels | Acropolis of Athens → Athens | Pulkovo Observatory → Moscow | Tanah Lot → Jakarta | Skull Tower → Belgrade | Palace of Caserta → Rome | Golden Gate Park → Washington, D.C. || **Final:** Petershagen → Berlin

- **Query 1367 — Context:** Zuma Rock → Abuja | Besakih → Jakarta | Gol Gumbaz → New Delhi | Bacho Kiro cave → Sofia | Castello Estense → Rome | KV4 → Cairo | Tokyo Disneyland → Tokyo | Persepolis → Tehran | Guggenheim Museum → Madrid | Van Gogh Museum → Amsterdam || **Final:** Soltau → Berlin

- **Query 1368 — Context:** Książ Castle and park complex → Warsaw | Bad Pyrmont → Berlin | Crazy Horse Memorial → Washington, D.C. | Lia Fáil → Dublin | Eyüp Sultan Mosque → Ankara | Viñales Valley → Havana | National September 11 Memorial &amp; Museum → Washington, D.C. | Baltrum → Berlin | Batu Caves → Kuala Lumpur | National Museum of Beirut → Beirut || **Final:** Castel Sant&#x27;Angelo → Rome

- **Query 1369 — Context:** Colosseum → Rome | Palazzo Ducale Mantua → Rome | Grand Bazaar → Ankara | Arches National Park → Washington, D.C. | Khaju Bridge → Tehran | Ortaköy Mosque → Ankara | India Gate → New Delhi | Si-o-se Pol → Tehran | Amélie-les-Bains-Palalda → Paris | Petrie Museum of Egyptian Archaeology → London || **Final:** Westerbork Transit Camp → Amsterdam

- **Query 1371 — Context:** Schwangau → Berlin | Bacho Kiro cave → Sofia | Buckow → Berlin | Postojna Cave → Ljubljana | Ustroń → Warsaw | Castello Estense → Rome | One World Trade Center → Washington, D.C. | Belfry of Bruges → City of Brussels | Solovetsky Monastery → Moscow | Ancient Theatre of Epidaurus → Athens || **Final:** Jelling stones → Copenhagen

- **Query 1373 — Context:** Bronze Horseman → Moscow | Puente romano → Madrid | Tierradentro → Bogotá | Liseberg → Stockholm | Bridge of Sighs → Rome | Ludlow Castle → London | M. H. de Young Memorial Museum → Washington, D.C. | Kingda Ka → Washington, D.C. | Monument to the Great Fire of London → London | Blue Mosque → Kabul || **Final:** Boltenhagen → Berlin

- **Query 1375 — Context:** National Gallery of Norway → Oslo | Atakule → Ankara | Tower of Hercules → Madrid | Lugo Cathedral → Madrid | Tomb of Caecilia Metella → Rome | Cascata delle Marmore → Rome | Royal Palace of Naples → Rome | Rembrandt House Museum → Amsterdam | Walt Disney World Resort → Washington, D.C. | Monument to the Great Fire of London → London || **Final:** Siegsdorf → Berlin

- **Query 1376 — Context:** Bad Endorf → Berlin | Ain Dubai → Abu Dhabi | Tomb of Askia → Bamako | Bad Rothenfelde → Berlin | Hollywood Walk of Fame → Washington, D.C. | Basilica of Candelaria → Madrid | Bad Berleburg → Berlin | Bad Mergentheim → Berlin | War of Independence Victory Column → Tallinn | Brancacci Chapel → Rome || **Final:** Amélie-les-Bains-Palalda → Paris

- **Query 1378 — Context:** Arlington National Cemetery → Washington, D.C. | Yellowstone National Park → Washington, D.C. | Ha Long Bay → Hanoi | Colosseum → Rome | Củ Chi tunnels → Hanoi | Roman Walls of Lugo → Madrid | Aqueduct of Valens → Ankara | Salamanca New Cathedral → Madrid | Stirling Castle → London | KV14 → Cairo || **Final:** Bad Lausick → Berlin

- **Query 1382 — Context:** Gripsholm Castle → Stockholm | Keukenhof → Amsterdam | Amber Mountain National Park → Antananarivo | Nördlingen → Berlin | Che Guevara Mausoleum → Havana | Museum Ludwig → Berlin | British Museum → London | Piantedo → Rome | Arch of Trajan → Rome | Archcathedral Basilica of St. Peter and St. Paul → Warsaw || **Final:** Egyptian pyramids → Cairo

**Part 2: Strongest Logit-Lens Evidence**

Layers are zero-indexed. Only layers tied for the highest reciprocal rank are shown.

**Compositional (370)**

- **Query 1:** Palace of Versailles → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20

- **Query 8:** Persepolis → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 25, 26, 27

- **Query 11:** Tabernas Desert → Madrid | **Intermediate country:** Spain | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 21:** Rök Runestone → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 24:** Solovetsky Monastery → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 35:** Thien Duong Cave → Hanoi | **Intermediate country:** Vietnam | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28, 29, 30

- **Query 37:** Luxor → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 23, 24, 25, 26, 27, 30

- **Query 46:** Susa → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 25

- **Query 55:** Mausoleum of Theodoric → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 56:** Las Médulas → Madrid | **Intermediate country:** Spain | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 66:** Bad Lauterberg im Harz → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 73:** Sachsenhausen concentration camp → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21

- **Query 77:** Bad Marienberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 80:** Bad Wünnenberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 26

- **Query 96:** Château de Montsoreau-Museum of Contemporary Art → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 98:** Heringsdorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 101:** Arlington National Cemetery → Washington, D.C. | **Intermediate country:** United States | **Highest RR:** 1 | **Peak layer(s):** 17, 18, 19

- **Query 106:** Sverd i fjell → Oslo | **Intermediate country:** Norway | **Highest RR:** 1 | **Peak layer(s):** 22, 26, 27, 28

- **Query 107:** Pombia Safari Park → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 108:** KV15 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 23, 25

- **Query 115:** Dervio → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22

- **Query 116:** Bad Sassendorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 118:** Wittdün auf Amrum → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 26

- **Query 122:** Lia Fáil → Dublin | **Intermediate country:** Ireland | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 123:** Olympia → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 25

- **Query 135:** Circus Maximus → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 30

- **Query 136:** Petralona cave → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 26, 27

- **Query 139:** Merneptah Stele → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 23, 24, 25, 26

- **Query 143:** KV12 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 25, 26

- **Query 144:** Cascata delle Marmore → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27

- **Query 147:** Deidesheim → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 150:** Dahme → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 151:** Great Pyramid of Giza → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 25, 26

- **Query 155:** Mount Longonot → Nairobi | **Intermediate country:** Kenya | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 25, 26, 27, 28, 29

- **Query 157:** Neuharlingersiel → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22

- **Query 158:** Bad Gastein → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 160:** Heilbad Heiligenstadt → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 166:** Bad Saarow → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22

- **Query 167:** Rijksmuseum → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 0.5 | **Peak layer(s):** 19, 21, 22

- **Query 169:** Riddarholm Church → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 17, 18, 20, 21, 22, 23, 24, 25

- **Query 174:** Rembrandt House Museum → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 0.5 | **Peak layer(s):** 19, 21, 22, 29

- **Query 177:** Scharbeutz → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 27, 28

- **Query 178:** Bad Schandau → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 179:** Ahrenshoop → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 27, 28, 29, 30

- **Query 185:** Bad Iburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 25, 26, 27, 28

- **Query 186:** Todtmoos → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 190:** Bad Bertrich → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 203:** Veliky Ustyug → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 205:** Buckow → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27, 28

- **Query 214:** Kellenhusen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 216:** Bad Grönenbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 217:** Bad Sulza → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22

- **Query 220:** KV11 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 223:** Warnemünde → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22

- **Query 225:** Kalmar Castle → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 235:** Zingst → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 238:** Kyllburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 239:** Gersfeld → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22

- **Query 248:** Statue of Zeus at Olympia → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 22

- **Query 249:** Sozopol → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 1 | **Peak layer(s):** 25

- **Query 251:** KV10 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26

- **Query 261:** Brühl&#x27;s Terrace → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 263:** Museum of Anatolian Civilizations → Ankara | **Intermediate country:** Turkey | **Highest RR:** 0.5 | **Peak layer(s):** 26

- **Query 268:** Mount Fuji → Tokyo | **Intermediate country:** Japan | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 269:** Batu Caves → Kuala Lumpur | **Intermediate country:** Malaysia | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 25, 26, 27

- **Query 274:** Raj Ghat and associated memorials → New Delhi | **Intermediate country:** India | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22

- **Query 277:** Tecklenburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 278:** Kudowa-Zdrój → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 21, 25, 26, 27

- **Query 280:** Gardaland → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 25, 26, 27, 30

- **Query 282:** Schömberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 19, 21, 22

- **Query 284:** KV18 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22, 23, 26

- **Query 285:** Bad König → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27

- **Query 288:** Bad Pyrmont → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 293:** Wustrow → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 23

- **Query 294:** Świeradów-Zdrój → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.5 | **Peak layer(s):** 20, 21, 22, 23, 25

- **Query 313:** Ferapontov Monastery → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 25, 26

- **Query 315:** KV34 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25

- **Query 316:** Bad Schwartau → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 317:** Pelion → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 325:** Soltaniyeh Dome → Tehran | **Intermediate country:** Iran | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 330:** Pompey&#x27;s Pillar → Cairo | **Intermediate country:** Egypt | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 23

- **Query 331:** Templin → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 344:** Spiekeroog → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 346:** Dolmen of Viera → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.5 | **Peak layer(s):** 31

- **Query 349:** Gołdap → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28

- **Query 350:** Mölln → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22

- **Query 352:** Athena Parthenos → Athens | **Intermediate country:** Greece | **Highest RR:** 0.5 | **Peak layer(s):** 19, 21, 22, 23, 24, 25, 26, 27, 29

- **Query 353:** Bad Homburg vor der Höhe → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 26

- **Query 355:** Baltrum → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 358:** Szczawnica → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27, 28

- **Query 359:** Rietveld Schröder House → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 360:** Kungur Ice Cave → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22, 23, 24, 26, 27, 28, 29, 30

- **Query 363:** Mastabet el-Fara&#x27;un → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 367:** Bad Freienwalde → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 369:** Graal-Müritz → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 26, 27

- **Query 372:** Bad Dürrheim → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26

- **Query 377:** Tarxien Temples → Valletta | **Intermediate country:** Malta | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 22, 25, 26, 27

- **Query 378:** Sandanski → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 379:** Monastery of Saint John of Rila → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 1 | **Peak layer(s):** 22, 25, 26

- **Query 381:** Dikteon Andron → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 24, 25, 26, 27

- **Query 382:** Morskie Oko → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 27, 28

- **Query 386:** Van Gogh Museum → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22

- **Query 390:** Vulci → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 392:** Hohwacht → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23

- **Query 394:** Vittskövle Church → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23

- **Query 396:** Munch Museum → Oslo | **Intermediate country:** Norway | **Highest RR:** 0.5 | **Peak layer(s):** 20, 25, 26, 31

- **Query 398:** KV1 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22, 23

- **Query 400:** Bad Düben → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 401:** Bad Liebenwerda → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 25, 26

- **Query 402:** Kreuth → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 405:** Mandello del Lario → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26

- **Query 408:** Mount Kumgang Tourist Region → Pyongyang | **Intermediate country:** North Korea | **Highest RR:** 1 | **Peak layer(s):** 30

- **Query 409:** Bad Soden-Salmünster → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 414:** Bad Lippspringe → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27, 28

- **Query 418:** KV3 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22, 23

- **Query 429:** Sigüenza Cathedral → Madrid | **Intermediate country:** Spain | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 434:** Church of the Intercession on the Nerl → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 22, 23

- **Query 438:** Hitzacker → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 448:** Bad Schwalbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 454:** Blagaj, Mostar → Sarajevo | **Intermediate country:** Bosnia and Herzegovina | **Highest RR:** 1 | **Peak layer(s):** 22, 24, 25, 26, 27, 28, 29, 30, 31

- **Query 456:** Manderscheid → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 459:** KV6 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 0.5 | **Peak layer(s):** 22, 23, 25

- **Query 461:** Wiesbaden → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 462:** Valaam Monastery → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 26

- **Query 467:** Yuste → Madrid | **Intermediate country:** Spain | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 470:** Church of the Savior on Blood → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 22, 23, 24

- **Query 478:** Chehel Sotun → Tehran | **Intermediate country:** Iran | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23

- **Query 482:** Bad Harzburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 484:** Schönwald im Schwarzwald → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22

- **Query 488:** Palacio Episcopal de Astorga → Madrid | **Intermediate country:** Spain | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 493:** Athena Promachos → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 495:** Château de Montsoreau → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 505:** Bad Ischl → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 25, 26, 27

- **Query 514:** Mobility Resort Motegi → Tokyo | **Intermediate country:** Japan | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 515:** Biedenkopf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22

- **Query 521:** Dadiani Palaces Museum → Tbilisi | **Intermediate country:** Georgia | **Highest RR:** 0.5 | **Peak layer(s):** 26, 27, 28

- **Query 522:** Ytterby mine → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23, 25, 26, 27

- **Query 527:** Książ Castle and park complex → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22

- **Query 533:** Catacombs of Kom el Shoqafa → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21

- **Query 534:** Bad Belzig → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 535:** Puy de Dôme → Paris | **Intermediate country:** France | **Highest RR:** 0.5 | **Peak layer(s):** 18, 19, 21, 22, 23, 24, 25, 26

- **Query 542:** Bad Aussee → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 25, 26, 27, 28, 29

- **Query 548:** Blankenburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 551:** Newgrange → Dublin | **Intermediate country:** Ireland | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 27

- **Query 553:** Bad Neuenahr-Ahrweiler → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26

- **Query 554:** Nikkō Tōshō-gū → Tokyo | **Intermediate country:** Japan | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 561:** tomb of Tutankhamun → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24

- **Query 564:** Frasassi Caves → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 566:** Vallendar → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30

- **Query 571:** Eutin → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 572:** Bad Rothenfelde → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 574:** Bad Segeberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 26, 27

- **Query 575:** Madurodam → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 580:** Kizhi Pogost → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 585:** Nümbrecht → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 587:** Wangerooge → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 590:** Parc Astérix → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 597:** Bad Soden am Taunus → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 27

- **Query 599:** Balatonfüred → Budapest | **Intermediate country:** Hungary | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 23

- **Query 602:** KV21 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 23, 25

- **Query 604:** Bad Salzuflen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 605:** Zolotoy Rog → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 25, 26

- **Query 606:** Ny Carlsberg Glyptotek → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.5 | **Peak layer(s):** 26

- **Query 608:** Kenilworth Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.5 | **Peak layer(s):** 18

- **Query 613:** KV57 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23

- **Query 614:** Benaki Museum → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 616:** Bad Elster → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22

- **Query 617:** Spodek → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.5 | **Peak layer(s):** 22, 23, 24

- **Query 634:** Woburn Abbey → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.5 | **Peak layer(s):** 18

- **Query 638:** Bad Bayersoien → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22, 26

- **Query 645:** Choragic Monument of Lysicrates → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 646:** Škocjan Caves → Ljubljana | **Intermediate country:** Slovenia | **Highest RR:** 1 | **Peak layer(s):** 18, 22, 25, 26, 27

- **Query 651:** Museum of Cycladic Art → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21

- **Query 652:** Bad Schlema → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22

- **Query 654:** Naumburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 656:** Cliffs of Moher → Dublin | **Intermediate country:** Ireland | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 27

- **Query 657:** Lądek-Zdrój → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 666:** Serdobsk → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 25

- **Query 668:** Röbel → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 671:** Củ Chi tunnels → Hanoi | **Intermediate country:** Vietnam | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 23, 25, 26, 27

- **Query 676:** Badajoz Cathedral → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 683:** Jeita Grotto → Beirut | **Intermediate country:** Lebanon | **Highest RR:** 0.5 | **Peak layer(s):** 31

- **Query 685:** Heimbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 686:** Astrid Lindgren&#x27;s World → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 23

- **Query 689:** Königsfeld im Schwarzwald → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26

- **Query 691:** Tatranská Lomnica → Bratislava | **Intermediate country:** Slovakia | **Highest RR:** 1 | **Peak layer(s):** 26, 27, 28

- **Query 692:** Tomb of Caecilia Metella → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 20, 29

- **Query 694:** Skansen → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21

- **Query 696:** Wings of Tatev → Yerevan | **Intermediate country:** Armenia | **Highest RR:** 1 | **Peak layer(s):** 18, 25, 26, 27

- **Query 698:** Admont Abbey → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 701:** Stützerbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 703:** Uppsala Cathedral → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 709:** Bad Oeynhausen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22

- **Query 713:** Schönau am Königsee → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22

- **Query 720:** Vintgar Gorge → Ljubljana | **Intermediate country:** Slovenia | **Highest RR:** 1 | **Peak layer(s):** 22, 25, 26, 27, 28, 29

- **Query 722:** Ladonia → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 25, 26, 27, 28

- **Query 729:** Postojna Cave → Ljubljana | **Intermediate country:** Slovenia | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 25, 26, 27, 28

- **Query 731:** Mausoleum of Galla Placidia → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 732:** Bad Karlshafen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22

- **Query 734:** Feldherrnhalle → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21

- **Query 746:** Galleria Borghese → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 21, 26, 27, 29, 30

- **Query 748:** Bad Wilsnack → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22

- **Query 759:** Dierhagen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 760:** Piskaryovskoye Memorial Cemetery → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 764:** Schwerin Castle → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 767:** Bad Heilbrunn → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 26, 27

- **Query 771:** Büsum → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 773:** Vjetrenica → Sarajevo | **Intermediate country:** Bosnia and Herzegovina | **Highest RR:** 1 | **Peak layer(s):** 25, 26, 27

- **Query 775:** KV17 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 26

- **Query 776:** Altenberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27, 28, 29, 30

- **Query 778:** Mycenae → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 783:** Font-de-Gaume → Paris | **Intermediate country:** France | **Highest RR:** 0.5 | **Peak layer(s):** 18, 21, 22

- **Query 785:** Goa Gajah → Jakarta | **Intermediate country:** Indonesia | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 787:** Blieskastel → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 24, 25, 26

- **Query 791:** Kraków-Płaszów concentration camp → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 25, 26

- **Query 794:** Bad Blankenburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 805:** Nürburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 24, 25, 26, 27, 28

- **Query 807:** Bad Friedrichshall → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 808:** Galapagos Islands → Quito | **Intermediate country:** Ecuador | **Highest RR:** 1 | **Peak layer(s):** 26

- **Query 810:** Sukiennice → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22

- **Query 812:** Grand Egyptian Museum → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 813:** Jastrzębie-Zdrój → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22

- **Query 814:** Vadstena Castle → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 818:** Louisiana Museum of Modern Art → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.5 | **Peak layer(s):** 22, 23, 26

- **Query 819:** Bad Bevensen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28, 30

- **Query 820:** Wissen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28, 30

- **Query 821:** German Federal Archives → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 25

- **Query 827:** Orkhon inscriptions → Ulaanbaatar | **Intermediate country:** Mongolia | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 25, 26, 27, 28, 29

- **Query 828:** Obelisk of Axum → Addis Ababa | **Intermediate country:** Ethiopia | **Highest RR:** 1 | **Peak layer(s):** 21, 23, 24, 25, 26

- **Query 832:** Canadian Museum of History → Ottawa | **Intermediate country:** Canada | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 836:** Rundetaarn → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22

- **Query 846:** Kalmar Cathedral → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 850:** Läckö Castle → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26

- **Query 854:** Knowth → Dublin | **Intermediate country:** Ireland | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28

- **Query 864:** Śniardwy → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 23, 25

- **Query 871:** The Little Mermaid → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 1 | **Peak layer(s):** 26

- **Query 874:** Bad Arolsen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 879:** Bad Berleburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 880:** Cathedral of Zamora → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 888:** Bad Bodenteich → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27

- **Query 895:** Bad Sachsa → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 25, 26, 27

- **Query 897:** Damavand → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 21, 22, 25, 26, 27, 28, 31

- **Query 899:** Heiligenhafen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 900:** Mnajdra → Valletta | **Intermediate country:** Malta | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 22, 23, 24, 25, 26, 27, 28

- **Query 903:** Bischofswiesen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 909:** Heligoland → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 910:** Mausoleum of Khoja Ahmed Yasawi → Astana | **Intermediate country:** Kazakhstan | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 916:** Bad Kreuznach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 921:** German Wine Route → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 25

- **Query 926:** Anne Frank House → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 0.5 | **Peak layer(s):** 19, 25, 26, 27, 28, 29

- **Query 928:** Abbadia Lariana → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25

- **Query 930:** Kumu → Tallinn | **Intermediate country:** Estonia | **Highest RR:** 1 | **Peak layer(s):** 21

- **Query 932:** Bad Berka → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28

- **Query 933:** Niedenstein → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 21, 22

- **Query 935:** Gripsholm Castle → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 950:** MAXXI → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 26

- **Query 951:** Efteling → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22

- **Query 954:** Khaju Bridge → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 25

- **Query 958:** Racławice Panorama → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22, 23

- **Query 961:** Homberg (Ohm) → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 962:** Lion of Belfort → Paris | **Intermediate country:** France | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 967:** Luxor Museum → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25

- **Query 972:** Holy Trinity Column in Olomouc → Prague | **Intermediate country:** Czech Republic | **Highest RR:** 1 | **Peak layer(s):** 26

- **Query 974:** Wat Arun → Bangkok | **Intermediate country:** Thailand | **Highest RR:** 0.5 | **Peak layer(s):** 25, 26, 27, 28, 29

- **Query 977:** Bad Wildungen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 980:** Grossglockner High Alpine Road → Vienna | **Intermediate country:** Austria | **Highest RR:** 0.5 | **Peak layer(s):** 21, 25, 26

- **Query 985:** Grūtas Park → Vilnius | **Intermediate country:** Lithuania | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23

- **Query 988:** Canaima National Park → Caracas | **Intermediate country:** Venezuela | **Highest RR:** 1 | **Peak layer(s):** 25, 26

- **Query 999:** Kalka–Shimla Railway → New Delhi | **Intermediate country:** India | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27, 28

- **Query 1003:** Gladenbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23, 24, 25, 26, 27, 28

- **Query 1004:** Wenningstedt-Braderup → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 26, 27, 28, 30

- **Query 1006:** Călimănești → Bucharest | **Intermediate country:** Romania | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23

- **Query 1009:** Bad Breisig → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26

- **Query 1011:** Bad Sülze → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27, 28

- **Query 1012:** Buziaș → Bucharest | **Intermediate country:** Romania | **Highest RR:** 1 | **Peak layer(s):** 20, 21, 22, 23, 26

- **Query 1014:** Bad Staffelstein → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 23

- **Query 1015:** Băile Herculane → Bucharest | **Intermediate country:** Romania | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 1022:** Wasserburg → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1023:** Bad Emstal → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27

- **Query 1027:** Nesebar → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 1 | **Peak layer(s):** 26

- **Query 1030:** iron pillar of Delhi → New Delhi | **Intermediate country:** India | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21

- **Query 1041:** Tel Aviv Museum of Art → Jerusalem | **Intermediate country:** Israel | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 27

- **Query 1045:** Moderna Museet → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 1050:** Angel Falls → Caracas | **Intermediate country:** Venezuela | **Highest RR:** 1 | **Peak layer(s):** 25, 26, 27, 28, 29

- **Query 1051:** Bad Nenndorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 1056:** Philopappos Monument → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 1070:** Skokloster Castle → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28

- **Query 1073:** Troldhaugen → Oslo | **Intermediate country:** Norway | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 26

- **Query 1081:** Busan → Seoul | **Intermediate country:** South Korea | **Highest RR:** 0.5 | **Peak layer(s):** 18, 19, 30

- **Query 1083:** Sammallahdenmäki → Helsinki | **Intermediate country:** Finland | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 26

- **Query 1084:** Everland → Seoul | **Intermediate country:** South Korea | **Highest RR:** 0.5 | **Peak layer(s):** 30, 31

- **Query 1085:** Bad Münstereifel → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 27, 28

- **Query 1086:** Waren → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 28

- **Query 1090:** Piešťany → Bratislava | **Intermediate country:** Slovakia | **Highest RR:** 0.5 | **Peak layer(s):** 22

- **Query 1103:** Colosseum → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 20, 30, 31

- **Query 1115:** Bad Wildbad → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26

- **Query 1123:** Bad Grund → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 1130:** Tsūtenkaku → Tokyo | **Intermediate country:** Japan | **Highest RR:** 1 | **Peak layer(s):** 18, 19

- **Query 1139:** KV14 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 1140:** Travemünde → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1145:** Museum of Modern Art of Republika Srpska → Sarajevo | **Intermediate country:** Bosnia and Herzegovina | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 25, 26, 27

- **Query 1157:** Großenbrode → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1158:** Bad Hindelang → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27, 28

- **Query 1162:** Stoa Poikile → Athens | **Intermediate country:** Greece | **Highest RR:** 0.5 | **Peak layer(s):** 18, 19, 25

- **Query 1168:** Kunsthaus Graz → Vienna | **Intermediate country:** Austria | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 1169:** Moskovsky railway station → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.5 | **Peak layer(s):** 18, 21, 22

- **Query 1170:** Bad Bramstedt → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1172:** Galleria Nazionale d&#x27;Arte Moderna e Contemporanea di Roma → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 1174:** Gröna Lund → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 0.5 | **Peak layer(s):** 18, 21, 22, 23, 25, 26, 27

- **Query 1175:** Bad Neustadt an der Saale → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 1177:** Royal Palace of La Granja de San Ildefonso → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.5 | **Peak layer(s):** 22, 25, 26

- **Query 1183:** Gernsbach → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23, 24, 25, 26

- **Query 1185:** Rabka-Zdrój → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1187:** Bad Essen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25

- **Query 1191:** Ancient Theatre of Epidaurus → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 25

- **Query 1195:** Thracian Tomb of Sveshtari → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 1 | **Peak layer(s):** 22, 23

- **Query 1197:** Ha Long Bay → Hanoi | **Intermediate country:** Vietnam | **Highest RR:** 1 | **Peak layer(s):** 21, 25, 26, 27

- **Query 1201:** Bad Langensalza → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27, 28

- **Query 1213:** Borobudur → Jakarta | **Intermediate country:** Indonesia | **Highest RR:** 0.5 | **Peak layer(s):** 25

- **Query 1214:** Mariánské Lázně → Prague | **Intermediate country:** Czech Republic | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 25, 26, 27

- **Query 1219:** Willingen (Upland) → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28, 30

- **Query 1229:** The Great Sphinx → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23

- **Query 1232:** Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar | **Intermediate country:** Mongolia | **Highest RR:** 1 | **Peak layer(s):** 22, 23, 24, 25, 27

- **Query 1240:** KV13 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 26

- **Query 1244:** Shah Cheragh shrine → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 25, 26

- **Query 1245:** Nonnweiler → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 27, 28

- **Query 1247:** Bad Laasphe → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 23, 24, 25, 26, 27, 30

- **Query 1249:** Rengsdorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23, 27, 28

- **Query 1250:** Château de Malmaison → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 1251:** Altaussee → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 21, 26

- **Query 1260:** Keukenhof → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 1261:** Bad Frankenhausen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 1264:** Zaanse Schans → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 27, 28

- **Query 1266:** Weiskirchen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1267:** Muzeum Miniaturowej Sztuki Profesjonalnej Henryk Jan Dominiak in Tychy → Warsaw | **Intermediate country:** Poland | **Highest RR:** 1 | **Peak layer(s):** 23, 25, 26, 27

- **Query 1271:** Friedrichroda → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 24, 25, 26, 27, 28

- **Query 1273:** Ochtinská Aragonite Cave → Bratislava | **Intermediate country:** Slovakia | **Highest RR:** 1 | **Peak layer(s):** 28

- **Query 1275:** Ushiku Daibutsu → Tokyo | **Intermediate country:** Japan | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22

- **Query 1278:** Carnuntum → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 22, 26

- **Query 1279:** Millau Viaduct → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1280:** Sybaris → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 27

- **Query 1282:** Gardens of Bomarzo → Rome | **Intermediate country:** Italy | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 26, 27

- **Query 1292:** Nordic Museum → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 22

- **Query 1294:** KV35 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1295:** Alexander Nevsky Lavra → Moscow | **Intermediate country:** Russia | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 1296:** Drottningholm Palace → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 22, 26

- **Query 1300:** Bad Fallingbostel → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 25, 26, 27

- **Query 1305:** Bad Vöslau → Vienna | **Intermediate country:** Austria | **Highest RR:** 1 | **Peak layer(s):** 18, 21, 25, 26, 27

- **Query 1306:** Salamanca New Cathedral → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.5 | **Peak layer(s):** 26, 27

- **Query 1307:** Acropolis Museum → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 1308:** Si-o-se Pol → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.5 | **Peak layer(s):** 22, 25, 26, 27

- **Query 1322:** Wyk auf Föhr → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 28

- **Query 1324:** Linköping Cathedral → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22, 23, 24, 25, 26, 27

- **Query 1329:** Kühlungsborn → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30

- **Query 1331:** Omonoia Square → Athens | **Intermediate country:** Greece | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 1343:** Swiss Alps → Bern | **Intermediate country:** Switzerland | **Highest RR:** 1 | **Peak layer(s):** 18, 20, 21, 22, 23, 24, 25, 26, 27, 28

- **Query 1345:** Gothenburg Museum of Art → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18

- **Query 1346:** Birka → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27

- **Query 1349:** Bad Schmiedeberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.5 | **Peak layer(s):** 21

- **Query 1363:** Pyramid of Userkaf → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28

- **Query 1365:** Petershagen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 1367:** Soltau → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23, 25, 26, 27, 28, 29, 30

- **Query 1368:** Castel Sant&#x27;Angelo → Rome | **Intermediate country:** Italy | **Highest RR:** 0.5 | **Peak layer(s):** 20, 21

- **Query 1369:** Westerbork Transit Camp → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30

- **Query 1371:** Jelling stones → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 1 | **Peak layer(s):** 19

- **Query 1373:** Boltenhagen → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 21, 22

- **Query 1375:** Siegsdorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 23

- **Query 1376:** Amélie-les-Bains-Palalda → Paris | **Intermediate country:** France | **Highest RR:** 1 | **Peak layer(s):** 21, 22

- **Query 1378:** Bad Lausick → Berlin | **Intermediate country:** Germany | **Highest RR:** 1 | **Peak layer(s):** 21, 22, 26

- **Query 1382:** Egyptian pyramids → Cairo | **Intermediate country:** Egypt | **Highest RR:** 1 | **Peak layer(s):** 18, 19, 20, 21, 22, 23
