"""Original, Mexican-Spanish-first vocabulary for Calabaza."""

import unicodedata


LEVELS = ("A1–A2 · Beginner", "B1–B2 · Intermediate", "C1–C2 · Advanced")
CATEGORIES = (
    "Greetings & courtesy",
    "Food & drink",
    "Travel",
    "Everyday needs",
    "Conversation",
    "Connecting words",
    "Question words",
    "Verbs",
)

# Content is original starter material, not imported from a third-party app.
VOCABULARY = [
    {"id":"hola","spanish":"hola","english":"hello","example":"Hola, ¿cómo estás?","example_translation":"Hi, how are you?","level":LEVELS[0],"category":"Greetings & courtesy","emoji":"👋"},
    {"id":"buenos_dias","spanish":"buenos días","english":"good morning","example":"Buenos días, señora.","example_translation":"Good morning, ma’am.","level":LEVELS[0],"category":"Greetings & courtesy","emoji":"🌞"},
    {"id":"por_favor","spanish":"por favor","english":"please","example":"Un café, por favor.","example_translation":"A coffee, please.","level":LEVELS[0],"category":"Greetings & courtesy","emoji":"🌼"},
    {"id":"gracias","spanish":"gracias","english":"thank you","example":"Gracias por ayudarme.","example_translation":"Thanks for helping me.","level":LEVELS[0],"category":"Greetings & courtesy","emoji":"🙏"},
    {"id":"agua","spanish":"agua","english":"water","example":"Quiero agua, por favor.","example_translation":"I’d like water, please.","level":LEVELS[0],"category":"Food & drink","emoji":"💧"},
    {"id":"cafe","spanish":"café","english":"coffee","example":"¿Tomamos un café?","example_translation":"Shall we have a coffee?","level":LEVELS[0],"category":"Food & drink","emoji":"☕"},
    {"id":"manzana","spanish":"manzana","english":"apple","example":"La manzana está rica.","example_translation":"The apple tastes good.","level":LEVELS[0],"category":"Food & drink","emoji":"🍎"},
    {"id":"tortilla","spanish":"tortilla","english":"corn tortilla","example":"Quiero dos tortillas, por favor.","example_translation":"I’d like two tortillas, please.","level":LEVELS[0],"category":"Food & drink","emoji":"🌮"},
    {"id":"bano","spanish":"baño","english":"bathroom","example":"¿Dónde está el baño?","example_translation":"Where is the bathroom?","level":LEVELS[0],"category":"Travel","emoji":"🚻"},
    {"id":"estacion","spanish":"estación","english":"station","example":"La estación está cerca.","example_translation":"The station is nearby.","level":LEVELS[0],"category":"Travel","emoji":"🚉"},
    {"id":"boleto","spanish":"boleto","english":"ticket","example":"Necesito un boleto para Puebla.","example_translation":"I need a ticket to Puebla.","level":LEVELS[0],"category":"Travel","emoji":"🎟️"},
    {"id":"cerca","spanish":"cerca","english":"near / nearby","example":"¿Hay una farmacia cerca?","example_translation":"Is there a pharmacy nearby?","level":LEVELS[0],"category":"Travel","emoji":"📍"},
    {"id":"ayuda","spanish":"ayuda","english":"help","example":"Necesito ayuda, por favor.","example_translation":"I need help, please.","level":LEVELS[0],"category":"Everyday needs","emoji":"🆘"},
    {"id":"casa","spanish":"casa","english":"house / home","example":"Mi casa está cerca.","example_translation":"My house is nearby.","level":LEVELS[0],"category":"Everyday needs","emoji":"🏡"},
    {"id":"no_entiendo","spanish":"no entiendo","english":"I don’t understand","example":"Perdón, no entiendo.","example_translation":"Sorry, I don’t understand.","level":LEVELS[0],"category":"Everyday needs","emoji":"💭"},
    {"id":"me_puede_ayudar","spanish":"¿Me puede ayudar?","english":"Can you help me? (polite)","example":"Disculpe, ¿me puede ayudar?","example_translation":"Excuse me, can you help me?","level":LEVELS[0],"category":"Everyday needs","emoji":"🤝"},
    {"id":"mucho_gusto","spanish":"mucho gusto","english":"nice to meet you","example":"Hola, soy Luis. Mucho gusto.","example_translation":"Hi, I’m Luis. Nice to meet you.","level":LEVELS[0],"category":"Conversation","emoji":"😊"},
    {"id":"como_estas","spanish":"¿cómo estás?","english":"how are you? (informal)","example":"¡Hola, Ana! ¿Cómo estás?","example_translation":"Hi, Ana! How are you?","level":LEVELS[0],"category":"Conversation","emoji":"💬"},
    {"id":"y","spanish":"y","english":"and","example":"Tengo café y pan.","example_translation":"I have coffee and bread.","level":LEVELS[0],"category":"Connecting words","emoji":"🔗"},
    {"id":"o","spanish":"o","english":"or","example":"¿Quieres té o café?","example_translation":"Do you want tea or coffee?","level":LEVELS[0],"category":"Connecting words","emoji":"↔️"},
    {"id":"con","spanish":"con","english":"with","example":"Voy con mi amiga.","example_translation":"I’m going with my friend.","level":LEVELS[0],"category":"Connecting words","emoji":"🫶"},
    {"id":"en","spanish":"en","english":"in / on / at","example":"El libro está en la mesa.","example_translation":"The book is on the table.","level":LEVELS[0],"category":"Connecting words","emoji":"📚"},
    {"id":"que","spanish":"¿qué?","english":"what? / which?","example":"¿Qué quieres comer?","example_translation":"What do you want to eat?","level":LEVELS[0],"category":"Question words","emoji":"❔"},
    {"id":"donde","spanish":"¿dónde?","english":"where?","example":"¿Dónde está la estación?","example_translation":"Where is the station?","level":LEVELS[0],"category":"Question words","emoji":"🧭"},
    {"id":"cuando","spanish":"¿cuándo?","english":"when?","example":"¿Cuándo sale el autobús?","example_translation":"When does the bus leave?","level":LEVELS[0],"category":"Question words","emoji":"🕒"},
    {"id":"cuanto","spanish":"¿cuánto cuesta?","english":"how much does it cost?","example":"Disculpe, ¿cuánto cuesta?","example_translation":"Excuse me, how much does it cost?","level":LEVELS[0],"category":"Question words","emoji":"💵"},
    {"id":"hablar","spanish":"hablar","english":"to speak","example":"Hablo español un poco.","example_translation":"I speak a little Spanish.","level":LEVELS[0],"category":"Verbs","emoji":"🗣️"},
    {"id":"comer","spanish":"comer","english":"to eat","example":"Comemos temprano.","example_translation":"We eat early.","level":LEVELS[0],"category":"Verbs","emoji":"🍽️"},
    {"id":"vivir","spanish":"vivir","english":"to live","example":"Vivo en México.","example_translation":"I live in Mexico.","level":LEVELS[0],"category":"Verbs","emoji":"🌱"},
    {"id":"tener","spanish":"tener","english":"to have","example":"Tengo dos hermanas.","example_translation":"I have two sisters.","level":LEVELS[0],"category":"Verbs","emoji":"👐"},
    {"id":"a_menudo","spanish":"a menudo","english":"often","example":"A menudo caminamos al parque.","example_translation":"We often walk to the park.","level":LEVELS[1],"category":"Connecting words","emoji":"🔁"},
    {"id":"sin_embargo","spanish":"sin embargo","english":"however","example":"Quería salir; sin embargo, empezó a llover.","example_translation":"I wanted to go out; however, it started to rain.","level":LEVELS[1],"category":"Connecting words","emoji":"🌧️"},
    {"id":"por_eso","spanish":"por eso","english":"that’s why / for that reason","example":"Tengo una cita; por eso, salgo temprano.","example_translation":"I have an appointment; that’s why I’m leaving early.","level":LEVELS[1],"category":"Connecting words","emoji":"➡️"},
    {"id":"darse_cuenta","spanish":"darse cuenta de","english":"to realize","example":"Me di cuenta de que era tarde.","example_translation":"I realized it was late.","level":LEVELS[1],"category":"Verbs","emoji":"💡"},
    {"id":"quedar_con","spanish":"quedar con","english":"to meet up with","example":"Quedé con mis amigos en el centro.","example_translation":"I met up with my friends downtown.","level":LEVELS[1],"category":"Conversation","emoji":"📅"},
    {"id":"me_pregunto","spanish":"me pregunto si…","english":"I wonder if…","example":"Me pregunto si llega hoy.","example_translation":"I wonder if they’ll arrive today.","level":LEVELS[1],"category":"Conversation","emoji":"🤔"},
    {"id":"cual","spanish":"¿cuál?","english":"which one? / what?","example":"¿Cuál prefieres, este o aquel?","example_translation":"Which one do you prefer, this one or that one?","level":LEVELS[1],"category":"Question words","emoji":"🧩"},
    {"id":"por_que","spanish":"¿por qué?","english":"why?","example":"¿Por qué estudias español?","example_translation":"Why are you studying Spanish?","level":LEVELS[1],"category":"Question words","emoji":"❓"},
    {"id":"hacer_reserva","spanish":"hacer una reservación","english":"to make a reservation","example":"Quisiera hacer una reservación para dos.","example_translation":"I’d like to make a reservation for two.","level":LEVELS[1],"category":"Travel","emoji":"🍽️"},
    {"id":"llevarse_bien","spanish":"llevarse bien","english":"to get along well","example":"Mis hermanos se llevan bien.","example_translation":"My siblings get along well.","level":LEVELS[1],"category":"Conversation","emoji":"🫂"},
    {"id":"a_fin_de_cuentas","spanish":"a fin de cuentas","english":"when all is said and done","example":"A fin de cuentas, decidimos quedarnos.","example_translation":"When all was said and done, we decided to stay.","level":LEVELS[2],"category":"Connecting words","emoji":"⚖️"},
    {"id":"no_obstante","spanish":"no obstante","english":"nevertheless","example":"El camino era largo; no obstante, seguimos adelante.","example_translation":"The road was long; nevertheless, we kept going.","level":LEVELS[2],"category":"Connecting words","emoji":"🛤️"},
    {"id":"tener_en_cuenta","spanish":"tener en cuenta","english":"to take into account","example":"Hay que tener en cuenta el horario.","example_translation":"We have to take the schedule into account.","level":LEVELS[2],"category":"Verbs","emoji":"🧠"},
    {"id":"dar_por_hecho","spanish":"dar por hecho","english":"to take for granted / assume","example":"No des por hecho que todos pueden venir.","example_translation":"Don’t assume that everyone can come.","level":LEVELS[2],"category":"Verbs","emoji":"📝"},
    {"id":"aun_así","spanish":"aun así","english":"even so","example":"Estaba cansada; aun así, terminó el trabajo.","example_translation":"She was tired; even so, she finished the work.","level":LEVELS[2],"category":"Connecting words","emoji":"✨"},
    {"id":"por_consiguiente","spanish":"por consiguiente","english":"consequently","example":"No llegó a tiempo y, por consiguiente, perdió el autobús.","example_translation":"They didn’t arrive on time and consequently missed the bus.","level":LEVELS[2],"category":"Connecting words","emoji":"🪄"},
    {"id":"a_que_te_refieres","spanish":"¿a qué te refieres?","english":"what do you mean?","example":"¿A qué te refieres con esa palabra?","example_translation":"What do you mean by that word?","level":LEVELS[2],"category":"Conversation","emoji":"🧐"},
    {"id":"hasta_que_punto","spanish":"¿hasta qué punto?","english":"to what extent?","example":"¿Hasta qué punto cambia la situación?","example_translation":"To what extent does the situation change?","level":LEVELS[2],"category":"Question words","emoji":"📏"},
    {"id":"independientemente","spanish":"independientemente de","english":"regardless of","example":"Independientemente del resultado, aprendimos mucho.","example_translation":"Regardless of the result, we learned a lot.","level":LEVELS[2],"category":"Everyday needs","emoji":"🌈"},
]


def _fold(text):
    normalized = unicodedata.normalize("NFD", str(text).casefold())
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")


def filter_words(words=VOCABULARY, level="All levels", category="All categories", query=""):
    needle = _fold(query.strip())
    result = []
    for word in words:
        if level != "All levels" and word["level"] != level:
            continue
        if category != "All categories" and word["category"] != category:
            continue
        haystack = _fold(" ".join(str(value) for value in word.values()))
        if needle and needle not in haystack:
            continue
        result.append(word)
    return result


def summarize_progress(words, progress):
    known = sum(progress.get(word["id"], {}).get("status") == "known" for word in words)
    learning = sum(progress.get(word["id"], {}).get("status") == "learning" for word in words)
    return {"total": len(words), "known": known, "learning": learning, "new": len(words) - known - learning}
