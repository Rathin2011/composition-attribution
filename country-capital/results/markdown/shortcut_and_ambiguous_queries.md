**OLMo 3 Stage-One: Landmark–Country–Capital Shortcut and Ambiguous Queries**

All queries were answered correctly. Composition has RR ≥ 0.5; shortcut candidates have RR ≤ 0.2; values between the thresholds are ambiguous.

**Part 1: Queries and In-Context Examples**

**Shortcut candidates (105)**

- **Query 0 — Context:** Ninth Fort → Vilnius | KV11 → Cairo | Bad Klosterlausnitz → Berlin | Bad Sulza → Berlin | Schotten → Berlin | Bad Aussee → Vienna | Cathedral of Zamora → Madrid | Fisherman&#x27;s Wharf → Washington, D.C. | Bad Vöslau → Vienna | Soltau → Berlin || **Final:** Caernarfon Castle → London

- **Query 3 — Context:** Indianapolis Museum of Art → Washington, D.C. | Piskaryovskoye Memorial Cemetery → Moscow | Fallingwater → Washington, D.C. | Gonbad-e Qabus → Tehran | Knossos → Athens | Vitra Design Museum → Berlin | Śniardwy → Warsaw | Lion of Judah → Addis Ababa | Neuharlingersiel → Berlin | Sofiyivsky Park → Kyiv || **Final:** Queen&#x27;s House → London

- **Query 14 — Context:** Cave of Altacosa → Madrid | Büsum → Berlin | St. Mary&#x27;s Basilica in Gdańsk → Warsaw | Carlsbad Caverns National Park → Washington, D.C. | Badenweiler → Berlin | Egyptian pyramids → Cairo | KV4 → Cairo | Four Corners Monument → Washington, D.C. | Mecca → Riyadh | Nümbrecht → Berlin || **Final:** Westminster Abbey → London

- **Query 19 — Context:** Bad Salzungen → Berlin | Alexander Nevsky Lavra → Moscow | Niagara Falls → Ottawa | Glory&#x27;s Portico → Madrid | Bad Füssing → Berlin | Medici Chapels → Rome | Cedar Point → Washington, D.C. | Istanbul Archaeology Museums → Ankara | Nümbrecht → Berlin | Heringsdorf → Berlin || **Final:** Chengde Mountain Resort and its outlying temples → Beijing

- **Query 23 — Context:** Mobility Resort Motegi → Tokyo | Universal Studios Japan → Tokyo | Jedlina-Zdrój → Warsaw | Bad Kötzting → Berlin | Baden-Baden → Berlin | Gammelstad Church Town → Stockholm | Zhouzhuang Town → Beijing | Newgrounds → Washington, D.C. | Stützerbach → Berlin | Świnoujście → Warsaw || **Final:** The Wallace Collection → London

- **Query 28 — Context:** Uraniborg → Stockholm | Eyüp Sultan Mosque → Ankara | Europa-Park → Berlin | Jasna Góra Monastery → Warsaw | Admiralty building in Saint Petersburg → Moscow | Basilica of San Francesco d&#x27;Assisi → Rome | Graceland → Washington, D.C. | Bad Oeynhausen → Berlin | Liberty Bell → Washington, D.C. | Metropolitan Cathedral Basilica of St. James the Apostle → Madrid || **Final:** British Library → London

- **Query 30 — Context:** Porta Nigra → Berlin | Mount Longonot → Nairobi | Heimbach → Berlin | Bad Wildbad → Berlin | Coves del Drach → Madrid | Nikkō Tōshō-gū → Tokyo | J. Paul Getty Museum → Washington, D.C. | Homomonument → Amsterdam | Sequoia National Park → Washington, D.C. | Gröna Lund → Stockholm || **Final:** Alnwick Castle → London

- **Query 33 — Context:** Bad Windsheim → Berlin | Bad Endorf → Berlin | KV18 → Cairo | One World Trade Center → Washington, D.C. | Galapagos Islands → Quito | Trinity Cathedral → Moscow | Lia Fáil → Dublin | Nordic Museum → Stockholm | Rök Runestone → Stockholm | Mount Vesuvius → Rome || **Final:** Stadium MK → London

- **Query 41 — Context:** Royal Museum for Central Africa → City of Brussels | Alamo Mission in San Antonio → Washington, D.C. | KV35 → Cairo | Tropaeum Traiani → Bucharest | Novocherkassk Cathedral → Moscow | Spiekeroog → Berlin | Martigny-les-Bains → Paris | Monument to the Sun → Zagreb | Valaam Monastery → Moscow | New Athos Cave → Tbilisi || **Final:** Stonehenge → London

- **Query 57 — Context:** Santa Claus Village → Helsinki | Lion Monument Lucerne → Bern | Fort Sumter → Washington, D.C. | Hoover Dam → Washington, D.C. | Menshikov Palace (Saint Petersburg) → Moscow | Wings of Tatev → Yerevan | Doge&#x27;s Palace, Genoa → Rome | Pennsylvania Academy of the Fine Arts → Washington, D.C. | Atherton Tableland → Canberra | Grande Arche → Paris || **Final:** Buckingham Palace → London

- **Query 65 — Context:** Bavarian National Museum → Berlin | Church of All Saints → Moscow | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Wyk auf Föhr → Berlin | Madinat Al-Zahra → Madrid | Hisarya → Sofia | KV17 → Cairo | Bad Tölz → Berlin | Detroit Institute of Arts → Washington, D.C. | Bad Hönningen → Berlin || **Final:** Chatsworth House → London

- **Query 74 — Context:** Obelisk of Axum → Addis Ababa | Bursa Grand Mosque → Ankara | Ramoji Film City → New Delhi | Dune of Pilat → Paris | Accademia Carrara → Rome | Friedrichskoog → Berlin | Băile Herculane → Bucharest | Sybaris → Rome | Bad König → Berlin | Gallerie dell&#x27;Accademia → Rome || **Final:** Sirius Arena → Moscow

- **Query 84 — Context:** Gülhane Park → Ankara | Pool of Siloam → Jerusalem | Yuste → Madrid | Mazar-e-Quaid → Islamabad | Tomb of Cyrus the Great → Tehran | Orvieto Cathedral → Rome | Wolfegg → Berlin | Upper German-Raetian Limes → Berlin | Pyramid of Userkaf → Cairo | Museo dell&#x27;Opera del Duomo → Rome || **Final:** ArcelorMittal Orbit → London

- **Query 95 — Context:** Chehel Sotun → Tehran | Bad Sülze → Berlin | Sankt Englmar → Berlin | Fingal&#x27;s Cave → London | St. Andrew&#x27;s Church → Warsaw | Walhalla memorial → Berlin | Bischofsgrün → Berlin | Ain Dubai → Abu Dhabi | National Gallery of Victoria → Canberra | Naples National Archaeological Museum → Rome || **Final:** Putuoshan → Beijing

- **Query 97 — Context:** Alcatraz Island → Washington, D.C. | Teylers Museum → Amsterdam | Bad Schmiedeberg → Berlin | Dervio → Rome | Waldbronn → Berlin | Statue of Zeus at Olympia → Athens | Bad Herrenalb → Berlin | Persepolis → Tehran | Castel Sant&#x27;Angelo → Rome | Galata Bridge → Ankara || **Final:** Somerset House → London

- **Query 127 — Context:** Euromast → Amsterdam | Sydney Opera House → Canberra | Gol Gumbaz → New Delhi | Piazza San Marco → Rome | Falkirk Wheel → London | Museum of Fine Arts Boston → Washington, D.C. | Schluchsee → Berlin | Pont du Gard → Paris | Astrid Lindgren&#x27;s World → Stockholm | Bad Krozingen → Berlin || **Final:** Mount Lu → Beijing

- **Query 141 — Context:** 15 July Martyrs Bridge → Ankara | Cappadocia → Ankara | Fortifications of Kotor → Podgorica | Mausoleum of Maussollos → Ankara | İstiklal Avenue → Ankara | Museo di Capodimonte → Rome | Vigeland installation → Oslo | Miniatürk → Ankara | Famine Stela → Cairo | Ushiku Daibutsu → Tokyo || **Final:** Petrie Museum of Egyptian Archaeology → London

- **Query 149 — Context:** Cumalıkızık → Ankara | Cueva de los Verdes → Madrid | Lenzkirch → Berlin | Tecklenburg → Berlin | Bad Kissingen → Berlin | Heimbach → Berlin | Amalienborg → Copenhagen | Ale&#x27;s Stones → Stockholm | Gothenburg Museum of Art → Stockholm | Friedrichskoog → Berlin || **Final:** Tate Britain → London

- **Query 168 — Context:** Disney Adventure World → Paris | Newgrounds → Washington, D.C. | Gol Gumbaz → New Delhi | Củ Chi tunnels → Hanoi | Busko-Zdrój → Warsaw | Abbadia Lariana → Rome | Berchtesgaden → Berlin | Kresty Prison → Moscow | Silesian Stadium → Warsaw | Topkapı Palace → Ankara || **Final:** Covent Garden → London

- **Query 173 — Context:** Basilica of Saint Nicholas → Rome | Travemünde → Berlin | San Agustin archeological park → Bogotá | Alexander Nevsky Lavra → Moscow | Laykyun Sekkya → Naypyidaw | KV20 → Cairo | Merneptah Stele → Cairo | Bad Laasphe → Berlin | Abbadia Lariana → Rome | Höchenschwand → Berlin || **Final:** Tower Bridge → London

- **Query 180 — Context:** St. Florian&#x27;s Gate → Warsaw | Casa Loma → Ottawa | Malente → Berlin | Otrar → Astana | Galata Bridge → Ankara | Tian Tan Buddha → Beijing | Dervio → Rome | Schönwald im Schwarzwald → Berlin | Gateway Arch → Washington, D.C. | Uludağ → Ankara || **Final:** Apsley House → London

- **Query 209 — Context:** Busko-Zdrój → Warsaw | Putuoshan → Beijing | Sultan Ahmed Mosque → Ankara | KV26 → Cairo | İstanbul Modern → Ankara | Narva Triumphal Arch → Moscow | Yıldız Hamidi Mosque → Ankara | Bad Camberg → Berlin | Maes Howe → London | Bad Oeynhausen → Berlin || **Final:** Lion Gate → Athens

- **Query 229 — Context:** Imbros → Ankara | Nonnweiler → Berlin | Rök Runestone → Stockholm | Cyprus Museum → Nicosia | Kalmar Castle → Stockholm | Nordstrand → Berlin | Old House of Bank → Stockholm | Wings of Tatev → Yerevan | Tamme-Lauri oak → Tallinn | Silesian Stadium → Warsaw || **Final:** Sorico → Rome

- **Query 245 — Context:** Museum of Far Eastern Antiquities → Stockholm | Great Smoky Mountains → Washington, D.C. | Sklené Teplice → Bratislava | Naxos → Rome | KV1 → Cairo | Bad Pyrmont → Berlin | Cathedral of the Savior in his Epiphany of Zaragoza → Madrid | Narva Triumphal Arch → Moscow | Colosseum → Rome | Copenhagen Zoo → Copenhagen || **Final:** Sandringham House → London

- **Query 270 — Context:** Summer Garden → Moscow | Carrow Road → London | Sydney Tower → Canberra | Alnwick Castle → London | Lincoln Castle → London | İzmir Clock Tower → Ankara | Natzweiler-Struthof concentration camp → Paris | Tann → Berlin | Museum of Bad Art → Washington, D.C. | Hermannsdenkmal → Berlin || **Final:** Arch of Trajan → Rome

- **Query 279 — Context:** Baltrum → Berlin | Promenade des Anglais → Paris | Odesa Fine Arts Museum → Kyiv | Bad Birnbach → Berlin | Menshikov Palace (Saint Petersburg) → Moscow | National Library of Wales → London | Rietveld Schröder House → Amsterdam | Hong Kong Disneyland → Beijing | Gonbad-e Qabus → Tehran | Neuschwanstein Castle → Berlin || **Final:** Madinat Al-Zahra → Madrid

- **Query 289 — Context:** Palace of Caserta → Rome | Mandello del Lario → Rome | Liberty Bell → Washington, D.C. | Büsum → Berlin | Bad König → Berlin | Cleveland Museum of Art → Washington, D.C. | Gateway Arch → Washington, D.C. | Bad Bentheim → Berlin | Eutin → Berlin | Stützerbach → Berlin || **Final:** Piccadilly Circus → London

- **Query 291 — Context:** Laykyun Sekkya → Naypyidaw | Arlington National Cemetery → Washington, D.C. | Petra → Amman | Luxor Museum → Cairo | Horse Cave → Washington, D.C. | Bad Wilsnack → Berlin | Baltrum → Berlin | Cuxhaven → Berlin | Museum of Fine Arts Ghent (MSK) → City of Brussels | Baiersbronn → Berlin || **Final:** Mount Sanqing → Beijing

- **Query 298 — Context:** Ain Dubai → Abu Dhabi | Soltaniyeh Dome → Tehran | Puy de Dôme → Paris | Bad Bramstedt → Berlin | Banya → Sofia | KV11 → Cairo | Astrid Lindgren&#x27;s World → Stockholm | Europa-Park → Berlin | Bellano → Rome | Pyramid of Userkaf → Cairo || **Final:** Conventico Caves → Madrid

- **Query 300 — Context:** West Lake → Beijing | Sachsenhausen concentration camp → Berlin | Porta San Sebastiano → Rome | Taq-i Kisra → Baghdad | Borkum → Berlin | Wawel → Warsaw | Bad Iburg → Berlin | Todtmoos → Berlin | Royal Palace of Naples → Rome | Darjeeling Himalayan Railway → New Delhi || **Final:** Mansion House → London

- **Query 319 — Context:** City of Space → Paris | Athena Parthenos → Athens | Vigeland installation → Oslo | Bibi Ka Maqbara → New Delhi | Six Flags Magic Mountain → Washington, D.C. | Children&#x27;s Peace Monument → Tokyo | Nemrut → Ankara | Tatranská Lomnica → Bratislava | Alexander Nevsky Cathedral → Warsaw | Ramsau bei Berchtesgaden → Berlin || **Final:** Vindolanda → London

- **Query 328 — Context:** Sasbachwalden → Berlin | Galapagos Islands → Quito | Wild Wadi Water Park → Abu Dhabi | Acropolis of Athens → Athens | Peter and Paul Fortress → Moscow | Palace of Caserta → Rome | Petershagen → Berlin | Glasgow Cathedral → London | Kensington Palace → London | Isny im Allgäu → Berlin || **Final:** Jinggang Mountains → Beijing

- **Query 332 — Context:** Maya Ruins of Tulum → Mexico City | Bilbao Fine Arts Museum → Madrid | Tomb of Jahangir → Islamabad | Disney&#x27;s Animal Kingdom → Washington, D.C. | Danevirke → Berlin | Hadrian&#x27;s Villa → Rome | Bad Schussenried → Berlin | Pinakothek der Moderne → Berlin | Rök Runestone → Stockholm | Canyon de Chelly National Monument → Washington, D.C. || **Final:** Hever Castle → London

- **Query 361 — Context:** Fingal&#x27;s Cave → London | Amber Mountain National Park → Antananarivo | Tower of Hercules → Madrid | Kumu → Tallinn | Museu Nacional d&#x27;Art de Catalunya → Madrid | Thorvaldsen Museum → Copenhagen | Bad Elster → Berlin | Baden → Vienna | Naqsh-e Jahan Square → Tehran | Bad Friedrichshall → Berlin || **Final:** Hospital of Innocents → Rome

- **Query 375 — Context:** Walled Obelisk → Ankara | Denver Art Museum → Washington, D.C. | Danevirke → Berlin | Ali Qapu → Tehran | Machu Picchu → Lima | Thracian Tomb of Kazanlak → Sofia | Dallas Museum of Art → Washington, D.C. | Blue Mosque → Kabul | Bad Schwalbach → Berlin | KV1 → Cairo || **Final:** Palazzo Rosso → Rome

- **Query 399 — Context:** National Archaeological Museum of Athens → Athens | Yusupov Palace on Moika → Moscow | Baabe → Berlin | Grande Arche → Paris | Casa Buonarroti → Rome | Bad Vilbel → Berlin | Aflenz Kurort → Vienna | Bad Vöslau → Vienna | Empire State Building → Washington, D.C. | Oscar Niemeyer International Cultural Centre → Madrid || **Final:** St Martin-in-the-Fields → London

- **Query 412 — Context:** Istanbul Archaeology Museums → Ankara | KV4 → Cairo | Valle dei Templi → Rome | Antequera Dolmens Site → Madrid | Disney&#x27;s Hollywood Studios → Washington, D.C. | KV35 → Cairo | Museu Nacional d&#x27;Art de Catalunya → Madrid | Solomon R. Guggenheim Museum → Washington, D.C. | Tarxien Temples → Valletta | Royal Pavilion &amp; Garden → London || **Final:** Zhangjiajie Glass Bridge → Beijing

- **Query 413 — Context:** Mount Tai → Beijing | Death Valley → Washington, D.C. | Ain Dubai → Abu Dhabi | Galata Bridge → Ankara | Bad Schwalbach → Berlin | Vittskövle Church → Stockholm | Canyon de Chelly National Monument → Washington, D.C. | Gol Gumbaz → New Delhi | Spannagel Cave → Vienna | Osun-Osogbo Grove → Abuja || **Final:** Barbican Centre → London

- **Query 422 — Context:** Tomb of Hafez → Tehran | Ancient Agora of Athens → Athens | Baiersbronn → Berlin | Uzungöl → Ankara | Torre del Oro → Madrid | Märcani Mosque → Moscow | Bad Schwartau → Berlin | Bad Rothenfelde → Berlin | Gonbad-e Qabus → Tehran | Bad Endorf → Berlin || **Final:** Jingpo Lake → Beijing

- **Query 427 — Context:** Thien Duong Cave → Hanoi | Museu Picasso → Madrid | Royal Museums of Fine Arts of Belgium → City of Brussels | Buckow → Berlin | Kraków-Płaszów concentration camp → Warsaw | Redwood National and State Parks → Washington, D.C. | British Museum → London | Cliffs of Moher → Dublin | Musée d&#x27;Art et d&#x27;Histoire de Geneva → Bern | Gammelstad Church Town → Stockholm || **Final:** Baths of Caracalla → Rome

- **Query 492 — Context:** Font-de-Gaume → Paris | Bad Harzburg → Berlin | Salamanca New Cathedral → Madrid | Momine Khatun Mausoleum → Baku | Monastery of Saint John of Rila → Sofia | Hong Kong Museum of Art → Beijing | Altenberg → Berlin | KV18 → Cairo | Bad Wimpfen → Berlin | Bad Wildbad → Berlin || **Final:** Pickford&#x27;s House → London

- **Query 498 — Context:** Kudowa-Zdrój → Warsaw | Bremen Roland → Berlin | Catacombs of Kom el Shoqafa → Cairo | Naqsh-e Jahan Square → Tehran | Bad Sülze → Berlin | KV3 → Cairo | Palazzo Rosso → Rome | Thracian Tomb of Sveshtari → Sofia | Bad Feilnbach → Berlin | Admont Abbey → Vienna || **Final:** Trinity Cathedral → Moscow

- **Query 504 — Context:** Polanica-Zdrój → Warsaw | Śniardwy → Warsaw | Basilica of Notre-Dame de Fourvière → Paris | Świnoujście → Warsaw | Mount Kilimanjaro → Dodoma | KV9 → Cairo | Charminar → New Delhi | Fujian Tulou → Beijing | Hollywood Sign → Washington, D.C. | Fisherman&#x27;s Wharf → Washington, D.C. || **Final:** Roman Baths → London

- **Query 506 — Context:** Königstein im Taunus → Berlin | Schönwald im Schwarzwald → Berlin | Bayrischzell → Berlin | Bad König → Berlin | Ivolginsky Datsan → Moscow | Waldbronn → Berlin | Glasgow Cathedral → London | KV15 → Cairo | İstiklal Avenue → Ankara | Muszyna → Warsaw || **Final:** Pingyao → Beijing

- **Query 537 — Context:** Dune of Pilat → Paris | Bad Orb → Berlin | Chilean National Museum of Fine Arts → Santiago | Cathedral of Valladolid → Madrid | Disneyland Paris → Paris | Palacio Episcopal de Astorga → Madrid | Odesa Fine Arts Museum → Kyiv | Museum Ludwig → Berlin | Bad Sooden-Allendorf → Berlin | Marble Palace → Moscow || **Final:** Toughsheet Community Stadium → London

- **Query 577 — Context:** Sultan Ahmed Mosque → Ankara | Capital Cities and Tombs of the Ancient Koguryo Kingdom → Beijing | Caernarfon Castle → London | Riddarholm Church → Stockholm | Ferdowsi Mausoleum → Tehran | Groeningemuseum → City of Brussels | Sozopol → Sofia | Shah Cheragh shrine → Tehran | City of Arts and Sciences → Madrid | Mandello del Lario → Rome || **Final:** Winterberg → Berlin

- **Query 588 — Context:** Bad Schwartau → Berlin | Miniatürk → Ankara | Arch of Hadrian → Athens | St. Blasien → Berlin | Four Corners Monument → Washington, D.C. | Château de Montsoreau-Museum of Contemporary Art → Paris | Bad Pyrmont → Berlin | Läckö Castle → Stockholm | Freiburg im Breisgau → Berlin | Rothenburg ob der Tauber → Berlin || **Final:** Royal Pavilion &amp; Garden → London

- **Query 591 — Context:** Eyüp Sultan Mosque → Ankara | Fisherman&#x27;s Wharf → Washington, D.C. | Groeningemuseum → City of Brussels | Cologne Cathedral → Berlin | Melsungen → Berlin | Nuruosmaniye Mosque → Ankara | Moskovsky railway station → Moscow | Cueva de los Verdes → Madrid | Königsfeld im Schwarzwald → Berlin | Beylerbeyi Palace → Ankara || **Final:** Mount Song → Beijing

- **Query 592 — Context:** Statue of Zeus at Olympia → Athens | Sukur → Abuja | Reformation Wall → Bern | Conch Republic → Washington, D.C. | Shanhai Pass → Beijing | Ölüdeniz → Ankara | Bad Friedrichshall → Berlin | Weiskirchen → Berlin | Humayun&#x27;s Tomb → New Delhi | Schömberg → Berlin || **Final:** Harrods → London

- **Query 601 — Context:** Czocha Castle → Warsaw | Marktschellenberg → Berlin | Bad Aussee → Vienna | Church of All Saints → Moscow | Alexander Column → Moscow | Lindenfels → Berlin | Vulci → Rome | Kailasa Temple, Ellora → New Delhi | Torre del Oro → Madrid | Gulangyu → Beijing || **Final:** British Museum → London

- **Query 607 — Context:** tomb of Tutankhamun → Cairo | Brooklyn Museum → Washington, D.C. | Bad Kreuznach → Berlin | Hearst Castle → Washington, D.C. | Aqueduct of Segovia → Madrid | Schwangau → Berlin | St. Paul&#x27;s Church, Frankfurt am Main → Berlin | Homomonument → Amsterdam | Design Museum Holon → Jerusalem | Gothenburg Museum of Art → Stockholm || **Final:** Pyramid of Cestius → Rome

- **Query 609 — Context:** Cappadocia → Ankara | Lion of Judah → Addis Ababa | Willis Tower → Washington, D.C. | Space Needle → Washington, D.C. | J. Paul Getty Museum → Washington, D.C. | Bad Säckingen → Berlin | Euromast → Amsterdam | Everland → Seoul | Royal Palace of Milan → Rome | Orvieto Cathedral → Rome || **Final:** Tomb of Absalom → Jerusalem

- **Query 612 — Context:** Marmurova Pechera → Kyiv | Krynica-Zdrój → Warsaw | Sammallahdenmäki → Helsinki | Dierhagen → Berlin | Bad Feilnbach → Berlin | Museu Picasso → Madrid | Busko-Zdrój → Warsaw | Gripsholm Castle → Stockholm | Hirschhorn → Berlin | Bad Wimpfen → Berlin || **Final:** Alexander Column → Moscow

- **Query 644 — Context:** Sun Yat-sen Mausoleum → Beijing | Royal Museums of Fine Arts of Belgium → City of Brussels | Gardens of Bomarzo → Rome | Kraków-Płaszów concentration camp → Warsaw | Milan Cathedral → Rome | Torre del Oro → Madrid | Trafalgar Square → London | Royal Pavilion &amp; Garden → London | Antwerp City Hall → City of Brussels | Fingal&#x27;s Cave → London || **Final:** Skull Tower → Belgrade

- **Query 647 — Context:** Bad Krozingen → Berlin | Taj Mahal → New Delhi | Wustrow → Berlin | Stadium MK → London | Świeradów-Zdrój → Warsaw | Walled Obelisk → Ankara | Metropolitan Museum of Art → Washington, D.C. | Niagara Falls → Ottawa | Colossi of Memnon → Cairo | Wittdün auf Amrum → Berlin || **Final:** Metropolitan Cathedral Basilica of St. James the Apostle → Madrid

- **Query 650 — Context:** Gur-e Amir → Tashkent | Astrid Lindgren&#x27;s World → Stockholm | Cascata delle Marmore → Rome | Disney Adventure World → Paris | Langeoog → Berlin | Museum of Anatolian Civilizations → Ankara | Shanhai Pass → Beijing | Imam Reza Shrine → Tehran | Cathedral of the Savior in his Epiphany of Zaragoza → Madrid | Al Khazneh → Amman || **Final:** Big Ben → London

- **Query 658 — Context:** Tabernas Desert → Madrid | Khaju Bridge → Tehran | Racławice Panorama → Warsaw | Ferapontov Monastery → Moscow | Columbus Monument → Madrid | Baden → Vienna | Bellano → Rome | Holstentor → Berlin | Fujian Tulou → Beijing | Timmendorfer Strand → Berlin || **Final:** Burghley House → London

- **Query 665 — Context:** Admont Abbey → Vienna | Galata Tower → Ankara | Eisriesenwelt → Vienna | Seikilos epitaph → Athens | Efteling → Amsterdam | Goa Gajah → Jakarta | Bertha Benz Memorial Route → Berlin | Segovia Cathedral → Madrid | Shah Mosque → Tehran | Bad Grund → Berlin || **Final:** Royal Academy of Arts → London

- **Query 682 — Context:** San Francisco Museum of Modern Art → Washington, D.C. | Yellowstone National Park → Washington, D.C. | Tamme-Lauri oak → Tallinn | Art Gallery of South Australia → Canberra | Church of the Savior on Blood → Moscow | National Library of Wales → London | Pura Luhur → Jakarta | Rijksmuseum → Amsterdam | Diamond Head → Washington, D.C. | Petra → Amman || **Final:** Dubino → Rome

- **Query 711 — Context:** Süleymaniye Mosque → Ankara | Sinan Pasha Mosque → Prishtina | Nonnweiler → Berlin | Nilgiri Mountain Railway → New Delhi | The Motherland Calls → Moscow | Oberstdorf → Berlin | Rök Runestone → Stockholm | Bad Zwischenahn → Berlin | Siegsdorf → Berlin | Hitzacker → Berlin || **Final:** Dulwich Picture Gallery → London

- **Query 721 — Context:** Stirling Castle → London | Roman Baths → London | Cueva de Nerja → Madrid | Sozopol → Sofia | Kraków Barbican → Warsaw | Mecca → Riyadh | Niterói Contemporary Art Museum → Brasília | Schönwald im Schwarzwald → Berlin | Bad Düben → Berlin | Mount Song → Beijing || **Final:** Famine Stela → Cairo

- **Query 738 — Context:** Vallendar → Berlin | Great Smoky Mountains → Washington, D.C. | Arch of the Sergii → Zagreb | Arch of Hadrian → Athens | Bad Blankenburg → Berlin | Blue Mosque → Kabul | Niterói Contemporary Art Museum → Brasília | Bad Harzburg → Berlin | Wangerooge → Berlin | Nordic Museum → Stockholm || **Final:** Blackpool Tower → London

- **Query 770 — Context:** Grand Bazaar → Ankara | Bischofsgrün → Berlin | Arch of Galerius and Rotunda → Athens | Cave of Swallows → Mexico City | Fort Sumter → Washington, D.C. | Yumen Pass → Beijing | Wieliczka Salt Mine → Warsaw | Kalyan Minaret → Tashkent | Ani → Ankara | Bad Salzuflen → Berlin || **Final:** Piton des Neiges → Paris

- **Query 772 — Context:** Bad Kreuznach → Berlin | KV12 → Cairo | Palace of Versailles → Paris | Lion of Judah → Addis Ababa | Solovetsky Monastery → Moscow | Garmisch-Partenkirchen → Berlin | Brooklyn Museum → Washington, D.C. | Nelson&#x27;s Column → London | Rök Runestone → Stockholm | Stromberg → Berlin || **Final:** Astorga Cathedral → Madrid

- **Query 786 — Context:** Sublime Porte → Ankara | Catholic Church of St. Catherine → Moscow | Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar | Rabka-Zdrój → Warsaw | Malmö Castle → Stockholm | Yıldız Hamidi Mosque → Ankara | Mausoleum of Khoja Ahmed Yasawi → Astana | Millau Viaduct → Paris | Blackpool Tower → London | Uzungöl → Ankara || **Final:** Al-Rifa&#x27;i Mosque → Cairo

- **Query 809 — Context:** Silesian Stadium → Warsaw | Orvieto Cathedral → Rome | Krynica-Zdrój → Warsaw | Bad Driburg → Berlin | Abbadia Lariana → Rome | Winchester Mystery House → Washington, D.C. | Cathedral of Zamora → Madrid | CN Tower → Ottawa | Wissen → Berlin | Masuleh → Tehran || **Final:** Hampton Court Palace → London

- **Query 830 — Context:** Tokyo Disneyland → Tokyo | Wiesbaden → Berlin | Oberstdorf → Berlin | Susa → Tehran | Ferapontov Monastery → Moscow | Blenheim Palace → London | The Cloisters → Washington, D.C. | Serdobsk → Moscow | Ortaköy Mosque → Ankara | Murnau am Staffelsee → Berlin || **Final:** Teide → Madrid

- **Query 837 — Context:** Nanjing Museum → Beijing | Iglesia de la Concepción → Madrid | Naxos → Rome | Troldhaugen → Oslo | Spice Bazaar → Ankara | Chełmno extermination camp → Warsaw | Newgrounds → Washington, D.C. | Vulci → Rome | Mount Wutai → Beijing | Walhalla memorial → Berlin || **Final:** Homomonument → Amsterdam

- **Query 838 — Context:** Mazar-e-Quaid → Islamabad | Sukur → Abuja | Baabe → Berlin | Puente Nuevo → Madrid | Meteor Crater → Washington, D.C. | Pinakothek der Moderne → Berlin | Bad Blankenburg → Berlin | Serpentine Galleries → London | Freud Museum London → London | Besakih → Jakarta || **Final:** Shanhai Pass → Beijing

- **Query 858 — Context:** Bad Bayersoien → Berlin | Fischen im Allgäu → Berlin | Old Faithful → Washington, D.C. | Naumburg → Berlin | Promenade des Anglais → Paris | Mount Kilimanjaro → Dodoma | Bad Kreuznach → Berlin | Poverty Point → Washington, D.C. | Holy Trinity Column in Olomouc → Prague | Palazzo Vecchio → Rome || **Final:** National Portrait Gallery → London

- **Query 863 — Context:** Tomb of Caecilia Metella → Rome | Bad Kreuznach → Berlin | Herbstein → Berlin | Alhambra → Madrid | Jaén Cathedral → Madrid | Shah Cheragh shrine → Tehran | Dervio → Rome | Nilgiri Mountain Railway → New Delhi | War of Independence Victory Column → Tallinn | Museum of Far Eastern Antiquities → Stockholm || **Final:** Portman Road → London

- **Query 867 — Context:** Norddorf → Berlin | Wild Wadi Water Park → Abu Dhabi | The Huntington Library, Art Museum, and Botanical Gardens → Washington, D.C. | Omonoia Square → Athens | Admiralty Arch → London | Bad Camberg → Berlin | BMW Welt → Berlin | The Cloisters → Washington, D.C. | Lahnstein → Berlin | Dobšinská Ice Cave → Bratislava || **Final:** Our Lady of the Pillar → Madrid

- **Query 876 — Context:** Templin → Berlin | Masuleh → Tehran | Mount Etna → Rome | Mount Longonot → Nairobi | Mount Wutai → Beijing | Bad Birnbach → Berlin | 15 July Martyrs Bridge → Ankara | Canaima National Park → Caracas | Bad Soden am Taunus → Berlin | Bad Gastein → Vienna || **Final:** Serpentine Galleries → London

- **Query 881 — Context:** Tel Aviv Museum of Art → Jerusalem | Sigüenza Cathedral → Madrid | Warwick Castle → London | Triberg im Schwarzwald → Berlin | Dikteon Andron → Athens | Downing Street → London | Canadian Museum of History → Ottawa | Museum of Fine Arts Ghent (MSK) → City of Brussels | Casa Vicens → Madrid | Archcathedral Basilica of St. Peter and St. Paul → Warsaw || **Final:** Jamkaran Mosque → Tehran

- **Query 883 — Context:** Admont Abbey → Vienna | Bad Bentheim → Berlin | Bad Saulgau → Berlin | İstiklal Avenue → Ankara | Spiekeroog → Berlin | Chilean National Museum of Fine Arts → Santiago | Monument Valley → Washington, D.C. | Bad Königshofen im Grabfeld → Berlin | Yuste → Madrid | Bad Rodach → Berlin || **Final:** Hadrian&#x27;s Wall → London

- **Query 893 — Context:** Sequoia National Park → Washington, D.C. | Ħaġar Qim → Valletta | Magic Kingdom → Washington, D.C. | Muszyna → Warsaw | National Museum of Iran → Tehran | Stockholm City Hall → Stockholm | City of Arts and Sciences → Madrid | Altaussee → Vienna | Central Stadium Yekaterinburg → Moscow | Athena Parthenos → Athens || **Final:** Victoria and Albert Museum → London

- **Query 911 — Context:** Popeye Village → Valletta | Mariánské Lázně → Prague | Reformation Wall → Bern | Grūtas Park → Vilnius | Ninth Fort → Vilnius | Gardaland → Rome | Medici Chapels → Rome | Arch of Galerius and Rotunda → Athens | Heligoland → Berlin | Burj Khalifa → Abu Dhabi || **Final:** Kensington Palace → London

- **Query 936 — Context:** Sankt Peter-Ording → Berlin | Wellington Arch → London | Kingda Ka → Washington, D.C. | Bad Salzungen → Berlin | Statue of Liberty → Washington, D.C. | Fingal&#x27;s Cave → London | Acropolis of Athens → Athens | Laykyun Sekkya → Naypyidaw | Bad Breisig → Berlin | Bad Säckingen → Berlin || **Final:** Yungang Grottoes → Beijing

- **Query 938 — Context:** Lychakiv Cemetery → Kyiv | Hinterzarten → Berlin | Menshikov Palace (Saint Petersburg) → Moscow | Palazzo Vecchio → Rome | Cyprus Museum → Nicosia | Old Town of Lijiang → Beijing | Beylerbeyi Palace → Ankara | Russian Museum → Moscow | Bad Vöslau → Vienna | Banya → Sofia || **Final:** Basilica of Our Lady of the Pillar → Madrid

- **Query 945 — Context:** Natzweiler-Struthof concentration camp → Paris | Heiligenhafen → Berlin | Stützerbach → Berlin | Truskavets → Kyiv | Bad Lauterberg im Harz → Berlin | Sasbachwalden → Berlin | Piazza San Marco → Rome | Winchester Mystery House → Washington, D.C. | Viñales Valley → Havana | Tabernas Desert → Madrid || **Final:** Mount Tai → Beijing

- **Query 948 — Context:** Bad Friedrichshall → Berlin | Sankt Englmar → Berlin | Stonehenge → London | Arch of Galerius and Rotunda → Athens | Royal Museums of Fine Arts of Belgium → City of Brussels | Columbus Circle → Washington, D.C. | Bad Hindelang → Berlin | Carlsbad Caverns National Park → Washington, D.C. | Orkhon inscriptions → Ulaanbaatar | Pura Luhur → Jakarta || **Final:** Puente romano → Madrid

- **Query 953 — Context:** Museo dell&#x27;Opera del Duomo → Rome | Uzungöl → Ankara | Bad Kleinkirchheim → Vienna | Bad Kreuznach → Berlin | Bad Waldsee → Berlin | Spiekeroog → Berlin | Druskininkai → Vilnius | Kalyan Minaret → Tashkent | Juventus Stadium → Rome | Postojna Cave → Ljubljana || **Final:** Ludlow Castle → London

- **Query 960 — Context:** Bad Emstal → Berlin | Lion Gate → Athens | Willis Tower → Washington, D.C. | Sofiyivsky Park → Kyiv | Stützerbach → Berlin | Bad Berka → Berlin | Heligoland → Berlin | Ambras Castle → Vienna | St Mark&#x27;s Basilica → Rome | Bad Herrenalb → Berlin || **Final:** Trafalgar Square → London

- **Query 996 — Context:** Egyptian pyramids → Cairo | St. Nicholas’ Church, Hamburg → Berlin | KV15 → Cairo | Chełmno extermination camp → Warsaw | Museo Correr → Rome | Nürburg → Berlin | Mausoleum of Khoja Ahmed Yasawi → Astana | Mausoleum of Theodoric → Rome | Jastrzębie-Zdrój → Warsaw | Chengde Mountain Resort and its outlying temples → Beijing || **Final:** Banqueting House → London

- **Query 1036 — Context:** Tomb of Cyrus the Great → Tehran | KV4 → Cairo | Aiguille du Midi → Paris | Ludlow Castle → London | Badajoz Cathedral → Madrid | Gothenburg Museum of Art → Stockholm | Banqueting House → London | Kimbell Art Museum → Washington, D.C. | Bad Brambach → Berlin | Spannagel Cave → Vienna || **Final:** West Lake → Beijing

- **Query 1047 — Context:** Fatima Masumeh Shrine → Tehran | Zhangjiajie Glass Bridge → Beijing | Kalmar Castle → Stockholm | Teide → Madrid | The Nelson-Atkins Museum of Art → Washington, D.C. | Choragic Monument of Lysicrates → Athens | Tomb of I&#x27;timād-ud-Daulah → New Delhi | Fatih Istanbul Mosque → Ankara | Madinat Al-Zahra → Madrid | Imam Reza Shrine → Tehran || **Final:** Warwick Castle → London

- **Query 1061 — Context:** Mausoleum of Theodoric → Rome | Dolmen of Menga → Madrid | Mevlâna Museum → Ankara | Ladonia → Stockholm | Vallendar → Berlin | Putuoshan → Beijing | Bad Schmiedeberg → Berlin | Ballabio → Rome | Obelisk of Axum → Addis Ababa | Potala Palace → Beijing || **Final:** Marble Arch → London

- **Query 1064 — Context:** Busan → Seoul | Bronze Horseman → Moscow | Museum of Fine Arts, Houston → Washington, D.C. | Narva Triumphal Arch → Moscow | The Little Mermaid → Copenhagen | Pool of Siloam → Jerusalem | Brilon → Berlin | Grasellenbach → Berlin | Philopappos Monument → Athens | Salar Jung Museum → New Delhi || **Final:** Lincoln Castle → London

- **Query 1069 — Context:** Hermannsdenkmal → Berlin | Cave of Altamira and Paleolithic Cave Art of Northern Spain → Madrid | Bad Zwischenahn → Berlin | Solovetsky Monastery → Moscow | Cedar Point → Washington, D.C. | Kresty Prison → Moscow | Grande Arche → Paris | Mausoleum of Galla Placidia → Rome | Fort Jesus Museum → Nairobi | Norton Simon Museum → Washington, D.C. || **Final:** Albert Memorial → London

- **Query 1129 — Context:** Amalienborg → Copenhagen | Szczawnica → Warsaw | Koporye → Moscow | Lindenfels → Berlin | Pyramid of Userkaf → Cairo | Bad Lippspringe → Berlin | Piton des Neiges → Paris | Royal Palace of Naples → Rome | Natzweiler-Struthof concentration camp → Paris | Burj Khalifa → Abu Dhabi || **Final:** Tate Modern → London

- **Query 1150 — Context:** Sky Tower → Wellington | Ninth Fort → Vilnius | Yumen Pass → Beijing | Königsberg Cathedral → Moscow | Weilburg → Berlin | Postojna Cave → Ljubljana | Fundació Joan Miró → Madrid | Brooklyn Museum → Washington, D.C. | Museum of Fine Arts of Lyon → Paris | Wild Wadi Water Park → Abu Dhabi || **Final:** Hatfield House → London

- **Query 1152 — Context:** Benaki Museum → Athens | Jedlina-Zdrój → Warsaw | Burj Khalifa → Abu Dhabi | Mesha Stele → Amman | Koporye → Moscow | Bad Driburg → Berlin | Gernsbach → Berlin | Trinity Cathedral → Moscow | Baabe → Berlin | Kneiff → Luxembourg || **Final:** Masuleh → Tehran

- **Query 1160 — Context:** Ny Carlsberg Glyptotek → Copenhagen | Bad Neustadt an der Saale → Berlin | Galata Tower → Ankara | Tower of the Winds → Athens | Turkish and Islamic Arts Museum → Ankara | Serengeti National Park → Dodoma | Istanbul Archaeology Museums → Ankara | Rottach-Egern → Berlin | Sümela Monastery → Ankara | Jinggang Mountains → Beijing || **Final:** Brick Lane → London

- **Query 1176 — Context:** National Museum of Iran → Tehran | Izium mass graves → Kyiv | Olympia → Athens | Gardens of Bomarzo → Rome | Friedrichroda → Berlin | Sontra → Berlin | Pyramid of Cestius → Rome | Călimănești → Bucharest | Piazza San Marco → Rome | Fountains Abbey → London || **Final:** Basilica of Candelaria → Madrid

- **Query 1194 — Context:** Bad Segeberg → Berlin | Frasassi Caves → Rome | Empire State Building → Washington, D.C. | Gateway Arch → Washington, D.C. | Kneiff → Luxembourg | Kalmar Castle → Stockholm | Vallendar → Berlin | Cueva de las Manos → Buenos Aires | Athena Promachos → Athens | Kizhi Pogost → Moscow || **Final:** Nelson&#x27;s Column → London

- **Query 1205 — Context:** Shah Mosque → Tehran | Bad Breisig → Berlin | Avtovo → Moscow | West Bali National Park → Jakarta | Bad Alexandersbad → Berlin | Las Médulas → Madrid | Old Faithful → Washington, D.C. | Cascata delle Marmore → Rome | Bargello National Museum → Rome | Yellowstone National Park → Washington, D.C. || **Final:** Bingling Temple → Beijing

- **Query 1231 — Context:** Sun Yat-sen Mausoleum → Beijing | Röbel → Berlin | Tomb of Safdar Jang → New Delhi | Angel Falls → Caracas | Si-o-se Pol → Tehran | Arch of Trajan → Rome | Mariánské Lázně → Prague | KV10 → Cairo | Chichen Itza → Mexico City | Bad Freienwalde → Berlin || **Final:** Charing Cross → London

- **Query 1234 — Context:** KV6 → Cairo | San Francisco Museum of Modern Art → Washington, D.C. | Bad Laasphe → Berlin | Bad Ischl → Vienna | Bad Rappenau → Berlin | Doge&#x27;s Palace, Genoa → Rome | Museum of San Marco → Rome | Atakule → Ankara | Grand Canal → Rome | Kazimierz → Warsaw || **Final:** Kew Palace → London

- **Query 1265 — Context:** Düden Waterfalls → Ankara | Hever Castle → London | Statue of Zeus at Olympia → Athens | Holstentor → Berlin | Bad Hönningen → Berlin | Kyllburg → Berlin | Fatih Istanbul Mosque → Ankara | Wawel Cathedral → Warsaw | Nümbrecht → Berlin | Bad Breisig → Berlin || **Final:** Iglesia de la Concepción → Madrid

- **Query 1287 — Context:** Bad Rodach → Berlin | Städel Museum → Berlin | Patriarchate of Peja → Belgrade | Izium mass graves → Kyiv | Baltrum → Berlin | Juventus Stadium → Rome | Europa-Park → Berlin | Fort Jesus Museum → Nairobi | Cuxhaven → Berlin | Lincoln Castle → London || **Final:** Dolmen of Menga → Madrid

- **Query 1315 — Context:** Ortaköy → Ankara | Shanhai Pass → Beijing | Gonio → Tbilisi | Yıldız Hamidi Mosque → Ankara | Zingst → Berlin | Bad Lippspringe → Berlin | Great Pyramid of Giza → Cairo | Musée Fabre → Paris | Lascaux → Paris | Eyüp Sultan Mosque → Ankara || **Final:** Tower of the Winds → Athens

- **Query 1319 — Context:** KV2 → Cairo | Bad Elster → Berlin | Serpent Column → Ankara | Church of All Saints → Moscow | Yuriev Monastery → Moscow | Khaju Bridge → Tehran | Königstein im Taunus → Berlin | Marmurova Pechera → Kyiv | Aulendorf → Berlin | Kumu → Tallinn || **Final:** Kenwood House → London

- **Query 1330 — Context:** Gateway Arch → Washington, D.C. | Gemäldegalerie Alte Meister → Berlin | KV57 → Cairo | Museum of Fine Arts of Lyon → Paris | Nümbrecht → Berlin | Schwerin Castle → Berlin | Nieheim → Berlin | Epcot → Washington, D.C. | Al-Rifa&#x27;i Mosque → Cairo | Megara Hyblaea → Rome || **Final:** Star of Nanchang → Beijing

- **Query 1359 — Context:** Pulkovo Observatory → Moscow | Zhangjiajie Glass Bridge → Beijing | Titisee-Neustadt → Berlin | Homomonument → Amsterdam | Royal Palace of La Granja de San Ildefonso → Madrid | Milan Cathedral → Rome | St. Blasien → Berlin | Herzog Anton Ulrich Museum → Berlin | Kingda Ka → Washington, D.C. | Stromberg → Berlin || **Final:** Glastonbury Tor → London

- **Query 1383 — Context:** Blagaj, Mostar → Sarajevo | Vallendar → Berlin | Monument Valley → Washington, D.C. | Louisiana Museum of Modern Art → Copenhagen | KV14 → Cairo | Bad Bramstedt → Berlin | Disneyland → Washington, D.C. | Palazzo Rosso → Rome | Arch of Galerius and Rotunda → Athens | Museo dell&#x27;Opera del Duomo → Rome || **Final:** Mount Wutai → Beijing

**Ambiguous (45)**

- **Query 2 — Context:** Burj Khalifa → Abu Dhabi | Heiligendamm → Berlin | Great Ocean Road → Canberra | Mnajdra → Valletta | Stadium MK → London | Grand Canal → Rome | Astrid Lindgren&#x27;s World → Stockholm | Bad Köstritz → Berlin | Christ the King statue → Warsaw | Bad Marienberg → Berlin || **Final:** Mazar-e-Quaid → Islamabad

- **Query 59 — Context:** Golden Gate → Moscow | Monument to the Great Fire of London → London | Chatsworth House → London | National Museum in Wrocław → Warsaw | Kunstkamera → Moscow | Akbar&#x27;s Tomb → New Delhi | Fingal&#x27;s Cave → London | KV3 → Cairo | Tsūtenkaku → Tokyo | Meteor Crater → Washington, D.C. || **Final:** Igel Column → Berlin

- **Query 88 — Context:** Goa Gajah → Jakarta | Stonehenge → London | Tropaeum Alpium → Paris | Bad Salzdetfurth → Berlin | Bibi Ka Maqbara → New Delhi | Wieliczka Salt Mine → Warsaw | KV2 → Cairo | Golden Circle → Reykjavík | KV8 → Cairo | İstiklal Avenue → Ankara || **Final:** Novocherkassk Cathedral → Moscow

- **Query 137 — Context:** Ahrenshoop → Berlin | Hadrian&#x27;s Villa → Rome | Gothenburg Museum of Art → Stockholm | Bad Liebenzell → Berlin | Dahme → Berlin | Pellworm → Berlin | Radcliffe Camera → London | Ħaġar Qim → Valletta | Acropolis Museum → Athens | Montreal Museum of Fine Arts → Ottawa || **Final:** Statens Museum for Kunst → Copenhagen

- **Query 163 — Context:** Ramoji Film City → New Delhi | Alexander Nevsky Lavra → Moscow | Besakih → Jakarta | Mount Vesuvius → Rome | Brick Lane → London | Peter and Paul Fortress → Moscow | Mount Longonot → Nairobi | Soltau → Berlin | National Museum of Pakistan → Islamabad | Bad Bevensen → Berlin || **Final:** Alcázar of Toledo → Madrid

- **Query 176 — Context:** Durham Castle → London | St. Blasien → Berlin | Gol Gumbaz → New Delhi | Golden Gate Bridge → Washington, D.C. | Gülhane Park → Ankara | Bad Bentheim → Berlin | Carlsbad Caverns National Park → Washington, D.C. | Scrovegni Chapel → Rome | Czocha Castle → Warsaw | Acropolis of Athens → Athens || **Final:** Pura Luhur → Jakarta

- **Query 182 — Context:** Brest Fortress → Minsk | Royal Museum for Central Africa → City of Brussels | Big Sur → Washington, D.C. | Tropaeum Traiani → Bucharest | Mauritshuis → Amsterdam | Al-Masjid Al-Haram → Riyadh | Kunsthaus Graz → Vienna | Golden Gate Park → Washington, D.C. | Malmö Castle → Stockholm | Brooklyn Museum → Washington, D.C. || **Final:** Porta San Sebastiano → Rome

- **Query 197 — Context:** Sublime Porte → Ankara | Alte Pinakothek → Berlin | Turkish and Islamic Arts Museum → Ankara | Fort Sumter → Washington, D.C. | Ottobeuren → Berlin | Arch of Hadrian → Athens | Cathedral of Zamora → Madrid | Lascaux → Paris | Saihō-ji → Tokyo | Taj Mahal → New Delhi || **Final:** Admiralty Arch → London

- **Query 244 — Context:** Triberg im Schwarzwald → Berlin | Osmangazi Bridge → Ankara | Fifth Avenue → Washington, D.C. | Royal Museum for Central Africa → City of Brussels | Guédelon Castle → Paris | Chichen Itza → Mexico City | Bad Zwischenahn → Berlin | Sklené Teplice → Bratislava | Lahnstein → Berlin | Bad Frankenhausen → Berlin || **Final:** Downing Street → London

- **Query 256 — Context:** Victoria and Albert Museum → London | Bad Rappenau → Berlin | Tamme-Lauri oak → Tallinn | Alexander Column → Moscow | Bad Homburg vor der Höhe → Berlin | Roman Walls of Lugo → Madrid | Empire State Building → Washington, D.C. | Postojna Cave → Ljubljana | Sozopol → Sofia | Disneyland Park → Paris || **Final:** Treblinka extermination camp → Warsaw

- **Query 273 — Context:** The Huntington Library, Art Museum, and Botanical Gardens → Washington, D.C. | Gur-e Amir → Tashkent | Druskininkai → Vilnius | Vjetrenica → Sarajevo | Aljafería → Madrid | Ludlow Castle → London | Rijksmuseum → Amsterdam | Świeradów-Zdrój → Warsaw | Bara Imambara → New Delhi | Keukenhof → Amsterdam || **Final:** Thorvaldsen Museum → Copenhagen

- **Query 302 — Context:** Acropolis of Athens → Athens | Majuli → New Delhi | Great Pyramid of Giza → Cairo | Bad Zwischenahn → Berlin | Schluchsee → Berlin | Pont du Gard → Paris | Canaima National Park → Caracas | Caernarfon Castle → London | Bad Liebenzell → Berlin | KV20 → Cairo || **Final:** Summer Garden → Moscow

- **Query 336 — Context:** Neubulach → Berlin | Sofiyivsky Park → Kyiv | Museo di Capodimonte → Rome | Casa Vicens → Madrid | Medici Chapels → Rome | Macau Tower → Beijing | Shanghai Disneyland Park → Beijing | Smrdáky → Bratislava | Bad Heilbrunn → Berlin | Osun-Osogbo Grove → Abuja || **Final:** Liseberg → Stockholm

- **Query 384 — Context:** Dolmen of Viera → Madrid | Atherton Tableland → Canberra | Puy de Dôme → Paris | Ruhpolding → Berlin | J. Paul Getty Museum → Washington, D.C. | Tomb of Jahangir → Islamabad | Murtala Muhammed International Airport → Abuja | Iglesia de la Concepción → Madrid | India Gate → New Delhi | Bad Schwalbach → Berlin || **Final:** Palazzo Barberini → Rome

- **Query 391 — Context:** Bad Sassendorf → Berlin | Pool of Siloam → Jerusalem | Bad Vöslau → Vienna | Bad Grund → Berlin | Bad Camberg → Berlin | Athena Parthenos → Athens | Ming Xiaoling → Beijing | Bad Mergentheim → Berlin | Bad Driburg → Berlin | Colossus of Rhodes → Athens || **Final:** Althorp → London

- **Query 450 — Context:** Bad Griesbach im Rottal → Berlin | Alexander Nevsky Lavra → Moscow | Eisriesenwelt → Vienna | Aflenz Kurort → Vienna | Freudenstadt → Berlin | Al Khazneh → Amman | Turkish and Islamic Arts Museum → Ankara | Feldherrnhalle → Berlin | Mandello del Lario → Rome | Fatima Masumeh Shrine → Tehran || **Final:** Windsor Castle → London

- **Query 472 — Context:** Atherton Tableland → Canberra | Inveraray Castle → London | Hoover Dam → Washington, D.C. | Al Khazneh → Amman | Europa-Park → Berlin | Porta San Sebastiano → Rome | Susa → Tehran | Maiden&#x27;s Tower → Ankara | Fifth Avenue → Washington, D.C. | Altenberg → Berlin || **Final:** Krakus Mound → Warsaw

- **Query 494 — Context:** Odesa Fine Arts Museum → Kyiv | The Motherland Calls → Moscow | Naracoorte Caves National Park → Canberra | Rainbow Bridge National Monument → Washington, D.C. | Bad Wörishofen → Berlin | Seikilos epitaph → Athens | Kunstkamera → Moscow | Vjetrenica → Sarajevo | St. Mary&#x27;s Basilica in Gdańsk → Warsaw | St. Nicholas Naval Cathedral, St. Petersburg → Moscow || **Final:** Valle dei Templi → Rome

- **Query 516 — Context:** Krakus Mound → Warsaw | Örebro Castle → Stockholm | Kunsthaus Graz → Vienna | Bad Sülze → Berlin | Einsiedeln Abbey → Bern | Salamanca New Cathedral → Madrid | Nizhny Novgorod Kremlin → Moscow | Novocherkassk Cathedral → Moscow | Nikkō Tōshō-gū → Tokyo | Shanghai World Financial Center → Beijing || **Final:** Grande Arche → Paris

- **Query 538 — Context:** Museum of Far Eastern Antiquities → Stockholm | Neuschwanstein Castle → Berlin | Deidesheim → Berlin | Galata Tower → Ankara | Admiralty Arch → London | Pamplona Cathedral → Madrid | Museum of Contemporary Art, Los Angeles → Washington, D.C. | Fort Jesus Museum → Nairobi | Museum of Modern Art of Republika Srpska → Sarajevo | Carlsbad Caverns National Park → Washington, D.C. || **Final:** Menshikov Palace (Saint Petersburg) → Moscow

- **Query 586 — Context:** Postojna Cave → Ljubljana | Segovia Cathedral → Madrid | National Museum of Pakistan → Islamabad | Bad Kleinkirchheim → Vienna | Hermannsdenkmal → Berlin | Spa → City of Brussels | Fisherman&#x27;s Wharf → Washington, D.C. | Piantedo → Rome | Su Nuraxi di Barumini → Rome | Circus Maximus → Rome || **Final:** Trinity Lavra of St. Sergius → Moscow

- **Query 670 — Context:** Wuppertal Schwebebahn → Berlin | DeviantArt → Washington, D.C. | KV8 → Cairo | Mammoth Cave National Park → Washington, D.C. | Column of Constantine → Ankara | Şehzade Mosque → Ankara | Bad Reichenhall → Berlin | Domica → Bratislava | Traben-Trarbach → Berlin | Thorvaldsen Museum → Copenhagen || **Final:** Bletchley Park → London

- **Query 705 — Context:** Grand Bazaar → Ankara | Ferapontov Monastery → Moscow | St. Mary&#x27;s Basilica → Warsaw | Munch Museum → Oslo | Bad Camberg → Berlin | Portman Road → London | Bad Bocklet → Berlin | Avtovo → Moscow | Scharbeutz → Berlin | Castel Sant&#x27;Angelo → Rome || **Final:** Hisarya → Sofia

- **Query 714 — Context:** Kenilworth Castle → London | Neubulach → Berlin | St. Florian&#x27;s Gate → Warsaw | Uraniborg → Stockholm | Ladonia → Stockholm | Walled Obelisk → Ankara | Sequoia National Park → Washington, D.C. | KV7 → Cairo | Baden-Baden → Berlin | Kew Palace → London || **Final:** La Défense → Paris

- **Query 724 — Context:** Museo Egizio In Turin (IT) → Rome | Potala Palace → Beijing | Everland → Seoul | Zhouzhuang Town → Beijing | Willis Tower → Washington, D.C. | Chichen Itza → Mexico City | New Athos Cave → Tbilisi | Nanjing Museum → Beijing | Rockefeller Center → Washington, D.C. | Kühlungsborn → Berlin || **Final:** Aqueduct of Segovia → Madrid

- **Query 859 — Context:** Busan → Seoul | Denver Art Museum → Washington, D.C. | Naples National Archaeological Museum → Rome | Bad Schussenried → Berlin | Archcathedral Basilica of St. Peter and St. Paul → Warsaw | Bad Wünnenberg → Berlin | Luxor Museum → Cairo | Hever Castle → London | Old Faithful → Washington, D.C. | Nanjing Museum → Beijing || **Final:** Puente Nuevo → Madrid

- **Query 860 — Context:** Galleria dell&#x27;Accademia → Rome | Pombia Safari Park → Rome | Tomb of Safdar Jang → New Delhi | Arches National Park → Washington, D.C. | Bad Kreuznach → Berlin | Universal Studios Japan → Tokyo | Jasna Góra Monastery → Warsaw | Bamburgh Castle → London | Ale&#x27;s Stones → Stockholm | iron pillar of Delhi → New Delhi || **Final:** Tivoli Gardens → Copenhagen

- **Query 869 — Context:** Grūtas Park → Vilnius | Alte Pinakothek → Berlin | Bertha Benz Memorial Route → Berlin | Bad Kissingen → Berlin | Martigny-les-Bains → Paris | Tomb of Askia → Bamako | Prophet&#x27;s Mosque → Riyadh | Westminster Abbey → London | Hohwacht → Berlin | Carisbrooke Castle → London || **Final:** Fatima Masumeh Shrine → Tehran

- **Query 884 — Context:** The Cloisters → Washington, D.C. | Jeita Grotto → Beirut | Cave of Swallows → Mexico City | Kraków Barbican → Warsaw | Berchtesgaden → Berlin | Chehel Sotun → Tehran | Mount Wutai → Beijing | Redwood National and State Parks → Washington, D.C. | KV11 → Cairo | Cathedral of Valladolid → Madrid || **Final:** 30 St Mary Axe → London

- **Query 920 — Context:** Behistun Inscription → Tehran | Epcot → Washington, D.C. | Racławice Panorama → Warsaw | Ytterby mine → Stockholm | Bryn Celli Ddu → London | Bad Bentheim → Berlin | Vittskövle Church → Stockholm | Bad Alexandersbad → Berlin | Mount Jiuhua → Beijing | Tatranská Lomnica → Bratislava || **Final:** Metropolitan Cathedral Basilica of the Holy Saviour, Oviedo → Madrid

- **Query 981 — Context:** Bad Laer → Berlin | Grūtas Park → Vilnius | Big Ben → London | St. Blasien → Berlin | Serdobsk → Moscow | Tokyo Disney Resort → Tokyo | Astrid Lindgren&#x27;s World → Stockholm | Saint Michael&#x27;s Castle → Moscow | West Bali National Park → Jakarta | Raj Ghat and associated memorials → New Delhi || **Final:** Sheikh Lotfollah Mosque → Tehran

- **Query 1013 — Context:** Museo di Capodimonte → Rome | Rundetaarn → Copenhagen | Teylers Museum → Amsterdam | Eisriesenwelt → Vienna | Spice Bazaar → Ankara | KV2 → Cairo | San Agustin archeological park → Bogotá | KV19 → Cairo | Soltaniyeh Dome → Tehran | Fujian Tulou → Beijing || **Final:** Cave of Altacosa → Madrid

- **Query 1025 — Context:** Ytterby mine → Stockholm | Milan Cathedral → Rome | Basilica of Our Lady of the Pillar → Madrid | Spannagel Cave → Vienna | Świnoujście → Warsaw | Świeradów-Zdrój → Warsaw | Roman Walls of Lugo → Madrid | Cleveland Museum of Art → Washington, D.C. | Palacio Episcopal de Astorga → Madrid | Jameh Mosque of Yazd → Tehran || **Final:** Pool of Siloam → Jerusalem

- **Query 1033 — Context:** Borobudur → Jakarta | Nizhny Novgorod Kremlin → Moscow | Tower of Hercules → Madrid | Bischofsgrün → Berlin | Getty Villa → Washington, D.C. | Kołobrzeg → Warsaw | Chehel Sotun → Tehran | Treasury of Atreus → Athens | Bad Sobernheim → Berlin | Bad Tölz → Berlin || **Final:** Bankya → Sofia

- **Query 1082 — Context:** Pera Museum → Ankara | Doge&#x27;s Palace → Rome | KV7 → Cairo | Bad Kleinkirchheim → Vienna | Liberty Bell → Washington, D.C. | ArcelorMittal Orbit → London | Arlington National Cemetery → Washington, D.C. | Czocha Castle → Warsaw | Castel Sant&#x27;Angelo → Rome | Brancacci Chapel → Rome || **Final:** Saadiyat Island → Abu Dhabi

- **Query 1097 — Context:** Mulholland Drive → Washington, D.C. | Oberstaufen → Berlin | Menshikov Palace (Saint Petersburg) → Moscow | Gonbad-e Qabus → Tehran | Leshan Giant Buddha → Beijing | St. Andrew&#x27;s Church → Warsaw | Athena Parthenos → Athens | Schömberg → Berlin | Cliffs of Moher → Dublin | Heiligendamm → Berlin || **Final:** Gochang, Hwasun and Ganghwa Dolmen Sites → Seoul

- **Query 1101 — Context:** Wuyi Mountains → Beijing | Beylerbeyi Palace → Ankara | Ourense Cathedral → Madrid | Cathedral of Zamora → Madrid | Hearst Castle → Washington, D.C. | Forest of the Martyrs → Jerusalem | Rock and Roll Hall of Fame → Washington, D.C. | Woburn Abbey → London | Bad Schwartau → Berlin | Leshan Giant Buddha → Beijing || **Final:** Amalienborg → Copenhagen

- **Query 1110 — Context:** Malmö Castle → Stockholm | Millennium of Russia → Moscow | Royal Museum for Central Africa → City of Brussels | KV17 → Cairo | Basilica of Candelaria → Madrid | Amélie-les-Bains-Palalda → Paris | Son Doong Cave → Hanoi | Death Valley → Washington, D.C. | Stromberg → Berlin | Big Sur → Washington, D.C. || **Final:** Wellington Arch → London

- **Query 1120 — Context:** Universal Studios Japan → Tokyo | Norderney → Berlin | Grossglockner High Alpine Road → Vienna | Falkirk Wheel → London | Mariánské Lázně → Prague | Chilean National Museum of Fine Arts → Santiago | Niagara Falls → Ottawa | Georgia Guidestones → Washington, D.C. | Las Médulas → Madrid | Columbus Circle → Washington, D.C. || **Final:** Che Guevara Mausoleum → Havana

- **Query 1147 — Context:** Gaztelugatxe → Madrid | Stromberg → Berlin | Oriental Pearl Tower → Beijing | Palace of Versailles → Paris | Kołobrzeg → Warsaw | Nemrut → Ankara | Palacio Episcopal de Astorga → Madrid | Yamunotri → New Delhi | Condé Museum → Paris | Petroglyphic Complexes of the Mongolian Altai → Ulaanbaatar || **Final:** Sir John Soane&#x27;s Museum → London

- **Query 1166 — Context:** Vigeland installation → Oslo | Universal Studios Japan → Tokyo | Ta&#x27; Ħaġrat → Valletta | Solomon R. Guggenheim Museum → Washington, D.C. | Champaner-Pavagadh Archaeological Park → New Delhi | Atakule → Ankara | Statens Museum for Kunst → Copenhagen | Royal Pavilion &amp; Garden → London | Anne Frank House → Amsterdam | Gardaland → Rome || **Final:** The Motherland Calls → Moscow

- **Query 1180 — Context:** Verona Arena → Rome | Spa → City of Brussels | Besakih → Jakarta | Ourense Cathedral → Madrid | Saadiyat Island → Abu Dhabi | Kunsthaus Graz → Vienna | Admont Abbey → Vienna | Momine Khatun Mausoleum → Baku | Tate Britain → London | Bad Dürkheim → Berlin || **Final:** KV7 → Cairo

- **Query 1301 — Context:** Naxos → Rome | Kneiff → Luxembourg | Masuleh → Tehran | Städel Museum → Berlin | Sheikh Lotfollah Mosque → Tehran | Otrar → Astana | Bad Fallingbostel → Berlin | Columbus Circle → Washington, D.C. | Nestorian Stele → Beijing | Narva Triumphal Arch → Moscow || **Final:** Vigeland installation → Oslo

- **Query 1348 — Context:** Yamunotri → New Delhi | Museum of Fine Arts Ghent (MSK) → City of Brussels | DeviantArt → Washington, D.C. | Dadiani Palaces Museum → Tbilisi | Monument to the Battle of the Nations → Berlin | National Library of Wales → London | Scharinska villa → Stockholm | Museum of San Marco → Rome | Treasury of Atreus → Athens | Rosa Khutor Alpine Resort → Moscow || **Final:** Lychakiv Cemetery → Kyiv

- **Query 1356 — Context:** Yellowstone National Park → Washington, D.C. | Bellano → Rome | Buziaș → Bucharest | Copenhagen Zoo → Copenhagen | Statue of Liberty → Washington, D.C. | One World Trade Center → Washington, D.C. | Druskininkai → Vilnius | Cueva de Nerja → Madrid | Cyprus Museum → Nicosia | National Portrait Gallery → London || **Final:** Norddorf → Berlin

**Part 2: Strongest Logit-Lens Evidence**

Layers are zero-indexed. Only layers tied for the highest reciprocal rank are shown.

**Shortcut candidates (105)**

- **Query 0:** Caernarfon Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0181818 | **Peak layer(s):** 30

- **Query 3:** Queen&#x27;s House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0178571 | **Peak layer(s):** 30

- **Query 14:** Westminster Abbey → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0344828 | **Peak layer(s):** 18

- **Query 19:** Chengde Mountain Resort and its outlying temples → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.025 | **Peak layer(s):** 25

- **Query 23:** The Wallace Collection → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0909091 | **Peak layer(s):** 17

- **Query 28:** British Library → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0555556 | **Peak layer(s):** 30

- **Query 30:** Alnwick Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0454545 | **Peak layer(s):** 18

- **Query 33:** Stadium MK → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0384615 | **Peak layer(s):** 18

- **Query 41:** Stonehenge → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.03125 | **Peak layer(s):** 31

- **Query 57:** Buckingham Palace → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.166667 | **Peak layer(s):** 18

- **Query 65:** Chatsworth House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0357143 | **Peak layer(s):** 18, 30

- **Query 74:** Sirius Arena → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.00862069 | **Peak layer(s):** 26

- **Query 84:** ArcelorMittal Orbit → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.166667 | **Peak layer(s):** 18, 19

- **Query 95:** Putuoshan → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0212766 | **Peak layer(s):** 29

- **Query 97:** Somerset House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.03125 | **Peak layer(s):** 18

- **Query 127:** Mount Lu → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0147059 | **Peak layer(s):** 29

- **Query 141:** Petrie Museum of Egyptian Archaeology → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0833333 | **Peak layer(s):** 18

- **Query 149:** Tate Britain → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0526316 | **Peak layer(s):** 30

- **Query 168:** Covent Garden → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0555556 | **Peak layer(s):** 18

- **Query 173:** Tower Bridge → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.111111 | **Peak layer(s):** 18

- **Query 180:** Apsley House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0344828 | **Peak layer(s):** 30

- **Query 209:** Lion Gate → Athens | **Intermediate country:** Greece | **Highest RR:** 0.125 | **Peak layer(s):** 19

- **Query 229:** Sorico → Rome | **Intermediate country:** Italy | **Highest RR:** 0.0212766 | **Peak layer(s):** 28

- **Query 245:** Sandringham House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.1 | **Peak layer(s):** 18, 30

- **Query 270:** Arch of Trajan → Rome | **Intermediate country:** Italy | **Highest RR:** 0.0666667 | **Peak layer(s):** 31

- **Query 279:** Madinat Al-Zahra → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0555556 | **Peak layer(s):** 26

- **Query 289:** Piccadilly Circus → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0714286 | **Peak layer(s):** 18

- **Query 291:** Mount Sanqing → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0147059 | **Peak layer(s):** 29

- **Query 298:** Conventico Caves → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0588235 | **Peak layer(s):** 31

- **Query 300:** Mansion House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.030303 | **Peak layer(s):** 19

- **Query 319:** Vindolanda → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.00892857 | **Peak layer(s):** 30

- **Query 328:** Jinggang Mountains → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0175439 | **Peak layer(s):** 29

- **Query 332:** Hever Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.111111 | **Peak layer(s):** 30

- **Query 361:** Hospital of Innocents → Rome | **Intermediate country:** Italy | **Highest RR:** 0.00769231 | **Peak layer(s):** 31

- **Query 375:** Palazzo Rosso → Rome | **Intermediate country:** Italy | **Highest RR:** 0.142857 | **Peak layer(s):** 21

- **Query 399:** St Martin-in-the-Fields → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0833333 | **Peak layer(s):** 19

- **Query 412:** Zhangjiajie Glass Bridge → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0128205 | **Peak layer(s):** 29

- **Query 413:** Barbican Centre → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0227273 | **Peak layer(s):** 18

- **Query 422:** Jingpo Lake → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0384615 | **Peak layer(s):** 31

- **Query 427:** Baths of Caracalla → Rome | **Intermediate country:** Italy | **Highest RR:** 0.111111 | **Peak layer(s):** 30

- **Query 492:** Pickford&#x27;s House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.00520833 | **Peak layer(s):** 30

- **Query 498:** Trinity Cathedral → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.05 | **Peak layer(s):** 22

- **Query 504:** Roman Baths → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.00909091 | **Peak layer(s):** 18

- **Query 506:** Pingyao → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0149254 | **Peak layer(s):** 31

- **Query 537:** Toughsheet Community Stadium → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0117647 | **Peak layer(s):** 15

- **Query 577:** Winterberg → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.166667 | **Peak layer(s):** 21, 28, 30

- **Query 588:** Royal Pavilion &amp; Garden → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0188679 | **Peak layer(s):** 30

- **Query 591:** Mount Song → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0227273 | **Peak layer(s):** 29

- **Query 592:** Harrods → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.125 | **Peak layer(s):** 30

- **Query 601:** British Museum → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0294118 | **Peak layer(s):** 30

- **Query 607:** Pyramid of Cestius → Rome | **Intermediate country:** Italy | **Highest RR:** 0.0909091 | **Peak layer(s):** 30

- **Query 609:** Tomb of Absalom → Jerusalem | **Intermediate country:** Israel | **Highest RR:** 0.166667 | **Peak layer(s):** 22, 26, 27

- **Query 612:** Alexander Column → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.0526316 | **Peak layer(s):** 23

- **Query 644:** Skull Tower → Belgrade | **Intermediate country:** Serbia | **Highest RR:** 0.0555556 | **Peak layer(s):** 28

- **Query 647:** Metropolitan Cathedral Basilica of St. James the Apostle → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.03125 | **Peak layer(s):** 31

- **Query 650:** Big Ben → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.166667 | **Peak layer(s):** 18

- **Query 658:** Burghley House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0416667 | **Peak layer(s):** 30

- **Query 665:** Royal Academy of Arts → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.015625 | **Peak layer(s):** 30

- **Query 682:** Dubino → Rome | **Intermediate country:** Italy | **Highest RR:** 0.0833333 | **Peak layer(s):** 21

- **Query 711:** Dulwich Picture Gallery → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.125 | **Peak layer(s):** 18

- **Query 721:** Famine Stela → Cairo | **Intermediate country:** Egypt | **Highest RR:** 0.125 | **Peak layer(s):** 26

- **Query 738:** Blackpool Tower → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.047619 | **Peak layer(s):** 18

- **Query 770:** Piton des Neiges → Paris | **Intermediate country:** France | **Highest RR:** 0.0625 | **Peak layer(s):** 21

- **Query 772:** Astorga Cathedral → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.166667 | **Peak layer(s):** 21

- **Query 786:** Al-Rifa&#x27;i Mosque → Cairo | **Intermediate country:** Egypt | **Highest RR:** 0.02 | **Peak layer(s):** 26

- **Query 809:** Hampton Court Palace → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.04 | **Peak layer(s):** 30

- **Query 830:** Teide → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0833333 | **Peak layer(s):** 31

- **Query 837:** Homomonument → Amsterdam | **Intermediate country:** Netherlands | **Highest RR:** 0.0178571 | **Peak layer(s):** 28

- **Query 838:** Shanhai Pass → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0416667 | **Peak layer(s):** 25

- **Query 858:** National Portrait Gallery → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0294118 | **Peak layer(s):** 30

- **Query 863:** Portman Road → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0149254 | **Peak layer(s):** 19

- **Query 867:** Our Lady of the Pillar → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0416667 | **Peak layer(s):** 21, 31

- **Query 876:** Serpentine Galleries → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0144928 | **Peak layer(s):** 18

- **Query 881:** Jamkaran Mosque → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.125 | **Peak layer(s):** 26

- **Query 883:** Hadrian&#x27;s Wall → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0833333 | **Peak layer(s):** 30, 31

- **Query 893:** Victoria and Albert Museum → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0909091 | **Peak layer(s):** 18, 30

- **Query 911:** Kensington Palace → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.125 | **Peak layer(s):** 31

- **Query 936:** Yungang Grottoes → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0178571 | **Peak layer(s):** 25

- **Query 938:** Basilica of Our Lady of the Pillar → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.142857 | **Peak layer(s):** 25, 26

- **Query 945:** Mount Tai → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0144928 | **Peak layer(s):** 25

- **Query 948:** Puente romano → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0454545 | **Peak layer(s):** 31

- **Query 953:** Ludlow Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0285714 | **Peak layer(s):** 30

- **Query 960:** Trafalgar Square → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.047619 | **Peak layer(s):** 18

- **Query 996:** Banqueting House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0106383 | **Peak layer(s):** 31

- **Query 1036:** West Lake → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0131579 | **Peak layer(s):** 25

- **Query 1047:** Warwick Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0833333 | **Peak layer(s):** 18

- **Query 1061:** Marble Arch → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.166667 | **Peak layer(s):** 18

- **Query 1064:** Lincoln Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.00943396 | **Peak layer(s):** 30

- **Query 1069:** Albert Memorial → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0172414 | **Peak layer(s):** 30

- **Query 1129:** Tate Modern → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0625 | **Peak layer(s):** 18

- **Query 1150:** Hatfield House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.166667 | **Peak layer(s):** 30

- **Query 1152:** Masuleh → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.166667 | **Peak layer(s):** 31

- **Query 1160:** Brick Lane → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0204082 | **Peak layer(s):** 18

- **Query 1176:** Basilica of Candelaria → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.0285714 | **Peak layer(s):** 31

- **Query 1194:** Nelson&#x27;s Column → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0222222 | **Peak layer(s):** 30

- **Query 1205:** Bingling Temple → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0185185 | **Peak layer(s):** 25

- **Query 1231:** Charing Cross → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0136986 | **Peak layer(s):** 30

- **Query 1234:** Kew Palace → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.025 | **Peak layer(s):** 30

- **Query 1265:** Iglesia de la Concepción → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.047619 | **Peak layer(s):** 21

- **Query 1287:** Dolmen of Menga → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.142857 | **Peak layer(s):** 31

- **Query 1315:** Tower of the Winds → Athens | **Intermediate country:** Greece | **Highest RR:** 0.142857 | **Peak layer(s):** 25

- **Query 1319:** Kenwood House → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.0416667 | **Peak layer(s):** 31

- **Query 1330:** Star of Nanchang → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0169492 | **Peak layer(s):** 29

- **Query 1359:** Glastonbury Tor → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.047619 | **Peak layer(s):** 30

- **Query 1383:** Mount Wutai → Beijing | **Intermediate country:** People&#x27;s Republic of China | **Highest RR:** 0.0169492 | **Peak layer(s):** 29

**Ambiguous (45)**

- **Query 2:** Mazar-e-Quaid → Islamabad | **Intermediate country:** Pakistan | **Highest RR:** 0.333333 | **Peak layer(s):** 26

- **Query 59:** Igel Column → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.333333 | **Peak layer(s):** 21

- **Query 88:** Novocherkassk Cathedral → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.25 | **Peak layer(s):** 21

- **Query 137:** Statens Museum for Kunst → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27

- **Query 163:** Alcázar of Toledo → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.333333 | **Peak layer(s):** 21, 25, 26, 27, 28, 29, 30, 31

- **Query 176:** Pura Luhur → Jakarta | **Intermediate country:** Indonesia | **Highest RR:** 0.333333 | **Peak layer(s):** 25

- **Query 182:** Porta San Sebastiano → Rome | **Intermediate country:** Italy | **Highest RR:** 0.2 | **Peak layer(s):** 25, 26

- **Query 197:** Admiralty Arch → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.25 | **Peak layer(s):** 18

- **Query 244:** Downing Street → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.2 | **Peak layer(s):** 18

- **Query 256:** Treblinka extermination camp → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.25 | **Peak layer(s):** 22, 23, 25, 27

- **Query 273:** Thorvaldsen Museum → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27

- **Query 302:** Summer Garden → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.333333 | **Peak layer(s):** 19

- **Query 336:** Liseberg → Stockholm | **Intermediate country:** Sweden | **Highest RR:** 0.333333 | **Peak layer(s):** 22, 23

- **Query 384:** Palazzo Barberini → Rome | **Intermediate country:** Italy | **Highest RR:** 0.25 | **Peak layer(s):** 22

- **Query 391:** Althorp → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.333333 | **Peak layer(s):** 16

- **Query 450:** Windsor Castle → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.2 | **Peak layer(s):** 18

- **Query 472:** Krakus Mound → Warsaw | **Intermediate country:** Poland | **Highest RR:** 0.333333 | **Peak layer(s):** 25

- **Query 494:** Valle dei Templi → Rome | **Intermediate country:** Italy | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27

- **Query 516:** Grande Arche → Paris | **Intermediate country:** France | **Highest RR:** 0.25 | **Peak layer(s):** 26

- **Query 538:** Menshikov Palace (Saint Petersburg) → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.333333 | **Peak layer(s):** 18

- **Query 586:** Trinity Lavra of St. Sergius → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.333333 | **Peak layer(s):** 21

- **Query 670:** Bletchley Park → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.333333 | **Peak layer(s):** 18

- **Query 705:** Hisarya → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 0.25 | **Peak layer(s):** 26, 27

- **Query 714:** La Défense → Paris | **Intermediate country:** France | **Highest RR:** 0.333333 | **Peak layer(s):** 18, 19

- **Query 724:** Aqueduct of Segovia → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.333333 | **Peak layer(s):** 21, 22, 25, 26, 27, 28, 29

- **Query 859:** Puente Nuevo → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.333333 | **Peak layer(s):** 25

- **Query 860:** Tivoli Gardens → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.2 | **Peak layer(s):** 26, 27

- **Query 869:** Fatima Masumeh Shrine → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27

- **Query 884:** 30 St Mary Axe → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.2 | **Peak layer(s):** 19

- **Query 920:** Metropolitan Cathedral Basilica of the Holy Saviour, Oviedo → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.333333 | **Peak layer(s):** 22, 25

- **Query 981:** Sheikh Lotfollah Mosque → Tehran | **Intermediate country:** Iran | **Highest RR:** 0.333333 | **Peak layer(s):** 25, 26

- **Query 1013:** Cave of Altacosa → Madrid | **Intermediate country:** Spain | **Highest RR:** 0.2 | **Peak layer(s):** 31

- **Query 1025:** Pool of Siloam → Jerusalem | **Intermediate country:** Israel | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27

- **Query 1033:** Bankya → Sofia | **Intermediate country:** Bulgaria | **Highest RR:** 0.25 | **Peak layer(s):** 26

- **Query 1082:** Saadiyat Island → Abu Dhabi | **Intermediate country:** United Arab Emirates | **Highest RR:** 0.333333 | **Peak layer(s):** 29, 30

- **Query 1097:** Gochang, Hwasun and Ganghwa Dolmen Sites → Seoul | **Intermediate country:** South Korea | **Highest RR:** 0.25 | **Peak layer(s):** 30

- **Query 1101:** Amalienborg → Copenhagen | **Intermediate country:** Denmark | **Highest RR:** 0.333333 | **Peak layer(s):** 22, 25, 26

- **Query 1110:** Wellington Arch → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.333333 | **Peak layer(s):** 18

- **Query 1120:** Che Guevara Mausoleum → Havana | **Intermediate country:** Cuba | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 28

- **Query 1147:** Sir John Soane&#x27;s Museum → London | **Intermediate country:** United Kingdom | **Highest RR:** 0.333333 | **Peak layer(s):** 17

- **Query 1166:** The Motherland Calls → Moscow | **Intermediate country:** Russia | **Highest RR:** 0.2 | **Peak layer(s):** 26

- **Query 1180:** KV7 → Cairo | **Intermediate country:** Egypt | **Highest RR:** 0.2 | **Peak layer(s):** 22

- **Query 1301:** Vigeland installation → Oslo | **Intermediate country:** Norway | **Highest RR:** 0.333333 | **Peak layer(s):** 20, 22, 25, 26, 27, 31

- **Query 1348:** Lychakiv Cemetery → Kyiv | **Intermediate country:** Ukraine | **Highest RR:** 0.333333 | **Peak layer(s):** 25, 26

- **Query 1356:** Norddorf → Berlin | **Intermediate country:** Germany | **Highest RR:** 0.333333 | **Peak layer(s):** 21
