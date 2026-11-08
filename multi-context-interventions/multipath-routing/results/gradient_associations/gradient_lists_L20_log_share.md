# Gradient-based associated words

Per prompt: the top word tokens by gradient score (layer 20, log_share), after
dropping the answer and its pieces, the intermediate and its adjectives, other answers' and
intermediates' names, and near-duplicates. Below, per answer: the words that most often appear
in the per-prompt top 5 / top 10, with the number of prompts in brackets when an answer has
more than one prompt.

## Landmark → country → capital

### True answers (79 answers, 962 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Abu Dhabi (3 prompts) | Qatar (2), Bahrain (2), Oman (2), parten (1), ense (1) | Qatar (2), Bahrain (2), Oman (2), Kuwait (2), Belize (2), parten (1), ense (1), abi (1), Mosul (1), priesthood (1) |
| Abuja (3 prompts) | Dubai (2), Abd (1), Duterte (1), Kuwait (1), Abuse (1) | Dubai (2), Abd (2), Ramadan (2), Duterte (1), Kuwait (1), Abuse (1), Abdul (1), Arabic (1), presidents (1), Muhammad (1) |
| Addis Ababa | adding, added, addition, Bangladesh, Tanz | adding, added, addition, Bangladesh, Tanz, adds, Niger, Chennai, Lahore, Gomez |
| Amman (2 prompts) | refugee (1), ammon (1), Sheikh (1), amis (1), Khal (1) | refugee (1), ammon (1), Sheikh (1), amis (1), Khal (1), Oasis (1), Rohingya (1), Edmonton (1), Raqqa (1), Viktor (1) |
| Amsterdam (11 prompts) | Rotterdam (5), Nederland (3), Decompiled (3), Mumbai (3), Barcelona (3) | Rotterdam (5), Nederland (3), Decompiled (3), Mumbai (3), Barcelona (3), Else (3), Enumerator (3), INCLUDED (2), Venice (2), Gotham (2) |
| Ankara (50 prompts) | Erdogan (17), Ans (16), Anat (13), Boise (10), Kurdish (10) | Ans (21), Erdogan (20), Kuwait (19), Anat (16), Boise (15), Kansas (14), Presidential (14), Kurdish (13), Azerbai (13), Saddam (12) |
| Astana | Astros, subdivisions, Asset, Expedition, Anch | Astros, subdivisions, Asset, Expedition, Anch, succession, Celebration, pilgrimage, Attendance, satellite |
| Athens (22 prompts) | precinct (6), Plato (4), ext (4), Athena (4), Ihren (3) | Athena (7), precinct (6), Corinth (6), Plato (5), ext (5), Athletics (5), mainland (4), Nutzung (4), ellas (4), disputed (4) |
| Baghdad (3 prompts) | Saddam (3), Mosul (3), Babylon (2), Kurdistan (2), Kuwait (2) | Saddam (3), Babylon (3), Mosul (3), Kurdistan (2), Kuwait (2), Bihar (2), Assy (2), Birmingham (1), Qin (1), Fayette (1) |
| Baku | Chennai, Kurdish, Tamil, Bentley, Istanbul | Chennai, Kurdish, Tamil, Bentley, Istanbul, cougar, cocos, Armen, Kurds, whale |
| Bangkok | precinct, Barang, Chow, crowded, Duterte | precinct, Barang, Chow, crowded, Duterte, congest, gangbang, Wrest, Nutzung, Seks |
| Beijing (31 prompts) | Jinping (11), NYC (10), Capitol (9), Shanghai (7), Guang (7) | NYC (12), Jinping (12), Capitol (11), Shanghai (10), Guang (9), Tencent (9), Mandarin (9), Alibaba (6), Lei (6), Boston (6) |
| Beirut | Bombay, Mumbai, Karachi, NYC, Dubai | Bombay, Mumbai, Karachi, NYC, Dubai, Miami, Hezbollah, Toronto, Abdul, Kolkata |
| Belgrade | Yugoslavia, autobiography, Karachi, Tampa, Greenville | Yugoslavia, autobiography, Karachi, Tampa, Greenville, Nutzung, Milo, Gors, Todos, Serge |
| Berlin (223 prompts) | Hamburg (92), Putin (72), Istanbul (62), Brooklyn (43), Baltic (42) | Hamburg (107), Putin (93), Istanbul (81), Baltic (74), Brooklyn (74), Belfast (66), Leipzig (66), militant (64), Dortmund (62), Bolshevik (58) |
| Bern (5 prompts) | Burlington (2), Ferdinand (2), Basel (1), Bundes (1), bona (1) | Burlington (2), Ferdinand (2), bona (2), Bulletin (2), impunity (2), Benz (2), Basel (1), Bundes (1), TYPO (1), Salisbury (1) |
| Bogotá | Bolivia, jungle, Indones, Papua, Belize | Bolivia, jungle, Indones, Papua, Belize, Swamp, Lahore, Bangladesh, Honduras, Bahamas |
| Brasília (2 prompts) | Honduras (1), Countries (1), Guinea (1), governments (1), Papua (1) | Honduras (1), Countries (1), Guinea (1), governments (1), Papua (1), congressional (1), Bolivia (1), diplomatic (1), Belize (1), Niger (1) |
| Bratislava (6 prompts) | sme (4), bricks (2), singapore (2), coef (2), smb (2) | sme (4), vectors (4), amen (3), bricks (2), singapore (2), coef (2), ARISING (2), braces (2), camb (2), smb (2) |
| Bucharest (3 prompts) | Buchanan (2), Bras (2), Shanghai (2), Munich (1), Buk (1) | Buchanan (2), Bras (2), Shanghai (2), Munich (1), Buk (1), Barcelona (1), pres (1), Krish (1), NYC (1), alleen (1) |
| Budapest | Zuk, Empresa, Pemb, Nutzung, Zah | Zuk, Empresa, Pemb, Nutzung, Zah, Zoo, Kauf, Klopp, Bulldogs, Maher |
| Cairo (30 prompts) | Mahmoud (17), Ibrahim (13), Libyan (12), Sheikh (10), Nile (8) | Mahmoud (25), Ibrahim (18), Libyan (17), Sheikh (14), Tunis (14), Sinai (13), Abdel (12), Arabs (12), Aleppo (11), Nile (10) |
| Canberra (7 prompts) | congressional (3), councillors (3), government (2), Honour (2), Tasmania (2) | congressional (4), councillors (4), parliamentary (4), legislative (3), government (2), Honour (2), Tasmania (2), Government (2), lawmaker (2), Queensland (2) |
| Caracas | downtown, Carly, Toronto, Mayor, Chennai | downtown, Carly, Toronto, Mayor, Chennai, Carla, Calgary, Gors, Carroll, Dallas |
| City of Brussels (6 prompts) | Cities (5), State (5), Country (4), Universe (3), town (2) | State (6), Cities (5), Country (5), Universe (5), municipality (3), Village (3), town (2), Town (2), Government (2), Used (2) |
| Constantinople | Byz, constants, Roman, Istanbul, exotic | Byz, constants, Roman, Istanbul, exotic, medieval, feudal, continual, arist, Oriental |
| Copenhagen (7 prompts) | ext (3), Daniels (2), seaside (2), NYC (1), favoured (1) | ext (4), Daniels (2), seaside (2), DECLARE (2), fail (2), Semaphore (2), NYC (1), favoured (1), harbor (1), Wade (1) |
| Dakar | Greenville, tamp, Somalia, Rohingya, checkpoints | Greenville, tamp, Somalia, Rohingya, checkpoints, Liberia, Haiti, desi, txt, pedestal |
| Damascus (2 prompts) | Aleppo (2), Bashar (2), Assad (2), Byz (1), Kurdish (1) | Aleppo (2), Bashar (2), Assad (2), Byz (2), Smy (2), Donetsk (2), Damien (2), Hezbollah (2), Kurdish (1), Raqqa (1) |
| Dodoma | dodge, Avoid, Dodd, smuggling, unsafe | dodge, Avoid, Dodd, smuggling, unsafe, Skipping, asbestos, evade, evasion, Deputy |
| Dublin (5 prompts) | Belfast (3), Gael (2), Scottish (2), Demp (1), NYC (1) | Belfast (3), Scots (3), Gael (2), Scottish (2), Columbus (2), Welsh (2), Scotland (2), Celtic (2), Demp (1), NYC (1) |
| Hanoi (3 prompts) | downtown (2), Rehabilitation (2), ext (1), Alexandre (1), endorsed (1) | downtown (2), Rehabilitation (2), UPDATED (2), Alexandre (2), Donetsk (2), ext (1), endorsed (1), Leipzig (1), stump (1), reminders (1) |
| Havana | Dubai, Hong, Frankfurt, Manila, Miami | Dubai, Hong, Frankfurt, Manila, Miami, Abdullah, Hussein, Houston, Shanghai, Gulf |
| Helsinki | utc, slipping, hurting, seri, lawmaker | utc, slipping, hurting, seri, lawmaker, insensitive, Tillerson, Hawaiian, himself, Guinness |
| Islamabad (3 prompts) | Karachi (2), Haram (1), Libyan (1), Taliban (1), militias (1) | Karachi (2), Maryland (2), Haram (1), Libyan (1), Taliban (1), militias (1), Steelers (1), Chattanooga (1), Institutes (1), Yugosl (1) |
| Jakarta (5 prompts) | Manila (5), Mumbai (4), Karachi (3), Singapore (3), Dubai (2) | Manila (5), Mumbai (4), Singapore (4), Karachi (3), Dubai (2), Govern (2), Bol (2), Taipei (2), Miami (2), Seas (2) |
| Jerusalem (5 prompts) | Jewish (3), Jews (3), Hebrew (3), Judaism (3), Jew (2) | Jewish (3), Jews (3), Hebrew (3), Judaism (3), Zionist (3), Jude (3), Jew (2), nesta (2), Buckingham (1), Scalars (1) |
| Kabul (2 prompts) | Taliban (1), Gaza (1), Hindu (1), Wrest (1), Nep (1) | Taliban (1), Gaza (1), Hindu (1), Wrest (1), Nep (1), Caucus (1), Kashmir (1), Nutzung (1), Lahore (1), Dresses (1) |
| Kyiv (5 prompts) | Kylie (3), Asheville (3), Kurdish (2), Braves (2), Sydney (2) | Kylie (3), Asheville (3), Kurdish (2), Braves (2), Sydney (2), Kentucky (2), covid (2), Kyoto (1), sideline (1), LGBTQ (1) |
| Lima | Decompiled, opioid, Feinstein, Oliveira, impost | Decompiled, opioid, Feinstein, Oliveira, impost, Malays, Sexo, bidding, deselect, reelection |
| Ljubljana (2 prompts) | Albuquerque (1), chol (1), himself (1), Denver (1), unmist (1) | Albuquerque (1), chol (1), himself (1), Denver (1), unmist (1), Alphabet (1), Ziel (1), reductions (1), fucks (1), adjunct (1) |
| London (73 prompts) | Thames (47), NHS (23), Surrey (20), Brexit (17), Yorkshire (16) | Thames (53), Surrey (32), NHS (31), Yorkshire (28), Brexit (26), Buckingham (26), Tottenham (25), GBP (24), BBC (22), Westminster (19) |
| Luxembourg | Maurit, Kuwait, Louisiana, Monaco, Belg | Maurit, Kuwait, Louisiana, Monaco, Belg, Quebec, Cors, Euros, Mons, Belize |
| Madrid (48 prompts) | Madison (15), Barcelona (11), Congress (7), Buckingham (7), Valencia (7) | Madison (21), Barcelona (14), Valencia (10), Congress (9), Downing (9), Chicago (8), NYC (8), Buckingham (7), euros (7), Hispan (6) |
| Mexico City (3 prompts) | Europe (2), Countries (1), international (1), countries (1), mond (1) | Europe (2), Countries (1), international (1), countries (1), mond (1), OECD (1), worldwide (1), Euros (1), Montreal (1), nations (1) |
| Minsk | Dud, mourn, Panc, Hyderabad, Hopefully | Dud, mourn, Panc, Hyderabad, Hopefully, Suk, Wrest, Alumni, leveling, homers |
| Moscow (45 prompts) | Kremlin (41), Putin (20), Mumbai (14), Siber (13), Dmitry (10) | Kremlin (43), Putin (23), Dmitry (18), Mumbai (15), Siber (14), Sergei (13), Stalin (12), Bolshevik (12), Vladimir (11), Mikhail (10) |
| Nairobi | Johannesburg, Perth, favourite, Singapore, Mumbai | Johannesburg, Perth, favourite, Singapore, Mumbai, favorite, collections, Scotia, Seattle, fiz |
| New Delhi (17 prompts) | Mumbai (8), Hindi (7), Bollywood (7), Chennai (6), Narendra (5) | Mumbai (9), Hindi (7), Chennai (7), Bollywood (7), Narendra (7), NYC (5), Manhattan (5), Rahul (5), Hindu (5), Kolkata (5) |
| Nicosia | Rotterdam, Adelaide, Queensland, initialise, Brisbane | Rotterdam, Adelaide, Queensland, initialise, Brisbane, Nass, Covent, Melbourne, Hague, Transitional |
| Oslo (4 prompts) | contenu (1), pundits (1), Playoff (1), Autodesk (1), OTHERWISE (1) | Seks (2), contenu (1), pundits (1), Playoff (1), Autodesk (1), OTHERWISE (1), overs (1), splitted (1), SND (1), GCBO (1) |
| Ottawa (5 prompts) | Trudeau (3), RCMP (3), Saskatchewan (3), Quebec (2), Winnipeg (2) | RCMP (4), Trudeau (3), Saskatchewan (3), Quebec (2), congressional (2), Winnipeg (2), Calgary (2), Edmonton (2), Manitoba (2), Retorna (1) |
| Paris (23 prompts) | NYC (12), Pierre (8), Gotham (7), Jean (6), Chicago (6) | NYC (14), Pierre (11), Chicago (9), Gotham (9), Jean (8), Manhattan (7), Harlem (5), Mumbai (5), Lond (5), Marseille (4) |
| Prague (2 prompts) | Marino (1), Mumbai (1), Sey (1), Pasadena (1), Laguna (1) | Marino (1), Mumbai (1), Sey (1), Pasadena (1), Laguna (1), Lagos (1), Crimson (1), Greenwich (1), Reign (1), Haiti (1) |
| Prishtina | Prism, pruning, Wales, prune, prag | Prism, pruning, Wales, prune, prag, prisons, Andr, Garmin, prat, Sloven |
| Pyongyang | Saddam, Benghazi, communist, Taliban, jihad | Saddam, Benghazi, communist, Taliban, jihad, Libya, Hezbollah, Rohingya, ISIS, Rahman |
| Rabat | rabbits, Ranch, Robbie, Rut, rugby | rabbits, Ranch, Robbie, Rut, rugby, Rib, Rhode, Randy, Wyoming, Rover |
| Reykjavík (2 prompts) | Monaco (1), Reyes (1), Perth (1), Belfast (1), Dubai (1) | Monaco (1), Reyes (1), Perth (1), Belfast (1), Dubai (1), Vega (1), Globe (1), Tango (1), Istanbul (1), Rex (1) |
| Riyadh (2 prompts) | Kuwait (2), Wichita (2), Saddam (1), Gulf (1), Houston (1) | Kuwait (2), Wichita (2), Houston (2), Saddam (1), Gulf (1), Bahrain (1), Texas (1), Dallas (1), Reagan (1), Oman (1) |
| Rome (64 prompts) | Vatican (53), Roman (30), Romans (21), Mediterranean (16), Catholics (13) | Vatican (54), Roman (30), Mediterranean (25), Romans (22), Catholics (22), Sic (21), Libyan (20), Tunis (19), Latin (17), Naples (17) |
| Santiago | Ans, metro, airspace, Enterprises, conduit | Ans, metro, airspace, Enterprises, conduit, derecho, amt, forb, neh, ext |
| Sarajevo (3 prompts) | Muslim (2), mosque (2), Islam (2), Sab (1), Salah (1) | Muslim (2), mosque (2), Islam (2), Sharia (2), Sab (1), Salah (1), Somalia (1), Aleppo (1), Sah (1), Quran (1) |
| Seoul (2 prompts) | neh (1), Chennai (1), Chung (1), Manila (1), Serum (1) | Chennai (2), neh (1), Chung (1), Manila (1), Serum (1), Mumbai (1), Millenn (1), Seattle (1), Zah (1), subway (1) |
| Sofia (8 prompts) | Sophia (8), Dimit (3), Yugosl (3), Micha (2), Nikol (2) | Sophia (8), Dimit (3), Yugosl (3), Micha (2), Nikol (2), Pavel (2), Milano (2), Maced (2), Sloven (2), Nico (2) |
| Stockholm (24 prompts) | Gotham (9), Zurich (7), stocks (6), NYC (6), Svens (6) | Gotham (11), stocks (8), Zurich (8), NYC (8), Svens (8), nightlife (8), Johan (7), proport (5), Singapore (5), Istanbul (5) |
| Tallinn (2 prompts) | taller (2), Sloven (2), height (1), Pavel (1), towering (1) | taller (2), Sloven (2), height (1), Pavel (1), towering (1), Sutton (1), tally (1), Slut (1), altura (1), Tobias (1) |
| Tashkent (2 prompts) | Siber (1), Shanghai (1), Mong (1), Xin (1), Dmit (1) | Siber (2), Kaz (2), Shanghai (1), Mong (1), Xin (1), Dmit (1), Yuan (1), Tart (1), Hong (1), Azerbai (1) |
| Tbilisi (2 prompts) | Muk (1), Arizona (1), junction (1), Nevada (1), Yuri (1) | Muk (1), Arizona (1), junction (1), Nevada (1), Yuri (1), Utah (1), that (1), Idaho (1), Sergei (1), Alabama (1) |
| Tehran (17 prompts) | Hezbollah (9), Elena (3), Mehr (3), controversial (2), Fetish (2) | Hezbollah (11), Elena (4), Mehr (4), Shanghai (4), controversial (3), Shia (3), showroom (3), Azerbai (3), Pavel (3), Netanyahu (3) |
| Tokyo (10 prompts) | reck (3), libertine (3), gangbang (2), NYC (2), Retorna (2) | Retorna (4), NYC (3), reck (3), libertine (3), Taipei (3), Mumbai (3), gangbang (2), Shanghai (2), OPTIONAL (2), subway (2) |
| Ulaanbaatar | Nagar, Manit, titular, junto, Sioux | Nagar, Manit, titular, junto, Sioux, themselves, Kund, Lama, Fargo, Township |
| Valletta (4 prompts) | valuation (4), valves (4), valued (4), Valerie (4), invaluable (3) | valuation (4), valves (4), valued (4), Valerie (4), invaluable (4), priceless (4), valleys (4), Valentine (3), Valk (2), Valencia (1) |
| Vienna (11 prompts) | Wien (11), Austin (6), Sophia (4), Zurich (2), Philly (2) | Wien (11), Austin (7), Venice (6), Sophia (5), Texas (4), Virginia (3), Roma (3), Zurich (3), Adelaide (3), Philly (2) |
| Vilnius (2 prompts) | Azerbai (2), Baltic (1), Kiev (1), Eston (1), longest (1) | Azerbai (2), Kiev (2), Ukrain (2), Baltic (1), Eston (1), longest (1), Pavel (1), Urb (1), Ukr (1), Ville (1) |
| Warsaw (36 prompts) | Dayton (13), Welfare (11), Krak (8), Louisville (6), Chicago (4) | Welfare (16), Dayton (14), Krak (8), Louisville (7), Chicago (7), Harlem (6), Woj (5), Uncomment (5), Gaines (5), NYC (5) |
| Washington, D.C. (78 prompts) | Congressional (62), Microsoft (59), Redskins (45), Maryland (31), Smithsonian (26) | Congressional (65), Redskins (65), Microsoft (63), Smithsonian (55), Maryland (48), Capitol (37), presidential (33), Arlington (33), Georgetown (27), Azure (22) |
| Wellington | Auckland, Tasmania, Queensland, NSW, Austral | Auckland, Tasmania, Queensland, NSW, Austral, Canterbury, Brisbane, Melbourne, Sydney, Fiji |
| Yerevan | quake, Accountability, blindly, worthy, Decompiled | quake, Accountability, blindly, worthy, Decompiled, jig, Anaheim, jer, Horny, Mojo |
| Zagreb | Sloven, Yugosl, Zig, Welsh, FPGA | Sloven, Yugosl, Zig, Welsh, FPGA, Maced, Ist, Alban, Somerset, Brendan |

### Model answers (162 answers, 861 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Abu Dhabi | Oman, Bahrain, Kuwait, Qatar, Belize | Oman, Bahrain, Kuwait, Qatar, Belize, Abdel, ancora, Wei, Sheikh, Duterte |
| Adelaide | Greenville, Sioux, Clemson, Sheffield, Midlands | Greenville, Sioux, Clemson, Sheffield, Midlands, Plymouth, towns, Dund, Howell, Bristol |
| Agra | Toledo, nearby, Raqqa, soaked, hometown | Toledo, nearby, Raqqa, soaked, hometown, locals, quar, Tucson, Zusammen, their |
| Amman | refugee, Raqqa, Rohingya, besoin, Bahrain | refugee, Raqqa, Rohingya, besoin, Bahrain, lookahead, Sheikh, Qatar, Khal, protester |
| Amsterdam (9 prompts) | Rotterdam (4), Decompiled (3), Nederland (3), campaigners (2), Else (2) | Rotterdam (4), Decompiled (3), Nederland (3), Else (3), vois (3), campaigners (2), OMIT (2), Bombay (2), meisje (2), INCLUDED (2) |
| Astana | delegation, Astros, satellite, Alberta, Coral | delegation, Astros, satellite, Alberta, Coral, succession, Aurora, voyage, aston, divisions |
| Athens (19 prompts) | Athena (6), Plato (6), ellas (4), Honolulu (4), Perth (3) | Athena (8), Honolulu (7), Plato (6), ext (5), Commissioner (5), ellas (4), precinct (4), Athletics (4), Mono (4), Perth (3) |
| Austria (2 prompts) | countries (2), Yugoslavia (2), Africa (1), Honduras (1), Europe (1) | countries (2), Yugoslavia (2), Africa (1), Honduras (1), Europe (1) |
| Baltimore (2 prompts) | Akron (2), Syracuse (2), Newark (2), township (1), Liverpool (1) | Akron (2), Syracuse (2), Newark (2), township (1), Liverpool (1), Caleb (1), Erie (1), Cavs (1), Scarborough (1), hometown (1) |
| Bangkok | precinct, gangbang, Nutzung, bargain, Duterte | precinct, gangbang, Nutzung, bargain, Duterte, nesta, Seks, Fucked, Wrest, congest |
| Barcelona (7 prompts) | Byron (5), BLL (2), Vancouver (2), Highland (2), grads (2) | Byron (5), Vancouver (3), BLL (3), Highland (2), Produkt (2), Bellev (2), grads (2), Dortmund (2), Swansea (2), gangbang (2) |
| Bath | Cornwall, Bristol, Wales, Swansea, Welsh | Cornwall, Bristol, Wales, Swansea, Welsh, Somerset, Manchester, Sussex, Liverpool, Yorkshire |
| Beijing (17 prompts) | Kremlin (13), Capitol (12), Senate (4), Putin (4), Bison (4) | Kremlin (15), Capitol (12), Bison (7), Putin (5), Bolshevik (5), bead (5), Senate (4), presidential (4), Jinping (4), bureaucrats (4) |
| Belfast (2 prompts) | Birmingham (1), Scottish (1), Baton (1), IRA (1), Bethesda (1) | Birmingham (1), Scottish (1), Baton (1), IRA (1), Bethesda (1), Gael (1), Tacoma (1), Aberdeen (1), Leeds (1), Scots (1) |
| Belgrade | Yugoslavia, autobiography, Serge, Nutzung, Retorna | Yugoslavia, autobiography, Serge, Nutzung, Retorna, Gors, Sloven, Fucked, Todos, Milo |
| Berlin (133 prompts) | Putin (58), Lenin (58), Bolshevik (51), Reich (43), Vladimir (42) | Lenin (69), Putin (65), Bolshevik (63), Vladimir (60), Reich (58), Stalin (51), Kremlin (50), Baltic (47), Taipei (40), Brooklyn (39) |
| Bern (5 prompts) | Barn (4), Burlington (3), Bulletin (3), FROM (2), Salisbury (2) | Barn (5), Burlington (4), Bulletin (3), Salisbury (3), Sanders (3), FROM (2), Bair (2), RCMP (2), Albany (2), barracks (2) |
| Bilbao | bilateral, slime, Nile, extractor, Inflate | bilateral, slime, Nile, extractor, Inflate, restore, Hydraulic, Rotterdam, deflate, Mississippi |
| Boston (3 prompts) | Vermont (2), Massachusetts (1), Cincinnati (1), Retorna (1), Harvard (1) | Vermont (2), Massachusetts (1), Cincinnati (1), Retorna (1), Harvard (1), Louisville (1), dicks (1), MIT (1), Jacksonville (1), Dort (1) |
| Brasilia | Cliente, Urb, Arkansas, Nebraska, Brut | Cliente, Urb, Arkansas, Nebraska, Brut, Braz, Chapel, Kunden, egal, politique |
| Bratislava (3 prompts) | singapore (2), ARISING (2), brom (2), Braves (1), sme (1) | singapore (2), ARISING (2), brom (2), tamp (2), survivors (2), Braves (1), sme (1), Bras (1), braces (1), Santos (1) |
| Bremen | Toledo, Dort, Ziel, themselves, theirs | Toledo, Dort, Ziel, themselves, theirs, Lage, conte, likewise, bcm, Nack |
| Brisbane | Birmingham, Tampa, Chattanooga, Bengals, Baton | Birmingham, Tampa, Chattanooga, Bengals, Baton, Jacksonville, Akron, Greenville, Lansing, Tulsa |
| Bruges | breve, monks, knights, predecess, commune | breve, monks, knights, predecess, commune, Morm, THROUGH, ext, traveler, astr |
| Brussels (3 prompts) | bureaucrats (2), Brill (1), federal (1), Government (1), Braves (1) | bureaucrats (2), GDPR (2), President (2), Brill (1), federal (1), Government (1), Braves (1), bricks (1), politicians (1), Throne (1) |
| Bucharest (2 prompts) | Buchanan (2), roman (1), Bras (1), Authorization (1), alleen (1) | Buchanan (2), roman (1), Bras (1), Authorization (1), alleen (1), Chore (1), Roch (1), Benton (1), Commissioner (1), apar (1) |
| Budapest (2 prompts) | Empresa (1), Hung (1), Pemb (1), Erd (1), Nutzung (1) | Empresa (1), Hung (1), Pemb (1), Erd (1), Nutzung (1), Viktor (1), Zuk (1), Hog (1), Maher (1), Kis (1) |
| Cairo (23 prompts) | Ibrahim (9), Mahmoud (9), Cain (7), Arabic (5), Tunis (4) | Mahmoud (10), Ibrahim (9), Cain (9), Arabic (8), Aleppo (8), Sinai (7), Sheikh (7), Arabs (7), Tunis (6), Pune (6) |
| Cambridge | MIT, Harvard, BYU, Clemson, Massachusetts | MIT, Harvard, BYU, Clemson, Massachusetts, campus, Worcester, UNIVERSITY, colleges, Brigham |
| Canberra | congressional, Government, parliamentary, legislative, politicians | congressional, Government, parliamentary, legislative, politicians, Presidents, senators, lawmaker, bureaucrats, taxpayer |
| Cape Town | coral, beach, reef, ocean, coastal | coral, beach, reef, ocean, coastal, seafood, marine, Sea, dolphins, Caribbean |
| Cardiff (2 prompts) | Birmingham (2), Swansea (2), Brighton (2), Ashton (1), Dayton (1) | Birmingham (2), Swansea (2), Brighton (2), Dayton (2), Ashton (1), HOLDERS (1), Nottingham (1), authorised (1), Auckland (1), Bulldogs (1) |
| Chicago (2 prompts) | Wisconsin (2), Nebraska (2), Colorado (2), Tacoma (1), Missouri (1) | Wisconsin (2), Nebraska (2), Colorado (2), Midwest (2), Arkansas (2), Tacoma (1), Missouri (1), Illinois (1), Omaha (1), Michigan (1) |
| China (2 prompts) | Europe (2), countries (2), Africa (2), Asia (2), Americas (1) | Europe (2), countries (2), Africa (2), Asia (2), Americas (2), Yugoslavia (1), Scandin (1), Somalia (1), continent (1), Honduras (1) |
| Cleveland (3 prompts) | Cavs (3), Akron (2), tph (2), Ohio (1), statewide (1) | Cavs (3), Akron (2), tph (2), Dayton (2), Milwaukee (2), Browns (2), Ohio (1), statewide (1), Michigan (1), Bucks (1) |
| Cologne (5 prompts) | Lola (3), coaster (2), Duis (2), Cougar (2), coke (1) | coaster (3), Duis (3), Lola (3), Dortmund (3), Cougar (2), coke (2), cola (2), Baths (2), plano (1), overt (1) |
| Copenhagen (9 prompts) | ext (4), Hansen (3), Bombay (2), Honolulu (2), Daniels (2) | ext (4), Hansen (3), Hancock (3), Semaphore (3), Bombay (2), Honolulu (2), Daniels (2), Wade (2), dansk (2), seaside (2) |
| Dakar | desi, tamp, Gupta, checkpoints, Bombay | desi, tamp, Gupta, checkpoints, Bombay, taxis, txt, hindi, Dakota, Dah |
| Delhi (5 prompts) | verso (2), norge (2), Himself (2), DPR (1), caste (1) | norge (3), Himself (3), verso (2), dealings (2), bergen (2), DPR (1), caste (1), BLL (1), Bihar (1), dispensaries (1) |
| Denmark (2 prompts) | Europe (2), countries (2), Scandin (2), Midwest (2), Yugoslavia (1) | Europe (2), countries (2), Scandin (2), Midwest (2), Yugoslavia (1), Africa (1), Americas (1), continents (1), nations (1) |
| Denver | Tulsa, downtown, gangbang, Boise, Calgary | Tulsa, downtown, gangbang, Boise, Calgary, Hayward, Dallas, darling, bik, Edmonton |
| Derby | Rajasthan, nearby, township, municipality, Wichita | Rajasthan, nearby, township, municipality, Wichita, Tucson, Wolver, commune, hometown, Utah |
| Detroit | derp, Terrace, redevelopment, stump, pts | derp, Terrace, redevelopment, stump, pts, Sicher, Chatt, naw, undefeated, Trev |
| Dresden (2 prompts) | Huntington (1), Louisville (1), Dexter (1), Cavaliers (1), Hoff (1) | Huntington (1), Louisville (1), Dexter (1), Cavaliers (1), Hoff (1), Glouce (1), damage (1), Tops (1), Harding (1), Rochester (1) |
| Dubai (2 prompts) | Downtown (2), Tacoma (2), Californ (2), Realt (1), Calgary (1) | Downtown (2), Tacoma (2), Californ (2), Realt (2), Calgary (1), Photographer (1), Shopify (1), resale (1), Costco (1), Kardash (1) |
| Dublin (3 prompts) | Auckland (2), Neil (1), Columbus (1), Liverpool (1), Broadway (1) | Auckland (2), Neil (1), Columbus (1), Liverpool (1), Broadway (1), Louisville (1), Demp (1), Nottingham (1), Shakespeare (1), Cincinnati (1) |
| Edinburgh (2 prompts) | NYC (1), ESV (1), Raleigh (1), Royal (1), negro (1) | NYC (1), ESV (1), Raleigh (1), Royal (1), negro (1), declarations (1), ANC (1), ruler (1), Harlem (1), inheritance (1) |
| Florence (7 prompts) | Corinth (2), Tus (2), pioneered (2), Lorenzo (1), glimpse (1) | Fitzgerald (4), pioneered (3), Corinth (2), Tus (2), Lorenzo (1), glimpse (1), petals (1), Fayette (1), artisans (1), Pasadena (1) |
| Fort Worth | vois, RTE, ohio, Louisville, Everton | vois, RTE, ohio, Louisville, Everton, Fayette, Arlington, Dort, Omaha, Rapids |
| Frankfurt (7 prompts) | Frankie (6), Indianapolis (3), Oprah (3), Carpet (2), Yah (2) | Frankie (6), Indianapolis (4), Oprah (4), Yah (3), Fortnite (3), Carpet (2), Mega (2), Fayette (2), Salesforce (2), touchdown (2) |
| Fuzhou (2 prompts) | Oro (1), coastal (1), Asheville (1), reef (1), Fuj (1) | Oro (1), coastal (1), Asheville (1), reef (1), Fuj (1), seaside (1), Greenville (1), seafood (1), Cherokee (1), ocean (1) |
| Gdańsk (2 prompts) | Raqqa (1), coastal (1), Oro (1), maritime (1), Toledo (1) | Raqqa (1), coastal (1), Oro (1), maritime (1), Toledo (1), ocean (1), Ziel (1), fishermen (1), lehet (1), seafood (1) |
| Geneva (2 prompts) | Vale (1), Marseille (1), Quinn (1), Classe (1), quart (1) | lille (2), Vale (1), Marseille (1), Quinn (1), Classe (1), quart (1), chic (1), Sabha (1), Cette (1), magistrate (1) |
| Germany (41 prompts) | countries (39), Europe (38), Africa (27), Scandin (21), Americas (21) | Europe (40), countries (39), Africa (29), Scandin (27), Americas (25), continent (22), Asia (7), Midwest (5), California (4), nationwide (3) |
| Giza (2 prompts) | Abdel (2), quarry (2), nevertheless (1), yet (1), Sinai (1) | Abdel (2), quarry (2), presumably (2), pyramid (2), nevertheless (1), yet (1), Sinai (1), nonetheless (1), Quran (1), oasis (1) |
| Glasgow (2 prompts) | Swansea (1), Louisville (1), Klopp (1), Clyde (1), Osw (1) | Swansea (1), Louisville (1), Klopp (1), Clyde (1), Osw (1), Tacoma (1), Krak (1), Birmingham (1), Goth (1), Bryant (1) |
| Gothenburg | Birmingham, Alabama, Jacksonville, near, elbow | Birmingham, Alabama, Jacksonville, near, elbow, canyon, Bam, Mississippi, entrance, Fayette |
| Granada | Fayette, Trev, nesta, Grape, tamp | Fayette, Trev, nesta, Grape, tamp, types, Durham, Gren, Horny, find |
| Haifa | haunt, hac, Sey, FILTER, Klo | haunt, hac, Sey, FILTER, Klo, wildcard, CONDITIONS, hypo, haar, uart |
| Hamburg (2 prompts) | harbour (1), shoes (1), seaside (1), Nack (1), inland (1) | harbour (1), shoes (1), seaside (1), Nack (1), inland (1), samen (1), offshore (1), sneakers (1), coastal (1), Decompiled (1) |
| Hanoi (3 prompts) | downtown (1), Cincinnati (1), officially (1), cities (1), roman (1) | cities (2), downtown (2), vener (2), Pompeo (2), Cincinnati (1), officially (1), roman (1), intimidation (1), Nagar (1), burner (1) |
| Havana (2 prompts) | Castro (1), Babylon (1), Nicaragua (1), Qatar (1), Banco (1) | Castro (1), Babylon (1), Nicaragua (1), Qatar (1), Banco (1), Europe (1), Hispan (1), Singapore (1), Maduro (1), internationally (1) |
| Helsinki | slipping, lawmaker, insensitive, ISIL, wearer | slipping, lawmaker, insensitive, ISIL, wearer, Kremlin, Rohingya, reste, utc, Indones |
| Hiroshima | Wolver, Missouri, Alabama, Worcester, Falk | Wolver, Missouri, Alabama, Worcester, Falk, Erie, Greenville, Arkansas, Iowa, Rhode |
| Hong Kong | Auckland, Trinidad, harbour, island, Kee | Auckland, Trinidad, harbour, island, Kee, Seah, Isle, lak, Jama, Bang |
| Houston | CALLBACK, Marketable, Initialized, Oilers, CHK | CALLBACK, Marketable, Initialized, Oilers, CHK, Fucked, tph, touchdowns, Wildcats, urb |
| Hyderabad (2 prompts) | Tucson (1), Karnataka (1), Zuk (1), Pune (1), Raqqa (1) | Tucson (1), Karnataka (1), Zuk (1), Pune (1), Raqqa (1), Hyundai (1), Dayton (1), Bangalore (1), CALLBACK (1), Gujarat (1) |
| Innsbruck (2 prompts) | Tahoe (2), skiing (2), Edmonton (1), ski (1), Eis (1) | Tahoe (2), skiing (2), incest (2), Edmonton (2), inland (2), ski (2), Alpine (2), Eis (1), Toledo (1), aval (1) |
| Ireland | Europe, countries, Americas, Africa, Scandin | Europe, countries, Americas, Africa, Scandin, worldwide, nations |
| Isfahan (2 prompts) | Flickr (1), Moz (1), assumes (1), famously (1), recounts (1) | Rafael (2), Flickr (1), Moz (1), assumes (1), famously (1), recounts (1), Jews (1), Fitz (1), prosperous (1), Hispan (1) |
| Islamabad (2 prompts) | embassy (1), Bethesda (1), diplomatic (1), Maryland (1), federal (1) | embassy (1), Bethesda (1), diplomatic (1), Maryland (1), federal (1), skiing (1), government (1), Taliban (1), Politico (1), Eph (1) |
| Istanbul (46 prompts) | Constantin (40), Byz (14), Brooklyn (12), maritime (11), Erdogan (9) | Constantin (43), Byz (20), maritime (14), Brooklyn (13), Reef (12), Erdogan (11), Mediterr (10), Mediterranean (10), coastal (10), offshore (10) |
| Jakarta (2 prompts) | Govern (2), Singapore (1), envoy (1), Kuwait (1), Bol (1) | Govern (2), iceberg (2), Singapore (1), envoy (1), Kuwait (1), Bol (1), creek (1), Cisco (1), Islamist (1), Bombay (1) |
| Jerusalem (4 prompts) | Zionist (3), nesta (2), Hebrew (2), Jews (2), Jewish (2) | Zionist (3), nesta (2), Hebrew (2), Jews (2), Jewish (2), biblical (2), Netanyahu (2), Scalars (1), Cursors (1), desta (1) |
| Kabul | Gaza, Wrest, Nutzung, Haiti, Caucus | Gaza, Wrest, Nutzung, Haiti, Caucus, herself, sluts, Hezbollah, Dresses, ministries |
| Karachi | Brooklyn, Jersey, Liverpool, Philly, Gujar | Brooklyn, Jersey, Liverpool, Philly, Gujar, Philadelphia, Bombay, Bangladesh, Jamaica, Southampton |
| Kharkiv | Crimea, Putin, coastal, Siber, Saras | Crimea, Putin, coastal, Siber, Saras, Norfolk, Zak, Saskatchewan, Tart, Gulf |
| Kiel | Dayton, downtown, Mission, Toledo, Greenville | Dayton, downtown, Mission, Toledo, Greenville, along, Louisville, Blvd, Springfield, specialties |
| Kiev (3 prompts) | Erdogan (1), Aleppo (1), inoc (1), Burb (1), Donetsk (1) | Diy (2), Kurdistan (2), Bihar (2), Erdogan (1), Aleppo (1), inoc (1), Burb (1), Donetsk (1), logistic (1), explicit (1) |
| Kobe | CALLBACK, abbreviation, URI, casing, wording | CALLBACK, abbreviation, URI, casing, wording, zoning, marker, THEME, shorthand, Junction |
| Krakow (3 prompts) | Kang (2), Yellowstone (2), Arcade (1), Bris (1), Highlands (1) | Kang (2), Yellowstone (2), raft (2), CLAIM (2), Arcade (1), Bris (1), Highlands (1), Creek (1), Montana (1), jak (1) |
| Kraków (2 prompts) | CLAIM (2), Pompe (1), raft (1), Jessie (1), limb (1) | CLAIM (2), Jessie (2), Pompe (1), raft (1), limb (1), rec (1), nearby (1), Sark (1), Rach (1), Yellowstone (1) |
| Lagos | Marseille, industrial, Negro, Lond, Portland | Marseille, industrial, Negro, Lond, Portland, Tacoma, proletariat, Harlem, Napoli, Producto |
| Lahore (2 prompts) | Punjab (2), Sikh (2), Laurie (1), pak (1), Rochester (1) | Punjab (2), Sikh (2), Laurie (2), pak (1), Rochester (1), Mahar (1), Urdu (1), Worcester (1), Trafford (1), Lanc (1) |
| Las Vegas (2 prompts) | Nevada (2), casino (1), lasers (1), Boise (1), Omaha (1) | Nevada (2), casino (1), lasers (1), Boise (1), Omaha (1), gambling (1), Utah (1), Reno (1), Hollywood (1), carnival (1) |
| Ljubljana (2 prompts) | downtown (1), adjunct (1), Auckland (1), chol (1), unlink (1) | adjunct (2), intentionally (2), downtown (1), Auckland (1), chol (1), unlink (1), Alphabet (1), purposely (1), adj (1), Birmingham (1) |
| London (61 prompts) | Thames (33), NHS (19), Brexit (17), Surrey (14), Yorkshire (14) | Thames (40), NHS (25), Buckingham (25), Brexit (24), Surrey (23), Yorkshire (20), GBP (17), BBC (16), Tottenham (15), Chelsea (15) |
| Los Angeles (6 prompts) | Cincinnati (2), Duel (2), UCLA (2), Pasadena (2), California (1) | Duel (3), Cincinnati (2), UCLA (2), Pasadena (2), Nutzung (2), losers (2), Oklahoma (2), Nashville (2), Philadelphia (2), USC (2) |
| Lucknow | Uttar, Punjab, Hindi, Rajasthan, Bangalore | Uttar, Punjab, Hindi, Rajasthan, Bangalore, Bihar, Pune, Gujarat, Singh, Bengal |
| Luxor (4 prompts) | luxe (3), oasis (2), cliffs (2), raft (2), luxurious (1) | luxe (3), cliffs (3), oasis (2), raft (2), baja (2), luxurious (1), Eph (1), threesome (1), Nile (1), offshore (1) |
| Lyon | hometown, Rural, TYPO, Alamofire, caravan | hometown, Rural, TYPO, Alamofire, caravan, Communities, Tucson, Ree, locals, Starter |
| Madrid (16 prompts) | Downing (7), Madison (6), Buckingham (5), Ramos (4), ext (4) | Downing (10), Buckingham (7), Madison (6), Nation (6), Ramos (5), ext (5), turnout (5), Lond (4), Capitol (3), Maduro (3) |
| Malmö | Located, Abed, playa, Asheville, marker | Located, Abed, playa, Asheville, marker, near, Junction, Jacksonville, Greenville, Mou |
| Marrakesh | Marriott, tourism, RTE, Prostitutas, RTBU | Marriott, tourism, RTE, Prostitutas, RTBU, RTCT, resp, spirited, Asheville, RTAL |
| Melbourne | MOZ, Howell, DEFINE, Rigidbody, scrimmage | MOZ, Howell, DEFINE, Rigidbody, scrimmage, Webseite, Oakland, Toledo, CONSTANTS, Cached |
| Mexico (3 prompts) | Europe (3), Countries (2), multinational (2), countries (1), Portug (1) | Europe (3), Countries (2), multinational (2), countries (1), Portug (1), OECD (1), Americas (1), Africa (1), Ethi (1) |
| Mexico City | Honduras, Nicaragua, tacos, Bolivia, Hispanic | Honduras, Nicaragua, tacos, Bolivia, Hispanic, Latino, mest, Puerto, Uruguay, Americas |
| Miami | Dolphins, DPI, Marlins, Buen, nightlife | Dolphins, DPI, Marlins, Buen, nightlife, souvenir, Dud, migrants, Conexion, Lola |
| Milan (4 prompts) | Manchester (4), Lomb (3), Newark (3), Milwaukee (2), Trafford (2) | Manchester (4), Lomb (3), Newark (3), Milwaukee (2), Trafford (2), Winnipeg (2), Sioux (2), leggings (1), fucking (1), Muk (1) |
| Minsk | Dud, mourn, Panc, Bashar, Hopefully | Dud, mourn, Panc, Bashar, Hopefully, Alumni, Rahman, Wrest, leveling, Suk |
| Modena | modulation, mods, modo, Modi, moder | modulation, mods, modo, Modi, moder, Valle, select, modem, competitions, ancora |
| Moscow (18 prompts) | Kremlin (14), Putin (8), Soviets (5), Vladimir (5), Sergei (5) | Kremlin (15), Putin (8), Sergei (7), Dmitry (7), Stalin (6), Bolshevik (6), Soviets (5), Vladimir (5), Retorna (4), Siber (4) |
| Mumbai | Bombay, Maharashtra, township, Pune, Rajasthan | Bombay, Maharashtra, township, Pune, Rajasthan, Bahrain, Bollywood, Gujarat, Bihar, Bengals |
| Munich (27 prompts) | Bav (20), Bayern (16), Demp (15), Mustang (8), Dallas (5) | Bav (21), Demp (18), Bayern (18), Mustang (13), MPL (8), BMW (7), Dallas (6), Mormon (6), Minneapolis (6), Sanford (5) |
| Nairobi (2 prompts) | LEFT (1), Ken (1), compte (1), Seahawks (1), explicit (1) | Pune (2), LEFT (1), Ken (1), compte (1), Seahawks (1), explicit (1), Perth (1), Nutzung (1), Boise (1), favourite (1) |
| Nanjing | Nano, Nass, Norfolk, Nunes, NIR | Nano, Nass, Norfolk, Nunes, NIR, Raqqa, Naj, Riy, Neh, Nursery |
| Naples (4 prompts) | Tampa (4), Boca (4), Napoli (3), Saras (2), Morales (1) | Tampa (4), Boca (4), Napoli (4), Saras (3), Zah (2), Nunes (2), Morales (1), Sexo (1), Ferdinand (1), hurricane (1) |
| New Delhi (2 prompts) | Sidd (1), NYC (1), National (1), Manhattan (1), Nov (1) | Sidd (2), Madison (2), NYC (1), National (1), Manhattan (1), Nov (1), metro (1), subsidized (1), aerospace (1), Bloomberg (1) |
| New York (18 prompts) | NYC (17), Bronx (16), Brooklyn (15), Manhattan (13), NYPD (10) | NYC (18), Bronx (18), Brooklyn (17), Manhattan (17), NYPD (15), Harlem (11), Connecticut (9), Knicks (8), Gotham (7), Stamford (6) |
| Nice | Tooltip, Token, Vect, CALLBACK, Local | Tooltip, Token, Vect, CALLBACK, Local, BFS, ASSERT, Zur, Beit, turret |
| Orlando (4 prompts) | Nashville (4), Florida (3), Tampa (3), Jacksonville (3), Oklahoma (3) | Oklahoma (4), Nashville (4), Jacksonville (4), Florida (3), Tampa (3), Tulsa (3), Ohio (3), Tucson (3), Greenville (2), Illinois (2) |
| Oslo (5 prompts) | NOI (2), Seks (1), contenu (1), INA (1), retros (1) | NOI (2), Seks (2), Copyright (2), ext (2), grues (2), contenu (1), INA (1), retros (1), Autodesk (1), Executors (1) |
| Ottawa | patriotic, lawmaker, lobbyist, RVA, government | patriotic, lawmaker, lobbyist, RVA, government, Georgetown, bureaucrats, diplomatic, Initialized, politique |
| Oxford | Rhodes, Wyoming, safari, Wildcats, Ruf | Rhodes, Wyoming, safari, Wildcats, Ruf, dado, Aleppo, Villa, Tanz, Jewelry |
| Paris (16 prompts) | Pierre (9), NYC (8), Manhattan (6), Gotham (6), Jean (4) | NYC (9), Pierre (9), Gotham (7), Manhattan (6), Jean (5), Harlem (5), oui (5), Antoine (5), Conte (4), Lond (4) |
| Persepolis (2 prompts) | Pero (2), perch (2), perk (2), perish (1), peri (1) | Pero (2), perch (2), perk (2), perish (1), peri (1), peripherals (1), Perm (1), perms (1), Archae (1), FINSEQ (1) |
| Pittsburgh | Steelers, Wolverine, Winnipeg, Michigan, Erie | Steelers, Wolverine, Winnipeg, Michigan, Erie, Akron, Cincinnati, Louisville, Chattanooga, Ohio |
| Portugal | Europe, countries, Africa, Yugoslavia, Uruguay | Europe, countries, Africa, Yugoslavia, Uruguay, Scandin, Honduras, Bolivia |
| Prague (6 prompts) | Sey (4), Pasadena (2), Marino (1), Blitz (1), Pry (1) | Sey (4), Pasadena (2), Pry (2), Marino (2), heavily (2), Reign (2), Crimson (2), Elis (2), Trevor (2), Audrey (2) |
| Pyongyang | Saddam, Benghazi, Hezbollah, Taliban, jihad | Saddam, Benghazi, Hezbollah, Taliban, jihad, Rohingya, Baghd, Rahman, communist, Libya |
| Reykjavik (2 prompts) | Monaco (1), Reyes (1), Globe (1), Vega (1), Perth (1) | Monaco (1), Reyes (1), Globe (1), Vega (1), Perth (1), Tango (1), compte (1), Rex (1), Taipei (1), Rory (1) |
| Rio de Janeiro | bordel, Monaco, Disneyland, Cannes, Incontri | bordel, Monaco, Disneyland, Cannes, Incontri, oui, cruise, soundtrack, yacht, Titanic |
| Rome (25 prompts) | Vatican (16), Romans (12), Giul (6), Roma (5), Roman (4) | Vatican (17), Romans (12), Francesco (9), Giul (7), Conte (7), Roma (6), Ital (6), Catholics (6), Luigi (6), Angelo (6) |
| Saint Petersburg (5 prompts) | Enlight (3), WINAPI (2), nineteenth (2), Insider (1), Mister (1) | Enlight (3), WINAPI (3), Mister (3), Insider (2), nineteenth (2), Dort (2), eighty (2), subparagraph (1), Credential (1), pratique (1) |
| Salzburg | saline, Salisbury, lodge, salts, trout | saline, Salisbury, lodge, salts, trout, saliva, Highlands, ski, Salad, putt |
| San Antonio | Blvd, Hayward, Scalars, Spurs, MOCK | Blvd, Hayward, Scalars, Spurs, MOCK, Monterey, Oakland, Fresno, OMIT, tph |
| San Francisco (8 prompts) | Sacramento (6), Monterey (5), California (4), Oakland (4), Hawaii (3) | Monterey (7), Sacramento (7), Oakland (6), Oregon (6), California (4), Palo (4), Hawaii (3), Pacific (3), Fresno (3), Yosemite (3) |
| Santiago (2 prompts) | Antarctic (1), Ans (1), Hawaiian (1), metro (1), Spokane (1) | Antarctic (1), Ans (1), Hawaiian (1), metro (1), Spokane (1), airspace (1), Auckland (1), ext (1), Papua (1), derecho (1) |
| Scotland | Scottish, Europe, Scots, Africa, Wales | Scottish, Europe, Scots, Africa, Wales, Scandin, countries, Asia |
| Seattle | Tampa, Appalachian, Boise, Utah, Oklahoma | Tampa, Appalachian, Boise, Utah, Oklahoma, Cincinnati, Wisconsin, Jacksonville, Tacoma, Omaha |
| Seoul (2 prompts) | Auckland (1), neh (1), California (1), Realty (1), Parl (1) | Parl (2), Auckland (1), neh (1), California (1), Realty (1), Chung (1), guild (1), keyed (1), Austin (1), Taipei (1) |
| Seville (3 prompts) | Sevilla (3), seaside (2), Southampton (2), Portsmouth (2), Indianapolis (1) | Sevilla (3), seaside (2), Southampton (2), Portsmouth (2), Swansea (2), Indianapolis (1), Sey (1), seizure (1), selenium (1), Birmingham (1) |
| Shanghai (4 prompts) | Brooklyn (2), Silicone (2), Tencent (1), Rigidbody (1), Singapore (1) | Brooklyn (2), Surf (2), Silicone (2), NYC (2), Tencent (1), Rigidbody (1), Singapore (1), skys (1), Jiang (1), Sleeve (1) |
| Sofia (9 prompts) | Sophia (8), Micha (2), Pavel (2), Sloven (2), indef (2) | Sophia (9), Micha (3), Sloven (3), Pavel (2), indef (2), DFA (2), Yugosl (2), Chelsea (2), Rafael (2), Telerik (2) |
| St. Petersburg (10 prompts) | perhaps (3), ceremonial (3), sunk (3), Alic (3), formal (3) | perhaps (5), formal (4), ceremonial (3), sunk (3), Alic (3), princes (3), familiar (3), hopefully (2), Sta (2), pomp (2) |
| Stockholm (14 prompts) | Gotham (7), downtown (4), nightlife (4), Weinstein (3), stocks (2) | Gotham (8), Weinstein (5), downtown (4), nightlife (4), NYC (4), Kremlin (4), meisje (4), stocks (3), subway (3), Constantin (3) |
| Strasbourg | Strait, strang, Gron, striped, Dort | Strait, strang, Gron, striped, Dort, Lite, truncate, collar, checkpoints, straw |
| Switzerland | countries, Europe, Scandin | countries, Europe, Scandin |
| Sydney (3 prompts) | Sidney (3), Santos (1), reef (1), Bair (1), Siri (1) | Sidney (3), Santos (3), reef (1), Bair (1), Siri (1), NSW (1), Combo (1), Brooklyn (1), Auckland (1), Darling (1) |
| Tallinn | Sloven, Pavel, Sutton, Slut, Kremlin | Sloven, Pavel, Sutton, Slut, Kremlin, Ukr, Tobias, Tart, Ukrain, taller |
| Tashkent | Putin, Dmitry, Lenin, Siber, Premier | Putin, Dmitry, Lenin, Siber, Premier, Soviets, Russ, Eugene, Boris, Kremlin |
| Tehran (10 prompts) | Trudeau (4), Taipei (3), rally (3), Retorna (3), Feinstein (2) | rally (5), Retorna (5), Trudeau (4), Taipei (3), Congress (3), Presidential (3), Feinstein (2), bootloader (2), Retrieved (2), Kremlin (2) |
| Thessaloniki | Township, nearby, Locator, commune, villages | Township, nearby, Locator, commune, villages, residents, marker, Junction, vicinity, hometown |
| Tokyo (7 prompts) | downtown (4), NYC (3), Greenwich (2), Observatory (2), borough (2) | downtown (4), borough (4), subway (4), NYC (3), Greenwich (3), Manhattan (3), Retorna (3), Observatory (2), reck (2), metropolitan (2) |
| Toronto (2 prompts) | Tampa (2), Ontario (1), Cavs (1), Winnipeg (1), Newark (1) | Tampa (2), Newark (2), Ontario (1), Cavs (1), Winnipeg (1), Cincinnati (1), Weinstein (1), Auckland (1), Scarborough (1), Minnesota (1) |
| Turin (2 prompts) | ext (1), Turbo (1), concession (1), Utah (1), Bris (1) | ext (1), Turbo (1), concession (1), Utah (1), Bris (1), turbines (1), genu (1), Tibet (1), Expires (1), Tasmania (1) |
| Turkey | countries, Europe, nations, Yugoslavia, Scandin | countries, Europe, nations, Yugoslavia, Scandin |
| Ulaanbaatar (2 prompts) | Lama (2), Nagar (1), Ning (1), junto (1), Tibet (1) | Nagar (2), Lama (2), Sioux (2), Tibet (2), Ning (1), junto (1), titular (1), Manit (1), Kun (1), Rajasthan (1) |
| Valencia | valves, Valle, Valent, Valor, Valerie | valves, Valle, Valent, Valor, Valerie, Toledo, Validators, Vue, valuation, Naj |
| Valletta (3 prompts) | valuation (2), valves (2), Valerie (2), valued (2), fisheries (1) | valuation (2), valves (2), Valerie (2), valued (2), invaluable (2), valleys (2), Brighton (2), fisheries (1), fishing (1), paz (1) |
| Venice (14 prompts) | Venez (9), seaside (8), coastal (8), ocean (3), reefs (3) | seaside (10), Venez (9), coastal (8), ocean (5), carnival (5), Sic (5), MOZ (5), reefs (4), seafood (4), beach (4) |
| Vienna (18 prompts) | Wien (18), Aust (7), Sophia (6), Viktor (6), Philadelphia (4) | Wien (18), Sophia (8), Viktor (8), Aust (7), Philly (6), Philadelphia (6), Vaughan (6), Waterloo (4), Howard (4), Nashville (4) |
| Vilnius | Azerbai, Pavel, Ukr, Donetsk, Ukrain | Azerbai, Pavel, Ukr, Donetsk, Ukrain, Urb, Kremlin, Yugosl, choking, Nicaragua |
| Warsaw (17 prompts) | Harlem (6), urban (5), Welfare (5), Bangalore (3), Dayton (3) | Welfare (9), urban (8), Harlem (7), Gaines (5), Bangalore (4), Dayton (4), NYC (4), Sao (4), Urb (3), Kremlin (3) |
| Washington (4 prompts) | Capitol (3), Maryland (2), presidential (2), Georgetown (2), Arlington (2) | Maryland (3), Capitol (3), Redskins (3), Smithsonian (3), presidential (2), Georgetown (2), Arlington (2), Congressional (2), Obama (2), Bethesda (2) |
| Washington, D.C. (8 prompts) | Congressional (6), USDA (6), Maryland (4), Smithsonian (4), Capitol (2) | Congressional (6), USDA (6), Maryland (5), Smithsonian (5), Capitol (3), Americ (3), Pennsylvania (3), federally (3), Redskins (3), Arlington (3) |
| Wrocław | radial, local, Glouce, cord, brushing | radial, local, Glouce, cord, brushing, approximately, hometown, patches, rop, Wolfe |
| Xi'an | Maher, Qatar, Qur, Sic, Vinci | Maher, Qatar, Qur, Sic, Vinci, millennium, Sang, Ancient, Paso, Quran |
| Yekaterinburg | nearby, township, local, villagers, hike | nearby, township, local, villagers, hike, creek, Spokane, Spicer, Nack, jade |
| Yerevan (2 prompts) | poisoned (1), blindly (1), Sergei (1), quake (1), Pavel (1) | poisoned (1), blindly (1), Sergei (1), quake (1), Pavel (1), worthy (1), vodka (1), Decompiled (1), Dmit (1), Accountability (1) |
| Zagreb | Bav, Laguna, Nederland, Maharashtra, Mazda | Bav, Laguna, Nederland, Maharashtra, Mazda, EXTRA, pagan, Florida, Welsh, Giovanni |
| Zurich | Silicone, Zack, Corpus, Akron, Zuckerberg | Silicone, Zack, Corpus, Akron, Zuckerberg, Scientology, OCI, turnover, Zion, hoodie |

## Park → country → capital

### True answers (106 answers, 514 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Accra | Serena, Braves, Brenda, Angebot, Feinstein | Serena, Braves, Brenda, Angebot, Feinstein, Bernie, Rao, Kushner, presently, interim |
| Addis Ababa (4 prompts) | Cadillac (1), NYC (1), Tibet (1), Maurit (1), Detroit (1) | Added (2), Sudan (2), Pune (2), Cadillac (1), NYC (1), Tibet (1), Maurit (1), Detroit (1), Seattle (1), Arabian (1) |
| Algiers | Africa, Lagos, Niger, Johannesburg, Maurit | Africa, Lagos, Niger, Johannesburg, Maurit, Mumbai, Afro, CFG, Harlem, Sahara |
| Amsterdam (5 prompts) | Tottenham (2), NYC (2), Mumbai (2), Gotham (2), OTHERWISE (1) | Tottenham (2), NYC (2), Mumbai (2), Gotham (2), Chicago (2), OTHERWISE (1), Brussels (1), Manhattan (1), Rotterdam (1), Toronto (1) |
| Ankara (3 prompts) | Politico (3), Headquarters (2), campaigned (1), lawmaker (1), Applicants (1) | Politico (3), Headquarters (2), patriotic (2), campaigned (1), lawmaker (1), Applicants (1), legis (1), Kremlin (1), Riyadh (1), Conservatives (1) |
| Antananarivo (4 prompts) | Bulldogs (2), ants (2), antennas (2), antenna (1), Uncomment (1) | Bulldogs (2), ants (2), antennas (2), Antoine (2), antenna (1), Uncomment (1), Maurit (1), Bangladesh (1), Antar (1), explicit (1) |
| Astana | retrospective, Omaha, Astros, Retorna, subdivisions | retrospective, Omaha, Astros, Retorna, subdivisions, classifications, pilgrimage, searchable, offices, asthma |
| Athens (3 prompts) | Anglic (2), NHS (2), Munich (1), ext (1), Greenwich (1) | Anglic (2), NHS (2), Greenwich (2), Thames (2), Boston (2), Munich (1), ext (1), precinct (1), Vatican (1), turnout (1) |
| Baku (5 prompts) | Kurdish (2), Sergei (2), Aleks (1), Arabian (1), Armen (1) | Kurdish (3), Sergei (3), Armen (2), Arabs (2), Hassan (2), Sunni (2), Kaz (2), Hasan (2), Aleks (1), Arabian (1) |
| Bangkok (4 prompts) | Mumbai (4), NYC (4), Istanbul (3), Chicago (2), Shanghai (1) | Mumbai (4), NYC (4), Istanbul (3), blackmail (3), Chicago (2), Shanghai (2), BJP (2), subway (2), Huffington (2), downtown (1) |
| Bangui | Bangladesh, banged, banging, nesta, Rohingya | Bangladesh, banged, banging, nesta, Rohingya, Papua, Bashar, Kurdistan, safest, Sark |
| Basseterre | Caribbean, island, Jamaica, Trinidad, Bermuda | Caribbean, island, Jamaica, Trinidad, Bermuda, Bahamas, Bourbon, hurricane, Gulf, anchored |
| Beijing | NYC, Microsoft, Toronto, Disney, Verizon | NYC, Microsoft, Toronto, Disney, Verizon, NASA, Excel, Houston, Chicago, Jupiter |
| Belgrade | Yugoslavia, Milo, Jug, Bos, Balk | Yugoslavia, Milo, Jug, Bos, Balk, Adri, Lagos, Bris, Glam, Karachi |
| Berlin (16 prompts) | Istanbul (6), Kremlin (5), Brussels (4), Hamburg (3), NYC (3) | NYC (8), Kremlin (7), Istanbul (7), Brussels (7), Manhattan (5), Chicago (4), Cologne (4), Hamburg (3), Reich (3), Brooklyn (3) |
| Bishkek | Azerbai, Abdel, Abdul, secured, Hasan | Azerbai, Abdel, Abdul, secured, Hasan, Yemen, Beirut, Kurdish, Bek, Hassan |
| Bogotá (3 prompts) | Brussels (2), Dallas (1), Roths (1), Atlanta (1), stare (1) | Brussels (2), Dallas (1), Roths (1), Atlanta (1), stare (1), Beirut (1), Houston (1), airspace (1), NYC (1), Swamp (1) |
| Brasília (9 prompts) | congressional (7), governments (7), Minister (4), Senator (3), legislative (3) | congressional (7), governments (7), Minister (5), legislative (5), diplomatic (5), federal (5), Niger (5), Senator (3), bureaucratic (3), lawmaker (3) |
| Bratislava (3 prompts) | sme (1), ext (1), singapore (1), BYU (1), attracting (1) | sme (1), ext (1), singapore (1), BYU (1), attracting (1), blindness (1), Brewery (1), blinded (1), capitals (1), Batt (1) |
| Brazzaville | Quebec, Latin, Rio, Europeans, Rousse | Quebec, Latin, Rio, Europeans, Rousse, Alexandre, Marseille, Texans, Bras, Alger |
| Bucharest | Buchanan, Constantin, Istanbul, clinics, Beirut | Buchanan, Constantin, Istanbul, clinics, Beirut, Wishlist, Chennai, Bureau, blindness, chlor |
| Budapest (6 prompts) | Munich (3), Hamburg (3), Istanbul (2), Brisbane (2), Manhattan (2) | Munich (3), Hamburg (3), Manhattan (3), skys (3), Istanbul (2), Brisbane (2), Brussels (2), Leipzig (2), Luft (2), billionaires (2) |
| Buenos Aires (12 prompts) | Johannesburg (6), Philadelphia (6), Sydney (5), Adelaide (4), NYC (4) | Philadelphia (7), Johannesburg (6), Sydney (6), Melbourne (5), Adelaide (4), NYC (4), Philly (4), Chicago (3), Napoli (3), gunmen (3) |
| Cairo | Nile, Sinai, Isis, Pune, Mumbai | Nile, Sinai, Isis, Pune, Mumbai, Shanghai, Acid, Chennai, Bangalore, Karachi |
| Canberra (9 prompts) | congressional (6), Capitol (4), parliamentary (4), Westminster (2), Melbourne (2) | congressional (6), parliamentary (5), Capitol (5), senators (3), Senators (3), Pty (3), Westminster (2), Melbourne (2), Ministers (2), Perth (2) |
| Caracas | Hast, Carly, eval, Duterte, Suarez | Hast, Carly, eval, Duterte, Suarez, Nutzung, cartridge, Dresden, beloved, hac |
| Copenhagen | utc, Decompiled, ext, NYC, DECLARE | utc, Decompiled, ext, NYC, DECLARE, BUF, Nichols, Bombay, alerted, disrupting |
| Dakar (2 prompts) | Johannesburg (1), Dakota (1), EVT (1), Muslim (1), Mumbai (1) | Johannesburg (1), Dakota (1), EVT (1), Muslim (1), Mumbai (1), Ramadan (1), metropolitan (1), Tampa (1), Bombay (1), Sidd (1) |
| Dodoma (6 prompts) | dodge (6), Dodd (5), Maced (2), Deputy (2), Bucc (2) | dodge (6), Dodd (6), Donne (4), Deputy (3), Mosul (3), Maced (2), Bucc (2), Kurdistan (2), gad (2), lawmaker (2) |
| Dublin (3 prompts) | Istanbul (2), spiked (1), Gael (1), metros (1), Euro (1) | Istanbul (3), spiked (1), Gael (1), metros (1), Euro (1), Brisbane (1), Retorna (1), Guinness (1), AUD (1), cities (1) |
| Dushanbe | Kata, Tibetan, Zhao, bestowed, keys | Kata, Tibetan, Zhao, bestowed, keys, Sheikh, solutions, Mahar, Geld, looping |
| Gaborone | Jad, Howell, JOB, GOLD, Hiring | Jad, Howell, JOB, GOLD, Hiring, Potion, Persistent, SOCKET, Township, Ranked |
| Gitega | mining, Gat, cycle, Herz, Swarm | mining, Gat, cycle, Herz, Swarm, Gund, Viol, Cush, visited, enumerator |
| Guatemala City (2 prompts) | Honduras (1), Yugoslavia (1), Belize (1), countries (1), Nicaragua (1) | countries (2), Honduras (1), Yugoslavia (1), Belize (1), Nicaragua (1), Europe (1), Haiti (1), Jamaica (1), Guinea (1), Liberia (1) |
| Hanoi | NYC, Kremlin, Manhattan, Kiev, Toronto | NYC, Kremlin, Manhattan, Kiev, Toronto, Harlem, Pyongyang, Brooklyn, Chicago, Alexandre |
| Harare (3 prompts) | Auckland (3), Rosenstein (2), HDF (1), Johannesburg (1), dara (1) | Auckland (3), Rosenstein (2), Brisbane (2), Desde (2), HDF (1), Johannesburg (1), dara (1), keyed (1), Raq (1), Typeface (1) |
| Havana | Alabama, Mississippi, Florida, Louisiana, Jamaica | Alabama, Mississippi, Florida, Louisiana, Jamaica, Chicago, Michigan, Miami, Detroit, Anthony |
| Helsinki (16 prompts) | Mumbai (7), Brussels (6), Westminster (5), Metropolitan (5), Dubai (4) | Metropolitan (9), Mumbai (7), Westminster (7), Dubai (7), Brussels (6), Istanbul (6), NYC (6), utc (4), Singapore (4), Athen (4) |
| Islamabad | Karachi, Sharia, Abu, Baghdad, Haram | Karachi, Sharia, Abu, Baghdad, Haram, Islamic, Imam, Somali, Hassan, Amir |
| Jakarta (12 prompts) | Mumbai (8), Singapore (7), Brussels (5), Riyadh (5), Amazon (3) | Mumbai (11), Singapore (8), Riyadh (7), Brussels (6), Sydney (6), Amazon (4), Dubai (4), Bangalore (4), Seattle (3), Karachi (3) |
| Jerusalem (8 prompts) | Jewish (5), Jews (4), spiritual (4), Judaism (4), Hebrew (3) | Jewish (5), Jews (5), spiritual (4), Judaism (4), biblical (4), Hebrew (3), Zionist (3), nesta (2), adjoining (2), Juda (2) |
| Kabul | Kath, Broncos, Hindu, Bihar, Taliban | Kath, Broncos, Hindu, Bihar, Taliban, Nep, Freddy, Kashmir, Maul, Himal |
| Kampala (6 prompts) | Bangalore (3), Chicago (2), Camp (2), Hamp (1), Portland (1) | Bangalore (4), Chicago (3), Camp (2), Hamp (2), Pasadena (2), Kolkata (2), Kapoor (2), Gaines (2), Kensington (2), interstate (2) |
| Kathmandu (6 prompts) | sluts (3), Himal (2), erotica (2), angle (2), disqualified (2) | sluts (3), Copa (3), angle (3), Katherine (3), Cath (3), Himal (2), erotica (2), Tibetan (2), disqualified (2), Kerala (2) |
| Kigali (2 prompts) | rubble (2), feats (2), nesta (2), pact (1), granite (1) | rubble (2), feats (2), nesta (2), granite (2), pact (1), disproportion (1), oneself (1), yourself (1), ext (1), RESET (1) |
| Kinshasa (4 prompts) | kinetic (4), kinase (4), Alger (2), Pierre (1), Macron (1) | kinetic (4), kinase (4), Alger (2), Kinect (2), Pierre (2), Jean (2), Quebec (2), Francois (2), Macron (1), rewind (1) |
| Kuala Lumpur | Istanbul, Dubai, Chennai, Singapore, Toronto | Istanbul, Dubai, Chennai, Singapore, Toronto, Miami, Chicago, Lahore, Barcelona, prod |
| Kyiv (3 prompts) | LGBTQ (2), Kylie (1), Crimea (1), sneak (1), Sydney (1) | LGBTQ (3), Kylie (2), Crimea (1), sneak (1), Sydney (1), Donetsk (1), Vaults (1), Georg (1), Sergey (1), Shine (1) |
| Libreville | Liber, librarian, libido, Lexus, libs | Liber, librarian, libido, Lexus, libs, Oman, Abrams, RFID, EGL, Netanyahu |
| Lilongwe | Manhattan, Shanghai, Metro, Denver, Harlem | Manhattan, Shanghai, Metro, Denver, Harlem, debut, Lily, Lionel, Beirut, fetching |
| Lima (2 prompts) | legislation (1), Commod (1), favoured (1), IDC (1), columna (1) | legislation (1), Commod (1), favoured (1), IDC (1), columna (1), Alphabet (1), parliament (1), Colon (1), Geneva (1), turnaround (1) |
| Lisbon | Istanbul, Constantin, Mumbai, Chennai, Hindu | Istanbul, Constantin, Mumbai, Chennai, Hindu, Bombay, Judith, Singapore, Latin, European |
| Ljubljana | Moines, Stamford, ext | Moines, Stamford, ext |
| London (14 prompts) | NYC (5), Thames (5), Surrey (4), Retorna (4), Yorkshire (4) | Thames (6), NYC (5), Surrey (5), Mumbai (5), Tottenham (5), NHS (5), Retorna (4), Yorkshire (4), Brexit (4), Webseite (4) |
| Luanda (3 prompts) | Luo (3), Liu (2), Africans (1), MPL (1), Jiang (1) | Luo (3), Liu (2), Qin (2), Jin (2), Africans (1), MPL (1), Jiang (1), Moz (1), Somali (1), Wang (1) |
| Lusaka | subdivisions, incest, play, sectarian, Shelf | subdivisions, incest, play, sectarian, Shelf, isize, interracial, Pharmaceutical, prostitution, patriarch |
| Madrid (14 prompts) | Brussels (5), Retorna (4), Mumbai (4), presidential (3), Istanbul (3) | Brussels (6), Istanbul (5), Madison (5), Retorna (4), Mumbai (4), NYC (4), Riyadh (4), Cristiano (4), Buckingham (4), presidential (3) |
| Manila | Indones, Mumbai, Bombay, Singapore, Chennai | Indones, Mumbai, Bombay, Singapore, Chennai, Duterte, metropolitan, nationwide, mainland, Malays |
| Maputo | Maps, curry, Bangalore, REVIEW, bikini | Maps, curry, Bangalore, REVIEW, bikini, Preview, Chennai, Sistema, Bik, squad |
| Maseru | Init, Swansea, Bethlehem, intentions, Cumberland | Init, Swansea, Bethlehem, intentions, Cumberland, stationed, Barn, rode, Haley, withhold |
| Minsk (3 prompts) | Sergei (2), Ukrain (2), Nicar (1), Ukr (1), Dmitry (1) | Ukrain (3), Sergei (2), Kiev (2), Dud (2), Nicar (1), Ukr (1), Dmitry (1), Belize (1), Siber (1), Louisville (1) |
| Moscow (17 prompts) | Kremlin (16), NYC (8), Putin (7), Manhattan (6), Brussels (5) | Kremlin (17), Manhattan (11), Putin (10), NYC (8), Milan (8), Vladimir (7), Stalin (6), Hollywood (6), Siber (6), Brussels (5) |
| N'Djamena | Allah, Ibn, Desert, Islamic, Imam | Allah, Ibn, Desert, Islamic, Imam, ranch, Sultan, Ramadan, Alam, icing |
| Nairobi (6 prompts) | Pune (3), Perth (2), Bangalore (2), Chicago (1), Colo (1) | Pune (3), Perth (3), Brisbane (3), Bangalore (2), Sydney (2), subsidized (2), Chicago (1), Colo (1), Funding (1), libertine (1) |
| New Delhi (19 prompts) | NYC (9), NYPD (8), Mumbai (6), Manhattan (6), Hindi (5) | NYC (10), NYPD (9), Mumbai (8), Manhattan (8), NYT (7), Hindi (6), Rahul (5), Kolkata (5), Narendra (5), Chennai (4) |
| Nouakchott | Nevada, nouveau, Oasis, Khal, Louisiana | Nevada, nouveau, Oasis, Khal, Louisiana, Nuevo, Missouri, Anast, Cherokee, Oman |
| Nuuk | Guam, nuances, Arctic, Maui, island | Guam, nuances, Arctic, Maui, island, Nun, Samoa, Chu, Kata, Mesa |
| Oslo (11 prompts) | Bloomberg (6), parliamentary (4), NYC (3), Brussels (3), nationwide (3) | Bloomberg (6), parliamentary (5), NYC (3), Brussels (3), nationwide (3), legislators (3), Scandinavian (2), Norse (2), Chicago (2), lawmaker (2) |
| Ottawa (27 prompts) | Toronto (12), Quebec (12), Ontario (11), RCMP (8), Trudeau (7) | Toronto (16), Quebec (14), RCMP (13), Trudeau (13), Ontario (12), Montreal (12), Winnipeg (11), Calgary (10), government (8), Edmonton (8) |
| Panama City | Loki, Qatar, Tyson, Babe, Rockefeller | Loki, Qatar, Tyson, Babe, Rockefeller, AMAZ, Yankees, conditioner, Sultan, Jehovah |
| Paris (7 prompts) | NYC (6), Manhattan (6), Europe (2), Boston (2), Parliament (2) | NYC (6), Manhattan (6), Boston (4), Parliament (3), Chicago (3), Mumbai (3), Congress (3), Europe (2), Lond (2), nationwide (2) |
| Phnom Penh | pivot, presidential, fiercely, price, dominated | pivot, presidential, fiercely, price, dominated, solicit |
| Podgorica | pods, episode, Podcast, Wales, Clemson | pods, episode, Podcast, Wales, Clemson, Gros, Tasmania, villages, locator, Bahamas |
| Prague (2 prompts) | metropolitan (2), Istanbul (1), Mumbai (1), range (1), Pasadena (1) | metropolitan (2), Istanbul (2), Mumbai (1), range (1), Pasadena (1), Beirut (1), DISPATCH (1), initially (1), Rey (1), Christie (1) |
| Quito (3 prompts) | Toledo (1), Hawai (1), quarters (1), subdivisions (1), tropical (1) | Seattle (2), Toledo (1), Hawai (1), quarters (1), subdivisions (1), tropical (1), Regents (1), camps (1), Belize (1), congressional (1) |
| Rabat | rabbits, Hawai, Ranch, Royals, riff | rabbits, Hawai, Ranch, Royals, riff, Robbins, Riyadh, Huckabee, rib, Honolulu |
| Ramallah | Ramadan, Rahman, Rams, Ramirez, Bangladesh | Ramadan, Rahman, Rams, Ramirez, Bangladesh, Raj, Abdullah, Arabic, Sheikh, Kuwait |
| Reykjavík (2 prompts) | Istanbul (1), Papua (1), Sydney (1), Reyes (1), Venice (1) | Istanbul (1), Papua (1), Sydney (1), Reyes (1), Venice (1), Rae (1), bordel (1), RTAL (1), Gotham (1), Isabel (1) |
| Riga (3 prompts) | Saga (1), lobster (1), trustees (1), Lair (1), Sharks (1) | Saga (1), lobster (1), trustees (1), Lair (1), Sharks (1), Prelude (1), mitt (1), Admir (1), Builders (1), Cay (1) |
| Rome (20 prompts) | Vatican (14), Romans (11), Venice (6), Roman (3), Brussels (3) | Vatican (14), Romans (12), Venice (7), Milano (5), Giul (5), Brussels (4), Kremlin (4), Judiciary (4), Roman (3), NYC (3) |
| San José (2 prompts) | Laguna (1), sanitation (1), Caj (1), sanction (1), seaside (1) | Sanchez (2), Laguna (1), sanitation (1), Caj (1), sanction (1), seaside (1), Oakland (1), Puerto (1), Palo (1), Trinidad (1) |
| Santiago (8 prompts) | ext (2), weekdays (2), Aws (2), Puerto (1), Hend (1) | weekdays (3), ext (2), Aws (2), Bolivia (2), Seattle (2), Contributors (2), disconnected (2), Puerto (1), Hend (1), Adelaide (1) |
| Sarajevo (3 prompts) | Muslim (2), Quran (2), Islam (2), Muslims (1), Islamic (1) | Muslim (2), Quran (2), Islam (2), Arabic (2), jihad (2), Imam (2), Abu (2), Ramadan (2), Sharia (2), Ibn (2) |
| Seoul | Mitar, Helpers, singapore, dependable, umbrella | Mitar, Helpers, singapore, dependable, umbrella, PIXEL, Sloan, seri, Regents, Shanghai |
| Skopje | Scandinavian, skating, skiing, sketch, Vancouver | Scandinavian, skating, skiing, sketch, Vancouver, exceptions, upwards, AUD, skate, Melbourne |
| Sofia (2 prompts) | Sophia (2), Pavel (2), Eug (1), Dmitry (1), Annunci (1) | Sophia (2), Pavel (2), Hollande (2), Theodore (2), Nicolas (2), Eug (1), Dmitry (1), Annunci (1), metro (1), Sergey (1) |
| Stockholm (20 prompts) | NYC (11), Gotham (9), Manhattan (7), Svens (7), nightlife (6) | NYC (13), Gotham (12), Manhattan (9), Istanbul (9), nightlife (8), Svens (7), subway (7), Scandinavian (5), Nordic (5), Lund (5) |
| Taipei | Wang, Cheng, Qin, Huang, Liu | Wang, Cheng, Qin, Huang, Liu, Jiang, Xin, Yuan, Zhao, Yang |
| Tallinn | Ziel, uninitialized, udp, noop, rop | Ziel, uninitialized, udp, noop, rop, Recursive, inst, fie, obe, Baxter |
| Tbilisi (3 prompts) | explicit (2), subdivisions (2), salsa (1), nesta (1), preached (1) | explicit (2), subdivisions (2), manifestations (2), LEFT (2), salsa (1), nesta (1), preached (1), Mohamed (1), Hispan (1), ext (1) |
| Tehran | Scient, tourist, trendy, Beirut, Venice | Scient, tourist, trendy, Beirut, Venice, SCI, NOI, Springer, MEP, dens |
| Thimphu | ellas, explicit, campaigned, uphill, tamil | ellas, explicit, campaigned, uphill, tamil, Trom, fils, besoin, filles, Milf |
| Tirana (6 prompts) | Azerbai (1), Splash (1), Cait (1), Zag (1), applaud (1) | EFI (2), Balk (2), Sean (2), Azerbai (1), Splash (1), Cait (1), Zag (1), applaud (1), Tamil (1), protesting (1) |
| Tokyo (13 prompts) | NYC (8), Mumbai (6), Singapore (4), Shib (3), Osaka (2) | NYC (8), Mumbai (6), skys (6), Singapore (5), Shib (5), Sydney (4), Manhattan (4), Metropolitan (4), Toronto (3), Samurai (3) |
| Tunis | Marseille, Alger, Sic, Pessoa, Asheville | Marseille, Alger, Sic, Pessoa, Asheville, Blanc, Hait, Sloven, Philippe, Bordeaux |
| Ulaanbaatar | Habitat, bordered, Kamp, Tamb, titular | Habitat, bordered, Kamp, Tamb, titular, Mandal, Township, villages, Nagar, Hut |
| Vienna (4 prompts) | Wien (2), Columbia (2), Austin (2), Ivy (1), Chicago (1) | Wien (4), Columbia (2), Austin (2), Ivy (1), Chicago (1), Zurich (1), Bau (1), Sloven (1), Vanity (1), diligence (1) |
| Vilnius (3 prompts) | Istanbul (2), Barcelona (2), Kiev (1), Kyoto (1), Brussels (1) | Istanbul (2), Barcelona (2), Kiev (2), Shanghai (2), Kyoto (1), Brussels (1), Nashville (1), Munich (1), Chicago (1), Osaka (1) |
| Warsaw (14 prompts) | NYC (5), Chicago (4), capitals (4), Manhattan (4), Vatican (3) | NYC (6), Manhattan (6), Brussels (5), Chicago (4), capitals (4), Constantin (4), Vatican (3), legis (3), populous (3), Scandinavian (3) |
| Washington, D.C. (60 prompts) | Congressional (42), Microsoft (34), presidential (28), government (18), Redskins (16) | Congressional (42), Microsoft (39), presidential (38), Capitol (31), government (29), Redskins (28), Pentagon (27), Smithsonian (25), Obama (23), politicians (18) |
| Wellington (10 prompts) | Auckland (5), Westminster (5), Thames (3), embassy (3), Kremlin (2) | Westminster (7), Auckland (5), Thames (5), Honour (4), Manhattan (4), Wishlist (3), embassy (3), Waterloo (3), Vanity (3), Baghd (3) |
| Windhoek | windy, Brisbane, councillors, Turnbull, dicks | windy, Brisbane, councillors, Turnbull, dicks, commuters, windshield, Voters, Adelaide, favourite |
| Yamoussoukro | Fuk, yen, Kum, Nak, Hir | Fuk, yen, Kum, Nak, Hir, Yah, Yas, Yad, Kaw, Nag |
| Yaoundé (2 prompts) | Newport (1), wann (1), Presidents (1), Atlanta (1), Navy (1) | Newport (1), wann (1), Presidents (1), Atlanta (1), Navy (1), Wein (1), Yale (1), Overwatch (1), Quebec (1), imperial (1) |
| Yerevan | Kurds, quake, Assy, Auss, Bundy | Kurds, quake, Assy, Auss, Bundy, Bour, earthquake, randomly, Anaheim, Yaz |
| Zagreb (4 prompts) | Mumbai (3), teg (2), aggregator (2), NYC (2), Lagos (1) | Mumbai (3), teg (2), aggregator (2), NYC (2), plano (2), harness (2), nog (2), Lagos (1), Vancouver (1), HRESULT (1) |

### Model answers (158 answers, 447 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Accra | Feinstein, Narendra, Chavez, algum, Braves | Feinstein, Narendra, Chavez, algum, Braves, Baghd, Kushner, Nagar, NYC, Bollywood |
| Addis Ababa (4 prompts) | Added (2), porcelain (1), Minneapolis (1), Tibet (1), Hyderabad (1) | Hyderabad (2), Added (2), Pune (2), Bangalore (2), urban (2), Bombay (2), porcelain (1), Minneapolis (1), Tibet (1), Himal (1) |
| Adelaide | Greenville, Sioux, Clemson, Charleston, Dund | Greenville, Sioux, Clemson, Charleston, Dund, Midlands, Birmingham, Missouri, Moor, Newport |
| Algiers | Niger, Africa, Lagos, Maurit, Sahara | Niger, Africa, Lagos, Maurit, Sahara, CFG, Afro, Harlem, Lac, Libya |
| Amsterdam (3 prompts) | Tottenham (2), NYC (2), OTHERWISE (1), Gotham (1), selv (1) | Tottenham (2), NYC (2), bigot (2), OTHERWISE (1), Gotham (1), selv (1), Dortmund (1), Manhattan (1), nederland (1), metro (1) |
| Anchorage (4 prompts) | anchors (4), Alaska (2), Pruitt (1), Retorna (1), Honolulu (1) | anchors (4), Alaska (2), Pompeo (2), Pruitt (1), Retorna (1), Honolulu (1), Yemen (1), Kremlin (1), Hawaiian (1), Balk (1) |
| Ankara (4 prompts) | Government (3), congressional (2), nationalists (1), Boise (1), Erdogan (1) | Government (3), congressional (2), politicians (2), nationalists (1), Boise (1), Erdogan (1), Guam (1), Anat (1), Republican (1), bureaucrats (1) |
| Antananarivo (2 prompts) | Antoine (2), antennas (1), Maurit (1), reordered (1), Uncomment (1) | Antoine (2), Bulldogs (2), antennas (1), Maurit (1), reordered (1), Uncomment (1), Olivier (1), Xavier (1), Hispan (1), cds (1) |
| Arusha (2 prompts) | ski (2), skiing (2), seated (1), Arctic (1), snow (1) | ski (2), skiing (2), seated (1), Arctic (1), snow (1), seaside (1), Campo (1), parks (1), vertically (1), arthritis (1) |
| Astana | office, Election, palabras, Sanford, Asset | office, Election, palabras, Sanford, Asset, asthma, apps, Kasich, delegation, Omaha |
| Asunción | Paso, asynchronous, mest, Oklahoma, Fiscal | Paso, asynchronous, mest, Oklahoma, Fiscal, Juli, Hond, Oro, Alamofire, Mej |
| Athens (3 prompts) | Mediterranean (2), ext (2), Athena (1), chosen (1), Ihren (1) | Mediterranean (2), ext (2), Ethi (2), Athena (1), chosen (1), Ihren (1), Plato (1), Gaut (1), precinct (1), turnout (1) |
| Atlanta | Dort, bigot, requester, fucks, Bellev | Dort, bigot, requester, fucks, Bellev, freezer, hurd, tph, keyed, Rapids |
| Baku (3 prompts) | Azerbai (2), Abdel (2), Arabian (1), Sergei (1), monopoly (1) | Kurdish (3), Azerbai (2), Abdel (2), Hassan (2), Hasan (2), Sheikh (2), Arabian (1), Sergei (1), monopoly (1), Arabs (1) |
| Bangkok (5 prompts) | Huffington (2), downtown (1), BJP (1), travelers (1), Faker (1) | Huffington (2), BJP (2), bigot (2), YYS (2), congest (2), downtown (1), travelers (1), Faker (1), Shanghai (1), Hindi (1) |
| Bangui (2 prompts) | Bangladesh (2), banged (2), banging (2), Kurdish (1), nesta (1) | Bangladesh (2), banged (2), banging (2), Rohingya (2), Kurdish (1), nesta (1), fist (1), Bashar (1), Bach (1), Papua (1) |
| Barcelona (4 prompts) | Byron (3), Produkt (2), zaman (2), coastal (1), Constantin (1) | Byron (4), Produkt (2), zaman (2), busty (2), coastal (1), Constantin (1), camb (1), bigot (1), ERROR (1), Shanghai (1) |
| Beirut (3 prompts) | Hezbollah (3), Baghd (2), Philippe (1), Armen (1), Yugosl (1) | Hezbollah (3), Baghd (2), Aleppo (2), Philippe (1), Armen (1), Yugosl (1), Arabs (1), Gaza (1), Brittany (1), Kurdish (1) |
| Belfast | Bradley, Bethlehem, Cork, Birmingham, Covent | Bradley, Bethlehem, Cork, Birmingham, Covent, Baltimore, Liam, Leeds, IRA, Camden |
| Belgrade (2 prompts) | Yugoslavia (2), Milo (1), Adri (1), Jug (1), Sloven (1) | Yugoslavia (2), Milo (2), Adri (2), Jug (2), Balk (2), Sloven (1), Bos (1), belie (1), belts (1), Lagos (1) |
| Berlin (6 prompts) | Leipzig (2), Kremlin (2), Putin (2), Vladimir (2), Bolshevik (2) | Merkel (4), Bolshevik (3), Metro (3), Leipzig (2), Kremlin (2), Putin (2), Vladimir (2), Bundesliga (2), Bayern (2), Lenin (2) |
| Bishkek (2 prompts) | Azerbai (1), Yemen (1), Malik (1), Kurdish (1), Hasan (1) | Azerbai (1), Yemen (1), Malik (1), Kurdish (1), Hasan (1), Abbas (1), Abdul (1), Aleppo (1), Rahman (1), Bahrain (1) |
| Bogotá | diplomatic, Downing, bureaucrats, Kremlin, congressional | diplomatic, Downing, bureaucrats, Kremlin, congressional, Baghdad, Harlem, Demp, NYC, Roths |
| Bonn | bonuses, Sciences, Pets, barracks, Humans | bonuses, Sciences, Pets, barracks, Humans, Nearby, overhead, Diseases, Government, Petra |
| Brasilia (3 prompts) | Bolivia (2), governments (1), Braz (1), Maduro (1), Nebraska (1) | Bolivia (2), Nicaragua (2), Maduro (2), congressional (2), Uruguay (2), governments (1), Braz (1), Nebraska (1), Minister (1), Honduras (1) |
| Brasília | governments, Minister, legislative, bureaucrats, politicians | governments, Minister, legislative, bureaucrats, politicians, lawmaker, parliament, diplomatic, lobbyists, nationals |
| Bratislava (3 prompts) | sme (1), ext (1), singapore (1), Wichita (1), find (1) | sme (1), ext (1), singapore (1), Wichita (1), find (1), blindness (1), BYU (1), prosper (1), capitals (1), Brewery (1) |
| Brazzaville | Latin, Europeans, Bras, Rousse, Arabs | Latin, Europeans, Bras, Rousse, Arabs, Alexandre, Texans, Alger, Cannes, Renault |
| Bucharest (2 prompts) | Constantin (2), Buchanan (2), Mediterranean (1), clinics (1), Bureau (1) | Constantin (2), Buchanan (2), Commissioner (2), Mediterranean (1), clinics (1), Bureau (1), roman (1), Wishlist (1), Alban (1), Aristotle (1) |
| Budapest (6 prompts) | skys (3), NYC (3), Manhattan (3), Shanghai (3), billionaires (2) | Shanghai (4), skys (3), NYC (3), Manhattan (3), billionaires (3), Pemb (3), Dubai (2), Leipzig (2), Lager (2), favoured (2) |
| Buenos Aires (7 prompts) | Napoli (3), NYC (2), Detroit (2), gunmen (2), Philadelphia (2) | Philadelphia (4), Napoli (3), gunmen (3), NYC (2), Detroit (2), Gors (2), Alban (2), Uruguay (2), Constantin (2), creamy (2) |
| Bulawayo (2 prompts) | bulb (2), bully (2), Bullet (1), Bucc (1), Rosenberg (1) | bulb (2), bully (2), Bullet (2), Burnett (2), Buckley (2), Bounty (2), Trevor (2), Bucc (1), Rosenberg (1), Bryce (1) |
| Calgary (2 prompts) | Sheffield (2), Birmingham (1), Dallas (1), Bangalore (1), Tulsa (1) | Sheffield (2), Dallas (2), Birmingham (1), Bangalore (1), Tulsa (1), REUTERS (1), Sioux (1), Derby (1), Sapphire (1), Wichita (1) |
| Canberra (3 prompts) | congressional (2), Capitol (2), parliament (1), bipartisan (1), Honour (1) | congressional (2), Capitol (2), bipartisan (2), Government (2), legislators (2), Presidents (2), politicians (2), parliament (1), Honour (1), chancellor (1) |
| Caracas | Nicaragua, hac, Burlington, Suarez, eval | Nicaragua, hac, Burlington, Suarez, eval, Hast, init, Maduro, Duterte, Kensington |
| Cardiff (2 prompts) | accession (1), Columbus (1), Sheffield (1), Theodore (1), asian (1) | accession (1), Columbus (1), Sheffield (1), Theodore (1), asian (1), Brighton (1), consultancy (1), Cornel (1), CAD (1), Afro (1) |
| Chengdu | Sheffield, Ciudad, Covent, Wichita, Cities | Sheffield, Ciudad, Covent, Wichita, Cities, Trev, Medina, Input, Bren, Keller |
| Chicago (2 prompts) | Illinois (2), Midwest (2), Oklahoma (1), Michigan (1), Milwaukee (1) | Illinois (2), Midwest (2), Milwaukee (2), Iowa (2), Oklahoma (1), Michigan (1), Cincinnati (1), Nebraska (1), Wisconsin (1), Omaha (1) |
| Christchurch (2 prompts) | Tacoma (2), Christoph (1), Crist (1), Canyon (1), Sacramento (1) | Tacoma (2), Oregon (2), Sacramento (2), Spokane (2), Christoph (1), Crist (1), Canyon (1), Jesus (1), Montana (1), Antarctic (1) |
| Cleveland | Detroit, Toledo, Cavs, Syracuse, Buffalo | Detroit, Toledo, Cavs, Syracuse, Buffalo, Milwaukee, Niagara, Tampa, pendant, nickel |
| Copenhagen (2 prompts) | utc (1), European (1), Decompiled (1), Deutsche (1), ext (1) | utc (1), European (1), Decompiled (1), Deutsche (1), ext (1), Scandinavian (1), NYC (1), Oxford (1), DECLARE (1), Eur (1) |
| Dakar (2 prompts) | Dakota (2), EVT (1), Muslim (1), Emacs (1), Ramadan (1) | Dakota (2), EVT (1), Muslim (1), Emacs (1), Ramadan (1), Carlo (1), Tampa (1), Dallas (1), Sidd (1), Lyon (1) |
| Dar es Salaam (3 prompts) | cate (2), ocean (1), Karachi (1), Ramadan (1), Rajasthan (1) | cate (2), UNIX (2), Beng (2), ocean (1), Karachi (1), Ramadan (1), Rajasthan (1), Charleston (1), darling (1), Muslim (1) |
| Denver | Omaha, Detroit, Milwaukee, Nuggets, Houston | Omaha, Detroit, Milwaukee, Nuggets, Houston, Minneapolis, Colorado, Winnipeg, Dallas, Broncos |
| Dublin (2 prompts) | spiked (1), Retorna (1), AUD (1), metros (1), Dubai (1) | spiked (1), Retorna (1), AUD (1), metros (1), Dubai (1), favored (1), Constantin (1), cities (1), Metropolitan (1), licensors (1) |
| Edmonton (3 prompts) | Alberta (2), Oilers (2), Texans (2), PROT (1), Sacramento (1) | Alberta (3), Oilers (3), Texans (2), Saskatchewan (2), Texas (2), PROT (1), Sacramento (1), Tacoma (1), BCHP (1), Boise (1) |
| Florence | Oakland, Fresno, Lyon, artisans, Renaissance | Oakland, Fresno, Lyon, artisans, Renaissance, Cincinnati, oak, Pied, Tus, Toledo |
| Frankfurt | Surrey, Fresno, Oprah, Roths, Porsche | Surrey, Fresno, Oprah, Roths, Porsche, futuristic, Nass, Frankie, skys, Yosemite |
| Gaborone | JOB, Howell, Jad, GOLD, Hiring | JOB, Howell, Jad, GOLD, Hiring, Potion, Scheduled, SOCKET, Jog, FAILED |
| Gdańsk | coastal, maritime, fishermen, seaside, ocean | coastal, maritime, fishermen, seaside, ocean, shoreline, pond, fishing, sailors, aquatic |
| Glasgow | Clyde, Scotland, Scottish, Birmingham, Wildcats | Clyde, Scotland, Scottish, Birmingham, Wildcats, Wolver, Kendrick, Decompiled, Highland, Cosby |
| Grenoble (2 prompts) | grenade (1), skiing (1), Paginator (1), ski (1), lam (1) | grenade (2), skiing (1), Paginator (1), ski (1), lam (1), sled (1), Overrides (1), mountain (1), lain (1), Idaho (1) |
| Guatemala City | Yugoslavia, countries, Gujarat, Bangladesh, Honduras | Yugoslavia, countries, Gujarat, Bangladesh, Honduras, Haiti |
| Haifa | seaside, coastal, Nack, aquatic, beaches | seaside, coastal, Nack, aquatic, beaches, aquarium, Laguna, shore, Aberdeen, Ville |
| Halifax (4 prompts) | Harbor (2), Harvard (2), Moff (1), RCMP (1), Hancock (1) | Harvard (3), Nova (3), Harbor (2), Hancock (2), Moff (1), RCMP (1), Clemson (1), eval (1), Winnipeg (1), Sunderland (1) |
| Hamburg (3 prompts) | coastal (2), seaside (2), ships (1), Ragnar (1), Texas (1) | coastal (2), seaside (2), ships (1), Ragnar (1), Texas (1), Tampa (1), harbor (1), maritime (1), originally (1), harbour (1) |
| Harare (2 prompts) | venez (1), HIV (1), vorhand (1), Fiji (1), Toledo (1) | venez (1), HIV (1), vorhand (1), Fiji (1), Toledo (1), Lagos (1), Nicaragua (1), Niger (1), gere (1), apartheid (1) |
| Helsinki (15 prompts) | Dubai (7), Westminster (6), Metropolitan (6), NYC (5), Singapore (5) | Dubai (9), Metropolitan (8), Westminster (7), Singapore (7), NYC (5), utc (4), airy (4), ancora (3), Gotham (3), skys (3) |
| Islamabad | Baghdad, Sharia, Abu, Karachi, Islamic | Baghdad, Sharia, Abu, Karachi, Islamic, Haram, Imam, Amir, Somali, Hussein |
| Istanbul (2 prompts) | Constantin (2), Brooklyn (1), continents (1), mystical (1), Europe (1) | Constantin (2), Brooklyn (2), continents (1), mystical (1), Europe (1), oceans (1), Mediterranean (1), Karachi (1), worldwide (1), Mediterr (1) |
| Jaipur | Desert, Nevada, Rajasthan, Frem, Reno | Desert, Nevada, Rajasthan, Frem, Reno, Mormon, Jaune, Tahoe, Jaime, Tucson |
| Jakarta (10 prompts) | Dubai (6), Singapore (5), Bombay (3), Riyadh (3), NYC (3) | Singapore (7), Dubai (7), Riyadh (6), Bombay (5), NYC (4), Amazon (4), Shanghai (3), Lagos (3), Bangalore (3), Manhattan (3) |
| Jerusalem (5 prompts) | nesta (3), praying (2), Buckingham (1), Hebrew (1), Vatican (1) | nesta (3), praying (2), prayed (2), Buckingham (2), Jewish (2), Kushner (2), Hebrew (1), Vatican (1), Whitney (1), Protestant (1) |
| Kabul | Kath, Broncos, Bihar, Hindu, Taliban | Kath, Broncos, Bihar, Hindu, Taliban, Nep, Freddy, Kashmir, Maul, Himal |
| Kampala (6 prompts) | Bangalore (4), Boise (3), Camp (2), Hamp (2), Gaines (2) | Bangalore (4), Boise (3), Camp (2), Hamp (2), Gaines (2), Kapoor (2), Thames (2), interstate (2), Indianapolis (2), Uttar (2) |
| Kassel | Newfoundland, preacher, heed, molt, ohio | Newfoundland, preacher, heed, molt, ohio, Label, scripture, sermon, EACH, defiant |
| Kathmandu (6 prompts) | sluts (3), Copa (3), Himal (2), Tibetan (2), angle (2) | sluts (3), Copa (3), angle (3), Cath (3), Katherine (3), Himal (2), Tibetan (2), IDX (2), disqualified (2), taxis (2) |
| Kiev (5 prompts) | Donetsk (3), insure (2), Ukrain (2), ISIS (2), disclosed (2) | Donetsk (3), Aleppo (3), insure (2), Ukrain (2), ISIS (2), disclosed (2), Ukr (2), Bihar (2), Crimea (2), Liberia (2) |
| Kigali (2 prompts) | nesta (2), feats (2), rubble (1), pact (1), disproportion (1) | nesta (2), feats (2), rubble (1), pact (1), disproportion (1), granite (1), turnovers (1), ext (1), oneself (1), defiance (1) |
| Kinshasa (2 prompts) | kinetic (2), kinase (2), Alger (1), rewind (1), Haiti (1) | kinetic (2), kinase (2), Alger (1), rewind (1), Haiti (1), Todd (1), Macron (1), Bethesda (1), Trinidad (1), Kamp (1) |
| Kolkata | Beng, Bangladesh, Camb, Protestant, Scotch | Beng, Bangladesh, Camb, Protestant, Scotch, Dunk, Gerard, Noir, Cocktail, dames |
| Kraków | BYU, Asheville, Yellowstone, Brewery, Montana | BYU, Asheville, Yellowstone, Brewery, Montana, skiing, Highlands, unc, Wyoming, Skyrim |
| Libreville | Liber, librarian, libido, Oman, Lexus | Liber, librarian, libido, Oman, Lexus, libs, RFID, Abrams, EGL, Netanyahu |
| Lilongwe | Manhattan, debut, Lily, Shanghai, Lionel | Manhattan, debut, Lily, Shanghai, Lionel, avid, Emil, clit, Metro, Cute |
| Lima (2 prompts) | Wat (1), Commod (1), Kohana (1), IDC (1), Decompiled (1) | Anc (2), Wat (1), Commod (1), Kohana (1), IDC (1), Decompiled (1), Alphabet (1), Tik (1), Colon (1), Mayo (1) |
| Lisbon | Bombay, Constantin, Singapore, Elis, domestically | Bombay, Constantin, Singapore, Elis, domestically, Pune, Karachi, Rotterdam, INA, Europe |
| Ljubljana | Stamford, Metodo, metropolitan, Moines, Retorna | Stamford, Metodo, metropolitan, Moines, Retorna, constituency, ext |
| London (11 prompts) | Surrey (7), Thames (6), Retorna (4), Tottenham (4), NHS (3) | Surrey (7), Thames (6), Retorna (5), Tottenham (5), NHS (4), Brexit (4), Yorkshire (4), Downing (4), Buckingham (4), Webseite (3) |
| Los Angeles (4 prompts) | UCLA (3), Hollywood (3), Pasadena (2), Rosenstein (1), Californ (1) | UCLA (4), Hollywood (3), Pasadena (2), Lakers (2), USC (2), Fresno (2), Rosenstein (1), Californ (1), California (1), Gotham (1) |
| Louisville | Missouri, Arkansas, Louisiana, Kentucky, Memphis | Missouri, Arkansas, Louisiana, Kentucky, Memphis, Sioux, Manitoba, LSU, Chattanooga, Baton |
| Lucknow (2 prompts) | Kentucky (2), Illinois (1), Arkansas (1), Lucky (1), Alabama (1) | Kentucky (2), Illinois (2), Tennessee (2), Arkansas (1), Lucky (1), Alabama (1), Cincinnati (1), Caleb (1), Ohio (1), Missouri (1) |
| Lusaka (2 prompts) | subdivisions (2), incest (1), Clayton (1), sectarian (1), Viagra (1) | subdivisions (2), patriarch (2), incest (1), Clayton (1), sectarian (1), Viagra (1), play (1), Indianapolis (1), campaigned (1), isize (1) |
| Madrid (8 prompts) | Riyadh (3), Mandarin (2), metropolitan (2), Milano (2), NYC (2) | Milano (5), Downing (4), Riyadh (3), metropolitan (3), NYC (3), Buckingham (3), ext (3), President (3), Mandarin (2), Congress (2) |
| Manila | nationwide, Bombay, Indones, Hindi, metropolitan | nationwide, Bombay, Indones, Hindi, metropolitan, globalization, franca, Duterte, Singapore, Asia |
| Marseille | urban, unlike, Cities, alike, Buildings | urban, unlike, Cities, alike, Buildings, Rural, Relief, QLD, barrel, suburban |
| Maseru | Swansea, Cumberland, Init, intentions, stationed | Swansea, Cumberland, Init, intentions, stationed, Bethlehem, hut, Yun, Perez, Clarence |
| Medan (2 prompts) | Fayette (2), Asheville (2), mediation (1), Hud (1), Medic (1) | Fayette (2), Asheville (2), mediation (1), Hud (1), Medic (1), Bundy (1), Greenville (1), Panther (1), tup (1), Medal (1) |
| Melbourne | MOZ, Oakland, Toledo, Pearce, Verde | MOZ, Oakland, Toledo, Pearce, Verde, Blvd, shores, Lauderdale, Michigan, mural |
| Mexico City | Houston, Americas, Shanghai, Asia, NYC | Houston, Americas, Shanghai, Asia, NYC, subway, Texans, Detroit, metro, taco |
| Miami | Memphis, NYC, Brooklyn, bigot, Conveyor | Memphis, NYC, Brooklyn, bigot, Conveyor, Speedway, Lauderdale, Ebay, Csv, fucks |
| Minsk | lem, Vander, Abed, Nicar, Bengals | lem, Vander, Abed, Nicar, Bengals, Midlands, Balt, Zus, Belize, Celt |
| Moscow (8 prompts) | Kremlin (7), Manhattan (3), Putin (2), Hollywood (2), NYC (2) | Kremlin (8), Manhattan (5), NYC (5), Marxist (3), Stalin (3), Putin (2), Lub (2), Hollywood (2), Rossi (2), Milano (2) |
| Munich (2 prompts) | Demp (1), Bav (1), nationwide (1), oneself (1), Riyadh (1) | Demp (1), Bav (1), nationwide (1), oneself (1), Riyadh (1), Sanford (1), Bangalore (1), Bayern (1), subsidized (1), bumper (1) |
| Nairobi (7 prompts) | Bangalore (4), Pune (3), Ken (1), Funding (1), Oracle (1) | Pune (5), Bangalore (4), favoured (2), Ken (1), Funding (1), Oracle (1), Ukrain (1), stere (1), headquartered (1), coconut (1) |
| New Delhi (9 prompts) | government (4), Narendra (4), Patriot (3), President (2), Rahul (2) | government (4), Narendra (4), Patriot (3), Rahul (3), Congress (3), President (2), Sidd (2), political (2), presidential (2), diplomats (2) |
| New York (7 prompts) | NYC (7), Brooklyn (7), Manhattan (7), NYPD (6), Bronx (5) | NYC (7), Brooklyn (7), Manhattan (7), NYPD (7), Bronx (7), Harlem (7), Broadway (6), Gotham (5), Knicks (5), NYT (3) |
| Nice | Interesting, Crazy, Ocean, beach, coastal | Interesting, Crazy, Ocean, beach, coastal, seaside, Cool, sharks, Good, Pleasant |
| Nouakchott | Nevada, nouveau, Khal, Oasis, Louisiana | Nevada, nouveau, Khal, Oasis, Louisiana, Nuevo, Missouri, Cherokee, Alabama, Belize |
| Orlando | Oklahoma, Toledo, Nashville, Florida, Tampa | Oklahoma, Toledo, Nashville, Florida, Tampa, ext, Midwest, Tulsa, Chattanooga, Ohio |
| Oslo (12 prompts) | NYC (4), Bloomberg (4), parliamentary (4), Scandinavian (3), Columbia (2) | parliamentary (5), NYC (4), Bloomberg (4), Columbia (4), Scandinavian (3), lawmaker (3), Javascript (2), INA (2), Capitol (2), legislators (2) |
| Ottawa (3 prompts) | congressional (2), RCMP (2), bipartisan (2), Ontario (1), Trudeau (1) | congressional (3), RCMP (2), bipartisan (2), Ontario (2), parliament (2), senators (2), Trudeau (1), Tories (1), politicians (1), governments (1) |
| Palermo | Paladin, puerto, palms, tamp, Fayette | Paladin, puerto, palms, tamp, Fayette, palabras, find, fucks, Reyes, dicks |
| Panama City | Loki, Qatar, Tyson, AMAZ, Babe | Loki, Qatar, Tyson, AMAZ, Babe, Rockefeller, conditioner, Yankees, Sultan, FINAL |
| Perth | Sacramento, Frem, California, Surrey, Utah | Sacramento, Frem, California, Surrey, Utah, Tacoma, Spokane, Sinai, Pasadena, Swansea |
| Phnom Penh | pivot, presidential, chaired, price, dominated | pivot, presidential, chaired, price, dominated, fiercely |
| Phoenix | Arizona, Boise, Tulsa, Idaho, Oklahoma | Arizona, Boise, Tulsa, Idaho, Oklahoma, Milwaukee, Detroit, Tucson, Oakland, Michigan |
| Prague (2 prompts) | metropolitan (2), initially (1), range (1), originally (1), DISPATCH (1) | metropolitan (2), Pasadena (2), initially (1), range (1), originally (1), DISPATCH (1), Lond (1), Christie (1), Sey (1), Rey (1) |
| Pretoria (2 prompts) | pretend (2), Pty (2), interstate (1), apartheid (1), africa (1) | pretend (2), Pty (2), interstate (1), apartheid (1), africa (1), Queensland (1), Natal (1), NSW (1), filings (1), Gaut (1) |
| Quebec City | Kasich, siege, Medieval, historically, Politico | Kasich, siege, Medieval, historically, Politico, Muk, Kurdistan, Gujarat, newer, Pedido |
| Quito (6 prompts) | Toledo (2), Hawai (1), Nicaragua (1), quarters (1), Blazers (1) | Toledo (3), Burlington (2), Hawai (1), Nicaragua (1), quarters (1), Blazers (1), subdivisions (1), tropical (1), Felipe (1), pioneering (1) |
| Reykjavik (2 prompts) | compte (2), bordel (1), Papua (1), Gotham (1), Reyes (1) | compte (2), bordel (1), Papua (1), Gotham (1), Reyes (1), Monaco (1), RTAL (1), Rae (1), NYC (1), quantify (1) |
| Reykjavík | Norse, Ragnar, Viking, Loki, Arctic | Norse, Ragnar, Viking, Loki, Arctic, Nordic, Rei, Reaper, Reef, Newfoundland |
| Riga (3 prompts) | Saga (1), lobster (1), burge (1), Lair (1), Sharks (1) | Saga (1), lobster (1), burge (1), Lair (1), Sharks (1), trustees (1), mitt (1), Admir (1), Prelude (1), Caldwell (1) |
| Rio de Janeiro (2 prompts) | seaside (1), Braz (1), Brooklyn (1), Niger (1), Southampton (1) | seaside (1), Braz (1), Brooklyn (1), Niger (1), Southampton (1), Carnival (1), Newport (1), Renault (1), Portsmouth (1), Karachi (1) |
| Rome (10 prompts) | Vatican (4), Romans (4), Roman (3), Conte (3), Roma (2) | Vatican (5), Romans (4), Roman (3), Conte (3), Downing (3), IMF (3), Roma (2), Tamb (2), Manhattan (2), parliament (2) |
| Salt Lake City (3 prompts) | Minneapolis (2), Utah (2), Burlington (2), BYU (1), Rockies (1) | Utah (3), Minneapolis (2), Burlington (2), BYU (2), Rockies (2), Rocky (2), Weinstein (1), Mormons (1), Summit (1), Brigham (1) |
| San Diego | Monterey, Palo, Tucson, Southwest, Blvd | Monterey, Palo, Tucson, Southwest, Blvd, Asheville, Padres, Springs, bookmarks, ext |
| San Francisco (6 prompts) | sanitize (2), Monterey (2), Shanghai (2), Palo (2), catch (2) | sanitize (2), Monterey (2), Shanghai (2), Palo (2), Bay (2), catch (2), sanctions (2), Oakland (2), surg (2), Insets (2) |
| Santa Fe (2 prompts) | Gael (1), Wyoming (1), Vermont (1), Montana (1), tavern (1) | Gael (1), Wyoming (1), Vermont (1), Montana (1), tavern (1), Albuquerque (1), senators (1), Boulder (1), mana (1), Canyon (1) |
| Santiago (5 prompts) | Antarctic (2), airspace (2), Tasmania (2), office (2), Auckland (2) | Antarctic (2), airspace (2), Tasmania (2), Ans (2), office (2), corporate (2), Auckland (2), executive (2), weekdays (2), Bangalore (2) |
| Sapporo (3 prompts) | sled (1), Wilmington (1), Spokane (1), thaw (1), counseling (1) | Aberdeen (2), Boulder (2), sled (1), Wilmington (1), Spokane (1), thaw (1), counseling (1), Asheville (1), snow (1), choked (1) |
| Sarajevo (3 prompts) | Muslims (2), Quran (2), Arabian (2), mosques (2), Muslim (1) | Quran (3), Arabs (3), Muslims (2), Arabian (2), mosques (2), Islam (2), Baghdad (2), Qur (2), Muslim (1), Islamic (1) |
| Seattle (2 prompts) | Seahawks (2), Harbor (1), Tacoma (1), seaside (1), Minnesota (1) | Seahawks (2), Harbor (1), Tacoma (1), seaside (1), Minnesota (1), Spokane (1), Brooklyn (1), Mariners (1), Yelp (1), Wisconsin (1) |
| Seoul | Shanghai, dependable, Singapore, Mitar, pooled | Shanghai, dependable, Singapore, Mitar, pooled, PIXEL, sedan, collegiate, Cavaliers, Helpers |
| Seville | Sevilla, seaside, Tucson, Ortiz, Toledo | Sevilla, seaside, Tucson, Ortiz, Toledo, Ruiz, coastal, CALLBACK, Medina, Monterey |
| Skopje | ski, skating, dia, skateboard, skiing | ski, skating, dia, skateboard, skiing, ska, Andersen, Broncos, Manitoba, Fargo |
| Sofia (3 prompts) | Sophia (3), Pavel (2), Bulg (1), Annunci (1), Yugosl (1) | Sophia (3), Pavel (2), Hollande (2), Theodore (2), Nicolas (2), Bulg (1), Annunci (1), Yugosl (1), Dmitry (1), Nico (1) |
| St. Louis | Missouri, Memphis, Arkansas, Gaines, Chattanooga | Missouri, Memphis, Arkansas, Gaines, Chattanooga, leveling, Southwest, Rex, Lambert, tomb |
| Stockholm (13 prompts) | NYC (8), Gotham (7), nightlife (6), Manhattan (6), Svens (3) | Gotham (11), NYC (10), nightlife (8), Manhattan (7), subway (7), downtown (5), Constantin (5), Svens (4), meisje (4), skys (4) |
| Sydney (2 prompts) | Sidney (1), Brooklyn (1), Dud (1), Crosby (1), Filed (1) | Sidney (2), Brooklyn (1), Dud (1), Crosby (1), Filed (1), Bronx (1), Bris (1), Liverpool (1), EIF (1), tacos (1) |
| Taipei | Wang, Cheng, Qin, Huang, Liu | Wang, Cheng, Qin, Huang, Liu, Jiang, Xin, Xia, Yuan, Zhao |
| Tallinn (4 prompts) | Eston (2), taller (2), noop (2), Seit (1), Ziel (1) | Eston (2), taller (2), noop (2), uninitialized (2), Sloven (2), Pavel (2), Slut (2), Seit (1), Ziel (1), dct (1) |
| Tashkent | Azerbai, Kuwait, shell, pers, Muslim | Azerbai, Kuwait, shell, pers, Muslim, Gaines, Abu, Bash, Abbas, delaying |
| Tbilisi (2 prompts) | manifestations (2), explicit (2), subdivisions (2), nesta (1), preached (1) | manifestations (2), explicit (2), subdivisions (2), LEFT (2), nesta (1), preached (1), ext (1), titular (1), reelection (1), Isle (1) |
| Tehran | Scient, tourist, trendy, SCI, Springer | Scient, tourist, trendy, SCI, Springer, Milano, NOI, MEP, needy, dens |
| Thessaloniki (2 prompts) | combos (2), Appalachian (1), thematic (1), remover (1), hex (1) | combos (2), Greenville (2), Appalachian (1), thematic (1), remover (1), hex (1), teamed (1), blossom (1), Yii (1), wrought (1) |
| Thimphu | ellas, explicit, uphill, campaigned, fils | ellas, explicit, uphill, campaigned, fils, Trom, tamil, Municip, besoin, filles |
| Tirana (7 prompts) | Balk (2), Alban (2), Kurdish (2), Yugosl (2), Azerbai (1) | Balk (3), Alban (2), Kurdish (2), Yugosl (2), Sean (2), Cait (2), Erdogan (2), Taj (2), Azerbai (1), Amit (1) |
| Tokyo (10 prompts) | Customs (4), NYC (2), Osaka (2), yen (2), skys (2) | Customs (4), Broadway (4), yen (3), skys (3), Samurai (3), NYC (2), Osaka (2), Metropolitan (2), sushi (2), Hiro (2) |
| Toronto (2 prompts) | NYC (2), Singapore (2), Tampa (2), subway (2), SGD (1) | NYC (2), Singapore (2), Tampa (2), subway (2), SGD (2), Spike (1), Philadelphia (1), Corinth (1), Metro (1), skys (1) |
| Toulouse | Wichita, hometown, province, CALLBACK, Sioux | Wichita, hometown, province, CALLBACK, Sioux, Thesis, Fayette, quart, Manitoba, Chester |
| Tunis | Alger, Sic, Niger, Maurit, Cannes | Alger, Sic, Niger, Maurit, Cannes, Asheville, Blanc, Pessoa, Kemp, Bordeaux |
| Turin | turb, turf, Bris, skiing, Pied | turb, turf, Bris, skiing, Pied, Wolver, pendant, Chattanooga, Fresno, Spokane |
| Ulaanbaatar (2 prompts) | Mao (1), Habitat (1), Luo (1), titular (1), Qing (1) | Mao (1), Habitat (1), Luo (1), titular (1), Qing (1), bordered (1), Tibet (1), Tamb (1), Wang (1), Kamp (1) |
| Vancouver (2 prompts) | Canucks (2), Pacific (1), harbour (1), Winnipeg (1), Newfoundland (1) | Canucks (2), Pacific (1), harbour (1), Winnipeg (1), Newfoundland (1), Seah (1), RCMP (1), Vue (1), Trudeau (1), Stanford (1) |
| Venice | Venom, Venez, UNESCO, flooding, Alps | Venom, Venez, UNESCO, flooding, Alps, Vogue, Etsy, Venus, tidal, Renaissance |
| Vienna (3 prompts) | Wien (3), NYC (2), diligence (1), Sophia (1), Congress (1) | Wien (3), NYC (2), Bureau (2), diligence (1), Sophia (1), Congress (1), Austin (1), Columbia (1), Gotham (1), Bav (1) |
| Vilnius (2 prompts) | Shanghai (2), Kyoto (1), Leipzig (1), Osaka (1), Gotham (1) | Shanghai (2), Kyoto (1), Leipzig (1), Osaka (1), Gotham (1), Nashville (1), Deutsche (1), NYC (1), Vuex (1), Riyadh (1) |
| Warsaw (8 prompts) | Scandinavian (3), Harlem (3), NYC (3), Corporate (3), lawmaker (2) | Scandinavian (4), Harlem (4), NYC (3), Corporate (3), Legisl (3), Manhattan (3), lawmaker (2), Kremlin (2), Cabinet (2), urban (2) |
| Washington (4 prompts) | presidential (3), politicians (3), government (3), Congressional (2), Congress (1) | presidential (3), politicians (3), government (3), bipartisan (3), Congressional (2), Parliament (2), Capitol (2), Secretary (2), Obama (2), Senators (2) |
| Washington, D.C. (9 prompts) | Congressional (7), Smithsonian (6), presidential (5), federal (4), USDA (3) | Congressional (7), Smithsonian (7), Maryland (6), presidential (5), federal (5), USDA (5), Capitol (5), Obama (5), FBI (3), NIH (3) |
| Wellington (9 prompts) | parliament (5), Tolkien (5), Auckland (3), Westminster (3), Parliamentary (2) | Tolkien (7), parliament (5), Auckland (4), Westminster (4), politique (3), Manhattan (3), Labour (3), Trotsky (3), Parliamentary (2), Economist (2) |
| Whitehorse (2 prompts) | Saskatchewan (2), Manitoba (2), Whites (2), Alberta (1), Prairie (1) | Saskatchewan (2), Manitoba (2), Whites (2), Alberta (2), Prairie (2), Montana (2), Fayette (2), Yuk (1), Ontario (1), Idaho (1) |
| Windhoek | councillors, windy, dicks, Voters, Midlands | councillors, windy, dicks, Voters, Midlands, deputies, gord, Bengals, isize, decking |
| Wrocław | shock, indicted, Laden, rug, blas | shock, indicted, Laden, rug, blas, Duis, samen, briefed, revoke, fused |
| Yaoundé | wann, Wein, Overwatch, imperial, Ini | wann, Wein, Overwatch, imperial, Ini, guild, lame, CFG, Baghdad, Dortmund |
| Yerevan | Kurds, quake, Assy, Auss, Bundy | Kurds, quake, Assy, Auss, Bundy, randomly, Bour, earthquake, Anaheim, Yaz |
| Zagreb (5 prompts) | teg (2), aggregator (2), NYC (2), Copyright (2), harness (2) | plano (3), teg (2), aggregator (2), NYC (2), Copyright (2), harness (2), nog (2), dat (2), Maharashtra (1), Lagos (1) |

## Product → company → CEO

### True answers (54 answers, 1332 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Albert Bourla (3 prompts) | Einstein (3), Alibaba (2), Everest (1), Nobel (1), Tian (1) | Einstein (3), Alibaba (2), Himal (2), Zhao (2), Everest (1), Nobel (1), Tian (1), ein (1), COVID (1), China (1) |
| Amedeo Felisa (26 prompts) | Raj (10), Fort (7), Hindi (5), Barcelona (4), priests (4) | Raj (14), Fort (8), priests (6), Chand (6), Salah (6), Ibn (6), Bell (6), Hindi (5), Barcelona (4), Kumar (4) |
| Antonio Neri (3 prompts) | Italian (3), Roberto (2), Spanish (1), Puerto (1), Italy (1) | Italian (3), Roberto (2), Spanish (1), Puerto (1), Italy (1), Giul (1), Portuguese (1), Francisco (1), Argentine (1), Paolo (1) |
| Arvind Krishna (21 prompts) | Hindi (8), Bollywood (7), India (6), Kolkata (5), Mumbai (4) | Bollywood (11), Hindi (10), Hindu (10), India (7), Rahul (7), Hyderabad (7), Kolkata (6), Delhi (6), Mumbai (5), Indian (5) |
| Chris Kempczinski (5 prompts) | Holiday (3), Columbus (2), Game (1), automotive (1), Chef (1) | Holiday (3), Columbus (2), spoilers (2), Dave (2), Jason (2), Game (1), automotive (1), Chef (1), Wolver (1), turbo (1) |
| Christophe De Vusser | Jesus, Christians, Crist, baptized, Bible | Jesus, Christians, Crist, baptized, Bible, biblical, Protestant, Catholics, Lutheran, church |
| Cristiano Amon | EUR, Ronaldo, Liquid, Nietzsche, Luxembourg | EUR, Ronaldo, Liquid, Nietzsche, Luxembourg, discreet, unnoticed, Putin, Snapdragon, Infos |
| Elliott Hill | Eli, EPS, shoot, Bark, rebuild | Eli, EPS, shoot, Bark, rebuild, earnings, charity, Eigen, laundering, textile |
| Elon Musk (7 prompts) | Ronaldo (5), billionaire (4), Eug (3), Vladimir (2), controversial (2) | Ronaldo (6), billionaire (6), Eug (4), Lionel (4), famous (4), controversial (3), Vladimir (3), Fame (2), Famous (2), Danny (2) |
| Gernot Döllner (35 prompts) | CRE (22), mistress (17), Madame (13), Shiv (11), Rak (8) | CRE (26), mistress (21), Madame (17), Shiv (15), Rak (15), Mikhail (12), curry (11), desi (9), Chand (7), Lionel (7) |
| Guillaume Faury (4 prompts) | French (2), Gujarat (2), Guinea (2), Marseille (2), Alexandre (2) | Guinea (3), French (2), Gujarat (2), Marseille (2), Alexandre (2), COVID (2), Pierre (2), guilt (2), Guar (1), Biden (1) |
| H. Lawrence Culp Jr. (10 prompts) | Japanese (6), Iranian (3), Tokyo (2), Persian (2), Shah (2) | Japanese (6), Iranian (4), Fuj (4), Tokyo (3), Persian (3), Ryu (3), Shah (2), Huawei (2), Tamil (2), Miy (2) |
| Håkan Samuelsson (31 prompts) | Dong (9), thickness (9), contour (8), UNESCO (8), NGO (8) | Pendant (14), UNESCO (14), thickness (13), NGO (11), contour (10), Dong (10), Fucking (8), fucking (8), clit (8), CSR (8) |
| James Quincey (2 prompts) | William (2), Kenneth (2), Thomas (2), Andrew (1), Charles (1) | William (2), Kenneth (2), Thomas (2), Robert (2), Charles (2), Edward (2), Daniel (2), Andrew (1), Anthony (1), Donald (1) |
| Jim Farley (93 prompts) | Jimmy (45), Brewers (34), Bob (33), Keystone (32), Biden (24) | Jimmy (53), Brewers (45), Keystone (43), Bob (39), Dave (39), Pete (38), Mike (32), Larry (30), Broncos (29), Biden (27) |
| John S. Chen (3 prompts) | Bloomberg (2), Brexit (1), billionaire (1), Biden (1), Chairman (1) | Bloomberg (2), Chairman (2), Brexit (1), billionaire (1), Biden (1), Wiley (1), Trump (1), Chief (1), Stephen (1), CEO (1) |
| Joseph Jimenez | Joe, Joey, FTC, retail, bamboo | Joe, Joey, FTC, retail, bamboo, weekday, Plumbing, Debt, Arrow, priced |
| Justin Hotard (189 prompts) | Bieber (174), virus (97), Tyler (97), Lincoln (95), Mac (59) | Bieber (182), Lincoln (133), virus (131), Tyler (122), Mac (113), viral (71), service (59), Phone (56), Mand (52), Sydney (52) |
| Jürgen E. Schrempp (19 prompts) | Stuttgart (6), Hein (5), supplying (4), Richard (4), Bill (4) | Stuttgart (9), Hein (7), German (6), Berlin (6), Bill (5), RBI (5), Springer (5), supplying (4), Richard (4), Robbie (4) |
| Kathy J. Warden (9 prompts) | Cathy (7), Kathleen (4), she (4), Katie (4), woman (3) | Cathy (8), she (6), Katie (5), her (5), Kathleen (4), woman (4), Kathryn (4), female (4), Sally (4), women (3) |
| Kelly Ortberg (42 prompts) | Kelley (37), Sally (12), rocket (9), Gina (8), Girl (8) | Kelley (38), Kimberly (16), Gina (15), Katie (15), Sally (14), Tiffany (14), rocket (12), Girl (12), Emily (9), Kylie (8) |
| Klaus Zellmer (23 prompts) | Munich (21), German (18), Cologne (9), Kaiser (8), Schw (7) | Munich (22), German (18), Kaiser (14), Schw (14), Cologne (12), BMW (9), mayor (9), Hamburg (8), Fle (7), Georges (6) |
| Kōji Seto (107 prompts) | Svens (43), bey (37), dignity (21), palms (20), Otto (17) | Svens (52), bey (44), palms (32), dignity (27), Otto (26), CES (25), Jens (24), Munich (24), marches (22), Japanese (19) |
| Lee Jae-yong (101 prompts) | Korean (76), Japanese (54), Taiwanese (41), Chung (34), Lloyd (25) | Korean (79), Japanese (65), Chung (59), Taiwanese (50), Lloyd (42), Seoul (38), Huang (36), amid (35), Shen (32), Choi (31) |
| Makoto Uchida (66 prompts) | Maker (50), Nak (36), Lage (28), Resets (27), Japanese (19) | Maker (54), Nak (43), Lage (34), Resets (32), Hindered (24), Japanese (22), Biden (17), Yas (17), Yok (17), Tokyo (16) |
| Martin Sion (3 prompts) | Frankfurt (1), Edinburgh (1), lam (1), London (1), Martian (1) | Frankfurt (2), Deutsche (2), Leeds (2), Edinburgh (1), lam (1), London (1), Martian (1), Berlin (1), Alpine (1), Matthias (1) |
| Mary Barra (164 prompts) | woman (127), actress (96), feminist (84), female (77), women (74) | actress (136), woman (130), feminist (130), female (115), heroine (99), Women (84), lady (83), Girl (80), women (74), girl (69) |
| Michael Manley | Miche, David, Mike, microwave, Schw | Miche, David, Mike, microwave, Schw, Ober, Jeffrey, Ludwig, Deutsche, Mik |
| Michel Doukeris (2 prompts) | Belgian (1), French (1), Maurit (1), France (1), Xiaomi (1) | Belgian (1), French (1), Maurit (1), France (1), Xiaomi (1), Italian (1), Picasso (1), Pierre (1), Rodr (1), Quebec (1) |
| Miguel Ángel López Borrego (2 prompts) | Spanish (2), Juan (2), Santiago (1), Ecuador (1), Jorge (1) | Spanish (2), Juan (2), Ecuador (2), Santiago (1), Jorge (1), Gonz (1), Rafael (1), Madrid (1), Javier (1), Spain (1) |
| Morten Wierod (3 prompts) | mortality (3), mortgage (2), deaths (2), railroad (1), Danish (1) | mortality (3), mortgage (2), deaths (2), railroad (2), Mason (2), Danish (1), death (1), Norwegian (1), morality (1), banco (1) |
| Ola Källenius (58 prompts) | Serbia (28), Slovakia (27), European (21), Austria (18), Slovenia (14) | Slovakia (40), Serbia (38), Austria (31), European (24), Slovenia (22), Czech (16), VAT (15), Scandin (14), until (13), warp (12) |
| Oliver Blume (85 prompts) | Olivier (71), Brexit (27), German (19), Serbia (18), Oliveira (18) | Olivier (74), Brexit (46), Oliveira (31), Voll (30), Bundesliga (30), Overwatch (29), Deutschland (27), German (23), Nunes (21), OLED (21) |
| Patrice Caine | Patricia, patron, Patent, paternal, Patton | Patricia, patron, Patent, paternal, Patton, patience, Paulo, Serg, kindergarten, Georges |
| Peter Herweck | Dutch, Rotterdam, Bibli, Bav, Petra | Dutch, Rotterdam, Bibli, Bav, Petra, Munich, Austrian, Zust, Danish, Yugosl |
| Petr Novotný (8 prompts) | Slovak (5), Czech (4), pets (4), Polish (4), petition (3) | Czech (5), Slovak (5), pets (5), Polish (5), Sloven (5), Warsaw (5), Prague (4), petition (3), Ukrainian (3), Poland (3) |
| Ramon Laguarta | India, Hindi, Kumar, Ramirez, Rajasthan | India, Hindi, Kumar, Ramirez, Rajasthan, Rams, desi, raj, Tamil, Chennai |
| Raymond van Eck | rays, Raleigh, money, ang, mon | rays, Raleigh, money, ang, mon, chicken, payment, Willie, Arthur, consciousness |
| Roland Busch (10 prompts) | Wolfgang (8), Zurich (6), Roll (4), Munich (4), Florian (4) | Wolfgang (8), Zurich (7), Florian (6), Roll (5), Munich (5), Ober (5), Stuttgart (4), Ernst (4), Ronald (4), roll (3) |
| Satya Nadella (22 prompts) | COVID (10), Narendra (10), India (9), saturation (9), Biden (8) | Narendra (16), India (12), COVID (11), saturation (10), Biden (8), Zuckerberg (6), Rahul (6), GDPR (6), Brexit (5), satellites (5) |
| Scott Ernest (16 prompts) | Doyle (7), darling (5), aisle (4), FAA (4), Brett (4) | Doyle (10), Brett (9), darling (5), aisle (5), Lauderdale (5), FAA (4), Scots (4), dct (4), Fayette (4), Skywalker (4) |
| Shuntaro Furukawa (36 prompts) | Mario (15), Miy (14), manga (10), Yoshi (10), Japanese (9) | Mario (20), Miy (19), Yoshi (17), manga (13), Japanese (12), Naruto (9), Tokyo (9), Pikachu (8), Osaka (8), Satoshi (8) |
| Sundar Pichai (13 prompts) | Sunder (11), Narendra (8), Tamil (8), Chennai (7), Gujarat (6) | Sunder (13), Narendra (11), Tamil (9), Gujarat (9), Chennai (9), Rahul (4), Oprah (3), Gujar (3), Kerala (3), Kann (3) |
| Takehiko Kakiuchi (15 prompts) | Takes (9), Japanese (7), takeaway (6), Tokyo (6), Hiro (6) | Takes (10), Tokyo (8), Japanese (7), takeaway (7), Hiro (7), Miy (6), Kyoto (6), Osaka (5), takeover (5), Yosh (5) |
| Tim Cook (40 prompts) | timed (29), timely (19), timing (15), timers (13), Timothy (11) | timed (32), timely (27), timetable (21), timing (17), timers (17), CEO (14), Timothy (14), billionaire (12), Barack (11), shareholders (10) |
| Tobias Moers (3 prompts) | Vere (2), pien (2), fuck (1), collaboration (1), irreversible (1) | fuck (2), Vere (2), pien (2), whistle (2), recommendations (2), collaboration (1), irreversible (1), standings (1), hoof (1), Toby (1) |
| Tomáš Ignačák | tomatoes, Tomas, Tome, Thom, Tomb | tomatoes, Tomas, Tome, Thom, Tomb, Tommy, Kathryn, confession, Boston, cis |
| Tufan Erginbilgiç (7 prompts) | Sofia (3), Kylie (3), Japanese (2), generous (2), adorable (2) | Sofia (5), Kylie (4), adorable (4), Juliet (4), Fiona (3), Japanese (2), generous (2), Tokyo (2), her (2), granddaughter (2) |
| Ville Jaakonsalo (3 prompts) | Canadian (3), French (2), glide (1), France (1), Russian (1) | Canadian (3), French (2), Brazilian (2), glide (1), France (1), Russian (1), Koreans (1), CST (1), Italian (1), wilderness (1) |
| Vimal Kapur (3 prompts) | Vij (1), Soviet (1), Italian (1), Tamil (1), Russian (1) | Vish (2), Croatian (2), Vij (1), Soviet (1), Italian (1), Tamil (1), Russian (1), Italy (1), Raj (1), USSR (1) |
| Wayne Griffiths (20 prompts) | Oakland (8), Biden (7), Lisa (7), Denver (5), Debbie (5) | Oakland (11), Lisa (10), Biden (9), Debbie (9), Megan (9), Willie (8), Bucks (7), Denver (6), Travis (6), Meghan (6) |
| Yōichi Kise | Korean, yen, Yun, Seoul, Jiang | Korean, yen, Yun, Seoul, Jiang, Choi, Chung, Yuk, Yuan, Yan |
| Éric Martel | French, France, Pierre, Alexandre, Jean | French, France, Pierre, Alexandre, Jean, Antoine, Philippe, Quebec, Georges, Paris |
| Éric Trappier (8 prompts) | Pierre (4), Bermuda (3), adamant (3), Quebec (3), French (3) | Pierre (4), Bermuda (3), adamant (3), Quebec (3), French (3), favour (3), Alexandre (3), fatally (3), Antoine (3), TCHAR (3) |

### Model answers (66 answers, 1043 prompts)

| Answer | Top 5 | Top 10 |
|---|---|---|
| Akio Toyoda (66 prompts) | Bir (38), Ary (26), risking (15), Rit (14), aku (13) | Bir (48), Ary (30), aku (27), Abyss (26), risking (24), INTERRU (23), Rit (22), himself (15), raging (15), Deadly (15) |
| Albert Bourla | Einstein, Alibaba, Tian, China, Beijing | Einstein, Alibaba, Tian, China, Beijing, Himal, Zhao, Duterte, yuan, Laos |
| Amedeo Felisa (11 prompts) | Italians (3), Banc (2), Affero (2), aforementioned (2), thankful (2) | Affero (4), Italians (3), Banc (2), aforementioned (2), thankful (2), Uzbek (2), ext (2), Italy (2), Xxx (2), Andr (2) |
| Andy Palmer (6 prompts) | Pete (5), Dave (4), Mike (4), Gregg (4), favourite (2) | Pete (6), Mike (6), Dave (5), Gregg (5), Jerry (5), Roger (4), Jimmy (4), favourite (3), programme (2), Guinness (2) |
| Arvind Krishna (20 prompts) | reb (3), quotient (3), redd (3), Fehler (3), India (2) | drama (4), reb (3), quotient (3), redd (3), Fehler (3), Julius (3), Hyderabad (3), India (2), genius (2), IDX (2) |
| Bill Ford (10 prompts) | Johannes (6), Caucus (4), Levine (4), friend (3), voucher (3) | friend (10), Johannes (7), Caucus (7), voucher (5), Levine (5), somewhere (5), purse (5), Pierre (3), BASIS (3), Clintons (3) |
| Bill Gates (2 prompts) | Buffett (2), CEO (1), William (1), President (1), Cosby (1) | Buffett (2), Cosby (2), President (2), SCI (2), Rockefeller (2), CEO (1), William (1), Oprah (1), Louis (1), Nobel (1) |
| Carlos Ghosn (7 prompts) | Renault (7), Argentina (7), Spain (6), Aires (4), Buenos (4) | Renault (7), Argentina (7), Spain (7), Venezuelan (7), Aires (6), Buenos (5), NAFTA (5), Grupo (4), Spanish (3), Yugoslavia (2) |
| Chris Kempczinski | railroad, railways, Roads, highways, Asphalt | railroad, railways, Roads, highways, Asphalt, Gand, Chiefs, Boris, Rhodes, Salisbury |
| Dieter Zetsche (10 prompts) | Occupy (5), holdings (5), Diary (4), diag (3), diagonal (3) | Occupy (8), holdings (7), Diary (5), diabetic (4), diag (3), diagonal (3), himself (3), investor (3), Claus (3), unarmed (3) |
| DJ Koh (20 prompts) | rapper (20), Kanye (14), NFL (12), Spotify (8), Oculus (6) | rapper (20), Kanye (16), NFL (15), Spotify (10), musician (9), Huffington (8), ISIS (8), hip (8), Thrones (7), Oculus (6) |
| Elon Musk (5 prompts) | Ronaldo (5), billionaire (4), Eug (3), controversial (2), Famous (2) | Ronaldo (5), billionaire (5), Eug (4), controversial (3), famous (3), Lionel (3), Fame (2), Famous (2), Celebrity (2), Vladimir (2) |
| Ferdinand Piëch (5 prompts) | Baron (5), Nobel (4), Adolf (3), Yugosl (3), Automobile (2) | Baron (5), Adolf (5), Nobel (4), Yugosl (4), Austrian (3), Automobile (2), famously (2), famous (2), Chairman (2), renowned (2) |
| Gernot Döllner (44 prompts) | Compare (8), Manor (5), aforementioned (4), Durant (4), Muk (4) | Compare (8), Durant (7), Manor (5), Muk (5), tongues (5), Bulgarian (5), Ferrari (5), Uzbek (5), polished (5), aforementioned (4) |
| Guillaume Faury (2 prompts) | Hollande (1), Gujarat (1), intl (1), Biden (1), Italia (1) | Hollande (1), Gujarat (1), intl (1), Biden (1), Italia (1), Guinea (1), France (1), COVID (1), germany (1), Earlier (1) |
| H. Lawrence Culp Jr. (4 prompts) | aforementioned (2), HOUR (2), Affero (2), Herz (1), hrs (1) | Affero (3), unearth (3), aforementioned (2), HOUR (2), Herz (2), hrs (1), ERROR (1), Depths (1), Txt (1), aud (1) |
| Herbert Diess (28 prompts) | Dutch (14), Stanley (10), COVID (8), inaugur (8), Dortmund (7) | Dutch (16), inaugur (14), Stanley (11), Dortmund (11), patriarch (10), COVID (9), Hera (8), Archbishop (8), Voor (8), German (8) |
| Hiroto Saikawa (15 prompts) | nonatomic (11), raj (9), Bihar (7), Bengal (6), Reich (6) | nonatomic (13), raj (12), Reich (9), Mitar (9), Bengal (8), Bihar (8), rex (7), Gund (7), Sith (6), Dresden (6) |
| Håkan Samuelsson (21 prompts) | fucking (5), clit (4), thickness (4), Pendant (3), contour (3) | clit (7), thickness (5), fucking (5), Pendant (4), contour (4), UNESCO (4), aluminum (4), fucks (4), eth (4), Frau (3) |
| James Quincey (2 prompts) | Jehovah (1), canyon (1), telegram (1), USDA (1), PARAM (1) | Jehovah (1), canyon (1), telegram (1), USDA (1), PARAM (1), Pulitzer (1), Maison (1), Huffman (1), Rohingya (1), Cherokee (1) |
| Jim Farley (108 prompts) | Minecraft (33), Biden (20), Fargo (19), Keystone (19), NASCAR (12) | Minecraft (40), Keystone (28), Biden (27), Fargo (23), Ryzen (15), Brewers (14), Emoji (14), NASCAR (13), clubhouse (13), boys (13) |
| Jim Rowan (6 prompts) | Jimmy (6), Biden (5), Cody (2), Wyoming (2), Huffman (2) | Jimmy (6), Biden (6), Larry (4), Cody (3), Wyoming (3), Joe (3), Huffman (3), Bob (3), Josh (3), Huff (2) |
| John DeLorean (5 prompts) | Wiley (4), Blackburn (4), Knox (2), Matthews (2), Charles (1) | Wiley (5), Blackburn (4), Matthews (3), Knox (2), Hutchinson (2), Raleigh (2), Burke (2), Stephens (2), Charles (1), Wildcats (1) |
| John S. Chen (2 prompts) | William (1), reveal (1), Donald (1), mph (1), Thatcher (1) | William (1), reveal (1), Donald (1), mph (1), Thatcher (1), BBC (1), typed (1), Tide (1), Billy (1), STRUCT (1) |
| Jorma Ollila (36 prompts) | shareholder (19), Kop (13), Tattoo (11), Elias (8), reclaimed (8) | shareholder (21), Kop (20), Tattoo (15), Elias (12), reclaimed (12), nipple (11), inhibit (11), rip (10), Jaguar (10), Desktop (9) |
| Justin Hotard (38 prompts) | Denied (5), infected (5), explanations (5), help (4), Kodi (4) | infected (10), Denied (7), pistol (7), Kodi (6), help (6), explanations (6), Bieber (6), Django (6), Escort (6), Cleanup (6) |
| Jürgen E. Schrempp (24 prompts) | Trom (5), reclaimed (4), Duis (3), ext (2), rip (2) | Trom (6), reclaimed (4), Duis (3), curves (3), stret (3), splitted (3), pien (3), cli (3), ext (2), rip (2) |
| Kelly Ortberg (9 prompts) | Kelley (4), girls (3), Sisters (2), recommendations (2), woman (2) | Kelley (5), Granny (4), girls (3), printable (3), Sisters (2), recommendations (2), woman (2), GIS (2), aerial (2), glacier (2) |
| Klaus Zellmer (8 prompts) | Istanbul (4), Munich (3), ort (3), German (2), Esk (2) | Istanbul (5), Munich (3), Esk (3), ort (3), Cameroon (3), German (2), Hamburg (2), Coral (2), spat (2), Cairo (2) |
| Kōji Seto (35 prompts) | Osaka (8), japanese (7), Kou (5), Tokyo (5), Kyoto (5) | Osaka (9), Yosh (8), japanese (7), Kou (7), Tokyo (7), Kyoto (6), Scandinavian (5), Kohana (4), Suzuki (4), Hiro (4) |
| Lawrence Stroll (6 prompts) | Honda (3), Fame (3), boca (3), Bose (2), veniam (2) | campos (6), Fame (4), Pasta (4), Honda (3), boca (3), Affero (3), Barbie (3), Laure (3), Bose (2), veniam (2) |
| Lee Jae-yong (6 prompts) | Choi (2), Zhao (2), Luo (2), Oliveira (2), revenge (2) | Choi (4), Zhang (4), Luo (3), revenge (3), Zhao (2), Oliveira (2), Korean (2), Amid (2), Taiwan (2), businessmen (2) |
| Makoto Uchida (17 prompts) | PROGMEM (4), Japanese (3), Biden (3), manga (3), Osaka (3) | PROGMEM (4), Biden (4), manga (4), Playlist (4), ink (4), Japanese (3), Osaka (3), Invent (3), Lage (3), soaked (3) |
| Mark Fields (14 prompts) | marque (8), marc (7), Derrick (5), Stafford (4), Pens (4) | marque (8), marc (7), Derrick (5), Pens (5), Stafford (4), equiv (4), Newport (3), leadership (3), Holt (3), Indianapolis (3) |
| Mark Reuss (17 prompts) | Derrick (15), marc (7), Holt (6), Auburn (4), Sherman (3) | Derrick (15), Holt (9), Newport (9), marc (7), Auburn (7), Sherman (5), precinct (4), Hayden (4), hoodie (4), embar (4) |
| Markus Duesmann (10 prompts) | GFX (10), Messi (6), LGBTQ (5), Fortnite (4), Vulkan (4) | GFX (10), Messi (9), Vulkan (9), Fortnite (8), Zak (7), LGBTQ (6), COVID (5), optimized (5), predefined (5), Blockchain (3) |
| Martin Sion (2 prompts) | Tecn (1), Chennai (1), Munich (1), mainland (1), monster (1) | Tecn (1), Chennai (1), Munich (1), mainland (1), monster (1), Tahoe (1), Hamburg (1), Tup (1), Projekt (1), Burma (1) |
| Mary Barra (66 prompts) | Women (23), woman (22), women (17), actress (14), girl (14) | woman (29), Women (27), actress (26), heroine (24), girl (21), feminist (21), women (17), lady (16), female (13), Aunt (11) |
| Michael Manley | Miche, Perl, Lucifer, uid, STDERR | Miche, Perl, Lucifer, uid, STDERR, Rockefeller, PYTHON, NYPD, Norton, Reagan |
| Morten Wierod | mortality, Danish, Norwegian, Denmark, Nordic | mortality, Danish, Norwegian, Denmark, Nordic, Swedish, Norway, Svens, Anders, Estonia |
| Ola Källenius (43 prompts) | GDPR (6), Uzbek (5), tres (5), hugged (4), European (4) | GDPR (8), tres (7), Uzbek (6), hugged (6), warp (6), European (6), Sphere (6), mine (6), perfection (5), Ukrainian (5) |
| Oliver Blume (57 prompts) | Olivier (18), Oversight (15), Nunes (12), Camden (7), TYPO (7) | Olivier (22), Oversight (16), Nunes (16), Oliveira (14), Camden (9), Spicer (8), Outs (8), Voll (8), Stefan (8), Scaffold (8) |
| Pekka Lundmark (11 prompts) | COVID (8), Woman (8), Diana (7), Tik (6), she (4) | Woman (11), Diana (10), COVID (9), Tik (8), herself (7), Sonia (7), Biden (6), LGBTQ (6), SPDX (6), she (5) |
| Peter Herweck | Oro, Gujarat, Tantra, Sadd, Skywalker | Oro, Gujarat, Tantra, Sadd, Skywalker, Shib, Persian, Mandal, Locale, fellowship |
| Petr Novotný | envoy, Barang, Nagar, Fiscal, Oilers | envoy, Barang, Nagar, Fiscal, Oilers, Personnel, Beverage, STDMETHODCALLTYPE, Matte, Defensive |
| Rajeev Suri (58 prompts) | racked (33), ext (26), dues (19), India (18), Naj (18) | racked (42), Naj (35), ext (32), dues (27), alternatively (25), India (23), Hyderabad (22), Obama (21), fares (20), Kumar (20) |
| Reggie Fils-Aime (4 prompts) | Mayweather (3), WWE (2), Obama (2), Huffington (2), Barack (1) | Mayweather (3), WWE (3), Obama (3), Huffington (2), Rihanna (2), hoodie (2), Barack (1), stickers (1), Willie (1), Zelda (1) |
| Risto Siilasmaa (18 prompts) | Plains (15), Morr (12), skiing (11), sod (8), Vet (7) | Plains (17), skiing (15), Morr (14), sod (14), Cra (10), Vet (9), Vladimir (7), Pierre (6), BORDER (6), bells (5) |
| Roland Busch (4 prompts) | Grat (2), Christoph (1), Motorola (1), CAD (1), RFC (1) | Grat (2), Christoph (1), Motorola (1), CAD (1), RFC (1), Leipzig (1), Tulsa (1), iso (1), retired (1), Zurich (1) |
| Rupert Stadler (10 prompts) | Thatcher (3), AOL (3), Yugosl (3), vois (3), WHATSOEVER (2) | Thatcher (6), Russell (6), AOL (5), Burb (4), Yugosl (4), rat (4), vois (3), Newark (3), influences (3), Austrian (3) |
| Satya Nadella (7 prompts) | COVID (4), Amazon (3), GDPR (2), redundant (2), India (2) | COVID (5), Amazon (3), GDPR (3), Azure (3), Biden (3), redundant (2), India (2), Sharma (2), redundancy (2), Chennai (2) |
| Scott Ernest | Roberto, Spotify, Rahul, Alberto, superstar | Roberto, Spotify, Rahul, Alberto, superstar, Skate, Sebastian, himself, Bowie, tweeted |
| Shigeru Miyamoto (4 prompts) | Japanese (3), Tokyo (2), Osaka (2), manga (1), toilet (1) | Japanese (3), Tokyo (3), Osaka (2), manga (2), Kyoto (2), Yosh (2), Fuji (2), Shib (2), Hiro (2), prefect (2) |
| Shiro Nakamura (4 prompts) | Japanese (2), Fuj (2), Suzuki (2), Krish (2), Fuji (2) | Japanese (2), Fuj (2), Suzuki (2), Krish (2), Fuji (2), yen (2), Yok (2), Fuk (2), Modi (1), cellular (1) |
| Shuntaro Furukawa (13 prompts) | Tik (4), sovereignty (3), COVID (3), Satoshi (3), Japanese (2) | Tik (4), named (4), sovereignty (3), COVID (3), Satoshi (3), Biden (3), Czech (3), sovereign (3), Japanese (2), Tokyo (2) |
| Stephen Elop (14 prompts) | Obama (13), Oprah (13), Barack (12), Colbert (12), HTC (5) | Colbert (14), Obama (13), Oprah (13), Barack (13), Zucker (10), pope (8), HTC (7), Stephan (6), Steven (6), Kinect (6) |
| Steve Ballmer | Obama, Barack, businessmen, Occupy, unemployed | Obama, Barack, businessmen, Occupy, unemployed, Kanye, douche, Willie, Spielberg, Wii |
| Steve Jobs (10 prompts) | Stein (5), Sheldon (4), Nobel (3), extremists (3), protests (3) | Stein (6), extremists (5), protests (5), Sheldon (4), Nobel (4), Adolf (4), celebrities (4), Nazis (4), Holocaust (3), Spielberg (3) |
| Sundar Pichai (8 prompts) | Sunder (6), Tamil (5), Narendra (5), Gujarat (3), desi (2) | Sunder (8), Tamil (5), Narendra (5), Gujarat (5), Kerala (4), Chennai (4), desi (4), India (4), Rahul (4), Vish (3) |
| Takehiko Kakiuchi (5 prompts) | Kyoto (2), Prepare (2), Arrange (2), Yas (1), redes (1) | Kyoto (2), Prepare (2), Arrange (2), Proposed (2), japanese (2), Tokyo (2), Osaka (2), Tanz (2), FOREIGN (2), Yas (1) |
| Tetsuya Tada (4 prompts) | Tokyo (2), sama (2), Miy (2), Yosh (2), heights (1) | Miy (3), Tokyo (3), Yosh (3), manga (3), sama (2), yen (2), Carlo (2), Yun (2), heights (1), Kas (1) |
| Tim Cook (37 prompts) | timed (22), timely (17), Timothy (8), timings (8), CEO (6) | timed (25), timely (21), timings (12), timetable (12), Timothy (10), timers (10), billionaire (10), CEO (8), reins (8), timing (7) |
| TM Roh (18 prompts) | TPM (16), Tik (12), Biden (12), BJP (7), Covid (6) | TPM (18), Biden (14), Tik (14), BJP (12), Mahar (11), Kotlin (10), BFS (10), Covid (9), Dort (9), Emoji (8) |
| Tufan Erginbilgiç (3 prompts) | Hiro (1), Dud (1), Uzbek (1), Perez (1), Torrent (1) | Hiro (1), Dud (1), Uzbek (1), Perez (1), Torrent (1), Kurdish (1), Rao (1), Typeface (1), Nodo (1), Sug (1) |
| Wayne Griffiths (8 prompts) | Nashville (3), Tampa (3), Oilers (3), Havana (2), Campbell (2) | Nashville (6), Tampa (4), Oilers (4), Lauderdale (3), Havana (2), Campbell (2), Oslo (2), Detroit (2), Bradford (2), Pittsburgh (2) |
| Young Sohn (8 prompts) | Hung (7), dang (4), youthful (3), nerd (3), Shoe (3) | Hung (7), dang (6), youthful (4), Shoe (4), puzzled (4), nerd (3), Yup (3), Kids (3), Cute (3), Babies (3) |

