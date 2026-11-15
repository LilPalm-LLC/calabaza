"""100 high-frequency Mexican Spanish verbs, five in each practice batch."""
import re

VERBS = [
  {
    "id": "v001",
    "infinitive": "ser",
    "english": "to be (identity)",
    "batch_number": 1,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v002",
    "infinitive": "estar",
    "english": "to be (state or location)",
    "batch_number": 1,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v003",
    "infinitive": "ir",
    "english": "to go",
    "batch_number": 1,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v004",
    "infinitive": "hacer",
    "english": "to do / make",
    "batch_number": 1,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v005",
    "infinitive": "decir",
    "english": "to say / tell",
    "batch_number": 1,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v006",
    "infinitive": "poder",
    "english": "can / to be able",
    "batch_number": 2,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v007",
    "infinitive": "querer",
    "english": "to want / love",
    "batch_number": 2,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v008",
    "infinitive": "venir",
    "english": "to come",
    "batch_number": 2,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v009",
    "infinitive": "ver",
    "english": "to see",
    "batch_number": 2,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v010",
    "infinitive": "dar",
    "english": "to give",
    "batch_number": 2,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v011",
    "infinitive": "saber",
    "english": "to know (a fact)",
    "batch_number": 3,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v012",
    "infinitive": "conocer",
    "english": "to know / meet (people, places)",
    "batch_number": 3,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v013",
    "infinitive": "poner",
    "english": "to put",
    "batch_number": 3,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v014",
    "infinitive": "salir",
    "english": "to leave / go out",
    "batch_number": 3,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v015",
    "infinitive": "llegar",
    "english": "to arrive",
    "batch_number": 3,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v016",
    "infinitive": "pasar",
    "english": "to pass / happen",
    "batch_number": 4,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v017",
    "infinitive": "deber",
    "english": "should / owe",
    "batch_number": 4,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v018",
    "infinitive": "parecer",
    "english": "to seem",
    "batch_number": 4,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v019",
    "infinitive": "quedar",
    "english": "to stay / remain",
    "batch_number": 4,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v020",
    "infinitive": "creer",
    "english": "to believe",
    "batch_number": 4,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v021",
    "infinitive": "hablar",
    "english": "to speak",
    "batch_number": 5,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v022",
    "infinitive": "comer",
    "english": "to eat",
    "batch_number": 5,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v023",
    "infinitive": "vivir",
    "english": "to live",
    "batch_number": 5,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v024",
    "infinitive": "tener",
    "english": "to have",
    "batch_number": 5,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v025",
    "infinitive": "tomar",
    "english": "to take / drink",
    "batch_number": 5,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v026",
    "infinitive": "llevar",
    "english": "to carry / wear",
    "batch_number": 6,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v027",
    "infinitive": "traer",
    "english": "to bring",
    "batch_number": 6,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v028",
    "infinitive": "buscar",
    "english": "to look for",
    "batch_number": 6,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v029",
    "infinitive": "encontrar",
    "english": "to find",
    "batch_number": 6,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v030",
    "infinitive": "necesitar",
    "english": "to need",
    "batch_number": 6,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v031",
    "infinitive": "gustar",
    "english": "to like",
    "batch_number": 7,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v032",
    "infinitive": "pensar",
    "english": "to think",
    "batch_number": 7,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v033",
    "infinitive": "sentir",
    "english": "to feel",
    "batch_number": 7,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v034",
    "infinitive": "dormir",
    "english": "to sleep",
    "batch_number": 7,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v035",
    "infinitive": "pedir",
    "english": "to ask for / order",
    "batch_number": 7,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v036",
    "infinitive": "jugar",
    "english": "to play",
    "batch_number": 8,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v037",
    "infinitive": "trabajar",
    "english": "to work",
    "batch_number": 8,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v038",
    "infinitive": "estudiar",
    "english": "to study",
    "batch_number": 8,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v039",
    "infinitive": "aprender",
    "english": "to learn",
    "batch_number": 8,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v040",
    "infinitive": "enseñar",
    "english": "to teach",
    "batch_number": 8,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v041",
    "infinitive": "leer",
    "english": "to read",
    "batch_number": 9,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v042",
    "infinitive": "escribir",
    "english": "to write",
    "batch_number": 9,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v043",
    "infinitive": "abrir",
    "english": "to open",
    "batch_number": 9,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v044",
    "infinitive": "cerrar",
    "english": "to close",
    "batch_number": 9,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v045",
    "infinitive": "empezar",
    "english": "to begin",
    "batch_number": 9,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v046",
    "infinitive": "terminar",
    "english": "to finish",
    "batch_number": 10,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v047",
    "infinitive": "esperar",
    "english": "to wait / hope",
    "batch_number": 10,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v048",
    "infinitive": "llamar",
    "english": "to call",
    "batch_number": 10,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v049",
    "infinitive": "escuchar",
    "english": "to listen",
    "batch_number": 10,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v050",
    "infinitive": "oír",
    "english": "to hear",
    "batch_number": 10,
    "level": "A1–A2 · Beginner"
  },
  {
    "id": "v051",
    "infinitive": "mirar",
    "english": "to look at",
    "batch_number": 11,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v052",
    "infinitive": "andar",
    "english": "to walk",
    "batch_number": 11,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v053",
    "infinitive": "caminar",
    "english": "to walk",
    "batch_number": 11,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v054",
    "infinitive": "correr",
    "english": "to run",
    "batch_number": 11,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v055",
    "infinitive": "comprar",
    "english": "to buy",
    "batch_number": 11,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v056",
    "infinitive": "pagar",
    "english": "to pay",
    "batch_number": 12,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v057",
    "infinitive": "vender",
    "english": "to sell",
    "batch_number": 12,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v058",
    "infinitive": "usar",
    "english": "to use",
    "batch_number": 12,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v059",
    "infinitive": "lavar",
    "english": "to wash",
    "batch_number": 12,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v060",
    "infinitive": "limpiar",
    "english": "to clean",
    "batch_number": 12,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v061",
    "infinitive": "cocinar",
    "english": "to cook",
    "batch_number": 13,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v062",
    "infinitive": "desayunar",
    "english": "to eat breakfast",
    "batch_number": 13,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v063",
    "infinitive": "almorzar",
    "english": "to eat lunch",
    "batch_number": 13,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v064",
    "infinitive": "cenar",
    "english": "to eat dinner",
    "batch_number": 13,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v065",
    "infinitive": "viajar",
    "english": "to travel",
    "batch_number": 13,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v066",
    "infinitive": "manejar",
    "english": "to drive (common in Mexico)",
    "batch_number": 14,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v067",
    "infinitive": "subir",
    "english": "to go up / get on",
    "batch_number": 14,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v068",
    "infinitive": "bajar",
    "english": "to go down / get off",
    "batch_number": 14,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v069",
    "infinitive": "entrar",
    "english": "to enter",
    "batch_number": 14,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v070",
    "infinitive": "volver",
    "english": "to return",
    "batch_number": 14,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v071",
    "infinitive": "regresar",
    "english": "to come back",
    "batch_number": 15,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v072",
    "infinitive": "seguir",
    "english": "to follow / continue",
    "batch_number": 15,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v073",
    "infinitive": "repetir",
    "english": "to repeat",
    "batch_number": 15,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v074",
    "infinitive": "elegir",
    "english": "to choose",
    "batch_number": 15,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v075",
    "infinitive": "recordar",
    "english": "to remember",
    "batch_number": 15,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v076",
    "infinitive": "olvidar",
    "english": "to forget",
    "batch_number": 16,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v077",
    "infinitive": "entender",
    "english": "to understand",
    "batch_number": 16,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v078",
    "infinitive": "preguntar",
    "english": "to ask",
    "batch_number": 16,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v079",
    "infinitive": "contestar",
    "english": "to answer",
    "batch_number": 16,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v080",
    "infinitive": "ayudar",
    "english": "to help",
    "batch_number": 16,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v081",
    "infinitive": "compartir",
    "english": "to share",
    "batch_number": 17,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v082",
    "infinitive": "recibir",
    "english": "to receive",
    "batch_number": 17,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v083",
    "infinitive": "mandar",
    "english": "to send / order",
    "batch_number": 17,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v084",
    "infinitive": "decidir",
    "english": "to decide",
    "batch_number": 17,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v085",
    "infinitive": "costar",
    "english": "to cost",
    "batch_number": 17,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v086",
    "infinitive": "valer",
    "english": "to be worth",
    "batch_number": 18,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v087",
    "infinitive": "ganar",
    "english": "to win / earn",
    "batch_number": 18,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v088",
    "infinitive": "perder",
    "english": "to lose / miss",
    "batch_number": 18,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v089",
    "infinitive": "cambiar",
    "english": "to change",
    "batch_number": 18,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v090",
    "infinitive": "probar",
    "english": "to try / taste",
    "batch_number": 18,
    "level": "B1–B2 · Intermediate"
  },
  {
    "id": "v091",
    "infinitive": "sentarse",
    "english": "to sit down",
    "batch_number": 19,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v092",
    "infinitive": "levantarse",
    "english": "to get up",
    "batch_number": 19,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v093",
    "infinitive": "bañarse",
    "english": "to bathe / shower",
    "batch_number": 19,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v094",
    "infinitive": "vestirse",
    "english": "to get dressed",
    "batch_number": 19,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v095",
    "infinitive": "despertarse",
    "english": "to wake up",
    "batch_number": 19,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v096",
    "infinitive": "acostarse",
    "english": "to go to bed",
    "batch_number": 20,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v097",
    "infinitive": "quedarse",
    "english": "to stay",
    "batch_number": 20,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v098",
    "infinitive": "divertirse",
    "english": "to have fun",
    "batch_number": 20,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v099",
    "infinitive": "sonreír",
    "english": "to smile",
    "batch_number": 20,
    "level": "C1–C2 · Advanced"
  },
  {
    "id": "v100",
    "infinitive": "nadar",
    "english": "to swim",
    "batch_number": 20,
    "level": "C1–C2 · Advanced"
  }
]
TENSES = ("Present", "Preterite", "Simple future")
SUBJECTS = (("yo","I"),("tú","you, informal singular"),("él / ella / usted","he / she / you, formal"),("nosotros / nosotras","we"),("ustedes","you, plural in Mexico"),("ellos / ellas","they"))
_PRESENT = {"ser":["soy","eres","es","somos","son","son"],"estar":["estoy","estás","está","estamos","están","están"],"ir":["voy","vas","va","vamos","van","van"],"tener":["tengo","tienes","tiene","tenemos","tienen","tienen"],"hacer":["hago","haces","hace","hacemos","hacen","hacen"],"decir":["digo","dices","dice","decimos","dicen","dicen"],"poder":["puedo","puedes","puede","podemos","pueden","pueden"],"querer":["quiero","quieres","quiere","queremos","quieren","quieren"],"venir":["vengo","vienes","viene","venimos","vienen","vienen"],"dar":["doy","das","da","damos","dan","dan"],"ver":["veo","ves","ve","vemos","ven","ven"],"saber":["sé","sabes","sabe","sabemos","saben","saben"],"conocer":["conozco","conoces","conoce","conocemos","conocen","conocen"],"poner":["pongo","pones","pone","ponemos","ponen","ponen"],"salir":["salgo","sales","sale","salimos","salen","salen"],"traer":["traigo","traes","trae","traemos","traen","traen"],"oír":["oigo","oyes","oye","oímos","oyen","oyen"],"sonreír":["sonrío","sonríes","sonríe","sonreímos","sonríen","sonríen"],"gustar":["gusto","gustas","gusta","gustamos","gustan","gustan"]}
_PRETERITE = {"ser":["fui","fuiste","fue","fuimos","fueron","fueron"],"ir":["fui","fuiste","fue","fuimos","fueron","fueron"],"estar":["estuve","estuviste","estuvo","estuvimos","estuvieron","estuvieron"],"tener":["tuve","tuviste","tuvo","tuvimos","tuvieron","tuvieron"],"hacer":["hice","hiciste","hizo","hicimos","hicieron","hicieron"],"decir":["dije","dijiste","dijo","dijimos","dijeron","dijeron"],"poder":["pude","pudiste","pudo","pudimos","pudieron","pudieron"],"querer":["quise","quisiste","quiso","quisimos","quisieron","quisieron"],"venir":["vine","viniste","vino","vinimos","vinieron","vinieron"],"dar":["di","diste","dio","dimos","dieron","dieron"],"ver":["vi","viste","vio","vimos","vieron","vieron"],"saber":["supe","supiste","supo","supimos","supieron","supieron"],"poner":["puse","pusiste","puso","pusimos","pusieron","pusieron"],"traer":["traje","trajiste","trajo","trajimos","trajeron","trajeron"],"andar":["anduve","anduviste","anduvo","anduvimos","anduvieron","anduvieron"],"leer":["leí","leíste","leyó","leímos","leyeron","leyeron"],"oír":["oí","oíste","oyó","oímos","oyeron","oyeron"],"sonreír":["sonreí","sonreíste","sonrió","sonreímos","sonrieron","sonrieron"]}
_FUTURE_STEMS = {"decir":"dir","hacer":"har","tener":"tendr","poder":"podr","querer":"querr","venir":"vendr","poner":"pondr","salir":"saldr","saber":"sabr","valer":"valdr"}
_STEM = {"pensar":("e","ie"),"sentir":("e","ie"),"dormir":("o","ue"),"pedir":("e","i"),"jugar":("u","ue"),"encontrar":("o","ue"),"empezar":("e","ie"),"cerrar":("e","ie"),"costar":("o","ue"),"probar":("o","ue"),"volver":("o","ue"),"recordar":("o","ue"),"entender":("e","ie"),"seguir":("e","i"),"repetir":("e","i"),"elegir":("e","i"),"despertarse":("e","ie"),"acostarse":("o","ue"),"sentarse":("e","ie"),"divertirse":("e","ie"),"vestirse":("e","i")}
def _regular_present(base, ending):
    if ending == "ar": return [base+"o",base+"as",base+"a",base+"amos",base+"an",base+"an"]
    if ending == "er": return [base+"o",base+"es",base+"e",base+"emos",base+"en",base+"en"]
    return [base+"o",base+"es",base+"e",base+"imos",base+"en",base+"en"]
def conjugate(infinitive, tense):
    """Six Mexican Spanish subject forms, in SUBJECTS order."""
    reflexive = infinitive.endswith("se")
    verb = infinitive[:-2] if reflexive else infinitive
    ending, base = verb[-2:], verb[:-2]
    if tense == "Present":
        forms = list(_PRESENT[verb]) if verb in _PRESENT else _regular_present(base, ending)
        if verb not in _PRESENT and verb in _STEM:
            old, new = _STEM[verb]
            pos = base.rfind(old)
            changed_base = base[:pos] + new + base[pos + len(old):]
            forms = [changed_base + form[len(base):] if i != 3 else form for i, form in enumerate(forms)]
    elif tense == "Preterite":
        if verb in _PRETERITE:
            forms = list(_PRETERITE[verb])
        elif ending == "ar":
            forms = [base+"é",base+"aste",base+"ó",base+"amos",base+"aron",base+"aron"]
        else:
            forms = [base+"í",base+"iste",base+"ió",base+"imos",base+"ieron",base+"ieron"]
            if verb in {"dormir","pedir","sentir","seguir","elegir","repetir"}:
                vowel = "o" if verb == "dormir" else "e"
                changed = "u" if vowel == "o" else "i"
                forms[2] = forms[2].replace(vowel, changed, 1)
                forms[4] = forms[4].replace(vowel, changed, 1)
                forms[5] = forms[4]
            if verb == "leer": forms = ["leí","leíste","leyó","leímos","leyeron","leyeron"]
            if verb == "empezar": forms[0] = "empecé"
            if verb == "llegar": forms[0] = "llegué"
            if verb == "buscar": forms[0] = "busqué"
            if verb == "pagar": forms[0] = "pagué"
    elif tense == "Simple future":
        stem = _FUTURE_STEMS.get(verb, verb)
        forms = [stem+"é",stem+"ás",stem+"á",stem+"emos",stem+"án",stem+"án"]
    else:
        raise ValueError("Unsupported tense")
    if reflexive:
        forms = [p+" "+f for p, f in zip(("me","te","se","nos","se","se"), forms)]
    return forms
