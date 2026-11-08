# Gradient-based associated words

Per prompt: the top word tokens by gradient score (layer 20, log_prob), after
dropping the answer and its pieces, the intermediate and its adjectives, other answers' and
intermediates' names, and near-duplicates. Below, per answer: the words that most often appear
in the per-prompt top 5 / top 10, with the number of prompts in brackets when an answer has
more than one prompt.

## Landmark → country → capital

### True answers (79 answers, 962 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Abu Dhabi (3 prompts) | Niger (2), Oman (1), Adams (1), abb (1), Kuwait (1) | Niger (2), abb (2), Oman (1), Adams (1), Kuwait (1), Arkansas (1), abi (1), Bahrain (1), monarch (1), abdominal (1) |
| Abuja (3 prompts) | Abd (2), Ramadan (2), Dubai (1), Arabic (1), Supern (1) | Abd (2), Ramadan (2), Arabic (2), Allah (2), Abdel (2), Dubai (1), Supern (1), Kuwait (1), Abuse (1), Mohamed (1) |
| Addis Ababa | adding, added, addition, adds, Bangladesh | adding, added, addition, adds, Bangladesh, Tanz, Chennai, Niger, Lahore, supplemented |
| Amman (2 prompts) | Raqqa (1), Nashville (1), lookahead (1), Virginia (1), besoin (1) | Charlottesville (2), Raqqa (1), Nashville (1), lookahead (1), Virginia (1), besoin (1), det (1), refugee (1), desta (1), Orlando (1) |
| Amsterdam (11 prompts) | vois (4), Rotterdam (3), Nederland (3), Barcelona (3), Venice (3) | vois (4), Mumbai (4), Rotterdam (3), Nederland (3), Barcelona (3), Decompiled (3), Venice (3), Else (3), NYC (2), NDEBUG (2) |
| Ankara (50 prompts) | Boise (20), Ans (16), Kansas (16), Nebraska (13), congressional (13) | Ans (29), Boise (27), congressional (23), Nebraska (22), Kansas (21), Saskatchewan (19), Republican (18), anonymity (14), government (13), Saddam (13) |
| Astana | Astros, delegation, satellite, succession, Coral | Astros, delegation, satellite, succession, Coral, voyage, Aurora, aston, divisions, subdivisions |
| Athens (22 prompts) | Athena (6), Sydney (4), Nunes (3), ellas (3), Plato (3) | Athena (7), Melbourne (6), Plato (5), ext (5), Sydney (4), Nunes (4), ellas (4), Mono (4), turnout (4), Retorna (4) |
| Baghdad (3 prompts) | Saddam (2), Mosul (2), Assy (1), Bengal (1), Constantin (1) | Saddam (2), Mosul (2), Assy (2), Kuwait (2), Bihar (2), bags (2), Bengal (1), Constantin (1), Babylon (1), cities (1) |
| Baku | Chennai, Istanbul, seaside, Atlanta, Armen | Chennai, Istanbul, seaside, Atlanta, Armen, Gulf, offshore, yacht, Tamil, Kurdish |
| Bangkok | gangbang, bargain, precinct, Fucked, Nutzung | gangbang, bargain, precinct, Fucked, Nutzung, Wohnung, Seks, backdrop, congest, shootout |
| Beijing (31 prompts) | Kremlin (25), Capitol (18), Putin (8), Kiev (7), Denver (5) | Kremlin (27), Capitol (19), Kiev (16), Putin (12), Denver (8), Bolshevik (8), bead (7), Senate (7), Jinping (6), NYC (6) |
| Beirut | Bombay, NYC, Mumbai, Toronto, Taipei | Bombay, NYC, Mumbai, Toronto, Taipei, Honolulu, street, Manhattan, subway, Istanbul |
| Belgrade | Yugosl, Retorna, autobiography, Karachi, Aleks | Yugosl, Retorna, autobiography, Karachi, Aleks, Serge, Nutzung, Todos, Sloven, VECTOR |
| Berlin (223 prompts) | Istanbul (107), Putin (98), Lenin (70), Vladimir (63), Brooklyn (62) | Istanbul (154), Putin (120), Lenin (108), Vladimir (106), Brooklyn (105), Bolshevik (96), Kremlin (95), Stalin (92), Taipei (71), Belfast (64) |
| Bern (5 prompts) | Ferdinand (2), Bulletin (2), Barn (2), RCMP (1), Ben (1) | Bulletin (3), Ferdinand (2), Barn (2), Ben (2), Bundes (2), impunity (2), Burlington (2), RCMP (1), government (1), Bul (1) |
| Bogotá | Bolivia, Indones, jungle, Bangladesh, Fog | Bolivia, Indones, jungle, Bangladesh, Fog, Bush, Denver, Papua, Swamp, Haiti |
| Brasília (2 prompts) | governments (2), Minister (2), Niger (1), Countries (1), Guinea (1) | governments (2), Minister (2), Niger (1), Countries (1), Guinea (1), federal (1), Ras (1), Bundes (1), Nep (1), Political (1) |
| Bratislava (6 prompts) | sme (3), brunch (3), bras (2), vectors (2), Brisbane (2) | sme (3), brunch (3), vectors (3), bras (2), braces (2), Brisbane (2), bricks (2), amen (2), Honolulu (2), SAS (2) |
| Bucharest (3 prompts) | Buchanan (2), Shanghai (2), Bras (2), Sydney (1), NYC (1) | Buchanan (2), Shanghai (2), Bras (2), Sydney (1), NYC (1), Roch (1), blindness (1), Istanbul (1), alleen (1), Taipei (1) |
| Budapest | Istanbul, Kiev, Barcelona, Bols, toda | Istanbul, Kiev, Barcelona, Bols, toda, Metropolitan, Empresa, repost, Constantin, Gotham |
| Cairo (30 prompts) | Istanbul (12), Mahmoud (11), Ibrahim (10), Arabic (10), Cain (8) | Mahmoud (17), Istanbul (14), Arabic (14), Ibrahim (13), Arabs (12), Aleppo (10), Cain (9), Mumbai (9), Tunis (8), Karachi (8) |
| Canberra (7 prompts) | congressional (4), legislative (4), Congressional (3), government (3), Government (3) | legislative (5), congressional (4), government (4), parliamentary (4), politicians (4), senators (4), Congressional (3), Government (3), Kremlin (3), Minister (3) |
| Caracas | Carly, downtown, Gors, cartridge, Mayor | Carly, downtown, Gors, cartridge, Mayor, Auckland, Concord, carcinoma, Carr, Carp |
| City of Brussels (6 prompts) | Country (5), State (5), Cities (4), Universe (4), Town (2) | State (6), Country (5), Universe (5), Cities (4), Village (4), Town (2), town (2), municipality (2), House (2), World (2) |
| Constantinople | Byz, constants, Roman, feudal, continual | Byz, constants, Roman, feudal, continual, Emperor, medieval, Confederate, Theodore, Oriental |
| Copenhagen (7 prompts) | ext (2), favoured (2), Semaphore (2), Daniels (1), NYC (1) | ext (2), favoured (2), Daniels (2), Semaphore (2), Mumbai (2), Wade (2), Rotterdam (2), Chennai (2), cuckold (2), Bulldogs (2) |
| Dakar | niveau, checkpoints, Gupta, Dakota, tamp | niveau, checkpoints, Gupta, Dakota, tamp, NSK, GDK, Lakers, cruz, Kolkata |
| Damascus (2 prompts) | Assad (2), Aleppo (2), Bashar (2), Damien (2), Byz (1) | Assad (2), Aleppo (2), Bashar (2), Damien (2), Byz (2), Donetsk (2), Hezbollah (2), Smy (2), Raqqa (1), baptism (1) |
| Dodoma | dodge, Avoid, Dodd, smuggling, evade | dodge, Avoid, Dodd, smuggling, evade, safeguard, evasion, Deputy, asbestos, Donne |
| Dublin (5 prompts) | NYC (2), Belfast (2), Auckland (2), Toronto (2), Columbus (1) | NYC (2), Belfast (2), Auckland (2), Toronto (2), Johannesburg (2), Gael (2), Edinburgh (2), Cork (2), Istanbul (2), Columbus (1) |
| Hanoi (3 prompts) | Kremlin (3), downtown (2), Leipzig (1), basement (1), NYC (1) | Kremlin (3), downtown (2), Manhattan (2), Istanbul (2), Alexandre (2), appointment (2), Leipzig (1), basement (1), NYC (1), burner (1) |
| Havana | Dubai, Babylon, Shanghai, Hong, Frankfurt | Dubai, Babylon, Shanghai, Hong, Frankfurt, Qatar, Singapore, Manila, internationally, Hussein |
| Helsinki | Kiev, Kremlin, Westminster, Istanbul, wearer | Kiev, Kremlin, Westminster, Istanbul, wearer, Authorities, Dubai, Irma, Gotham, Mandela |
| Islamabad (3 prompts) | Maryland (2), diplomatic (2), embassy (1), Yugosl (1), Bethesda (1) | Maryland (2), diplomatic (2), embassy (1), Yugosl (1), Bethesda (1), Steelers (1), Politico (1), skiing (1), senators (1), Libyan (1) |
| Jakarta (5 prompts) | Karachi (4), Manila (2), Mohammad (2), Maduro (2), Toronto (1) | Karachi (4), Mumbai (4), Manila (3), Kremlin (3), Mohammad (2), Maduro (2), Yahoo (2), Lagos (2), Urdu (2), Amazon (2) |
| Jerusalem (5 prompts) | Jewish (3), Jews (3), Hebrew (3), Judaism (2), Jew (2) | Jewish (3), Jews (3), Hebrew (3), Jude (3), Zionist (3), Judaism (2), Jew (2), nesta (2), Capitals (1), Bulldogs (1) |
| Kabul (2 prompts) | Taliban (1), Zucker (1), Nep (1), Istanbul (1), Hindu (1) | Lahore (2), Taliban (1), Zucker (1), Nep (1), Istanbul (1), Hindu (1), Vinci (1), Kashmir (1), Karachi (1), Kaepernick (1) |
| Kyiv (5 prompts) | Sydney (4), Biden (3), LGBTQ (3), COVID (2), Krist (2) | Sydney (4), Biden (3), LGBTQ (3), COVID (3), Kylie (3), Kyoto (2), Krist (2), Melbourne (2), Peach (2), Kentucky (1) |
| Lima | steering, APA, impost, Taipei, Alzheimer | steering, APA, impost, Taipei, Alzheimer, manic, legislature, Cabinet, affecting, starch |
| Ljubljana (2 prompts) | downtown (2), Brisbane (2), Auckland (1), adjunct (1), chicago (1) | downtown (2), Brisbane (2), Auckland (1), adjunct (1), chicago (1), lect (1), Lahore (1), Sydney (1), Honolulu (1), adj (1) |
| London (73 prompts) | Thames (27), Mumbai (25), NYC (23), Europe (17), NHS (13) | Thames (31), Mumbai (29), NYC (28), Brexit (21), Europe (19), Manhattan (18), NHS (17), Istanbul (16), Venice (16), Retorna (13) |
| Luxembourg | Maurit, Kuwait, Monaco, Europe, Belg | Maurit, Kuwait, Monaco, Europe, Belg, Quebec, Euros, Louisiana, Philippe, Belize |
| Madrid (48 prompts) | Madison (28), Congress (17), Chicago (10), Barcelona (9), President (9) | Madison (30), Congress (19), NYC (14), Microsoft (13), Nation (12), Barcelona (11), Chicago (11), Mumbai (11), President (10), Downing (8) |
| Mexico City (3 prompts) | Mumbai (3), Montreal (3), Bollywood (2), Toronto (1), NYC (1) | Mumbai (3), Montreal (3), Bollywood (2), NYC (2), Toronto (2), Istanbul (2), Europe (1), multinational (1), Manhattan (1), Johannesburg (1) |
| Minsk | Dud, Panc, Hyderabad, mourn, Alumni | Dud, Panc, Hyderabad, mourn, Alumni, Bashar, leveling, Zah, Saud, Rahman |
| Moscow (45 prompts) | Kremlin (31), Putin (16), NYC (14), Manhattan (13), Siber (11) | Kremlin (33), Putin (19), NYC (15), Manhattan (15), Stalin (15), Dmitry (14), Sergei (14), Bolshevik (13), Mumbai (12), Siber (12) |
| Nairobi | Johannesburg, Perth, Mumbai, favourite, Bombay | Johannesburg, Perth, Mumbai, favourite, Bombay, compte, Singapore, Kirst, fiz, LEFT |
| New Delhi (17 prompts) | NYC (8), Manhattan (7), Mumbai (6), Congress (4), NYPD (4) | NYC (9), Manhattan (9), Mumbai (8), NYPD (7), Congress (7), Narendra (7), Bollywood (5), Reagan (5), National (4), NASA (4) |
| Nicosia | Sydney, Brisbane, Melbourne, Honolulu, Auckland | Sydney, Brisbane, Melbourne, Honolulu, Auckland, stop, pip, numbered, NYPD, Johannesburg |
| Oslo (4 prompts) | politicians (2), grues (1), INA (1), utc (1), Chicago (1) | politicians (2), analysts (2), grues (1), INA (1), utc (1), Chicago (1), BCHP (1), bureaucrats (1), governments (1), Metropolitan (1) |
| Ottawa (5 prompts) | congressional (2), parliament (2), RCMP (2), Saskatchewan (2), government (2) | RCMP (4), congressional (2), parliament (2), Saskatchewan (2), government (2), diplomatic (2), Quebec (2), legislative (2), OECD (2), Winnipeg (2) |
| Paris (23 prompts) | NYC (16), Manhattan (9), Pierre (8), Chicago (7), Gotham (7) | NYC (18), Manhattan (12), Pierre (10), Gotham (9), Chicago (8), Mumbai (8), Boston (8), Harlem (7), Hollande (5), Toronto (5) |
| Prague (2 prompts) | Johannesburg (2), Dubai (1), Reign (1), Mumbai (1), Marino (1) | Johannesburg (2), Dubai (1), Reign (1), Mumbai (1), Marino (1), Lagos (1), Trinidad (1), Istanbul (1), Premiership (1), DISPATCH (1) |
| Prishtina | Prism, pruning, prune, Forest, rural | Prism, pruning, prune, Forest, rural, Prairie, prag, server, Microsoft, Africa |
| Pyongyang | Benghazi, Baghd, Saddam, CRUD, Hezbollah | Benghazi, Baghd, Saddam, CRUD, Hezbollah, Rahman, jihad, Maduro, Gratis, Mahm |
| Rabat | rabbits, Fox, Reagan, Rut, Ronald | rabbits, Fox, Reagan, Rut, Ronald, Rod, bunny, Dub, Wyoming, RAT |
| Reykjavík (2 prompts) | Taipei (1), Reyes (1), Lahore (1), Belfast (1), Sydney (1) | Taipei (1), Reyes (1), Lahore (1), Belfast (1), Sydney (1), Vega (1), Brisbane (1), Tango (1), Hao (1), Rory (1) |
| Riyadh (2 prompts) | Kuwait (1), Albuquerque (1), Cabinet (1), Cheng (1), GCC (1) | Houston (2), Kuwait (1), Albuquerque (1), Cabinet (1), Cheng (1), GCC (1), Omaha (1), NASA (1), Dallas (1), Chicago (1) |
| Rome (64 prompts) | Vatican (53), Roman (43), Latin (18), Romans (12), Libyan (8) | Vatican (55), Roman (43), Latin (29), Libyan (18), Tunis (16), Pope (15), Romans (12), Caesar (10), Assy (10), Romney (10) |
| Santiago | ext, Aws, ung, Ans, Ngb | ext, Aws, ung, Ans, Ngb, Beacon, algum, forb, duro, unilateral |
| Sarajevo (3 prompts) | Sab (1), Muslim (1), Salah (1), Sabha (1), Arabs (1) | Sab (1), Muslim (1), Salah (1), Sabha (1), Arabs (1), Islam (1), simul (1), Persian (1), mosque (1), sabotage (1) |
| Seoul (2 prompts) | Chennai (2), Mumbai (2), Lahore (1), Sydney (1), Taipei (1) | Chennai (2), Mumbai (2), downtown (2), Milan (2), Lahore (1), Sydney (1), Taipei (1), Manila (1), Realty (1), Toronto (1) |
| Sofia (8 prompts) | Sophia (8), Milano (4), Dimit (3), Nikol (2), Geneva (2) | Sophia (8), Milano (4), Dimit (3), Roma (3), Nikol (2), Geneva (2), Yugosl (2), Pavel (2), Lisbon (2), Chelsea (2) |
| Stockholm (24 prompts) | NYC (10), Gotham (10), Zurich (8), stocks (7), Svens (6) | Gotham (12), NYC (11), Toronto (10), Zurich (9), Istanbul (8), Manhattan (8), stocks (7), Johan (7), Svens (6), Scandinavian (5) |
| Tallinn (2 prompts) | Sloven (2), taller (1), Pavel (1), height (1), towering (1) | Sloven (2), taller (1), Pavel (1), height (1), towering (1), Kremlin (1), Sutton (1), tally (1), Slut (1), altura (1) |
| Tashkent (2 prompts) | Siber (1), Shanghai (1), Dmit (1), Hong (1), Sergei (1) | Siber (1), Shanghai (1), Dmit (1), Hong (1), Sergei (1), Sydney (1), Putin (1), PCA (1), Soviets (1), declared (1) |
| Tbilisi (2 prompts) | Yuri (1), Fresno (1), Muk (1), Tucson (1), junction (1) | Yuri (2), Fresno (1), Muk (1), Tucson (1), junction (1), Cheng (1), Nikol (1), Chattanooga (1), Sergei (1), Wichita (1) |
| Tehran (17 prompts) | Congress (7), Kremlin (5), Toronto (4), Hezbollah (3), Trudeau (3) | Congress (8), Kremlin (6), Trudeau (5), Toronto (4), Deutsche (4), Hezbollah (3), Taipei (3), Retrieved (3), Sydney (3), Parl (3) |
| Tokyo (10 prompts) | NYC (5), downtown (3), Mumbai (3), Manhattan (3), metropolitan (3) | NYC (5), Mumbai (5), Retorna (5), Kremlin (4), downtown (3), Manhattan (3), metropolitan (3), Observatory (2), Hollywood (2), Greenwich (2) |
| Ulaanbaatar | Nagar, Rohingya, junto, Tibetan, Lama | Nagar, Rohingya, junto, Tibetan, Lama, Sioux, Sikh, Mandal, Bihar, nom |
| Valletta (4 prompts) | valuation (4), valves (4), Valerie (4), valued (4), invaluable (3) | valuation (4), valves (4), Valerie (4), valued (4), invaluable (4), valleys (4), Valent (2), priceless (2), Blasio (2), Lond (2) |
| Vienna (11 prompts) | Wien (10), Sophia (4), Venice (3), Zurich (3), Philadelphia (2) | Wien (10), Venice (5), Sophia (4), Austin (4), Geneva (4), Istanbul (4), Viktor (4), Zurich (3), Vinci (3), Sydney (3) |
| Vilnius (2 prompts) | Kiev (2), Eston (1), Baltic (1), Azerbai (1), Ville (1) | Kiev (2), Azerbai (2), Ukrain (2), Eston (1), Baltic (1), Ville (1), Istanbul (1), Kremlin (1), Sloven (1), choking (1) |
| Warsaw (36 prompts) | Mumbai (11), Harlem (9), Bangalore (9), Chicago (7), Istanbul (7) | Harlem (14), Chicago (13), Mumbai (12), Bangalore (12), Istanbul (12), Boston (11), urban (11), NYC (10), Sao (8), Constantin (8) |
| Washington, D.C. (78 prompts) | Microsoft (70), Congressional (58), Smithsonian (32), President (28), Redskins (27) | Microsoft (71), Congressional (64), Smithsonian (62), Redskins (52), Pentagon (40), Windows (37), President (36), government (31), Maryland (29), Obama (29) |
| Wellington | Auckland, Tasmania, Canterbury, NSW, Queensland | Auckland, Tasmania, Canterbury, NSW, Queensland, Austral, Brisbane, Melbourne, Fiji, Sydney |
| Yerevan | Decompiled, blindly, Raq, worthy, Nutzung | Decompiled, blindly, Raq, worthy, Nutzung, Suche, Wolver, duro, Horny, Accountability |
| Zagreb | Sloven, Yugosl, Zig, Welsh, Maced | Sloven, Yugosl, Zig, Welsh, Maced, FPGA, euros, Alban, Ist, Somerset |

### Model answers (162 answers, 861 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Abu Dhabi | Oman, Kuwait, Bahrain, Qatar, Belize | Oman, Kuwait, Bahrain, Qatar, Belize, ancora, Abdel, Sheikh, Wei, Duterte |
| Adelaide | Greenville, Sioux, Sheffield, Clemson, Midlands | Greenville, Sioux, Sheffield, Clemson, Midlands, Howell, Birmingham, towns, Dund, Plymouth |
| Agra | Toledo, Raqqa, nearby, soaked, hometown | Toledo, Raqqa, nearby, soaked, hometown, Zusammen, quar, Tucson, adjoining, Spicer |
| Amman | Raqqa, lookahead, besoin, refugee, desta | Raqqa, lookahead, besoin, refugee, desta, protester, projet, fils, politique, Charlottesville |
| Amsterdam (9 prompts) | Rotterdam (3), Nederland (3), vois (3), Decompiled (2), NYC (2) | Rotterdam (3), Nederland (3), Decompiled (3), vois (3), Else (3), NYC (2), meisje (2), Tottenham (2), Oprah (2), NDEBUG (2) |
| Astana | Astros, delegation, satellite, succession, Coral | Astros, delegation, satellite, succession, Coral, voyage, Aurora, aston, divisions, subdivisions |
| Athens (19 prompts) | Athena (5), ellas (4), Nunes (3), Perth (3), Seks (3) | Athena (7), Plato (5), ext (5), ellas (4), Nunes (4), Perth (4), Ihren (4), Mono (4), turnout (4), Retorna (4) |
| Austria (2 prompts) | countries (2), Yugoslavia (2), Europe (1), Honduras (1), Africa (1) | countries (2), Yugoslavia (2), Europe (1), Honduras (1), Africa (1) |
| Baltimore (2 prompts) | Syracuse (2), Newark (2), Liverpool (1), Akron (1), Scarborough (1) | Syracuse (2), Newark (2), Akron (2), Scarborough (2), Cincinnati (2), Liverpool (1), downtown (1), Hartford (1), Caleb (1), Toledo (1) |
| Bangkok | gangbang, bargain, precinct, Fucked, Nutzung | gangbang, bargain, precinct, Fucked, Nutzung, Wohnung, Seks, backdrop, congest, shootout |
| Barcelona (7 prompts) | Byron (5), BLL (2), Produkt (2), Vancouver (2), Retorna (2) | Byron (5), BLL (3), Produkt (3), Vancouver (2), Retorna (2), Swansea (2), Highland (2), Bellev (2), Dortmund (2), LOG (2) |
| Bath | Cornwall, Bristol, Swansea, Wales, Welsh | Cornwall, Bristol, Swansea, Wales, Welsh, Somerset, Manchester, Sussex, Liverpool, Yorkshire |
| Beijing (17 prompts) | Kremlin (15), Capitol (12), Senate (4), Putin (4), Bolshevik (3) | Kremlin (16), Capitol (12), Bolshevik (10), Putin (6), Bison (5), Cabinet (5), Senate (4), presidential (4), NYC (4), Westminster (4) |
| Belfast (2 prompts) | Birmingham (1), IRA (1), Philadelphia (1), Gael (1), Bethesda (1) | Birmingham (1), IRA (1), Philadelphia (1), Gael (1), Bethesda (1), Scottish (1), Tacoma (1), Scots (1), downtown (1), Aberdeen (1) |
| Belgrade | Yugosl, Retorna, autobiography, Aleks, Serge | Yugosl, Retorna, autobiography, Aleks, Serge, Nutzung, Todos, Sloven, VECTOR, Gors |
| Berlin (133 prompts) | Putin (58), Bolshevik (54), Lenin (51), Reich (38), Kremlin (35) | Lenin (68), Bolshevik (67), Putin (65), Kremlin (59), Reich (51), Vladimir (51), Stalin (49), Taipei (47), Brooklyn (42), Baltic (41) |
| Bern (5 prompts) | Burlington (4), Barn (4), Bulletin (2), FROM (2), Ihren (1) | Burlington (5), Barn (5), FROM (3), Sanders (3), Bulletin (2), Salisbury (2), Albany (2), RCMP (2), Bair (2), bona (2) |
| Bilbao | bilateral, slime, restore, Rotterdam, extractor | bilateral, slime, restore, Rotterdam, extractor, Nile, Hydraulic, Inflate, interceptor, deflate |
| Boston (3 prompts) | Massachusetts (1), Playoff (1), downtown (1), Harvard (1), Cincinnati (1) | Yankee (2), BCHP (2), Massachusetts (1), Playoff (1), downtown (1), Harvard (1), Cincinnati (1), Dort (1), MIT (1), precinct (1) |
| Brasilia | Cliente, Arkansas, Urb, politique, Braz | Cliente, Arkansas, Urb, politique, Braz, amen, Brut, egal, Legisl, Ngb |
| Bratislava (3 prompts) | brunch (3), Honolulu (2), singapore (1), braces (1), Bras (1) | brunch (3), braces (2), Honolulu (2), blinds (2), singapore (1), Bras (1), sme (1), CONCAT (1), Auckland (1), brom (1) |
| Bremen | Toledo, ext, themselves, Ziel, bcm | Toledo, ext, themselves, Ziel, bcm, unmist, theirs, Nunes, sophistic, Dort |
| Brisbane | Birmingham, Baton, Tampa, Lansing, Akron | Birmingham, Baton, Tampa, Lansing, Akron, Chattanooga, Milwaukee, Cincinnati, Bengals, Tulsa |
| Bruges | monks, breve, knights, ext, Morm | monks, breve, knights, ext, Morm, traveler, monuments, predecess, Oswald, pilgrimage |
| Brussels (3 prompts) | bureaucrats (2), Brady (1), GDPR (1), politicians (1), Braves (1) | bureaucrats (2), GDPR (2), Bourbon (2), Brady (1), politicians (1), Braves (1), Brill (1), Gover (1), Capitol (1), bricks (1) |
| Bucharest (2 prompts) | Buchanan (2), Authorization (1), Bras (1), roman (1), Roch (1) | Buchanan (2), Authorization (1), Bras (1), roman (1), Roch (1), Chore (1), alleen (1), apar (1), Commissioner (1), exposures (1) |
| Budapest (2 prompts) | Bols (1), Hung (1), toda (1), Viktor (1), Metropolitan (1) | Bols (1), Hung (1), toda (1), Viktor (1), Metropolitan (1), Erd (1), Empresa (1), Hog (1), repost (1), Kis (1) |
| Cairo (23 prompts) | Mahmoud (9), Ibrahim (8), Cain (6), Aleppo (5), Arabic (5) | Mahmoud (10), Ibrahim (10), Aleppo (9), Cain (8), Pune (8), Arabic (7), Sheikh (7), Arabs (7), Sinai (6), Nile (5) |
| Cambridge | MIT, Harvard, BYU, Clemson, Massachusetts | MIT, Harvard, BYU, Clemson, Massachusetts, campus, Worcester, UNIVERSITY, Brigham, collegiate |
| Canberra | congressional, Government, parliamentary, legislative, senators | congressional, Government, parliamentary, legislative, senators, politicians, lawmaker, Presidents, bureaucrats, lobbyist |
| Cape Town | coral, beach, reef, ocean, seafood | coral, beach, reef, ocean, seafood, marine, Sea, coastal, lobster, dolphins |
| Cardiff (2 prompts) | authorised (1), IDD (1), Dirk (1), accession (1), Ashton (1) | accession (2), Columbus (2), Dayton (2), authorised (1), IDD (1), Dirk (1), Ashton (1), diplomats (1), Brighton (1), Application (1) |
| Chicago (2 prompts) | Colorado (2), Tacoma (1), Nebraska (1), Wisconsin (1), Omaha (1) | Colorado (2), Nebraska (2), Wisconsin (2), Louisville (2), Tacoma (1), Omaha (1), Purdue (1), federally (1), Illinois (1), Missouri (1) |
| China (2 prompts) | Europe (2), countries (2), Americas (2), Africa (1), Asia (1) | Europe (2), countries (2), Americas (2), Africa (2), Asia (2), Scandin (1), Yugoslavia (1), nations (1), Somalia (1) |
| Cleveland (3 prompts) | Brooklyn (1), tph (1), Ohio (1), Harlem (1), drawer (1) | Brooklyn (1), tph (1), Ohio (1), Harlem (1), drawer (1), Akron (1), NYC (1), EFI (1), Michigan (1), Harvard (1) |
| Cologne (5 prompts) | coaster (2), Duis (2), Celtic (1), buffet (1), chances (1) | coaster (3), tiled (3), Combo (3), Duis (2), Baths (2), Lola (2), subdivisions (2), Celtic (1), buffet (1), chances (1) |
| Copenhagen (9 prompts) | ext (3), Bombay (3), Hansen (2), favoured (2), Semaphore (2) | ext (3), Bombay (3), Hansen (2), favoured (2), Daniels (2), Semaphore (2), Honolulu (2), Wade (2), Buckingham (2), Rotterdam (2) |
| Dakar | niveau, checkpoints, Gupta, Dakota, tamp | niveau, checkpoints, Gupta, Dakota, tamp, NSK, GDK, Lakers, cruz, txt |
| Delhi (5 prompts) | norge (3), verso (2), Himself (2), bergen (2), DPR (1) | norge (3), bergen (3), verso (2), Himself (2), DPR (2), dealings (2), caste (1), Harlem (1), BLL (1), Narendra (1) |
| Denmark (2 prompts) | countries (2), Europe (2), Scandin (2), nations (1) | countries (2), Europe (2), Scandin (2), nations (1) |
| Denver | downtown, gangbang, Vancouver, Dallas, Winnipeg | downtown, gangbang, Vancouver, Dallas, Winnipeg, Edmonton, Tulsa, ips, Hayward, Michaels |
| Derby | Rajasthan, nearby, Jain, Feng, adjoining | Rajasthan, nearby, Jain, Feng, adjoining, Vik, Jeb, rented, Pune, Petra |
| Detroit | redevelopment, derp, Terrace, stump, Chatt | redevelopment, derp, Terrace, stump, Chatt, pts, undefeated, Rosenstein, Trev, Downtown |
| Dresden (2 prompts) | Huntington (1), Cavaliers (1), Hoff (1), Louisville (1), Dexter (1) | Huntington (1), Cavaliers (1), Hoff (1), Louisville (1), Dexter (1), Glouce (1), damage (1), Tops (1), Harding (1), Rochester (1) |
| Dubai (2 prompts) | Tacoma (2), NYC (1), Downtown (1), Calgary (1), Craigslist (1) | Tacoma (2), Burb (2), NYC (1), Downtown (1), Calgary (1), Craigslist (1), Realt (1), Feinstein (1), Vancouver (1), Erick (1) |
| Dublin (3 prompts) | Auckland (2), NYC (1), Columbus (1), Demp (1), Liverpool (1) | Auckland (2), NYC (1), Columbus (1), Demp (1), Liverpool (1), Broadway (1), Winnipeg (1), Nottingham (1), IST (1), Cincinnati (1) |
| Edinburgh (2 prompts) | NYC (1), ESV (1), Europeans (1), Royal (1), Abdullah (1) | NYC (1), ESV (1), Europeans (1), Royal (1), Abdullah (1), declarations (1), Constantin (1), Rebellion (1), Harlem (1), ruler (1) |
| Florence (7 prompts) | Persian (2), Corinth (2), Tus (2), artisans (1), glimpse (1) | Persian (3), Corinth (3), Tus (2), Hassan (2), Fitzgerald (2), pioneered (2), Lionel (2), Ihrer (2), Renaissance (2), artisans (1) |
| Fort Worth | Uhr, Cooke, Weld, Pacers, pok | Uhr, Cooke, Weld, Pacers, pok, Brewers, Glouce, vois, Fairfield, Stoke |
| Frankfurt (7 prompts) | Frankie (5), Oprah (3), Indianapolis (3), skys (2), Carpet (2) | Frankie (6), Oprah (4), Indianapolis (4), skys (3), Fortnite (3), Carpet (2), Farage (2), Salesforce (2), Brick (2), Yah (2) |
| Fuzhou (2 prompts) | Oro (1), Newport (1), Ranch (1), Harbor (1), Chatt (1) | Oro (1), Newport (1), Ranch (1), Harbor (1), Chatt (1), Swansea (1), villagers (1), ocean (1), Cherokee (1), Plymouth (1) |
| Gdańsk (2 prompts) | Hindered (1), coastal (1), Ziel (1), maritime (1), Beitrag (1) | Hindered (1), coastal (1), Ziel (1), maritime (1), Beitrag (1), ocean (1), ext (1), fishermen (1), Zuk (1), sailor (1) |
| Geneva (2 prompts) | quaternion (2), quart (2), Vale (1), Quinn (1), genes (1) | quaternion (2), quart (2), Vale (1), Quinn (1), genes (1), genetics (1), Sabha (1), glimpse (1), gauche (1), detention (1) |
| Germany (41 prompts) | countries (39), Europe (39), Africa (29), Scandin (23), Americas (18) | countries (39), Europe (39), Africa (30), Scandin (26), Americas (22), continent (16), worldwide (4), Asia (3), California (2), Yugoslavia (2) |
| Giza (2 prompts) | Abdel (2), Quran (2), Sinai (2), nevertheless (1), pyramid (1) | Abdel (2), Quran (2), Sinai (2), Ibrahim (2), pyramid (2), Libyan (2), oasis (2), nevertheless (1), Gaza (1), Nile (1) |
| Glasgow (2 prompts) | Swansea (1), Clyde (1), Klopp (1), Tacoma (1), Osw (1) | Swansea (1), Clyde (1), Klopp (1), Tacoma (1), Osw (1), Louisville (1), Krak (1), Winnipeg (1), Goth (1), Blackhawks (1) |
| Gothenburg | Birmingham, Alabama, collision, Bengals, grouped | Birmingham, Alabama, collision, Bengals, grouped, corners, Bam, organized, Shay, behind |
| Granada | granularity, MILF, tamp, grads, Granite | granularity, MILF, tamp, grads, Granite, graduation, Durham, duration, Barker, Mature |
| Haifa | haunt, FILTER, Sey, haar, hac | haunt, FILTER, Sey, haar, hac, CONDITIONS, uart, wildcard, Singles, INTERRU |
| Hamburg (2 prompts) | harbour (1), sneakers (1), seaside (1), shoes (1), inland (1) | harbour (1), sneakers (1), seaside (1), shoes (1), inland (1), Decompiled (1), offshore (1), burgers (1), coastal (1), samen (1) |
| Hanoi (3 prompts) | Kremlin (3), downtown (2), Manhattan (2), basement (1), NYC (1) | Kremlin (3), downtown (2), Manhattan (2), Alexandre (2), NYC (2), appointment (2), basement (1), burner (1), Taipei (1), galer (1) |
| Havana (2 prompts) | Castro (1), Babylon (1), Banco (1), Qatar (1), Maduro (1) | Castro (1), Babylon (1), Banco (1), Qatar (1), Maduro (1), Singapore (1), Javier (1), internationally (1), Pablo (1), Hussein (1) |
| Helsinki | Kremlin, Westminster, wearer, Authorities, Irma | Kremlin, Westminster, wearer, Authorities, Irma, Gotham, Mandela, ISIL, utc, slipping |
| Hiroshima | Wolver, Missouri, Falk, Worcester, enlisted | Wolver, Missouri, Falk, Worcester, enlisted, Erie, Greenville, Alabama, hardened, Clears |
| Hong Kong | Auckland, Trinidad, harbour, island, Kee | Auckland, Trinidad, harbour, island, Kee, lak, Rain, Seah, ellas, Bang |
| Houston | CALLBACK, Rosenstein, Marketable, CHK, Raq | CALLBACK, Rosenstein, Marketable, CHK, Raq, ext, Lauderdale, lehet, GDK, gangbang |
| Hyderabad (2 prompts) | Zuk (1), Pune (1), Poz (1), Karnataka (1), Raqqa (1) | Zuk (1), Pune (1), Poz (1), Karnataka (1), Raqqa (1), Hyundai (1), ext (1), Gujarat (1), Preston (1), Bangalore (1) |
| Innsbruck (2 prompts) | Tahoe (2), skiing (2), Edmonton (2), incest (2), Eis (1) | Tahoe (2), skiing (2), Edmonton (2), incest (2), inland (2), Eis (1), ski (1), checkpoints (1), ext (1), Gast (1) |
| Ireland | Europe, countries, worldwide, Americas, Africa | Europe, countries, worldwide, Americas, Africa, globally, internationally |
| Isfahan (2 prompts) | recounts (1), Jews (1), assumes (1), Jewish (1), absorbed (1) | recounts (1), Jews (1), assumes (1), Jewish (1), absorbed (1), artisans (1), Has (1), famously (1), Flickr (1), domina (1) |
| Islamabad (2 prompts) | diplomatic (2), embassy (1), Bethesda (1), Maryland (1), Politico (1) | diplomatic (2), embassy (1), Bethesda (1), Maryland (1), Politico (1), skiing (1), senators (1), Arlington (1), lobbyist (1), federal (1) |
| Istanbul (46 prompts) | Constantin (25), Brooklyn (12), Erdogan (10), Reef (9), NYC (9) | Constantin (28), Brooklyn (15), Byz (13), Reef (12), Mediterranean (12), NYC (11), Erdogan (10), boutique (9), Milano (9), offshore (8) |
| Jakarta (2 prompts) | Mohammad (2), Urdu (2), Mahmoud (1), DOJ (1), Abdul (1) | Mohammad (2), Urdu (2), Mahmoud (2), Abdul (2), ASA (2), DOJ (1), Maduro (1), Ahmad (1), Naj (1), Kremlin (1) |
| Jerusalem (4 prompts) | Hebrew (2), Jewish (2), Zionist (2), Jews (2), nesta (1) | Hebrew (2), Jewish (2), Zionist (2), Jews (2), nesta (2), biblical (2), Netanyahu (2), Capitals (1), Bulldogs (1), Downtown (1) |
| Kabul | Zucker, Vinci, Kaepernick, Wrest, MILF | Zucker, Vinci, Kaepernick, Wrest, MILF, ung, Cubs, Maduro, Zam, Ruf |
| Karachi | Philly, Philadelphia, Brooklyn, Bangladesh, Jamaica | Philly, Philadelphia, Brooklyn, Bangladesh, Jamaica, Bombay, Jersey, NYC, Newark, Gujar |
| Kharkiv | Sikh, Baltic, Putin, Crimea, Chiefs | Sikh, Baltic, Putin, Crimea, Chiefs, Pune, Blackburn, Khan, Kush, Boris |
| Kiel | downtown, Dayton, Indianapolis, Toledo, Dortmund | downtown, Dayton, Indianapolis, Toledo, Dortmund, Blvd, Cincinnati, Louisville, Springfield, Jacksonville |
| Kiev (3 prompts) | Kensington (1), disclosed (1), inoc (1), Bangalore (1), kit (1) | Kensington (1), disclosed (1), inoc (1), Bangalore (1), kit (1), logistic (1), Burb (1), Aleppo (1), killing (1), nationally (1) |
| Kobe | CALLBACK, abbreviation, zoning, casing, URI | CALLBACK, abbreviation, zoning, casing, URI, wording, THEME, marker, shorthand, Junction |
| Krakow (3 prompts) | Yellowstone (2), Arcade (1), Kang (1), jak (1), Seahawks (1) | Yellowstone (2), Kang (2), Katrina (2), Bik (2), Arcade (1), jak (1), Seahawks (1), Kitty (1), rec (1), Rath (1) |
| Kraków (2 prompts) | Pompe (1), raft (1), Napoli (1), CLAIM (1), rec (1) | CLAIM (2), Jessie (2), Pompe (1), raft (1), Napoli (1), rec (1), limb (1), Aberdeen (1), Rach (1), nearby (1) |
| Lagos | Lond, Marseille, Modelo, Napoli, Bombay | Lond, Marseille, Modelo, Napoli, Bombay, Producto, Portland, Lon, Tacoma, Venez |
| Lahore (2 prompts) | Punjab (2), Sikh (2), Urdu (1), Rochester (1), pak (1) | Punjab (2), Sikh (2), Laurie (2), Urdu (1), Rochester (1), pak (1), Mahar (1), Worcester (1), Sunni (1), Lanc (1) |
| Las Vegas (2 prompts) | lasers (1), Boise (1), casino (1), Nashville (1), Honolulu (1) | downtown (2), lasers (1), Boise (1), casino (1), Nashville (1), Honolulu (1), Nevada (1), Gotham (1), Pavilion (1), Hollywood (1) |
| Ljubljana (2 prompts) | downtown (2), Auckland (1), adjunct (1), lect (1), Honolulu (1) | downtown (2), Auckland (2), adjunct (1), lect (1), Honolulu (1), Lond (1), adj (1), chr (1), commuting (1), Edmonton (1) |
| London (61 prompts) | Thames (30), Brexit (19), NHS (18), NYC (15), Retorna (11) | Thames (30), Brexit (24), NHS (22), GBP (18), NYC (15), Yorkshire (15), BBC (15), Surrey (14), Retorna (13), Buckingham (13) |
| Los Angeles (6 prompts) | Philadelphia (3), UCLA (2), loser (1), Californ (1), Syracuse (1) | Philadelphia (3), Milwaukee (3), UCLA (2), Syracuse (2), Pasadena (2), Lakers (2), Minneapolis (2), Tampa (2), USC (2), loser (1) |
| Lucknow | Uttar, Punjab, Bangalore, Hindi, Bihar | Uttar, Punjab, Bangalore, Hindi, Bihar, Rajasthan, Pune, Singh, Bengal, Pradesh |
| Luxor (4 prompts) | luxe (3), cliffs (3), oasis (2), luxurious (1), raft (1) | luxe (3), cliffs (3), oasis (2), raft (2), Saf (2), baja (2), luxurious (1), threesome (1), shuttle (1), Sinai (1) |
| Lyon | hometown, Rural, Alamofire, TYPO, caravan | hometown, Rural, Alamofire, TYPO, caravan, Communities, Raptors, Ree, notifier, Tucson |
| Madrid (16 prompts) | Nation (8), Madison (6), Downing (6), NYC (3), Buckingham (3) | Downing (10), Nation (9), Madison (6), Buckingham (6), NYC (5), Lond (4), metropolitan (3), Manhattan (3), President (3), Ramos (3) |
| Malmö | Located, Asheville, Mou, Abed, near | Located, Asheville, Mou, Abed, near, fists, Lans, Dayton, playa, marker |
| Marrakesh | Maui, Marriott, tourism, tavern, Voll | Maui, Marriott, tourism, tavern, Voll, setup, spa, marble, mtx, Merr |
| Melbourne | Lauderdale, Merrill, CALLBACK, Toledo, mural | Lauderdale, Merrill, CALLBACK, Toledo, mural, pillar, BUF, mouse, GDK, boarded |
| Mexico (3 prompts) | Europe (3), Countries (2), countries (1), Asia (1), Africa (1) | Europe (3), Countries (2), countries (1), Asia (1), Africa (1) |
| Mexico City | Honduras, tacos, Nicaragua, Bolivia, Hispanic | Honduras, tacos, Nicaragua, Bolivia, Hispanic, Latino, mest, Puerto, Americas, Uruguay |
| Miami | Taipei, subway, Brooklyn, metro, downtown | Taipei, subway, Brooklyn, metro, downtown, NYC, tokenize, nightlife, hustle, MSI |
| Milan (4 prompts) | Manchester (3), Lomb (3), Milwaukee (2), Ferdinand (1), Pearce (1) | Manchester (3), Lomb (3), Milwaukee (2), Newark (2), Ferdinand (1), Pearce (1), Sharma (1), Winnipeg (1), herself (1), anyway (1) |
| Minsk | Dud, Panc, mourn, Alumni, Bashar | Dud, Panc, mourn, Alumni, Bashar, leveling, Zah, Saud, Rahman, Bangalore |
| Modena | modulation, Mods, moderator, Modi, modo | modulation, Mods, moderator, Modi, modo, modem, mixture, selections, tomorrow, modal |
| Moscow (18 prompts) | Kremlin (15), Putin (8), NYC (5), Soviets (5), Vladimir (5) | Kremlin (15), Putin (8), Sergei (7), Dmitry (7), Stalin (7), Bolshevik (7), NYC (5), Soviets (5), Vladimir (5), Manhattan (5) |
| Mumbai | Maharashtra, Pune, Bahrain, TMZ, Maven | Maharashtra, Pune, Bahrain, TMZ, Maven, Bollywood, Rajasthan, Salman, Gaza, township |
| Munich (27 prompts) | Bav (19), Bayern (16), Demp (15), Mustang (6), Dallas (5) | Bav (19), Demp (19), Bayern (17), Minneapolis (12), MPL (9), Mustang (8), BMW (8), Dallas (7), museums (5), anchors (5) |
| Nairobi (2 prompts) | Perth (2), Ken (1), favourite (1), Bombay (1), Boise (1) | Perth (2), Bangalore (2), Ken (1), favourite (1), Bombay (1), Boise (1), compte (1), Seahawks (1), Singapore (1), Hawaiian (1) |
| Nanjing | Nano, Nass, Norfolk, Nunes, NIR | Nano, Nass, Norfolk, Nunes, NIR, Raqqa, Nursery, Riy, Naj, Neh |
| Naples (4 prompts) | Tampa (4), Boca (3), Saras (2), Napoli (1), Ferdinand (1) | Tampa (4), Boca (4), Saras (2), dames (2), Nunes (2), Napoli (1), Ferdinand (1), Morales (1), tying (1), refrigerator (1) |
| New Delhi (2 prompts) | Sidd (1), NYC (1), National (1), Manhattan (1), subsidized (1) | Madison (2), Sidd (1), NYC (1), National (1), Manhattan (1), subsidized (1), Bloomberg (1), Nov (1), Congressional (1), governmental (1) |
| New York (18 prompts) | NYC (11), Bronx (10), Brooklyn (7), NYPD (7), Manhattan (6) | NYC (11), Bronx (11), Brooklyn (10), NYPD (10), Manhattan (7), Yankee (7), Gotham (7), Albany (7), Harlem (7), Stamford (6) |
| Nice | Portsmouth, locals, Nottingham, travelers, Nathan | Portsmouth, locals, Nottingham, travelers, Nathan, Beit, Trom, Tooltip, Bedford, Oman |
| Orlando (4 prompts) | Nashville (4), Tampa (3), Jacksonville (3), Oklahoma (3), Florida (2) | Nashville (4), Oklahoma (4), Tampa (3), Jacksonville (3), Florida (3), Tulsa (3), Tucson (3), Greenville (2), Ohio (2), Raleigh (1) |
| Oslo (5 prompts) | politicians (2), Blasio (1), grues (1), INA (1), utc (1) | politicians (2), Bloomberg (2), Thames (2), analysts (2), Blasio (1), grues (1), INA (1), utc (1), Metropolitan (1), BCHP (1) |
| Ottawa | Kremlin, Georgetown, Retorna, diplomatic, patriotic | Kremlin, Georgetown, Retorna, diplomatic, patriotic, ACLU, bureaucrats, dcc, CAPITAL, IDC |
| Oxford | Rhodes, Wyoming, safari, Wildcats, Tanz | Rhodes, Wyoming, safari, Wildcats, Tanz, dado, ext, Aleppo, Ruf, RTVF |
| Paris (16 prompts) | NYC (10), Manhattan (8), Pierre (7), Gotham (6), Jean (4) | NYC (10), Pierre (9), Manhattan (8), Gotham (7), Harlem (7), Lond (5), Jean (4), Macron (4), Constantin (4), NYPD (4) |
| Persepolis (2 prompts) | peri (2), perch (2), Pero (2), perk (1), perf (1) | peri (2), perch (2), perk (2), Pero (2), perf (1), Perm (1), archaeological (1), perm (1), Providence (1), temples (1) |
| Pittsburgh | Steelers, Wolverine, Winnipeg, Michigan, Erie | Steelers, Wolverine, Winnipeg, Michigan, Erie, Chattanooga, Akron, Cincinnati, Manitoba, Dayton |
| Portugal | Europe, countries, Scandin, Africa, Yugoslavia | Europe, countries, Scandin, Africa, Yugoslavia, Uruguay |
| Prague (6 prompts) | Audrey (3), Pasadena (3), Sey (2), Premiership (2), Reign (1) | Audrey (4), Pasadena (3), Premiership (3), Sey (2), Pry (2), Reign (2), Monaco (2), DISPATCH (2), Elis (2), Kushner (2) |
| Pyongyang | Benghazi, Baghd, Saddam, CRUD, Hezbollah | Benghazi, Baghd, Saddam, CRUD, Hezbollah, Rahman, jihad, Maduro, Gratis, Mahm |
| Reykjavik (2 prompts) | Taipei (1), Reyes (1), Globe (1), Vega (1), glitter (1) | Taipei (1), Reyes (1), Globe (1), Vega (1), glitter (1), Rex (1), hoodie (1), Gomez (1), HOUR (1), Tango (1) |
| Rio de Janeiro | bordel, oui, cruise, Monaco, reef | bordel, oui, cruise, Monaco, reef, Disneyland, yacht, Titanic, tuna, inland |
| Rome (25 prompts) | Vatican (15), Romans (8), Roman (6), Roma (6), Giul (6) | Vatican (18), Francesco (9), Romans (8), Giul (7), Conte (7), Roman (6), Roma (6), Ital (5), Catholics (5), Luigi (5) |
| Saint Petersburg (5 prompts) | Enlight (3), Dort (2), WINAPI (2), Insider (1), subparagraph (1) | Enlight (3), WINAPI (3), Dort (2), Insider (2), Insets (2), nineteenth (2), Mister (2), fail (2), eighty (2), barred (2) |
| Salzburg | saline, saliva, salts, Salisbury, salaries | saline, saliva, salts, Salisbury, salaries, salads, lodge, ski, puss, Salon |
| San Antonio | Hayward, MOCK, Yong, Ziel, Feather | Hayward, MOCK, Yong, Ziel, Feather, Monterey, boarded, Yok, milestones, Honolulu |
| San Francisco (8 prompts) | Oakland (4), California (3), ext (3), Pacific (3), Sacramento (3) | Pacific (4), Oakland (4), Sacramento (4), Monterey (4), California (3), ext (3), Yosemite (3), pratique (3), Oregon (3), Californ (2) |
| Santiago (2 prompts) | Antarctic (1), ext (1), Spokane (1), Aws (1), Sergey (1) | Antarctic (1), ext (1), Spokane (1), Aws (1), Sergey (1), ung (1), Auckland (1), Ans (1), sled (1), Ngb (1) |
| Scotland | Scottish, Europe, Scots, Africa, Scandin | Scottish, Europe, Scots, Africa, Scandin, countries, Wales, Asia |
| Seattle | Tampa, Appalachian, Cincinnati, Oklahoma, Jacksonville | Tampa, Appalachian, Cincinnati, Oklahoma, Jacksonville, Omaha, Wisconsin, Seahawks, Minnesota, Boise |
| Seoul (2 prompts) | Auckland (1), Taipei (1), Parl (1), Realty (1), guild (1) | Auckland (1), Taipei (1), Parl (1), Realty (1), guild (1), neh (1), capitals (1), downtown (1), Carlo (1), intra (1) |
| Seville (3 prompts) | Sevilla (3), seaside (2), Southampton (2), Sey (1), seizure (1) | Sevilla (3), seaside (2), Southampton (2), selenium (2), Sey (1), seizure (1), Indianapolis (1), Swansea (1), playback (1), Birmingham (1) |
| Shanghai (4 prompts) | Brooklyn (2), NYC (2), Tencent (1), Rigidbody (1), Singapore (1) | Brooklyn (2), NYC (2), Bombay (2), Greenwich (2), Sharks (2), Tencent (1), Rigidbody (1), Singapore (1), skys (1), Alibaba (1) |
| Sofia (9 prompts) | Sophia (9), Milano (5), Pavel (2), Sloven (2), Yugosl (2) | Sophia (9), Milano (5), Sloven (3), Roma (3), IDF (3), Pavel (2), Yugosl (2), Chelsea (2), annex (2), Micha (2) |
| St. Petersburg (10 prompts) | ceremonial (3), sunk (3), perhaps (2), familiar (2), pomp (2) | formal (4), ceremonial (3), perhaps (3), sunk (3), pomp (3), Sta (3), princes (3), familiar (2), Alic (2), hopefully (2) |
| Stockholm (14 prompts) | Gotham (8), NYC (6), nightlife (3), Manhattan (3), meisje (3) | Gotham (8), NYC (7), Manhattan (5), nightlife (4), Weinstein (4), meisje (4), Constantin (4), proport (4), subway (4), Bollywood (3) |
| Strasbourg | Strait, strang, striped, Gron, straw | Strait, strang, striped, Gron, straw, truncate, stride, trunk, strut, checkpoints |
| Switzerland | countries, Europe, Scandin, Africa | countries, Europe, Scandin, Africa |
| Sydney (3 prompts) | Sidney (3), Santos (2), NYC (1), NSW (1), Bair (1) | Sidney (3), Santos (3), NYC (2), NSW (1), Bair (1), Siri (1), cheered (1), Darling (1), Brooklyn (1), Combo (1) |
| Tallinn | Pavel, Sloven, Kremlin, Sutton, Slut | Pavel, Sloven, Kremlin, Sutton, Slut, Ukr, Tobias, Dmitry, Ukrain, Stephan |
| Tashkent | Putin, Dmitry, Premier, Kremlin, presidential | Putin, Dmitry, Premier, Kremlin, presidential, Boris, Eugene, Soviets, thaw, Russ |
| Tehran (10 prompts) | Kremlin (5), Congress (4), Trudeau (3), Taipei (2), presidential (2) | Kremlin (6), Congress (5), Trudeau (5), Retrieved (4), Retorna (3), Reagan (3), Taipei (2), presidential (2), Presidential (2), rally (2) |
| Thessaloniki | Township, Locator, nearby, commune, villages | Township, Locator, nearby, commune, villages, residents, marker, vicinity, hometown, Junction |
| Tokyo (7 prompts) | NYC (4), Retorna (4), downtown (3), metropolitan (3), Observatory (2) | Retorna (5), NYC (4), downtown (3), metropolitan (3), Kremlin (3), NYPD (3), Observatory (2), Greenwich (2), Manhattan (2), subway (2) |
| Toronto (2 prompts) | Tampa (2), Newark (1), Ontario (1), Brooklyn (1), Winnipeg (1) | Tampa (2), Newark (2), Ontario (1), Brooklyn (1), Winnipeg (1), Harlem (1), Cincinnati (1), Cabr (1), Auckland (1), NYC (1) |
| Turin (2 prompts) | ext (1), Turbo (1), concession (1), turbines (1), Bris (1) | ext (1), Turbo (1), concession (1), turbines (1), Bris (1), Utah (1), genu (1), Tibet (1), titular (1), Bender (1) |
| Turkey | countries, Europe, nations, Yugoslavia, Scandin | countries, Europe, nations, Yugoslavia, Scandin |
| Ulaanbaatar (2 prompts) | Rohingya (2), Nagar (1), Punjab (1), junto (1), Tibet (1) | Rohingya (2), Sioux (2), Sikh (2), Nagar (1), Punjab (1), junto (1), Tibet (1), Tibetan (1), Nguyen (1), Lama (1) |
| Valencia | valves, Valent, Valor, Valle, Valerie | valves, Valent, Valor, Valle, Valerie, valuation, Toledo, Validators, Vue, Midlands |
| Valletta (3 prompts) | valuation (2), valves (2), Valerie (2), valued (2), invaluable (2) | valuation (2), valves (2), Valerie (2), valued (2), invaluable (2), valleys (2), fisheries (1), abduction (1), paz (1), flotation (1) |
| Venice (14 prompts) | seaside (8), coastal (7), Venez (5), ocean (3), Leonardo (3) | seaside (9), coastal (7), Venez (6), carnival (6), ocean (4), Leonardo (4), reefs (4), Sic (4), UNESCO (3), Philippe (3) |
| Vienna (18 prompts) | Wien (17), Sophia (8), Aust (6), Viktor (6), Philly (5) | Wien (17), Sophia (9), Viktor (8), Aust (6), Philly (6), Philadelphia (6), Vaughan (6), Waterloo (5), Nashville (5), NYC (4) |
| Vilnius | Azerbai, Kremlin, Ukrain, choking, Ukr | Azerbai, Kremlin, Ukrain, choking, Ukr, Urb, Pavel, gleich, Yugosl |
| Warsaw (17 prompts) | Harlem (6), urban (5), NYC (4), Bangalore (4), Kremlin (3) | Harlem (9), urban (6), Bangalore (6), Welfare (6), Kremlin (5), NYC (5), Gaines (5), Sao (5), Gotham (4), Urb (4) |
| Washington (4 prompts) | Capitol (3), Georgetown (2), Maryland (2), Redskins (2), presidential (2) | Capitol (3), Georgetown (3), Redskins (3), Obama (3), Maryland (2), Smithsonian (2), Congressional (2), presidential (2), Barack (2), Parliament (1) |
| Washington, D.C. (8 prompts) | Congressional (6), USDA (6), Smithsonian (6), Maryland (4), Barack (2) | Smithsonian (7), Congressional (6), USDA (6), Maryland (4), President (3), Americ (3), federally (3), Arlington (3), FBI (3), Barack (2) |
| Wrocław | local, brushing, Glouce, cord, radial | local, brushing, Glouce, cord, radial, hilar, rop, patches, overflowing, hometown |
| Xi'an | Astros, Qatar, Xiaomi, Vinci, UIS | Astros, Qatar, Xiaomi, Vinci, UIS, Taj, tau, Cristiano, Isis, masa |
| Yekaterinburg | nearby, township, locally, villagers, hike | nearby, township, locally, villagers, hike, Spicer, Nack, provisioning, nearest, jade |
| Yerevan (2 prompts) | neu (1), Decompiled (1), Lansing (1), blindly (1), poisoned (1) | neu (1), Decompiled (1), Lansing (1), blindly (1), poisoned (1), Raq (1), Kremlin (1), worthy (1), rewarding (1), Nutzung (1) |
| Zagreb | Bav, Laguna, Nederland, Maharashtra, EXTRA | Bav, Laguna, Nederland, Maharashtra, EXTRA, Mazda, pagan, Lug, Giovanni, Florida |
| Zurich | Silicone, Zack, turnover, OCI, Zion | Silicone, Zack, turnover, OCI, Zion, Zuckerberg, Zika, hoodie, Scientology, Corpus |

## Park → country → capital

### True answers (106 answers, 514 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Accra | Feinstein, NYC, Mumbai, Blasio, Manhattan | Feinstein, NYC, Mumbai, Blasio, Manhattan, Bombay, Rao, Chennai, NYPD, Kapoor |
| Addis Ababa (4 prompts) | NYC (2), Mumbai (2), Barcelona (1), Tibet (1), Chennai (1) | Seattle (3), NYC (2), Mumbai (2), Chennai (2), Pune (2), Minneapolis (2), Auckland (2), metropolitan (2), Added (2), Barcelona (1) |
| Algiers | Africa, Lagos, Niger, Johannesburg, Acrobat | Africa, Lagos, Niger, Johannesburg, Acrobat, Mumbai, Afro, CFG, Algorithm, pesos |
| Amsterdam (5 prompts) | Chicago (3), Toronto (3), Tottenham (2), NYC (2), Mumbai (2) | Chicago (3), Toronto (3), NYC (3), Mumbai (3), Tottenham (2), Barcelona (2), Minneapolis (2), Istanbul (2), Gotham (2), Venice (2) |
| Ankara (3 prompts) | Government (3), congressional (2), Boise (1), Republican (1), lawmakers (1) | Government (3), congressional (2), Republican (2), lawmakers (2), Politico (2), Boise (1), Applicants (1), Congressional (1), policy (1), Guam (1) |
| Antananarivo (4 prompts) | ants (2), antennas (2), promo (1), cds (1), antenna (1) | ants (2), antennas (2), cds (2), anticipate (2), promo (1), antenna (1), chicago (1), AGAIN (1), Antonio (1), Antar (1) |
| Astana | Election, office, palabras, Sanford, asthma | Election, office, palabras, Sanford, asthma, Kasich, Omaha, Asset, delegation, apps |
| Athens (3 prompts) | Anglic (2), Boston (2), Greenwich (2), Munich (1), ext (1) | Anglic (2), Boston (2), Greenwich (2), Thames (2), Munich (2), NHS (2), ext (1), turnout (1), gangbang (1), Vatican (1) |
| Baku (5 prompts) | Sergei (3), Armen (2), Crimea (2), Aleks (1), Arabian (1) | Sergei (3), Armen (3), Crimea (3), Kurdish (3), Aleks (2), Yuri (2), Kaz (2), Arabs (2), Kiev (2), Arabian (1) |
| Bangkok (4 prompts) | blackmail (3), Istanbul (3), Brussels (2), Shanghai (2), downtown (1) | blackmail (3), Istanbul (3), Mumbai (3), Weinstein (3), Brussels (2), Shanghai (2), subway (2), gunmen (2), Chicago (2), Huffington (2) |
| Bangui | Bangladesh, banging, banged, nesta, Bashar | Bangladesh, banging, banged, nesta, Bashar, Rohingya, Sark, safest, Kurdistan, alleen |
| Basseterre | Caj, Gulf, Bourbon, island, Banc | Caj, Gulf, Bourbon, island, Banc, Bapt, anchor, Bou, Guam, Bast |
| Beijing | Microsoft, Peter, NASA, Congress, Disney | Microsoft, Peter, NASA, Congress, Disney, Apple, Donald, Olympic, Harvard, NYC |
| Belgrade | Yugosl, Balk, Milo, Jug, Bos | Yugosl, Balk, Milo, Jug, Bos, Brisbane, Adri, Lagos, Maced, Karachi |
| Berlin (16 prompts) | Istanbul (8), Kremlin (6), Brussels (4), Metro (4), Brooklyn (3) | Istanbul (11), Vladimir (7), Kremlin (6), Putin (6), Brussels (5), NYC (5), Metro (4), Lenin (4), Brooklyn (3), Seattle (3) |
| Bishkek | Tibetan, Montana, Wyoming, Himal, elk | Tibetan, Montana, Wyoming, Himal, elk, Nep, Kashmir, Bolivia, Boise, Idaho |
| Bogotá (3 prompts) | Brussels (2), Baghdad (2), Istanbul (1), Downing (1), Seattle (1) | Brussels (2), Baghdad (2), NYC (2), Istanbul (1), Downing (1), Seattle (1), Atlanta (1), kang (1), Westminster (1), Dallas (1) |
| Brasília (9 prompts) | congressional (7), Minister (5), governments (5), federal (4), legislative (4) | congressional (7), federal (7), senators (7), Minister (6), governments (6), politicians (5), legislative (4), diplomatic (4), Bundes (3), Secretary (3) |
| Bratislava (3 prompts) | sme (1), ext (1), blindness (1), Brewery (1), Auckland (1) | sme (1), ext (1), blindness (1), Brewery (1), Auckland (1), capitals (1), Dayton (1), attracting (1), singapore (1), creeping (1) |
| Brazzaville | Europeans, Latin, Quebec, Bras, Arabs | Europeans, Latin, Quebec, Bras, Arabs, Alexandre, Colomb, Rousse, diplomats, Alger |
| Bucharest | Buchanan, Istanbul, Constantin, Riyadh, Beirut | Buchanan, Istanbul, Constantin, Riyadh, Beirut, Commissioner, Wohnung, Bureau, blindness, Wishlist |
| Budapest (6 prompts) | Istanbul (5), NYC (4), Munich (4), Manhattan (4), Brussels (3) | Istanbul (5), NYC (4), Munich (4), Manhattan (4), Brussels (4), downtown (3), Sydney (3), Beirut (2), Frankfurt (2), Kiev (2) |
| Buenos Aires (12 prompts) | Sydney (6), Philadelphia (6), Johannesburg (5), Adelaide (4), NYC (3) | Sydney (7), Johannesburg (7), Philadelphia (6), Melbourne (5), Philly (5), Adelaide (4), Broadway (4), NYC (3), Chicago (3), Napoli (3) |
| Cairo | Nile, Sinai, Isis, Pyramid, Pune | Nile, Sinai, Isis, Pyramid, Pune, Johannesburg, Mumbai, Lagos, Bangalore, Karnataka |
| Canberra (9 prompts) | congressional (4), government (4), Kremlin (3), presidential (3), Congressional (2) | government (5), Minister (5), congressional (4), Kremlin (4), politicians (4), senators (4), presidential (3), parliamentary (3), President (3), Congressional (2) |
| Caracas | Suarez, Kiev, Bloomberg, algum, Hast | Suarez, Kiev, Bloomberg, algum, Hast, Feinstein, eval, Beirut, hac, Rosenstein |
| Copenhagen | utc, Mumbai, UNION, Decompiled, NYC | utc, Mumbai, UNION, Decompiled, NYC, GOODMAN, ext, Bombay, BUF, alerted |
| Dakar (2 prompts) | Dakota (2), Seattle (1), Tampa (1), EVT (1), Ramadan (1) | Dakota (2), Seattle (1), Tampa (1), EVT (1), Ramadan (1), Beirut (1), Muslim (1), Denver (1), Daytona (1), Emacs (1) |
| Dodoma (6 prompts) | dodge (6), senators (4), Dodd (4), Deputy (2), Avoid (2) | dodge (6), Dodd (5), senators (4), Avoid (4), Deputy (3), lawmaker (2), gad (2), ministers (2), unaware (2), evade (2) |
| Dublin (3 prompts) | Istanbul (3), NYC (2), Mumbai (1), Kiev (1), metros (1) | Istanbul (3), Kiev (2), NYC (2), Mumbai (1), metros (1), Edinburgh (1), Retorna (1), euro (1), international (1), Baghdad (1) |
| Dushanbe | Kata, Tibetan, Sheikh, bestowed, keys | Kata, Tibetan, Sheikh, bestowed, keys, Zhao, Deputy, Mahar, looping, deco |
| Gaborone | GOLD, JOB, NXT, Howell, peg | GOLD, JOB, NXT, Howell, peg, sacked, spared, Hiring, DDS, Digit |
| Gitega | Viol, Herz, Gat, Cush, mining | Viol, Herz, Gat, Cush, mining, oasis, cycle, visited, Gund, edible |
| Guatemala City (2 prompts) | Honduras (1), Kolkata (1), Belize (1), multinational (1), Nicaragua (1) | Honduras (1), Kolkata (1), Belize (1), multinational (1), Nicaragua (1), Atlanta (1), Haiti (1), Chennai (1), Jamaica (1), Babylon (1) |
| Hanoi | Kremlin, NIH, Cabinet, Pyongyang, legislative | Kremlin, NIH, Cabinet, Pyongyang, legislative, Bundes, Yellowstone, Qin, Yosh, Alexandre |
| Harare (3 prompts) | kafka (2), harmonic (2), political (2), importing (1), Jinping (1) | kafka (3), harmonic (2), political (2), importing (1), Jinping (1), dara (1), Shanghai (1), vorhand (1), Riyadh (1), yuan (1) |
| Havana | Alabama, Chicago, Mississippi, Jamaica, Detroit | Alabama, Chicago, Mississippi, Jamaica, Detroit, Louisiana, Florida, Miami, Libyan, Trotsky |
| Helsinki (16 prompts) | Brussels (9), NYC (7), Westminster (5), Istanbul (5), Dubai (5) | Brussels (10), NYC (8), Westminster (8), Istanbul (8), Dubai (8), Metropolitan (8), Mumbai (7), Kiev (4), Kremlin (4), Athen (4) |
| Islamabad | Baghdad, ISIS, Islamist, Politico, Abu | Baghdad, ISIS, Islamist, Politico, Abu, Haram, Prosecutor, Riyadh, Sharia, EOS |
| Jakarta (12 prompts) | Mumbai (11), Brussels (6), NYC (5), Singapore (5), Riyadh (4) | Mumbai (11), NYC (8), Singapore (7), Brussels (6), Riyadh (6), Dubai (5), Sydney (4), Manhattan (4), Malays (3), frankfurt (3) |
| Jerusalem (8 prompts) | Jesus (4), Jewish (3), Hebrew (3), praying (3), Jews (3) | Jesus (6), Jewish (4), praying (4), prayed (4), theological (4), Hebrew (3), Jews (3), Zionist (3), spiritual (3), Judaism (3) |
| Kabul | Kath, Hindu, Bollywood, Hari, Nep | Kath, Hindu, Bollywood, Hari, Nep, Brussels, Himal, Mumbai, Bengal, Taliban |
| Kampala (6 prompts) | Bangalore (3), Kolkata (3), Chicago (2), Camp (2), Europe (2) | Bangalore (3), Chicago (3), Kolkata (3), NYC (3), Camp (2), Europe (2), Minneapolis (2), Boise (2), Istanbul (2), Kapoor (2) |
| Kathmandu (6 prompts) | Himal (3), Tibetan (2), Cath (2), Pang (2), weekdays (1) | Himal (3), Tibetan (2), Cath (2), Pang (2), IDX (2), angle (2), Kerala (2), grues (2), metropolitan (2), RVA (2) |
| Kigali (2 prompts) | nesta (2), pact (1), rubble (1), feats (1), disproportion (1) | nesta (2), feats (2), pact (1), rubble (1), disproportion (1), turnovers (1), libertine (1), granite (1), ext (1), RESET (1) |
| Kinshasa (4 prompts) | kinetic (4), kinase (4), Alger (2), Pierre (1), Macron (1) | kinetic (4), kinase (4), Alger (2), Pierre (2), Brussels (2), Geneva (2), Jean (2), Marseille (2), Francois (2), Macron (1) |
| Kuala Lumpur | Istanbul, Chennai, Singapore, Dubai, Toronto | Istanbul, Chennai, Singapore, Dubai, Toronto, Miami, Chicago, Atlanta, Lahore, Tamil |
| Kyiv (3 prompts) | Sydney (2), LGBTQ (2), Biden (2), COVID (2), Crimea (1) | Sydney (3), LGBTQ (3), Biden (2), COVID (2), Crimea (1), Putin (1), Kylie (1), Sergey (1), Madison (1), Melbourne (1) |
| Libreville | Liber, libido, librarian, libs, Libya | Liber, libido, librarian, libs, Libya, Lexus, Zion, Pyongyang, Abrams, freeing |
| Lilongwe | Tulsa, Denver, Manhattan, Honolulu, Shanghai | Tulsa, Denver, Manhattan, Honolulu, Shanghai, Lafayette, Harlem, Beirut, Baghdad, clit |
| Lima (2 prompts) | Auckland (1), IDC (1), parliament (1), Alphabet (1), Minist (1) | IDC (2), Auckland (1), parliament (1), Alphabet (1), Minist (1), Polit (1), legislation (1), columna (1), Riyadh (1), allocator (1) |
| Lisbon | Istanbul, Constantin, Mumbai, Chennai, Hindu | Istanbul, Constantin, Mumbai, Chennai, Hindu, Bombay, European, Singapore, Byz, Judith |
| Ljubljana | inconvenient, electorate, metropolitan, constituency, Brussels | inconvenient, electorate, metropolitan, constituency, Brussels, egret, Stamford, vai, hele, Gotham |
| London (14 prompts) | Europe (5), Retorna (5), NYC (5), Mumbai (4), Thames (3) | Europe (6), NYC (6), Retorna (5), Mumbai (5), Thames (5), Manhattan (4), Brexit (3), Istanbul (3), Surrey (3), Hollywood (3) |
| Luanda (3 prompts) | Luo (3), Africa (1), MPL (1), Liu (1), Moz (1) | Luo (3), Liu (2), Africa (1), MPL (1), Moz (1), Deng (1), Wang (1), Sudan (1), Capitals (1), Jiang (1) |
| Lusaka | metro, Riyadh, smo, EINVAL, Ciudad | metro, Riyadh, smo, EINVAL, Ciudad, choking, NYC, urban, Indianapolis, Constantin |
| Madrid (14 prompts) | Brussels (8), Madison (5), Mumbai (5), NYC (4), Congress (4) | Brussels (8), Congress (7), Madison (7), NYC (6), Chicago (6), Mumbai (5), Istanbul (5), Manhattan (4), President (4), national (3) |
| Manila | Mumbai, Indones, European, Constantin, Bombay | Mumbai, Indones, European, Constantin, Bombay, Asia, nationwide, Brussels, multinational, metropolitan |
| Maputo | Maps, Preview, Studios, Plaza, Bangalore | Maps, Preview, Studios, Plaza, Bangalore, ciudad, Dias, internationally, legis, backstage |
| Maseru | Swansea, Rut, Horton, Cumberland, Yun | Swansea, Rut, Horton, Cumberland, Yun, INIT, intentions, Vet, Hut, Bergen |
| Minsk (3 prompts) | Sergei (2), Ukrain (2), lem (1), Vander (1), Dmitry (1) | Sergei (2), Ukrain (2), Dmitry (2), Kiev (2), Donetsk (2), lem (1), Vander (1), Putin (1), Nicar (1), Kremlin (1) |
| Moscow (17 prompts) | Kremlin (17), NYC (8), Putin (7), Brussels (6), Stalin (5) | Kremlin (17), Manhattan (10), Putin (9), Stalin (9), NYC (8), Brussels (7), Milan (6), Vladimir (6), Hollywood (6), Dmitry (6) |
| N'Djamena | Allah, Ibn, distributed, icing, Islamic | Allah, Ibn, distributed, icing, Islamic, Alam, rollback, Sultan, Imam, Chronicles |
| Nairobi (6 prompts) | Bangalore (3), Pune (3), Mumbai (2), Perth (2), Chicago (1) | Bangalore (3), Pune (3), Mumbai (3), Perth (2), Sydney (2), Bombay (2), Brisbane (2), compte (2), Chicago (1), Seattle (1) |
| New Delhi (19 prompts) | NYC (10), Manhattan (8), Congress (7), NYPD (6), Mumbai (5) | NYC (11), Manhattan (9), Congress (9), NYPD (8), NATO (6), government (6), Mumbai (5), President (5), national (5), NYT (4) |
| Nouakchott | nouveau, Nevada, Nuevo, Louisiana, Khal | nouveau, Nevada, Nuevo, Louisiana, Khal, Livingston, reef, Cherokee, Nass, Oasis |
| Nuuk | nuances, Guam, Maui, Nun, island | nuances, Guam, Maui, Nun, island, Kata, Samoa, Chu, Arctic, sincerity |
| Oslo (11 prompts) | Brussels (7), parliamentary (6), Cabinet (4), Bloomberg (4), Istanbul (4) | Brussels (8), parliamentary (8), Cabinet (6), Istanbul (6), Bloomberg (6), INA (5), Chicago (4), politicians (3), Scandinavian (2), Norse (2) |
| Ottawa (27 prompts) | Toronto (8), Congress (7), Ontario (7), politicians (7), congressional (6) | OECD (11), Toronto (9), government (9), Obama (9), Congress (8), congressional (8), politicians (8), Quebec (8), RCMP (8), Ontario (7) |
| Panama City | Loki, Rockefeller, AMAZ, Qatar, NIH | Loki, Rockefeller, AMAZ, Qatar, NIH, Kremlin, Miami, Palace, Yankees, Singapore |
| Paris (7 prompts) | NYC (6), Boston (3), Chicago (3), Brussels (3), Manhattan (3) | NYC (7), Chicago (5), Europe (4), Parliament (4), Boston (3), Brussels (3), Manhattan (3), Congress (3), Harvard (3), President (3) |
| Phnom Penh | presidential, junto, toughness, hookers, pivot | presidential, junto, toughness, hookers, pivot, extremists, patriotic, senators, supremacist, embargo |
| Podgorica | pods, episode, Podcast, Wales, Clemson | pods, episode, Podcast, Wales, Clemson, Gros, Tasmania, locator, villages, device |
| Prague (2 prompts) | Istanbul (2), metropolitan (1), Brussels (1), Beirut (1), DISPATCH (1) | Istanbul (2), metropolitan (1), Brussels (1), Beirut (1), DISPATCH (1), European (1), Pasadena (1), Monaco (1), range (1), Constantin (1) |
| Quito (3 prompts) | Seattle (2), subdivisions (1), Toledo (1), Hawaii (1), Regents (1) | Seattle (2), subdivisions (1), Toledo (1), Hawaii (1), Regents (1), Mitar (1), tropical (1), quarters (1), disagreements (1), Vancouver (1) |
| Rabat | rabbits, diplomatic, redes, Congress, legis | rabbits, diplomatic, redes, Congress, legis, Parliament, monarch, Presidential, plur, Reagan |
| Ramallah | Ramadan, Rahman, Abdullah, Bangladesh, Sheikh | Ramadan, Rahman, Abdullah, Bangladesh, Sheikh, Islam, Arabic, Kuwait, Imam, Ramirez |
| Reykjavík (2 prompts) | Sydney (1), Reyes (1), Barcelona (1), Tasmania (1), Rio (1) | Vancouver (2), Moreno (2), Sydney (1), Reyes (1), Barcelona (1), Tasmania (1), Rio (1), RTAL (1), Felipe (1), Papua (1) |
| Riga (3 prompts) | Saga (1), lobster (1), trustee (1), Eston (1), Admir (1) | Saga (1), lobster (1), trustee (1), Eston (1), Admir (1), decorators (1), Lair (1), pau (1), suscept (1), Baltic (1) |
| Rome (20 prompts) | Vatican (14), Romans (10), Roman (6), Brussels (6), Venice (4) | Vatican (16), Romans (11), Brussels (8), Venice (7), IMF (7), Roman (6), Europe (6), Giul (4), Conte (3), European (3) |
| San José (2 prompts) | Puerto (1), Sierra (1), Francisco (1), Silicon (1), Hawai (1) | Sanchez (2), Puerto (1), Sierra (1), Francisco (1), Silicon (1), Hawai (1), sanitary (1), Palo (1), mest (1), Honduras (1) |
| Santiago (8 prompts) | NYC (3), executive (3), Bolivia (2), Capital (2), Bangalore (2) | NYC (3), executive (3), Bangalore (3), Bolivia (2), Capital (2), corporate (2), weekdays (2), Belfast (2), Manhattan (2), Gotham (2) |
| Sarajevo (3 prompts) | Muslim (2), Arabic (2), Muslims (1), Islamic (1), Islam (1) | Baghdad (3), Muslim (2), Arabic (2), mosques (2), Islam (2), Arabs (2), Quran (2), Abdul (2), Muslims (1), Islamic (1) |
| Seoul | metropolitan, Shanghai, Regents, milan, subsidized | metropolitan, Shanghai, Regents, milan, subsidized, keyed, sina, Sydney, capitals, Gilles |
| Skopje | Scandinavian, internationally, nationwide, European, UNESCO | Scandinavian, internationally, nationwide, European, UNESCO, AUD, Singapore, Nordic, Shanghai, Welfare |
| Sofia (2 prompts) | Sophia (2), Geneva (2), IDF (2), Eva (1), metro (1) | Sophia (2), Geneva (2), IDF (2), metro (2), Eva (1), semiclassical (1), Alicia (1), annex (1), Lucia (1), Leipzig (1) |
| Stockholm (20 prompts) | NYC (13), Gotham (12), Manhattan (8), Boston (5), nightlife (5) | NYC (13), Gotham (13), Manhattan (9), Istanbul (8), Mumbai (8), nightlife (7), subway (7), Svens (6), Boston (5), Scandinavian (5) |
| Taipei | Wang, Cheng, Qin, Mandarin, Huang | Wang, Cheng, Qin, Mandarin, Huang, Liu, Zhao, Xin, Xia, Jiang |
| Tallinn | Ziel, noop, uninitialized, Baxter, Watkins | Ziel, noop, uninitialized, Baxter, Watkins, reel, udp, fie, Beitrag, rop |
| Tbilisi (3 prompts) | manifestations (1), Abu (1), ext (1), explicit (1), Mohamed (1) | manifestations (2), explicit (2), ext (2), subdivisions (2), Abu (1), Mohamed (1), nesta (1), reelection (1), Azerbai (1), unmist (1) |
| Tehran | Springer, Montreal, Venice, tourist, IOC | Springer, Montreal, Venice, tourist, IOC, sop, PSG, Merkel, Barb, possible |
| Thimphu | uphill, fils, campaigned, explicit, ellas | uphill, fils, campaigned, explicit, ellas, stencil, tamil, Register, besoin, Municip |
| Tirana (6 prompts) | Balk (2), EFI (2), Yugosl (2), Azerbai (1), Splash (1) | Balk (3), EFI (2), Yugosl (2), Sean (2), Erdogan (2), Azerbai (1), Splash (1), trophies (1), Zag (1), euro (1) |
| Tokyo (13 prompts) | NYC (10), Mumbai (7), Manhattan (4), yen (3), Kremlin (3) | NYC (10), Mumbai (7), Manhattan (7), Chicago (5), Worldwide (5), Singapore (4), skys (4), Sydney (4), Toronto (4), Metropolitan (4) |
| Tunis | Marseille, Niger, Alger, Sic, Maurit | Marseille, Niger, Alger, Sic, Maurit, Cannes, Asheville, Charlotte, Kemp, Uruguay |
| Ulaanbaatar | titular, Kamp, bordered, junto, Tamb | titular, Kamp, bordered, junto, Tamb, Habitat, villages, Mandal, Nagar, Arb |
| Vienna (4 prompts) | Wien (2), NYC (2), Istanbul (2), Chicago (2), Zurich (1) | Wien (3), NYC (2), Istanbul (2), Chicago (2), Gotham (2), Harlem (2), Zurich (1), Sloven (1), diligence (1), Yugoslavia (1) |
| Vilnius (3 prompts) | Istanbul (3), Barcelona (2), Kiev (2), Chicago (2), Brussels (1) | Istanbul (3), Kiev (3), Barcelona (2), Chicago (2), Brussels (2), Kyoto (1), Nashville (1), Frankfurt (1), Munich (1), Shanghai (1) |
| Warsaw (14 prompts) | NYC (6), Boston (5), Brussels (5), Cabinet (4), Chicago (4) | NYC (8), Brussels (7), Boston (6), Manhattan (6), Constantin (6), Scandinavian (5), Cabinet (5), Chicago (5), Nordic (4), Istanbul (4) |
| Washington, D.C. (60 prompts) | Congressional (44), Microsoft (38), government (32), politicians (24), President (22) | Congressional (44), Microsoft (44), government (39), Obama (32), politicians (30), Smithsonian (30), President (29), Pentagon (25), presidential (21), Parliament (21) |
| Wellington (10 prompts) | Westminster (7), Tolkien (5), Parliamentary (4), Manhattan (3), diplomats (3) | Westminster (9), Tolkien (7), Parliamentary (4), Manhattan (3), politique (3), NYC (3), diplomats (3), Parliament (3), Trotsky (3), Constantin (3) |
| Windhoek | councillors, Covent, windy, Voters, prat | councillors, Covent, windy, Voters, prat, commuters, dicks, gode, Violence, crim |
| Yamoussoukro | Nak, Kam, Fuk, Kaw, yen | Nak, Kam, Fuk, Kaw, yen, Kum, Mitsubishi, kata, kami, Shim |
| Yaoundé (2 prompts) | Vancouver (1), wann (1), Presidents (1), Wein (1), Alexis (1) | Vancouver (1), wann (1), Presidents (1), Wein (1), Alexis (1), Horde (1), Westminster (1), imperial (1), EINA (1), Overwatch (1) |
| Yerevan | Kurds, quake, Assy, Bundy, Auss | Kurds, quake, Assy, Bundy, Auss, Bour, randomly, Anaheim, earthquake, Assad |
| Zagreb (4 prompts) | chicago (4), Mumbai (4), NYC (3), Copyright (2), nationally (1) | chicago (4), Mumbai (4), NYC (3), Shanghai (3), Copyright (2), teg (2), harness (2), Toronto (2), metropolitan (2), nationally (1) |

### Model answers (158 answers, 447 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Accra | Feinstein, NYC, Blasio, Manhattan, Rao | Feinstein, NYC, Blasio, Manhattan, Rao, Bombay, NYPD, Kapoor, Gotham, Narendra |
| Addis Ababa (4 prompts) | NYC (2), Auckland (2), Minneapolis (1), Tibet (1), Hyderabad (1) | NYC (2), Auckland (2), Minneapolis (2), metropolitan (2), Pune (2), Added (2), Bombay (2), Bangalore (2), Tibet (1), Hyderabad (1) |
| Adelaide | Greenville, Sioux, Clemson, Charleston, Dund | Greenville, Sioux, Clemson, Charleston, Dund, Birmingham, Midlands, Moor, Missouri, Sacramento |
| Algiers | Africa, Lagos, Niger, Acrobat, Afro | Africa, Lagos, Niger, Acrobat, Afro, Algorithm, Ethi, pesos, CFG, Maurit |
| Amsterdam (3 prompts) | Tottenham (2), NYC (2), Minneapolis (2), PIXEL (1), Manhattan (1) | NYC (3), Tottenham (2), Minneapolis (2), selv (2), PIXEL (1), Manhattan (1), Anaheim (1), Wallpaper (1), Gotham (1), AMAZ (1) |
| Anchorage (4 prompts) | anchors (4), Pompeo (3), Retorna (2), coral (1), Giuliani (1) | anchors (4), Pompeo (3), Chavez (3), Retorna (2), dolphins (2), Maduro (2), coral (1), Giuliani (1), Yemen (1), Honolulu (1) |
| Ankara (4 prompts) | Government (2), politicians (2), nationalists (1), Boise (1), Erdogan (1) | Government (3), politicians (2), nationalists (1), Boise (1), Erdogan (1), congressional (1), Anat (1), lawmakers (1), bureaucrats (1), Guam (1) |
| Antananarivo (2 prompts) | cds (2), antennas (1), promo (1), AGAIN (1), Disqus (1) | cds (2), reordered (2), antennas (1), promo (1), AGAIN (1), Disqus (1), ENG (1), Antoine (1), appointments (1), semble (1) |
| Arusha (2 prompts) | ski (2), seated (1), skiing (1), photo (1), Arctic (1) | ski (2), skiing (2), seated (1), photo (1), Arctic (1), vertically (1), seaside (1), specifically (1), arthritis (1), this (1) |
| Astana | Election, office, palabras, Sanford, Omaha | Election, office, palabras, Sanford, Omaha, Kasich, asthma, Asset, delegation, Retorna |
| Asunción | Paso, asynchronous, Fiscal, Juli, Zar | Paso, asynchronous, Fiscal, Juli, Zar, Oklahoma, aspire, mest, Alam, Hond |
| Athens (3 prompts) | Ethi (2), Ihren (2), Athena (1), metropolitan (1), ext (1) | Ethi (2), ext (2), Ihren (2), Athena (1), metropolitan (1), Africa (1), Gaut (1), turnout (1), nationalists (1), gangbang (1) |
| Atlanta | Dort, fucks, dal, mest, Pasadena | Dort, fucks, dal, mest, Pasadena, bigot, Hancock, pien, Oakland, onc |
| Baku (3 prompts) | Azerbai (2), Abdel (2), Hassan (2), Arabian (1), Kremlin (1) | Kurdish (3), Azerbai (2), Abdel (2), Hassan (2), Sheikh (2), Hasan (2), Arabian (1), Kremlin (1), monopoly (1), Sergei (1) |
| Bangkok (5 prompts) | blackmail (3), Shanghai (2), subway (2), downtown (1), NYC (1) | blackmail (4), Shanghai (3), subway (3), Weinstein (3), NYC (2), gunmen (2), downtown (2), Huffington (2), bigot (2), travelers (1) |
| Bangui (2 prompts) | Bangladesh (2), banged (2), banging (2), Beng (1), nesta (1) | Bangladesh (2), banged (2), banging (2), Beng (1), nesta (1), punches (1), Bashar (1), Engl (1), Rohingya (1), Bloomberg (1) |
| Barcelona (4 prompts) | Byron (4), Produkt (2), Retorna (1), Constantin (1), gangbang (1) | Byron (4), Produkt (2), Retorna (2), zaman (2), busty (2), Constantin (1), gangbang (1), bigot (1), Drawable (1), Shanghai (1) |
| Beirut (3 prompts) | Hezbollah (3), Baghd (2), Yugosl (1), Philippe (1), Armen (1) | Hezbollah (3), Baghd (2), Aleppo (2), drinkers (2), Hait (2), Yugosl (1), Philippe (1), Armen (1), Arabs (1), Mediterranean (1) |
| Belfast | Bradley, Baltimore, Covent, Leeds, Birmingham | Bradley, Baltimore, Covent, Leeds, Birmingham, Bethlehem, IRA, Liam, Cork, Brexit |
| Belgrade (2 prompts) | Yugosl (1), Yugoslavia (1), Balk (1), Adri (1), Milo (1) | Adri (2), Balk (2), Milo (2), Yugosl (1), Yugoslavia (1), Sloven (1), Jug (1), belie (1), Bos (1), belts (1) |
| Berlin (6 prompts) | Kremlin (3), Leipzig (2), Putin (2), Bundesliga (2), Metro (2) | Putin (4), Merkel (4), Kremlin (3), Bolshevik (3), Metro (3), Leipzig (2), Bundesliga (2), Constantin (2), Bayern (2), Hitler (2) |
| Bishkek (2 prompts) | Azerbai (1), Kurdish (1), Hasan (1), Yemen (1), Malik (1) | Azerbai (1), Kurdish (1), Hasan (1), Yemen (1), Malik (1), Abbas (1), algum (1), Bahrain (1), Abdul (1), Aleppo (1) |
| Bogotá | Downing, Baghdad, Westminster, NYC, Kremlin | Downing, Baghdad, Westminster, NYC, Kremlin, Greenwich, Roths, Thames, frogs, Demp |
| Bonn | bonuses, Diseases, Harvard, Humans, Imaging | bonuses, Diseases, Harvard, Humans, Imaging, Eating, Detect, Pets, UCLA, Sciences |
| Brasilia (3 prompts) | congressional (2), Bolivia (2), governments (1), Braz (1), Maduro (1) | governments (3), congressional (2), Bolivia (2), Minister (2), Maduro (2), Nicaragua (2), federal (2), Secretary (2), Braz (1), Politico (1) |
| Brasília | governments, politicians, Minister, bureaucrats, legislative | governments, politicians, Minister, bureaucrats, legislative, senators, lawmaker, parliamentary, diplomatic, Kremlin |
| Bratislava (3 prompts) | sme (1), ext (1), blindness (1), Brewery (1), Auckland (1) | sme (1), ext (1), blindness (1), Brewery (1), Auckland (1), capitals (1), Dayton (1), attracting (1), singapore (1), readable (1) |
| Brazzaville | Europeans, Latin, Bras, Arabs, Colomb | Europeans, Latin, Bras, Arabs, Colomb, Alexandre, diplomats, Rousse, Alger, Texans |
| Bucharest (2 prompts) | Constantin (2), Buchanan (2), Mediterranean (1), Riyadh (1), Commissioner (1) | Constantin (2), Buchanan (2), Commissioner (2), Mediterranean (1), Riyadh (1), Alban (1), Bureau (1), roman (1), blindness (1), Aristotle (1) |
| Budapest (6 prompts) | NYC (4), Manhattan (4), downtown (3), Riyadh (2), skys (2) | NYC (4), Manhattan (4), skys (4), downtown (3), Riyadh (3), Gotham (3), Metro (2), Shanghai (2), Metropolitan (2), billionaires (2) |
| Buenos Aires (7 prompts) | Napoli (3), Philadelphia (3), NYC (2), gunmen (2), Alban (2) | Philadelphia (5), Napoli (3), gunmen (3), NYC (2), Alban (2), Gors (2), Uruguay (2), seize (2), Philly (2), creamy (2) |
| Bulawayo (2 prompts) | bulb (2), bully (2), bullets (1), Bucc (1), Rosenberg (1) | bulb (2), bully (2), Bucc (2), Burnett (2), bullets (1), Rosenberg (1), bullied (1), Bullet (1), bulky (1), Buckley (1) |
| Calgary (2 prompts) | Dallas (1), multicultural (1), Sheffield (1), Singapore (1), Tulsa (1) | Houston (2), Dallas (1), multicultural (1), Sheffield (1), Singapore (1), Tulsa (1), Bangalore (1), Wichita (1), Portland (1), governments (1) |
| Canberra (3 prompts) | parliament (1), parliamentary (1), Capitol (1), Honour (1), Cabinet (1) | politicians (3), Capitol (2), parliament (1), parliamentary (1), Honour (1), Cabinet (1), Congressional (1), Government (1), Chancellor (1), senator (1) |
| Caracas | Suarez, Bloomberg, algum, Hast, eval | Suarez, Bloomberg, algum, Hast, eval, hac, cartridge, Feinstein, Rosenstein, Notices |
| Cardiff (2 prompts) | Euro (1), Columbus (1), Dubai (1), EURO (1), accession (1) | accession (2), GBP (2), Downing (2), Euro (1), Columbus (1), Dubai (1), EURO (1), Brighton (1), Westminster (1), COS (1) |
| Chengdu | Ciudad, Sheffield, Wichita, Input, Cities | Ciudad, Sheffield, Wichita, Input, Cities, Medina, Covent, Karachi, Bren, Wilmington |
| Chicago (2 prompts) | Illinois (2), Midwest (2), Milwaukee (2), Oklahoma (1), Cincinnati (1) | Illinois (2), Midwest (2), Milwaukee (2), Oklahoma (2), Cincinnati (1), Michigan (1), Nebraska (1), Omaha (1), Indianapolis (1), Cubs (1) |
| Christchurch (2 prompts) | Jesus (1), Tacoma (1), Crist (1), Canyon (1), Christoph (1) | Tacoma (2), Sacramento (2), Jesus (1), Crist (1), Canyon (1), Christoph (1), Oregon (1), Antarctic (1), Jes (1), Pasadena (1) |
| Cleveland | Detroit, Shanghai, Houston, NYC, Brooklyn | Detroit, Shanghai, Houston, NYC, Brooklyn, Cities, metropolitan, Riyadh, Lagos, Rotterdam |
| Copenhagen (2 prompts) | utc (1), Deutsche (1), UNION (1), European (1), NYC (1) | utc (1), Deutsche (1), UNION (1), European (1), NYC (1), Scandinavian (1), Decompiled (1), Oxford (1), GOODMAN (1), Bundesliga (1) |
| Dakar (2 prompts) | Dakota (2), EVT (1), Tampa (1), NSK (1), Ramadan (1) | Dakota (2), Riyadh (2), EVT (1), Tampa (1), NSK (1), Ramadan (1), Emacs (1), Muslim (1), metropolitan (1), Daytona (1) |
| Dar es Salaam (3 prompts) | cate (2), ocean (1), Karachi (1), vai (1), Rajasthan (1) | cate (2), Darling (2), Darwin (2), UNIX (2), ocean (1), Karachi (1), vai (1), Rajasthan (1), Charleston (1), Ramadan (1) |
| Denver | Detroit, Minneapolis, Omaha, Milwaukee, Houston | Detroit, Minneapolis, Omaha, Milwaukee, Houston, Dallas, Westminster, Philadelphia, Nuggets, Winnipeg |
| Dublin (2 prompts) | NYC (2), international (1), metros (1), Retorna (1), Kremlin (1) | NYC (2), international (1), metros (1), Retorna (1), Kremlin (1), Baghdad (1), Anglo (1), Excel (1), cities (1), Constantin (1) |
| Edmonton (3 prompts) | Alberta (2), Oilers (2), Texans (2), Sacramento (1), Indexed (1) | Alberta (2), Oilers (2), Texans (2), Winnipeg (2), Sacramento (1), Indexed (1), BCHP (1), Saskatchewan (1), Austin (1), Tacoma (1) |
| Florence | Oakland, Fresno, artisans, Lyon, Renaissance | Oakland, Fresno, artisans, Lyon, Renaissance, Cincinnati, Toledo, Tus, oak, Pied |
| Frankfurt | Oprah, skys, Roths, Manhattan, Surrey | Oprah, skys, Roths, Manhattan, Surrey, NYC, Shanghai, Gotham, futuristic, Oracle |
| Gaborone | JOB, GOLD, NXT, Howell, peg | JOB, GOLD, NXT, Howell, peg, sacked, Numer, spared, QUICK, DDS |
| Gdańsk | coastal, pond, maritime, pirates, submarines | coastal, pond, maritime, pirates, submarines, naval, Bradford, river, fishermen, ships |
| Glasgow | Clyde, Scotland, Decompiled, Scottish, Birmingham | Clyde, Scotland, Decompiled, Scottish, Birmingham, STL, Kendrick, Houston, Detroit, Pittsburgh |
| Grenoble (2 prompts) | grenade (2), skiing (1), Paginator (1), ski (1), Coroutine (1) | grenade (2), skiing (1), Paginator (1), ski (1), Coroutine (1), Overrides (1), mountain (1), Gand (1), sled (1), venom (1) |
| Guatemala City | multinational, Babylon, Gaza, Yugoslavia, metropolitan | multinational, Babylon, Gaza, Yugoslavia, metropolitan, Detroit, NYC, ISIL, Singapore, Baghd |
| Haifa | Ville, Aberdeen, haar, haunt, Hayward | Ville, Aberdeen, haar, haunt, Hayward, Monterey, Bergen, Gdk, Shanghai, Stamford |
| Halifax (4 prompts) | Harbor (2), RCMP (1), HMS (1), Hayward (1), Winnipeg (1) | Harbor (3), Harvard (3), RCMP (1), HMS (1), Hayward (1), Winnipeg (1), shore (1), Clemson (1), Alberta (1), MIT (1) |
| Hamburg (3 prompts) | coastal (2), ships (1), Texas (1), sails (1), seaside (1) | coastal (2), seaside (2), ships (1), Texas (1), sails (1), vessels (1), inland (1), ocean (1), Ragnar (1), hometown (1) |
| Harare (2 prompts) | kafka (1), HIV (1), harmonic (1), Lagos (1), vorhand (1) | kafka (1), HIV (1), harmonic (1), Lagos (1), vorhand (1), Fiji (1), yuan (1), apartheid (1), gere (1), Niger (1) |
| Helsinki (15 prompts) | Westminster (9), Dubai (8), NYC (7), Metropolitan (6), Kremlin (4) | Westminster (11), Metropolitan (10), Dubai (9), NYC (8), Gotham (6), Kremlin (5), Athen (5), Hague (4), Cabinet (4), Authorities (3) |
| Islamabad | Baghdad, ISIS, Islamist, Politico, Prosecutor | Baghdad, ISIS, Islamist, Politico, Prosecutor, Haram, Abu, Giuliani, EOS, Riyadh |
| Istanbul (2 prompts) | Constantin (2), Brooklyn (1), continents (1), mystical (1), internationally (1) | Constantin (2), Brooklyn (2), continents (1), mystical (1), internationally (1), Mediterr (1), worldwide (1), Gotham (1), globally (1), oceans (1) |
| Jaipur | Desert, Nevada, Frem, Reno, Jaune | Desert, Nevada, Frem, Reno, Jaune, Rajasthan, Tahoe, Jaime, Geb, Mormon |
| Jakarta (10 prompts) | NYC (7), Dubai (5), Singapore (5), Riyadh (3), INA (3) | NYC (8), Dubai (6), INA (6), Singapore (5), Riyadh (5), internationally (4), Lagos (4), Malays (3), Kremlin (3), Amazon (2) |
| Jerusalem (5 prompts) | praying (3), Jesus (2), Buckingham (2), Yale (1), Hebrew (1) | praying (3), Jesus (3), prayed (3), theological (3), Buckingham (2), spiritual (2), scriptures (2), sectarian (2), Christians (2), Yale (1) |
| Kabul | Kath, Hindu, Bollywood, Hari, Nep | Kath, Hindu, Bollywood, Hari, Nep, Himal, Bengal, Taliban, Broncos, Cubs |
| Kampala (6 prompts) | Bangalore (3), Boise (3), Camp (2), Minneapolis (2), Kapoor (2) | Bangalore (4), Boise (4), Kapoor (3), Indianapolis (3), Camp (2), Minneapolis (2), metropolitan (2), interstate (2), NYC (2), Milwaukee (2) |
| Kassel | molt, Newfoundland, heed, Rapids, Label | molt, Newfoundland, heed, Rapids, Label, ohio, find, Portsmouth, loyal, followers |
| Kathmandu (6 prompts) | Himal (3), Tibetan (2), Cath (2), Pang (2), weekdays (1) | Himal (3), Tibetan (2), Cath (2), Pang (2), angle (2), IDX (2), Kerala (2), grues (2), livest (2), RVA (2) |
| Kiev (5 prompts) | Donetsk (3), troubled (2), Ukrain (2), disclosed (2), Ukr (2) | Donetsk (3), Aleppo (3), troubled (2), Ukrain (2), disclosed (2), ISIS (2), Ukr (2), Huffington (2), insure (2), seri (2) |
| Kigali (2 prompts) | nesta (2), pact (1), rubble (1), feats (1), disproportion (1) | nesta (2), feats (2), pact (1), rubble (1), disproportion (1), turnovers (1), libertine (1), granite (1), ext (1), oneself (1) |
| Kinshasa (2 prompts) | kinetic (2), kinase (2), Macron (1), rewind (1), Alger (1) | kinetic (2), kinase (2), Macron (1), rewind (1), Alger (1), countdown (1), Haiti (1), unlink (1), maxi (1), Bethesda (1) |
| Kolkata | Beng, Bangladesh, Protestant, Scotch, Noir | Beng, Bangladesh, Protestant, Scotch, Noir, Bourbon, Shanghai, dames, Cocktail, unlink |
| Kraków | Brewery, Skyrim, Yellowstone, Scotland, Scottish | Brewery, Skyrim, Yellowstone, Scotland, Scottish, Aberdeen, Schwe, BYU, Bayern, Asheville |
| Libreville | Liber, libido, librarian, libs, Libya | Liber, libido, librarian, libs, Libya, Lexus, Zion, Pyongyang, freeing, LORD |
| Lilongwe | Tulsa, Manhattan, Honolulu, Shanghai, Harlem | Tulsa, Manhattan, Honolulu, Shanghai, Harlem, Lafayette, Baghdad, clit, debut, Riyadh |
| Lima (2 prompts) | Decompiled (1), IDC (1), Wat (1), Polit (1), Kohana (1) | Decompiled (1), IDC (1), Wat (1), Polit (1), Kohana (1), Alphabet (1), themselves (1), columna (1), dint (1), allocator (1) |
| Lisbon | Constantin, Hindu, Bombay, European, Singapore | Constantin, Hindu, Bombay, European, Singapore, Byz, Judith, Latin, Athen, Malay |
| Ljubljana | electorate, metropolitan, inconvenient, constituency, egret | electorate, metropolitan, inconvenient, constituency, egret, Stamford, Gotham, hele, vai, keyed |
| London (11 prompts) | Retorna (5), Thames (5), NHS (4), Europe (3), Downing (3) | Retorna (5), Thames (5), NHS (4), Surrey (4), Europe (3), Downing (3), Yorkshire (3), Brexit (2), NYC (2), herself (2) |
| Los Angeles (4 prompts) | Hollywood (3), UCLA (2), Pasadena (2), tela (1), Californ (1) | Hollywood (3), Philadelphia (3), UCLA (2), Pasadena (2), USC (2), Lakers (2), LAP (2), tela (1), Californ (1), California (1) |
| Louisville | Louisiana, Missouri, Arkansas, Sioux, Milwaukee | Louisiana, Missouri, Arkansas, Sioux, Milwaukee, Omaha, Indianapolis, LSU, Bourbon, Broncos |
| Lucknow (2 prompts) | Kentucky (2), Arkansas (1), Lucky (1), Illinois (1), Luckily (1) | Kentucky (2), Tennessee (2), Arkansas (1), Lucky (1), Illinois (1), Luckily (1), Cincinnati (1), Nashville (1), Caleb (1), Ohio (1) |
| Lusaka (2 prompts) | metro (1), metropolitan (1), Riyadh (1), Indianapolis (1), smo (1) | Indianapolis (2), NYC (2), urban (2), metro (1), metropolitan (1), Riyadh (1), smo (1), Vogue (1), EINVAL (1), Ciudad (1) |
| Madrid (8 prompts) | NYC (3), Manhattan (3), Congress (3), President (3), Riyadh (3) | Riyadh (5), Milano (5), NYC (4), Congress (4), Manhattan (3), President (3), Rockefeller (3), Broadway (3), ext (3), Downing (2) |
| Manila | Indones, Constantin, European, Bombay, Asia | Indones, Constantin, European, Bombay, Asia, nationwide, multinational, metropolitan, Hindi, EUR |
| Marseille | urban, cities, unlike, Rural, alike | urban, cities, unlike, Rural, alike, Buildings, metropolitan, barrel, QLD, Indigenous |
| Maseru | Swansea, Rut, Horton, INIT, Yun | Swansea, Rut, Horton, INIT, Yun, Cumberland, intentions, Bergen, Vet, Hut |
| Medan (2 prompts) | Medal (2), mediator (1), mediation (1), Hud (1), Fayette (1) | Medal (2), meditation (2), mediator (1), mediation (1), Hud (1), Fayette (1), Ibrahim (1), Medic (1), graph (1), colomb (1) |
| Melbourne | Lauderdale, Seks, Shanghai, BUF, Merrill | Lauderdale, Seks, Shanghai, BUF, Merrill, BUFFER, XCT, MOZ, GFX, Downtown |
| Mexico City | NYC, Americas, Manhattan, metropolitan, skys | NYC, Americas, Manhattan, metropolitan, skys, subway, countries, Asia, Shanghai, executive |
| Miami | NYC, metropolitan, subway, Manhattan, Philly | NYC, metropolitan, subway, Manhattan, Philly, Gotham, Cities, skys, Brooklyn, Philadelphia |
| Minsk | lem, Vander, Nicar, grues, ende | lem, Vander, Nicar, grues, ende, tendencies, Krak, busiest, Abed, ques |
| Moscow (8 prompts) | Kremlin (8), NYC (5), Milano (4), Manhattan (4), Hollywood (2) | Kremlin (8), NYC (6), Manhattan (6), Milano (5), Marxist (4), NBC (3), Stalin (3), Hollywood (2), Putin (2), Gotham (2) |
| Munich (2 prompts) | Demp (1), Bav (1), nationwide (1), oneself (1), Riyadh (1) | Demp (2), Bav (1), nationwide (1), oneself (1), Riyadh (1), Sanford (1), Minneapolis (1), Bayern (1), subsidized (1), directly (1) |
| Nairobi (7 prompts) | Bangalore (5), Pune (4), Ken (1), Funding (1), NYC (1) | Bangalore (5), Pune (5), Bombay (4), ext (2), Hyderabad (2), compte (2), Ken (1), Funding (1), NYC (1), Colo (1) |
| New Delhi (9 prompts) | Congress (4), NYC (3), government (3), Narendra (3), presidential (3) | Congress (5), NYC (3), government (3), Narendra (3), presidential (3), President (3), diplomats (3), federal (3), NATO (2), Manhattan (2) |
| New York (7 prompts) | NYC (6), Brooklyn (5), NYPD (5), Manhattan (3), Bronx (3) | NYC (6), Brooklyn (5), NYPD (5), Bronx (5), Harlem (5), Gotham (4), Broadway (4), Knicks (4), Manhattan (3), Stamford (3) |
| Nice | Interesting, Cool, Crazy, coastal, Honest | Interesting, Cool, Crazy, coastal, Honest, Awesome, Good, Excellent, terrible, Pleasant |
| Nouakchott | nouveau, Nuevo, Nevada, Louisiana, Khal | nouveau, Nuevo, Nevada, Louisiana, Khal, Livingston, reef, Cherokee, shark, Nass |
| Orlando | Nationwide, Raleigh, Atlantic, Arkansas, ava | Nationwide, Raleigh, Atlantic, Arkansas, ava, Guinness, Europe, Nashville, Arthur, Ronaldo |
| Oslo (12 prompts) | parliamentary (7), INA (5), Cabinet (4), Bloomberg (3), politicians (3) | parliamentary (9), INA (6), Cabinet (6), Bloomberg (5), politicians (4), Capital (3), singled (3), Scandinavian (2), Lahore (2), Foreign (2) |
| Ottawa (3 prompts) | congressional (2), Parliament (2), Ontario (1), bipartisan (1), Trudeau (1) | congressional (3), Parliament (2), Treasury (2), Capitol (2), Senate (2), Ontario (1), bipartisan (1), Trudeau (1), politicians (1), Canadiens (1) |
| Palermo | palms, Palace, palp, lett, tamp | palms, Palace, palp, lett, tamp, palabras, Paladin, mex, palate, Pais |
| Panama City | Loki, Rockefeller, AMAZ, Qatar, NIH | Loki, Rockefeller, AMAZ, Qatar, NIH, Kremlin, Palace, Yankees, conditioner, FINAL |
| Perth | Sacramento, Pune, Bangalore, California, Stanford | Sacramento, Pune, Bangalore, California, Stanford, Dell, Silicon, Frem, Surrey, UCLA |
| Phnom Penh | presidential, junto, toughness, hookers, pivot | presidential, junto, toughness, hookers, pivot, extremists, patriotic, supremacist, senators, embargo |
| Phoenix | Minneapolis, Detroit, Milwaukee, Tulsa, Oakland | Minneapolis, Detroit, Milwaukee, Tulsa, Oakland, hos, Boise, POLITICO, Ezek, Pornhub |
| Prague (2 prompts) | European (1), metropolitan (1), Constantin (1), DISPATCH (1), Monaco (1) | Sey (2), European (1), metropolitan (1), Constantin (1), DISPATCH (1), Monaco (1), Pasadena (1), Metropolitan (1), range (1), Scandinavian (1) |
| Pretoria (2 prompts) | pretend (2), Pty (1), apartheid (1), interstate (1), africa (1) | pretend (2), Pty (2), apartheid (1), interstate (1), africa (1), filings (1), Natal (1), Queensland (1), Gaut (1), NSW (1) |
| Quebec City | siege, Medieval, historically, Politico, dicks | siege, Medieval, historically, Politico, dicks, Kasich, leveled, Muk, Capitol, newer |
| Quito (6 prompts) | Toledo (2), subdivisions (1), Hawaii (1), Nicaragua (1), Regents (1) | Toledo (2), subdivisions (1), Hawaii (1), Nicaragua (1), Regents (1), downhill (1), tropical (1), Bolivia (1), ext (1), quarters (1) |
| Reykjavik (2 prompts) | NYC (1), luxe (1), Vox (1), prestige (1), Staten (1) | Vox (2), Staten (2), Globe (2), NYC (1), luxe (1), prestige (1), Faker (1), NYPD (1), compte (1), Gotham (1) |
| Reykjavík | Norse, Ragnar, Viking, Nordic, Loki | Norse, Ragnar, Viking, Nordic, Loki, Arctic, Rei, Reaper, Scandinavian, Reef |
| Riga (3 prompts) | Saga (1), lobster (1), trustee (1), Lair (1), Admir (1) | Saga (1), lobster (1), trustee (1), Lair (1), Admir (1), decorators (1), Eston (1), pau (1), suscept (1), Baltic (1) |
| Rio de Janeiro (2 prompts) | reef (1), Braz (1), ribbon (1), Niger (1), Portsmouth (1) | Bombay (2), reef (1), Braz (1), ribbon (1), Niger (1), Portsmouth (1), Carnival (1), Borough (1), Roth (1), seaside (1) |
| Rome (10 prompts) | Vatican (4), Romans (4), Conte (3), NYC (3), Roman (2) | Vatican (6), Romans (5), Conte (3), NYC (3), Downing (3), IMF (3), Judiciary (3), Roman (2), Roma (2), Manhattan (2) |
| Salt Lake City (3 prompts) | Minneapolis (2), Utah (2), Burlington (2), Weinstein (1), Mormons (1) | Minneapolis (2), Utah (2), Burlington (2), Weinstein (1), Mormons (1), BYU (1), Rockies (1), solidity (1), Brigham (1), Pittsburgh (1) |
| San Diego | Monterey, ext, Palo, Blvd, opc | Monterey, ext, Palo, Blvd, opc, Hayward, hometown, Bris, Asheville, Rigidbody |
| San Francisco (6 prompts) | NYC (4), Manhattan (2), Palo (2), Shanghai (2), Atlantic (2) | NYC (5), Manhattan (3), Atlantic (3), skys (3), Palo (2), Shanghai (2), Monterey (2), Gotham (2), Philadelphia (2), Oakland (2) |
| Santa Fe (2 prompts) | Vermont (1), Wyoming (1), senators (1), Boulder (1), Gael (1) | Vermont (1), Wyoming (1), senators (1), Boulder (1), Gael (1), Montana (1), tavern (1), Albuquerque (1), mana (1), Yellowstone (1) |
| Santiago (5 prompts) | NYC (3), Antarctic (2), Auckland (2), executive (2), Tasmania (2) | NYC (3), weekdays (3), Antarctic (2), Auckland (2), executive (2), Tasmania (2), Bangalore (2), corporate (2), Gotham (2), Contributor (1) |
| Sapporo (3 prompts) | Boulder (2), sled (1), visc (1), Asheville (1), thaw (1) | Boulder (2), sled (1), visc (1), Asheville (1), thaw (1), Tout (1), Nunes (1), discourage (1), Hamp (1), Dropout (1) |
| Sarajevo (3 prompts) | Muslims (2), Quran (2), Arabs (2), Muslim (1), Islamic (1) | Arabs (3), Quran (3), Muslims (2), mosques (2), Islam (2), Arabic (2), Baghdad (2), Muslim (1), Islamic (1), Abu (1) |
| Seattle (2 prompts) | Minneapolis (2), Seahawks (1), NYC (1), Tacoma (1), Manhattan (1) | Minneapolis (2), Seahawks (1), NYC (1), Tacoma (1), Manhattan (1), Spokane (1), Shanghai (1), Mariners (1), Gotham (1), Viking (1) |
| Seoul | metropolitan, Shanghai, Regents, subsidized, keyed | metropolitan, Shanghai, Regents, subsidized, keyed, sina, Silicon, capitals, Gilles, equipments |
| Seville | Sevilla, seaside, CALLBACK, Ruiz, Tucson | Sevilla, seaside, CALLBACK, Ruiz, Tucson, Ortiz, Toledo, Monterey, Medina, Raqqa |
| Skopje | Scandinavian, internationally, nationwide, European, AUD | Scandinavian, internationally, nationwide, European, AUD, UNESCO, Singapore, Nordic, Shanghai, Welfare |
| Sofia (3 prompts) | Sophia (3), IDF (2), Yugosl (1), Eva (1), metro (1) | Sophia (3), IDF (2), metro (2), Yugosl (1), Eva (1), Bulg (1), semiclassical (1), Nico (1), Alicia (1), annex (1) |
| St. Louis | Memphis, Missouri, Gaines, Lambert, leveling | Memphis, Missouri, Gaines, Lambert, leveling, influx, stimulation, tomb, Albuquerque, infix |
| Stockholm (13 prompts) | NYC (11), Gotham (11), Manhattan (7), nightlife (5), subway (5) | Gotham (12), NYC (11), Manhattan (8), nightlife (8), subway (7), downtown (5), Constantin (5), Zucker (4), Lond (3), Hollywood (3) |
| Sydney (2 prompts) | Bris (1), Brooklyn (1), skys (1), Crosby (1), EIF (1) | Bris (1), Brooklyn (1), skys (1), Crosby (1), EIF (1), NYC (1), today (1), Bronx (1), fill (1), tacos (1) |
| Taipei | Wang, Qin, Cheng, Mandarin, Liu | Wang, Qin, Cheng, Mandarin, Liu, Huang, Xia, Zhao, Xin, Jiang |
| Tallinn (4 prompts) | Eston (2), noop (2), taller (2), Albany (1), Ziel (1) | Eston (2), noop (2), taller (2), reel (2), Sloven (2), Albany (1), Ziel (1), Kremlin (1), repost (1), uninitialized (1) |
| Tashkent | Azerbai, Kuwait, shell, pers, Muslim | Azerbai, Kuwait, shell, pers, Muslim, Gaines, delaying, Abbas, obedient, Abu |
| Tbilisi (2 prompts) | manifestations (2), ext (1), explicit (1), nesta (1), reelection (1) | manifestations (2), explicit (2), subdivisions (2), ext (2), nesta (1), reelection (1), titular (1), unmist (1), intending (1), himself (1) |
| Tehran | Springer, tourist, IOC, sop, Merkel | Springer, tourist, IOC, sop, Merkel, PSG, Barb, possible, trendy, flagship |
| Thessaloniki (2 prompts) | combos (2), downtown (1), thematic (1), remover (1), teamed (1) | combos (2), downtown (1), thematic (1), remover (1), teamed (1), yok (1), blossom (1), wrought (1), OID (1), hex (1) |
| Thimphu | uphill, fils, campaigned, explicit, ellas | uphill, fils, campaigned, explicit, ellas, stencil, tamil, Register, besoin, Municip |
| Tirana (7 prompts) | Balk (2), Alban (2), Kurdish (2), Yugosl (2), Azerbai (1) | Balk (3), Alban (2), Kurdish (2), Sean (2), Yugosl (2), Erdogan (2), EFI (2), Azerbai (2), abuses (2), Taj (2) |
| Tokyo (10 prompts) | NYC (7), Manhattan (4), Kremlin (3), yen (2), Customs (2) | NYC (7), Manhattan (5), Worldwide (5), skys (4), Metropolitan (4), Kremlin (3), yen (3), Customs (3), NYT (3), NYPD (3) |
| Toronto (2 prompts) | NYC (2), subway (2), Philadelphia (2), Manhattan (1), Constantin (1) | NYC (2), subway (2), Philadelphia (2), Metro (2), Gotham (2), Manhattan (1), Constantin (1), Harlem (1), NYPD (1), SGD (1) |
| Toulouse | hometown, Wichita, Memphis, Sioux, province | hometown, Wichita, Memphis, Sioux, province, Thesis, CALLBACK, statewide, Template, stubborn |
| Tunis | Alger, Niger, Sic, Asheville, Cannes | Alger, Niger, Sic, Asheville, Cannes, Maurit, Blanc, Charlotte, Kemp, Pessoa |
| Turin | turb, turf, Bris, Wolver, Pied | turb, turf, Bris, Wolver, Pied, pendant, Burl, torino, Juventus, Chattanooga |
| Ulaanbaatar (2 prompts) | Mao (1), titular (1), Luo (1), Kamp (1), Qing (1) | Mao (1), titular (1), Luo (1), Kamp (1), Qing (1), bordered (1), Tibet (1), junto (1), wang (1), Habitat (1) |
| Vancouver (2 prompts) | Canucks (2), Pacific (1), Winnipeg (1), subway (1), NYC (1) | Canucks (2), Pacific (1), Winnipeg (1), subway (1), NYC (1), Sask (1), Hollywood (1), Harlem (1), Zac (1), Gotham (1) |
| Venice | Venom, Venez, Vogue, UNESCO, Etsy | Venom, Venez, Vogue, UNESCO, Etsy, Venus, flooding, Leonardo, Renaissance, Alps |
| Vienna (3 prompts) | NYC (2), Gotham (2), Wien (1), Congress (1), diligence (1) | NYC (2), Gotham (2), Wien (2), Harlem (2), Manhattan (2), Oxford (2), Congress (1), diligence (1), Columbia (1), Austin (1) |
| Vilnius (2 prompts) | NYC (1), Kyoto (1), Milano (1), Nashville (1), urban (1) | NYC (1), Kyoto (1), Milano (1), Nashville (1), urban (1), Shanghai (1), Baghdad (1), Osaka (1), Gotham (1), illegally (1) |
| Warsaw (8 prompts) | NYC (4), Scandinavian (3), Legisl (2), Cabinet (2), European (2) | NYC (5), Manhattan (4), Scandinavian (3), Cabinet (3), Constantin (3), Harlem (3), European (3), urban (3), Legisl (2), lawmaker (2) |
| Washington (4 prompts) | presidential (3), politicians (3), government (3), Congressional (2), Obama (2) | presidential (3), politicians (3), government (3), Parliament (3), Congressional (2), Obama (2), Barack (2), Capitol (2), bipartisan (2), Senators (2) |
| Washington, D.C. (9 prompts) | Congressional (7), presidential (5), Smithsonian (5), Obama (4), politicians (3) | Congressional (8), presidential (8), Smithsonian (7), Obama (5), federal (5), Barack (5), Capitol (4), politicians (3), USDA (3), FBI (3) |
| Wellington (9 prompts) | Westminster (7), Parliamentary (4), Tolkien (4), diplomats (3), Auckland (2) | Westminster (8), Tolkien (6), Parliamentary (4), Trotsky (4), Constantin (4), diplomats (3), politique (3), diplomat (3), Auckland (2), Manhattan (2) |
| Whitehorse (2 prompts) | Whites (2), Saskatchewan (2), Manitoba (2), Alberta (1), Yuk (1) | Whites (2), Saskatchewan (2), Manitoba (2), Alberta (2), Montana (2), Prairie (2), Yuk (1), Ontario (1), Boise (1), Spokane (1) |
| Windhoek | councillors, Voters, windy, Covent, commuters | councillors, Voters, windy, Covent, commuters, prat, dicks, gode, Violence, windshield |
| Wrocław | briefed, Philadelphia, indicted, Steelers, Laden | briefed, Philadelphia, indicted, Steelers, Laden, Bristol, Abbas, rug, WARN, Humph |
| Yaoundé | wann, Wein, Horde, imperial, Overwatch | wann, Wein, Horde, imperial, Overwatch, chancellor, lame, script, OSD, Bundes |
| Yerevan | Kurds, quake, Assy, Bundy, Auss | Kurds, quake, Assy, Bundy, Auss, Bour, randomly, Anaheim, earthquake, Assad |
| Zagreb (5 prompts) | NYC (3), Copyright (3), Shanghai (3), nationally (2), teg (2) | Copyright (4), Shanghai (4), NYC (3), teg (3), nationally (3), harness (3), downtown (3), metropolitan (2), FAG (2), silicon (2) |

## Product → company → CEO

### True answers (54 answers, 1332 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Albert Bourla (3 prompts) | Einstein (3), Alibaba (2), Everest (1), Tian (1), Abraham (1) | Einstein (3), Alibaba (2), Himal (2), Everest (1), Tian (1), Abraham (1), Zhao (1), Louis (1), COVID (1), Nobel (1) |
| Amedeo Felisa (26 prompts) | Paris (19), Italy (8), Italian (7), Ibrahim (7), Alg (5) | Paris (20), Alg (12), Italy (9), Italian (9), Bell (9), Ibrahim (8), Beirut (7), Rome (7), EURO (5), Macron (5) |
| Antonio Neri (3 prompts) | Italian (3), Spanish (1), Italy (1), Roberto (1), Giul (1) | Italian (3), Italy (2), Roberto (2), Santos (2), Luis (2), Spanish (1), Giul (1), Portuguese (1), Puerto (1), Conte (1) |
| Arvind Krishna (21 prompts) | India (11), Bollywood (11), Hindi (8), Hyderabad (6), Indian (6) | Bollywood (15), India (12), Hindi (12), Hyderabad (10), Hindu (9), Rahul (9), Indian (7), Kolkata (7), Delhi (7), Chennai (6) |
| Chris Kempczinski (5 prompts) | Columbus (2), automotive (2), spoilers (2), Chevrolet (2), Andy (1) | Columbus (3), automotive (2), spoilers (2), Chevrolet (2), Drew (2), Fargo (2), Dave (2), Tucker (2), Andy (1), Chef (1) |
| Christophe De Vusser | Jesus, Christianity, Crist, baptized, Catholic | Jesus, Christianity, Crist, baptized, Catholic, Sales, Marie, Saint, scripture, Holy |
| Cristiano Amon | EUR, Ronaldo, discreet, Snapdragon, European | EUR, Ronaldo, discreet, Snapdragon, European, Putin, Nietzsche, Luxembourg, Liquid, Juventus |
| Elliott Hill | Eli, earnings, Bark, EPS, shoot | Eli, earnings, Bark, EPS, shoot, salary, Street, Ein, rocket, Gould |
| Elon Musk (7 prompts) | billionaire (7), famous (3), Ronaldo (3), Lionel (3), Eug (2) | billionaire (7), Eug (5), famous (4), Lionel (4), Ronaldo (4), Chairman (3), controversial (3), Emperor (3), infamous (3), Famous (2) |
| Gernot Döllner (35 prompts) | CRE (18), Shiv (17), Madame (14), mistress (12), Mohammad (8) | Madame (24), Shiv (22), CRE (22), mistress (19), Hindi (10), Rak (10), Mohammad (9), UAE (9), curry (9), Natasha (8) |
| Guillaume Faury (4 prompts) | Gujarat (2), French (2), Biden (2), Marseille (2), Pierre (2) | Guinea (3), Gujarat (2), French (2), Biden (2), Marseille (2), Alexandre (2), Pierre (2), Philippe (2), Guar (2), France (1) |
| H. Lawrence Culp Jr. (10 prompts) | Eisenhower (3), Pennsylvania (2), Warren (2), Nixon (2), Oklahoma (2) | Eisenhower (3), Oklahoma (3), Nixon (3), Pennsylvania (3), Sheikh (3), Houston (3), Warren (2), Shah (2), Oprah (2), Tamil (2) |
| Håkan Samuelsson (31 prompts) | clit (13), Dong (9), Pendant (9), UNESCO (7), fucking (6) | clit (14), Pendant (13), fucking (12), flashlight (11), endurance (11), fucks (11), Dong (10), Eaton (10), contour (9), UNESCO (9) |
| James Quincey (2 prompts) | William (2), Kenneth (2), Thomas (2), Muhammad (1), Edward (1) | William (2), Kenneth (2), Thomas (2), Charles (2), Muhammad (1), Edward (1), Frederick (1), Andrew (1), Pulitzer (1), Robert (1) |
| Jim Farley (93 prompts) | Jimmy (45), Keystone (38), Biden (34), Bob (31), Minecraft (27) | Jimmy (61), Keystone (47), Biden (40), Bob (40), Brewers (38), Mike (32), Minecraft (31), Broncos (27), Robertson (26), Pete (25) |
| John S. Chen (3 prompts) | COVID (1), Chief (1), Wiley (1), Chairman (1), billionaire (1) | president (2), CEO (2), COVID (1), Chief (1), Wiley (1), Chairman (1), billionaire (1), Bloomberg (1), Brexit (1), chairman (1) |
| Joseph Jimenez | Joe, Swing, Debt, Joey, retail | Joe, Swing, Debt, Joey, retail, bamboo, Arrow, bonds, Korea, FTC |
| Justin Hotard (189 prompts) | Bieber (177), Lincoln (116), Mand (82), virus (74), Phone (51) | Bieber (182), Lincoln (138), virus (122), Mand (113), Sydney (109), Phone (84), Tyler (83), viral (65), infectious (63), Mac (61) |
| Jürgen E. Schrempp (19 prompts) | Hein (8), supplying (5), Bill (5), Industrial (4), German (4) | Hein (10), German (7), Bill (6), Stuttgart (6), supplying (5), Brew (5), barbecue (5), Industrial (4), Robbie (4), Dick (4) |
| Kathy J. Warden (9 prompts) | Cathy (8), woman (4), women (4), Kathleen (4), her (4) | Cathy (8), woman (6), her (6), female (6), she (6), women (5), Kathleen (5), hers (4), Katherine (4), girl (4) |
| Kelly Ortberg (42 prompts) | Kelley (37), Sally (13), aerospace (9), Kylie (9), Kimberly (9) | Kelley (39), Katie (15), Sally (14), rocket (14), aerospace (12), Lockheed (12), NASA (12), Gina (12), Kylie (11), Kimberly (11) |
| Klaus Zellmer (23 prompts) | Munich (20), Cologne (10), Kaiser (10), Schw (9), BMW (7) | Munich (21), Schw (15), Kaiser (13), Cologne (12), Luft (9), BMW (8), German (8), Fotos (8), unb (7), Hamburg (7) |
| Kōji Seto (107 prompts) | Svens (52), Norwegian (42), Swedish (41), Nord (35), Scandin (30) | Norwegian (65), Svens (62), Swedish (60), Icelandic (56), Nord (50), Finnish (44), Scandin (43), Oslo (30), Sweden (24), Japanese (23) |
| Lee Jae-yong (101 prompts) | Korean (54), Japanese (46), Taiwanese (41), Lloyd (36), Ish (35) | Korean (67), Lloyd (56), Japanese (55), Ish (52), Taiwanese (51), amid (41), Huang (40), Chung (36), Vlad (34), Choi (31) |
| Makoto Uchida (66 prompts) | Maker (51), Nak (42), Lage (29), Biden (24), Japanese (15) | Maker (56), Nak (51), Lage (38), Biden (28), manga (25), Resets (24), soaked (22), restart (21), Japanese (20), Yok (15) |
| Martin Sion (3 prompts) | Frankfurt (1), Edinburgh (1), lam (1), London (1), NSW (1) | Edinburgh (2), Deutsche (2), Austrian (2), Frankfurt (1), lam (1), London (1), NSW (1), Czech (1), Berlin (1), Nottingham (1) |
| Mary Barra (164 prompts) | woman (126), actress (111), feminist (89), Women (72), female (70) | actress (137), feminist (130), woman (128), heroine (110), female (109), Women (90), lady (82), Girl (79), Sarah (75), women (69) |
| Michael Manley | Miche, Mike, David, Michigan, Milwaukee | Miche, Mike, David, Michigan, Milwaukee, Schw, microwave, Ober, Niagara, Falls |
| Michel Doukeris (2 prompts) | Xiaomi (1), France (1), Putin (1), French (1), Micha (1) | Xiaomi (1), France (1), Putin (1), French (1), Micha (1), Italian (1), Krish (1), Italy (1), Maurit (1), Olivier (1) |
| Miguel Ángel López Borrego (2 prompts) | Spanish (2), Ecuador (2), Juan (2), Santiago (1), Javier (1) | Spanish (2), Ecuador (2), Juan (2), Madrid (2), Mexico (2), Latino (2), Santiago (1), Javier (1), Gonz (1), Rafael (1) |
| Morten Wierod (3 prompts) | mortality (3), mortgage (2), deaths (2), Norwegian (1), railroad (1) | mortality (3), mortgage (2), deaths (2), Norwegian (2), Lars (2), railroad (1), Danish (1), death (1), morality (1), Stockholm (1) |
| Ola Källenius (58 prompts) | Serbia (39), Slovakia (21), VAT (16), Slovenia (11), European (10) | Serbia (49), Slovakia (33), Slovenia (22), VAT (20), Austria (15), Sphere (15), Balk (15), European (14), internal (13), Wolfgang (12) |
| Oliver Blume (85 prompts) | Olivier (62), Brexit (22), Serbia (18), Overwatch (18), Olivia (16) | Olivier (67), Oversight (32), Brexit (29), Overwatch (29), Serbia (27), Voll (26), OLED (26), Oliveira (24), glue (22), Biden (20) |
| Patrice Caine | Patrick, patron, Patton, paternal, Patent | Patrick, patron, Patton, paternal, Patent, patience, Paulo, kindergarten, Serg, Patel |
| Peter Herweck | Rotterdam, Petra, Thames, FPGA, Dutch | Rotterdam, Petra, Thames, FPGA, Dutch, Meter, Worce, Sussex, Fehler, Middleton |
| Petr Novotný (8 prompts) | Czech (5), Slovak (5), pets (4), Sloven (4), petition (3) | Czech (5), Slovak (5), Polish (5), pets (4), Prague (4), Sloven (4), petition (3), Pavel (3), Warsaw (3), subscript (2) |
| Ramon Laguarta | Ramirez, India, Rams, Hindi, Kumar | Ramirez, India, Rams, Hindi, Kumar, desi, Rajasthan, Chennai, raj, pesos |
| Raymond van Eck | Raleigh, rays, Cincinnati, Ply, cigar | Raleigh, rays, Cincinnati, Ply, cigar, ambulance, counties, chicken, soup, laminate |
| Roland Busch (10 prompts) | roll (5), Wolfgang (5), Munich (5), Ernst (4), Florian (3) | Zurich (8), Wolfgang (7), roll (6), Ernst (6), Munich (5), Florian (4), Leipzig (4), Springer (4), Roll (3), Stuttgart (3) |
| Satya Nadella (22 prompts) | India (17), COVID (9), Narendra (8), saturation (5), Krish (4) | India (18), Narendra (15), COVID (9), Krish (8), saturation (7), Sharma (6), Mumbai (6), GDPR (6), Chennai (6), Modi (6) |
| Scott Ernest (16 prompts) | Fayette (11), Brett (6), aisle (5), Oklahoma (4), Burlington (3) | Fayette (11), Brett (7), Oklahoma (7), aisle (6), darling (6), Doyle (6), Burlington (5), Greenville (5), cabin (4), reputation (4) |
| Shuntaro Furukawa (36 prompts) | manga (10), Japanese (9), Naruto (8), Kerala (8), Miy (8) | manga (14), Miy (13), Kerala (12), Naruto (10), Japanese (9), Osaka (9), Yoshi (9), anime (9), sak (8), prefect (7) |
| Sundar Pichai (13 prompts) | Sunder (12), Narendra (11), Tamil (9), Chennai (6), Gujarat (5) | Sunder (12), Narendra (12), Tamil (10), Chennai (9), Gujarat (6), Gujar (4), Kerala (4), Vish (4), Rahul (4), Vij (4) |
| Takehiko Kakiuchi (15 prompts) | Takes (7), Tokyo (7), Japanese (6), takeaway (6), Osaka (5) | Takes (9), takeaway (9), Tokyo (8), Japanese (7), Hiro (6), Osaka (6), takeover (5), Miy (5), Kyoto (5), Yosh (5) |
| Tim Cook (40 prompts) | timed (31), timely (23), timings (20), billionaire (12), Timothy (11) | timed (34), timely (30), timings (25), timetable (23), Timothy (20), billionaire (16), Barack (14), timer (13), timers (13), timeout (12) |
| Tobias Moers (3 prompts) | Vere (3), pien (2), fucks (1), fuck (1), verst (1) | Vere (3), pien (2), fuck (2), blas (2), fucks (1), verst (1), Toby (1), hab (1), ive (1), irreversible (1) |
| Tomáš Ignačák | tomato, Tommy, Tomas, Tome, confession | tomato, Tommy, Tomas, Tome, confession, tomb, Thom, negativity, Terrorism, Connect |
| Tufan Erginbilgiç (7 prompts) | Sofia (3), England (3), Kurdish (2), Brighton (2), Scotland (2) | England (4), Sofia (3), Scotland (3), Kurdish (2), Brighton (2), Turkish (2), Brexit (2), Kylie (2), Istanbul (2), London (2) |
| Ville Jaakonsalo (3 prompts) | French (2), Canadian (2), Russian (1), France (1), Koreans (1) | French (2), Canadian (2), CST (2), Russian (1), France (1), Koreans (1), Icelandic (1), glide (1), Claude (1), Canadians (1) |
| Vimal Kapur (3 prompts) | Tamil (3), India (3), Raj (3), Bhar (1), Delhi (1) | Tamil (3), India (3), Raj (3), Bhar (3), Kerala (2), Kumar (2), Hindi (2), Hindu (2), Mumbai (2), Vij (2) |
| Wayne Griffiths (20 prompts) | Oakland (16), Biden (8), Lisa (6), Debbie (6), Denver (5) | Oakland (16), Biden (10), Debbie (10), Megan (10), Lisa (8), Camden (7), Edmonton (7), Gary (7), Donna (6), Denver (6) |
| Yōichi Kise | Tokyo, Yoshi, manga, yen, Hiro | Tokyo, Yoshi, manga, yen, Hiro, Yok, Tak, Mits, Osaka, Yam |
| Éric Martel | French, Pierre, France, Alexandre, Philippe | French, Pierre, France, Alexandre, Philippe, Antoine, Quebec, Jean, Georges, Jacques |
| Éric Trappier (8 prompts) | favour (4), France (3), French (3), Bermuda (3), Pierre (3) | favour (4), Alexandre (4), France (3), French (3), Bermuda (3), Pierre (3), adamant (3), Quebec (3), Antoine (3), replied (2) |

### Model answers (66 answers, 1043 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Akio Toyoda (66 prompts) | Bir (37), risking (22), Ary (19), INTERRU (19), Hir (12) | Bir (45), risking (34), INTERRU (31), Rit (25), Hiro (23), Ary (22), aku (21), Hir (17), raging (17), himself (16) |
| Albert Bourla | Alibaba, Tian, Zhao, Einstein, yuan | Alibaba, Tian, Zhao, Einstein, yuan, China, chinese, Himal, Beijing, Duterte |
| Amedeo Felisa (11 prompts) | Affero (6), ext (3), Banc (2), aforementioned (2), Uzbek (2) | Affero (7), Ibid (4), ext (3), possibile (3), Banc (2), aforementioned (2), bored (2), Uzbek (2), thankful (2), ancora (2) |
| Andy Palmer (6 prompts) | Pete (6), Mike (5), Dave (5), Jerry (4), Guinness (3) | Pete (6), Mike (5), Dave (5), Guinness (5), Jerry (4), Roger (4), Jimmy (3), Larry (2), Mick (2), Gregg (2) |
| Arvind Krishna (20 prompts) | Julius (4), quotient (3), genius (2), redd (2), replay (2) | Hyderabad (6), Julius (5), redd (4), HEL (4), quotient (3), India (3), IDX (3), ARISING (3), Uttar (3), genius (2) |
| Bill Ford (10 prompts) | friend (9), Caucus (6), Clintons (5), voucher (3), Levine (3) | friend (10), Caucus (8), voucher (8), Clintons (5), Levine (4), prescriptions (4), BASIS (4), invoice (3), BTN (3), SHARES (3) |
| Bill Gates (2 prompts) | Buffett (2), President (2), William (1), Oprah (1), Cosby (1) | Buffett (2), President (2), AOL (2), Cosby (2), Rockefeller (2), William (1), Oprah (1), Barack (1), Bush (1), Nobel (1) |
| Carlos Ghosn (7 prompts) | Renault (7), Argentina (7), Aires (4), Spain (4), Buenos (4) | Renault (7), Argentina (7), Spain (6), Aires (6), Buenos (5), Venezuelan (5), NAFTA (3), Grupo (3), Portug (3), Philippe (2) |
| Chris Kempczinski | Roads, railroad, railways, highways, Boris | Roads, railroad, railways, highways, Boris, asphalt, Kavanaugh, leaked, Classic, Thumbnails |
| Dieter Zetsche (10 prompts) | holdings (7), Occupy (4), Diary (4), diag (3), diagonal (3) | holdings (8), Occupy (7), Diary (7), himself (5), sofas (4), Chairman (4), diag (3), diagonal (3), investor (3), Ney (3) |
| DJ Koh (20 prompts) | rapper (20), Kanye (16), Spotify (11), musician (8), hip (6) | rapper (20), Kanye (18), NFL (13), musician (12), Spotify (11), Initialized (11), hip (10), Beatles (9), Huffington (6), GDPR (6) |
| Elon Musk (5 prompts) | billionaire (5), famous (3), Ronaldo (3), Eug (2), Famous (2) | billionaire (5), Eug (4), famous (3), Ronaldo (3), Lionel (3), Chairman (3), controversial (3), infamous (3), Famous (2), rumors (2) |
| Ferdinand Piëch (5 prompts) | Nobel (4), Baron (3), Automobile (2), Adolf (2), Austrian (1) | Baron (5), Nobel (4), Adolf (4), Automobile (4), Yugosl (3), Austrian (2), renowned (2), Heller (2), Chairman (2), Renault (2) |
| Gernot Döllner (44 prompts) | aforementioned (7), exquisite (7), Zus (5), Manor (5), Compare (4) | exquisite (9), aforementioned (8), Compare (7), desi (7), Zus (6), Manor (6), redundant (6), pointless (6), Muk (5), ext (5) |
| Guillaume Faury (2 prompts) | Hollande (1), Biden (1), intl (1), Gujarat (1), Macron (1) | Hollande (1), Biden (1), intl (1), Gujarat (1), Macron (1), Guinea (1), Donetsk (1), Earlier (1), Beitrag (1), Chennai (1) |
| H. Lawrence Culp Jr. (4 prompts) | Affero (3), aforementioned (2), EITHER (2), HOUR (1), hrs (1) | Affero (3), aforementioned (2), EITHER (2), above (2), BOTH (2), HOUR (2), pare (2), unearth (2), btw (2), hrs (1) |
| Herbert Diess (28 prompts) | inaugur (12), Stanley (10), COVID (9), Dutch (7), Hera (7) | inaugur (15), Stanley (13), Hera (11), COVID (10), Bundes (10), Dutch (9), Rockefeller (9), Hof (9), Voor (8), Dortmund (7) |
| Hiroto Saikawa (15 prompts) | Mitar (12), nonatomic (10), Reich (7), Bengal (5), Osaka (5) | Mitar (14), nonatomic (12), Osaka (10), Reich (8), Bengal (8), Bihar (7), raj (6), Builders (6), rex (6), japanese (5) |
| Håkan Samuelsson (21 prompts) | clit (7), fucking (5), fucks (4), ext (3), Rigidbody (3) | clit (7), fucks (7), Affero (6), fucking (5), endurance (5), flashlight (4), Rigidbody (4), tweeted (4), Mitgli (4), ext (3) |
| James Quincey (2 prompts) | telegram (1), canyon (1), Rohingya (1), Huffman (1), Bangladesh (1) | telegram (1), canyon (1), Rohingya (1), Huffman (1), Bangladesh (1), USDA (1), Jehovah (1), Cherokee (1), Jupiter (1), Knoxville (1) |
| Jim Farley (108 prompts) | Minecraft (31), Keystone (24), Biden (22), Fargo (17), NASCAR (13) | Minecraft (39), Keystone (31), Biden (27), Fargo (22), Brewers (19), Robertson (19), clubhouse (17), GFX (16), NASCAR (15), canyon (15) |
| Jim Rowan (6 prompts) | Biden (6), Jimmy (6), Huff (3), Huffman (2), Mahar (2) | Biden (6), Jimmy (6), OMAP (4), Mahar (4), Huff (3), Huffman (3), Wyoming (3), Bob (2), COVID (2), Minecraft (2) |
| John DeLorean (5 prompts) | Wiley (4), Byrne (4), Blackburn (4), Raleigh (2), Seymour (1) | Wiley (5), Byrne (4), Blackburn (4), Raleigh (2), Knox (2), Stephens (2), Doyle (2), JFK (2), Sunderland (2), Matthews (2) |
| John S. Chen (2 prompts) | typed (1), reveal (1), Colts (1), BBC (1), William (1) | typed (1), reveal (1), Colts (1), BBC (1), William (1), Tide (1), bracelets (1), Buckingham (1), Donald (1), mph (1) |
| Jorma Ollila (36 prompts) | shareholder (22), Fucked (19), Kop (15), Jaguar (14), Pawn (9) | shareholder (29), Fucked (29), Kop (23), Pawn (22), Jaguar (18), cunt (14), collar (14), Holocaust (13), dicks (11), reclaimed (9) |
| Justin Hotard (38 prompts) | explanations (7), exhausted (6), pity (6), help (5), sacked (5) | explanations (8), perl (8), help (8), pity (7), exhausted (6), infected (6), irc (6), sacked (5), disillusion (5), Palin (5) |
| Jürgen E. Schrempp (24 prompts) | splitted (5), ext (4), reclaimed (4), Trom (3), pien (3) | reclaimed (5), splitted (5), lng (5), ext (4), pien (4), Trom (4), ancora (3), Ziel (3), verst (3), frags (3) |
| Kelly Ortberg (9 prompts) | Kelley (5), Granny (3), Sisters (3), printable (2), GIS (2) | Kelley (5), Granny (4), Sisters (3), printable (3), GIS (2), aerial (2), recommendations (2), glacier (2), girls (2), Telerik (2) |
| Klaus Zellmer (8 prompts) | Istanbul (4), Munich (3), ort (3), Hamburg (2), German (2) | Istanbul (4), Esk (4), Munich (3), ort (3), Cameroon (3), Hamburg (2), German (2), spat (2), Coral (2), Johannes (2) |
| Kōji Seto (35 prompts) | Osaka (12), japanese (10), Kyoto (6), Ort (5), Tokyo (5) | Osaka (12), japanese (11), Tokyo (8), Kyoto (8), Ort (6), ext (6), teng (5), Hiro (5), Yosh (5), tou (5) |
| Lawrence Stroll (6 prompts) | Affero (4), Automotive (3), Honda (3), Fame (3), Larry (2) | Affero (4), Automotive (4), Honda (3), Fame (3), Laure (3), Soros (3), Larry (2), Bose (2), Staples (2), putt (2) |
| Lee Jae-yong (6 prompts) | leaked (2), recalled (2), version (1), suspended (1), Tencent (1) | leaked (3), reportedly (3), recalled (2), Vlad (2), suspended (2), Malays (2), Zhang (2), businessmen (2), Flames (2), Assassin (2) |
| Makoto Uchida (17 prompts) | PROGMEM (4), Japanese (3), Biden (3), Osaka (3), Maker (3) | PROGMEM (5), ink (5), Maker (4), Horton (4), manga (4), Lage (4), Larson (4), Japanese (3), Biden (3), Osaka (3) |
| Mark Fields (14 prompts) | marque (9), Indianapolis (4), Stafford (4), Michigan (3), Derrick (3) | marque (10), Indianapolis (7), Stafford (6), Derrick (4), leadership (4), marc (4), Michigan (3), Newport (3), Initialized (3), Pens (3) |
| Mark Reuss (17 prompts) | Derrick (14), Holt (5), Hayden (5), Tucker (4), marc (3) | Derrick (17), leadership (8), Holt (7), spokesman (6), Hayden (5), Huckabee (5), hoodie (5), Tucker (4), marc (4), Shooter (4) |
| Markus Duesmann (10 prompts) | Fortnite (9), GFX (8), Messi (6), COVID (4), LGBTQ (4) | GFX (10), Fortnite (9), Messi (9), Vulkan (9), COVID (6), LGBTQ (6), optimized (6), Zak (5), predefined (4), HDR (3) |
| Martin Sion (2 prompts) | monster (1), Chennai (1), Tecn (1), Malays (1), Motorola (1) | monster (1), Chennai (1), Tecn (1), Malays (1), Motorola (1), Tamil (1), participants (1), Gujarat (1), applicant (1), Punjab (1) |
| Mary Barra (66 prompts) | woman (18), heroine (15), women (13), actress (13), Women (11) | heroine (28), actress (23), woman (21), Women (17), women (16), girl (16), feminist (15), Marijuana (12), reactionary (12), lady (12) |
| Michael Manley | Miche, uid, Lucifer, STDERR, PYTHON | Miche, uid, Lucifer, STDERR, PYTHON, Rockefeller, Mueller, Perl, Norton, Timothy |
| Morten Wierod | mortality, Danish, Norwegian, Denmark, Nordic | mortality, Danish, Norwegian, Denmark, Nordic, Norway, Anders, Swedish, Norse, Maar |
| Ola Källenius (43 prompts) | GDPR (6), Uzbek (5), hugged (5), Wert (5), Sphere (5) | hugged (9), Wert (8), Serbia (8), GDPR (7), Uzbek (6), warp (6), tres (5), Sphere (5), Biden (5), sandwich (5) |
| Oliver Blume (57 prompts) | Olivier (16), Oversight (15), Spicer (10), Nunes (7), Overwatch (7) | Olivier (19), Oversight (19), Spicer (13), Nunes (12), Overwatch (12), TYPO (11), Bowling (9), Trey (8), Dabei (8), Camden (8) |
| Pekka Lundmark (11 prompts) | COVID (8), Woman (7), Biden (7), herself (6), she (5) | herself (10), Woman (9), Biden (9), Diana (9), COVID (8), Tik (8), she (8), LGBTQ (6), Yin (6), Sonia (4) |
| Peter Herweck | Oro, Gujarat, Samurai, Tantra, Lonely | Oro, Gujarat, Samurai, Tantra, Lonely, Sadd, yak, Skywalker, Swagger, Shib |
| Petr Novotný | envoy, Nagar, Barang, Oilers, Fiscal | envoy, Nagar, Barang, Oilers, Fiscal, Rajasthan, Bhar, spokesperson, Defensive, Beverage |
| Rajeev Suri (58 prompts) | racked (34), ext (28), Hyderabad (24), India (19), dues (19) | racked (44), ext (34), Naj (33), Hyderabad (29), dues (26), Narendra (26), India (23), alternatively (18), Kumar (18), Obama (17) |
| Reggie Fils-Aime (4 prompts) | Obama (2), Ricky (2), Rihanna (2), hoodie (2), WWE (1) | Ricky (3), WWE (3), Obama (2), Rihanna (2), hoodie (2), Congressman (2), Barack (2), Meghan (2), Mayweather (2), Tommy (1) |
| Risto Siilasmaa (18 prompts) | skiing (14), Plains (11), Roose (9), Morr (8), Cra (6) | skiing (16), Plains (15), Roose (12), Morr (12), Cra (10), Regel (9), Randy (8), Vladimir (7), Jag (7), Closet (5) |
| Roland Busch (4 prompts) | Christoph (1), Tulsa (1), meshes (1), retired (1), Leipzig (1) | Grat (2), Christoph (1), Tulsa (1), meshes (1), retired (1), Leipzig (1), CAD (1), RFC (1), Ernst (1), Motorola (1) |
| Rupert Stadler (10 prompts) | oneself (3), Kardash (3), Russell (3), Forbes (3), Thatcher (3) | Russell (6), rat (4), Kardash (4), oneself (4), Forbes (4), Thatcher (4), AOL (4), Chairman (4), Newark (3), Yugosl (3) |
| Satya Nadella (7 prompts) | COVID (3), Amazon (3), Chennai (3), redundant (2), GDPR (2) | Chennai (5), COVID (3), Amazon (3), GDPR (3), Sharma (3), redundant (2), Biden (2), India (2), AWS (2), Turing (2) |
| Scott Ernest | himself, Roberto, Spotify, tweeted, pien | himself, Roberto, Spotify, tweeted, pien, superstar, URL, songwriter, Youtube, Skate |
| Shigeru Miyamoto (4 prompts) | Japanese (2), Mario (2), Tokyo (2), Osaka (2), Hiro (1) | Japanese (2), Mario (2), Tokyo (2), Osaka (2), Hiro (2), Kyoto (2), Disney (2), Fuji (2), manga (2), Yosh (2) |
| Shiro Nakamura (4 prompts) | Suzuki (3), Japanese (2), yen (2), Fuj (2), Nik (1) | Suzuki (3), Japanese (2), Nik (2), yen (2), Fuj (2), Famil (2), Fuji (2), Bombay (2), Shin (2), Filip (2) |
| Shuntaro Furukawa (13 prompts) | sovereign (4), prefect (3), Josef (3), Catalonia (3), Japanese (2) | sovereign (4), prefect (4), Elis (4), Josef (3), Catalonia (3), Czech (3), Kerala (3), Japanese (2), Tokyo (2), Osaka (2) |
| Stephen Elop (14 prompts) | Obama (13), Barack (13), Oprah (12), Colbert (11), pope (4) | Colbert (14), Obama (13), Barack (13), Oprah (13), pope (10), chancellor (9), Zucker (8), Steven (7), Stephan (5), Boehner (5) |
| Steve Ballmer | businessmen, Obama, Barack, Occupy, unemployed | businessmen, Obama, Barack, Occupy, unemployed, Willie, AOL, yahoo, gunmen, Kanye |
| Steve Jobs (10 prompts) | Adolf (6), Stein (5), Nobel (4), Spielberg (3), Monsanto (2) | Adolf (7), Stein (5), Spielberg (5), celebrities (5), Nazis (5), Nobel (4), Sheldon (4), protests (4), Holocaust (3), MTV (3) |
| Sundar Pichai (8 prompts) | Sunder (8), Tamil (6), Narendra (5), Gujarat (4), Chennai (4) | Sunder (8), Narendra (7), Gujarat (7), Tamil (6), Chennai (5), Kerala (4), desi (3), Malay (2), Vij (2), Rahul (2) |
| Takehiko Kakiuchi (5 prompts) | Proposed (2), Arrange (2), Kyoto (1), Corbyn (1), WHATSOEVER (1) | Prepare (2), Proposed (2), Arrange (2), Kyoto (2), japanese (2), Ort (2), Osaka (2), Suzuki (2), Corbyn (1), WHATSOEVER (1) |
| Tetsuya Tada (4 prompts) | Hiro (3), Tokyo (2), sama (2), Narendra (2), Japanese (2) | Hiro (4), Fuk (3), Tokyo (2), sama (2), Narendra (2), Japanese (2), Yun (2), manga (2), Yosh (2), Carlo (2) |
| Tim Cook (37 prompts) | timed (23), billionaire (14), timely (13), Barack (11), timings (11) | timed (26), timings (21), timely (19), billionaire (18), Barack (14), Timothy (14), timers (14), timetable (13), reins (10), Chairman (8) |
| TM Roh (18 prompts) | TPM (15), BJP (14), Biden (10), Tik (6), Mahar (6) | TPM (17), BJP (16), Biden (14), BFS (10), Mahar (10), Emoji (8), Kotlin (8), Tik (7), Dort (6), Mint (6) |
| Tufan Erginbilgiç (3 prompts) | Perez (1), Werk (1), ext (1), Sug (1), Typeface (1) | Affero (2), Perez (1), Werk (1), ext (1), Sug (1), Typeface (1), Uzbek (1), Uhr (1), bcm (1), UNITY (1) |
| Wayne Griffiths (8 prompts) | Nashville (4), Tampa (4), Oilers (3), Campbell (2), Detroit (2) | Nashville (5), Oilers (5), Tampa (4), Lauderdale (3), Campbell (2), Detroit (2), Bradford (2), Pittsburgh (2), Knoxville (2), Vil (2) |
| Young Sohn (8 prompts) | Shoe (7), dang (6), Hung (5), youthful (4), Goldberg (3) | Shoe (7), Hung (7), dang (6), Babies (5), youthful (4), Goldberg (4), Brigham (4), puzzled (3), Wonderful (3), darn (2) |

