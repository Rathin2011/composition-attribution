**OLMo 3 Stage-One: Spanish–Antonym Shortcut and Ambiguous Queries**

All queries were answered correctly. Composition has RR ≥ 0.5; shortcut candidates have RR ≤ 0.2; values between the thresholds are ambiguous.

**Part 1: Queries and In-Context Examples**

**Shortcut candidates (5)**

- **Query 391 — Context:** secret → público | sham → genuino | cooling → calefacción | tiny → gigante | affirm → negar | brief → largo | brave → cobarde | healthy → insalubres | soil → cielo | ugly → hermosa || **Final:** inquiry → respuesta

- **Query 409 — Context:** evil → bien. | better → peor | newborn → personas | eastern → occidental | grant → negar | untrue → verdadero | humid → seco | leader → seguidor | simultaneous → consecutiva | prefix → sufijo || **Final:** deprive → proporcionar

- **Query 1268 — Context:** timid → negrita | comparative → superlativo | extra → falta | total → parcial | intentional → accidental | authorized → no | have → falta | inside → exterior | generate → consumir | studio → ubicación || **Final:** steady → inestable

- **Query 1674 — Context:** unmarried → casadas | unsuccessful → con | begin → fin | favorable → desfavorable | identical → diferentes | material → inmaterial | damp → seco | double → solo | park → inicio | close → lejos || **Final:** kickoff → final

- **Query 1901 — Context:** dependent → independiente | odd → incluso | judicial → extrajudicial | complete → incompleto | raise → inferior | worn → nuevo | favorite → menos | winner → perdedor | woman → hombre | inspire → desincentivar || **Final:** know → ignorar

**Ambiguous (16)**

- **Query 190 — Context:** tolerance → intolerancia | irresponsible → responsable | match → desajuste | credible → ¡increíble! | difference → similitud | lie → verdad | decline → aumento | downstream → aguas | disrespect → respeto | doubt → seguridad || **Final:** affirm → negar

- **Query 194 — Context:** lock → desbloquear | distance → proximidad | alternative → mainstream | tender → duro | center → borde | paternal → maternal | suspect → confirmar | inferior → superior | departure → llegada | supernatural → natural || **Final:** medium → grande

- **Query 294 — Context:** involve → excluir | veto → aprobar | idle → ocupado | obese → flacas | same → diferentes | elementary → avanzado | unfortunate → afortunado. | premature → maduro | infinite → finito | tail → cabeza || **Final:** steep → plano

- **Query 544 — Context:** neoliberal → conservador | weighted → sin | catch → liberación | bourgeois → proletario | transient → permanente | savage → civilizado | physical → mental | imperfect → perfecto | hooked → desenganchado | affirm → negar || **Final:** show → ocultar

- **Query 659 — Context:** servicing → desatender | rising → caída | draft → final | assure → duda | keen → apático | authorized → no | blue → rojo | intermittent → continuo | front → atrás | unmanned → tripuladas || **Final:** align → desalinear

- **Query 860 — Context:** balance → desequilibrio | hideous → hermosa | day → noche | ruin → conservar | patient → impaciente | inspiration → desesperación | primitive → avanzado | insignificant → significativa | elevation → depresión | visionary → práctico || **Final:** regression → progresión

- **Query 921 — Context:** hell → cielo | niece → sobrino | solution → problema | minute → hora | wise → tonto. | viewing → ignorando | chill → calor | height → profundidad | friend → enemigo | elder → más || **Final:** front → atrás

- **Query 1022 — Context:** buy → vender | right → mal. | resilient → frágil | dubious → ciertos | keep → descarte | swift → sluggish | tame → salvaje | utopian → distópico | obscurity → prominencia | vague → específico || **Final:** serious → gracioso

- **Query 1105 — Context:** ally → enemigo | enlarged → encogido | rapid → lento | mature → inmaduro | swift → sluggish | cold → tibio | climb → descendiendo | software → hardware | rise → caída | necessary → innecesario || **Final:** fix → romper

- **Query 1255 — Context:** strict → indulgente | sad → feliz | mad → sano | destroy → crear | furious → calma | huge → diminuta | legal → ilegal | mature → inmaduro | adjective → sustantivo | halt → proceder || **Final:** mourn → celebrar

- **Query 1260 — Context:** diluted → concentrado | accumulate → disipato | isolated → conectado | break → arreglar | enforce → derogación | cash → crédito | maximal → mínimo | forward → hacia | knowledge → ignorancia | unfavorable → favorable || **Final:** dull → brillante

- **Query 1515 — Context:** incur → crédito | corporate → individual | centrist → extremista | varied → uniforme | dissatisfaction → satisfacción | damp → seco | simplistic → complejo | freedom → opresión | sink → flotar | inferior → superior || **Final:** exacerbate → aliviar

- **Query 1879 — Context:** damp → seco | corrupt → honesto | grey → colorido | kid → adulto | root → tip | visible → invisible | denial → aceptación | binary → analógico | leftist → derechista | invent → destruir || **Final:** query → respuesta

- **Query 2046 — Context:** inquiry → respuesta | unknown → conocidos | delete → guardar | melody → discordia | consumer → productor | rim → centro | perceive → ignorar | super → inferior | beautiful → feo | complexity → simplicidad || **Final:** proceed → detener

- **Query 1968 — Context:** launch → tierra | infrared → ultravioleta | rapid → lento | masculine → femenina | beneficial → nocivo | qualitative → cuantitativa | solder → desoldador | unsafe → seguro | object → asunto | achievable → inalcanzable || **Final:** permit → prohibir

- **Query 2222 — Context:** attract → repel | local → extranjero | appear → desaparecer | unsuccessful → con | susceptibility → resistencia | unusual → habitual | like → disgusto | elder → más | unhealthy → saludable | aggregate → dispersar || **Final:** cause → efecto

**Part 2: Strongest Logit-Lens Evidence**

Layers are zero-indexed. The path is the stronger of the two candidate intermediates, even when its evidence is weak or ambiguous.

**Shortcut candidates (5)**

- **Query 391:** inquiry → respuesta | **Path:** English → English antonym → Spanish | **English antonym f(x):** response | **Highest RR:** 0.125 | **Peak layer(s):** 25, 26, 27

- **Query 409:** deprive → proporcionar | **Path:** English → English antonym → Spanish | **English antonym f(x):** provide | **Highest RR:** 0.037037 | **Peak layer(s):** 28

- **Query 1268:** steady → inestable | **Path:** English → Spanish translation → Spanish antonym | **Spanish translation g(x):** estacionario | **Highest RR:** 0.0909091 | **Peak layer(s):** 31

- **Query 1674:** kickoff → final | **Path:** English → Spanish translation → Spanish antonym | **Spanish translation g(x):** arranque | **Highest RR:** 0.142857 | **Peak layer(s):** 30

- **Query 1901:** know → ignorar | **Path:** English → Spanish translation → Spanish antonym | **Spanish translation g(x):** saber | **Highest RR:** 0.142857 | **Peak layer(s):** 30

**Ambiguous (16)**

- **Query 190:** affirm → negar | **Path:** English → English antonym → Spanish | **English antonym f(x):** deny | **Highest RR:** 0.333333 | **Peak layer(s):** 20, 24, 25, 26

- **Query 194:** medium → grande | **Path:** English → English antonym → Spanish | **English antonym f(x):** large | **Highest RR:** 0.333333 | **Peak layer(s):** 29

- **Query 294:** steep → plano | **Path:** English → English antonym → Spanish | **English antonym f(x):** flat | **Highest RR:** 0.25 | **Peak layer(s):** 26, 27

- **Query 544:** show → ocultar | **Path:** English → English antonym → Spanish | **English antonym f(x):** hide | **Highest RR:** 0.25 | **Peak layer(s):** 26, 29

- **Query 659:** align → desalinear | **Path:** English → English antonym → Spanish | **English antonym f(x):** misalign | **Highest RR:** 0.333333 | **Peak layer(s):** 25

- **Query 860:** regression → progresión | **Path:** English → English antonym → Spanish | **English antonym f(x):** progression | **Highest RR:** 0.333333 | **Peak layer(s):** 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29

- **Query 921:** front → atrás | **Path:** English → English antonym → Spanish | **English antonym f(x):** back | **Highest RR:** 0.25 | **Peak layer(s):** 23, 24, 25, 26, 27, 29

- **Query 1022:** serious → gracioso | **Path:** English → English antonym → Spanish | **English antonym f(x):** funny | **Highest RR:** 0.333333 | **Peak layer(s):** 27

- **Query 1105:** fix → romper | **Path:** English → English antonym → Spanish | **English antonym f(x):** break | **Highest RR:** 0.333333 | **Peak layer(s):** 29, 30, 31

- **Query 1255:** mourn → celebrar | **Path:** English → English antonym → Spanish | **English antonym f(x):** celebrate | **Highest RR:** 0.25 | **Peak layer(s):** 27

- **Query 1260:** dull → brillante | **Path:** English → English antonym → Spanish | **English antonym f(x):** bright | **Highest RR:** 0.333333 | **Peak layer(s):** 23

- **Query 1515:** exacerbate → aliviar | **Path:** English → English antonym → Spanish | **English antonym f(x):** alleviate | **Highest RR:** 0.333333 | **Peak layer(s):** 24, 25, 26, 27

- **Query 1879:** query → respuesta | **Path:** English → English antonym → Spanish | **English antonym f(x):** response | **Highest RR:** 0.333333 | **Peak layer(s):** 26, 27, 28, 29

- **Query 2046:** proceed → detener | **Path:** English → English antonym → Spanish | **English antonym f(x):** halt | **Highest RR:** 0.333333 | **Peak layer(s):** 23, 24, 25, 26, 27

- **Query 1968:** permit → prohibir | **Path:** English → Spanish translation → Spanish antonym | **Spanish translation g(x):** permiso | **Highest RR:** 0.333333 | **Peak layer(s):** 29

- **Query 2222:** cause → efecto | **Path:** English → Spanish translation → Spanish antonym | **Spanish translation g(x):** causa | **Highest RR:** 0.333333 | **Peak layer(s):** 31
