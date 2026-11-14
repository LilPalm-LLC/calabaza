import random
import streamlit as st

st.set_page_config(page_title="Calabaza | Spanish practice", page_icon="🎃", layout="centered", initial_sidebar_state="collapsed")

st.markdown("""
<style>
:root { --ink:#29372d; --muted:#68766b; --cream:#fbf8f0; --green:#315c45; --leaf:#e8f0df; --peach:#fff0df; }
html, body, [class*="css"] { font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }
.stApp { background:var(--cream); color:var(--ink); }
[data-testid="stHeader"] { background:rgba(251,248,240,.92); }
.block-container { width:100%; max-width:680px; padding:calc(env(safe-area-inset-top,0px) + 1.1rem) 1.1rem calc(env(safe-area-inset-bottom,0px) + 4rem); }
h1,h2,h3 { color:var(--ink); } h1 { font-family:Georgia,serif; letter-spacing:-.045em; line-height:1.08; }
.hero { background:linear-gradient(140deg,#fffdf8 5%,#f4eddd 100%); border:1px solid #eee7d8; border-radius:24px; padding:1.15rem 1.2rem .85rem; margin:.25rem 0 1.2rem; box-shadow:0 8px 24px #343d2d0a; }
.hero h1 { margin:.35rem 0; font-size:clamp(2rem,8vw,3rem); }
.hero p { color:var(--muted); font-size:1rem; margin:.25rem 0 .35rem; }
.eyebrow { color:var(--green); font-weight:750; letter-spacing:.11em; font-size:.72rem; text-transform:uppercase; }
.card { background:#fffefa; border:1px solid #ece8dc; border-radius:22px; padding:1.2rem; margin:.65rem 0 1rem; box-shadow:0 8px 25px #333f310b; }
.visual { background:radial-gradient(circle at 50% 45%,#fff9e9,#f3ebd8 70%); border:1px solid #f0e7d6; height:145px; border-radius:18px; display:flex; align-items:center; justify-content:center; font-size:4.7rem; margin-bottom:1rem; }
.prompt { color:var(--muted); font-size:.78rem; font-weight:750; letter-spacing:.1em; text-transform:uppercase; }
.answer { font-family:Georgia,serif; font-size:2rem; line-height:1.15; font-weight:700; color:var(--green); margin:.2rem 0; overflow-wrap:anywhere; }
.translation { color:var(--muted); font-style:italic; line-height:1.55; }
.soft-note { background:var(--leaf); border:1px solid #dce8d4; border-radius:15px; padding:.85rem 1rem; margin-top:.8rem; line-height:1.5; }
.word-chip { display:inline-block; background:var(--leaf); color:var(--green); padding:.3rem .7rem; border-radius:99px; font-weight:750; }
[data-testid="stTabs"] [role="tablist"] { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:.35rem; background:#fffefa; border:1px solid #eee8dc; border-radius:18px; padding:.35rem; }
[data-testid="stTabs"] button[role="tab"] { justify-content:center; min-height:48px; border-radius:13px; font-size:.9rem; font-weight:750; white-space:nowrap; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { background:var(--green); color:white; }
[data-testid="stTabs"] [data-baseweb="tab-highlight"] { display:none; }
[data-testid="stTabs"] [data-baseweb="tab-border"] { display:none; }
[data-testid="stMetric"] { background:#fffefa; border:1px solid #ece8dc; border-radius:16px; padding:.75rem; }
[data-testid="stTextInputRootElement"] input { min-height:48px; border-radius:14px; }
div.stButton > button,div.stFormSubmitButton > button { min-height:48px; border-radius:15px; font-weight:750; border-color:#dce4d8; }
div.stButton > button[kind="primary"],div.stFormSubmitButton > button[kind="primary"] { background:var(--green); border-color:var(--green); }
.stSelectbox [data-baseweb="select"] > div { min-height:48px; border-radius:14px; }
.footnote { color:var(--muted); font-size:.84rem; text-align:center; }
@media(max-width:520px) {
 .block-container { padding-left:.9rem; padding-right:.9rem; }
 .hero { border-radius:21px; padding:1rem 1rem .75rem; }
 [data-testid="stTabs"] [role="tablist"] { gap:.22rem; padding:.28rem; }
 [data-testid="stTabs"] button[role="tab"] { min-height:48px; font-size:.79rem; padding:.25rem .2rem; }
 .visual { height:128px; font-size:4.2rem; }
 .card { padding:1rem; border-radius:19px; }
 .answer { font-size:1.85rem; }
 div.stButton > button { font-size:.92rem; }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
 <div class="eyebrow">A little Spanish, every day</div>
 <h1>¡Hola! Soy Calabaza 🎃</h1>
 <p>Friendly practice for Mexican Spanish. Start small and grow your confidence.</p>
</div>
""", unsafe_allow_html=True)

cards = [
 {"en":"Thank you","es":"Gracias","emoji":"🙏","example":"Gracias por el café.","translation":"Thanks for the coffee.","note":"A warm, everyday way to say thank you."},
 {"en":"Water","es":"Agua","emoji":"💧","example":"Quiero agua, por favor.","translation":"I’d like water, please.","note":"Agua is feminine: el agua fría, but las aguas."},
 {"en":"Apple","es":"Manzana","emoji":"🍎","example":"La manzana está rica.","translation":"The apple tastes good.","note":"In Mexico, rico or rica often means delicious."},
 {"en":"Coffee","es":"Café","emoji":"☕","example":"¿Tomamos un café?","translation":"Shall we have a coffee?","note":"Café has an accent on the final é."},
 {"en":"House / home","es":"Casa","emoji":"🏡","example":"Mi casa está cerca.","translation":"My house is nearby.","note":"Casa is feminine: la casa."},
 {"en":"Dog","es":"Perro / perra","emoji":"🐕","example":"El perro juega en el parque.","translation":"The dog plays in the park.","note":"Use perro for a male dog and perra for a female dog."},
 {"en":"Book","es":"Libro","emoji":"📚","example":"Leo un libro en español.","translation":"I read a book in Spanish.","note":"Libro is masculine: un libro."},
 {"en":"Where is the bathroom?","es":"¿Dónde está el baño?","emoji":"🚻","example":"Disculpe, ¿dónde está el baño?","translation":"Excuse me, where is the bathroom?","note":"Disculpe is a polite way to get someone’s attention."},
 {"en":"I’d like a coffee, please.","es":"Quisiera un café, por favor.","emoji":"☕","example":"Quisiera un café con leche, por favor.","translation":"I’d like a coffee with milk, please.","note":"Quisiera is a polite way to make a request."},
 {"en":"Good morning","es":"Buenos días","emoji":"🌞","example":"Buenos días, ¿cómo está?","translation":"Good morning, how are you?","note":"A polite greeting you can use through the late morning."},
 {"en":"Please","es":"Por favor","emoji":"🌼","example":"Un vaso de agua, por favor.","translation":"A glass of water, please.","note":"Often added to requests to make them polite."},
 {"en":"I don’t understand","es":"No entiendo","emoji":"💭","example":"Perdón, no entiendo. ¿Puede repetir?","translation":"Sorry, I don’t understand. Can you repeat?","note":"Useful when you need someone to say something again."},
]

subjects = [
 ("yo","I"),("tú","you (informal, singular)"),("él / ella / usted","he / she / you (formal)"),
 ("nosotros / nosotras","we"),("ustedes","you (plural; used in Mexico)"),("ellos / ellas","they")
]

verbs = {
 "hablar":{"meaning":"to speak","forms":{
  "Present":["hablo","hablas","habla","hablamos","hablan","hablan"],
  "Preterite":["hablé","hablaste","habló","hablamos","hablaron","hablaron"],
  "Simple future":["hablaré","hablarás","hablará","hablaremos","hablarán","hablarán"]},
  "examples":{"Present":("Yo hablo español en casa.","I speak Spanish at home."),"Preterite":("Ayer hablé con Ana.","Yesterday I spoke with Ana."),"Simple future":("Mañana hablaré con el maestro.","Tomorrow I will speak with the teacher.")}},
 "comer":{"meaning":"to eat","forms":{
  "Present":["como","comes","come","comemos","comen","comen"],
  "Preterite":["comí","comiste","comió","comimos","comieron","comieron"],
  "Simple future":["comeré","comerás","comerá","comeremos","comerán","comerán"]},
  "examples":{"Present":("Nosotros comemos temprano.","We eat early."),"Preterite":("Ayer comí tacos.","Yesterday I ate tacos."),"Simple future":("Mañana comeremos en casa.","Tomorrow we will eat at home.")}},
 "vivir":{"meaning":"to live","forms":{
  "Present":["vivo","vives","vive","vivimos","viven","viven"],
  "Preterite":["viví","viviste","vivió","vivimos","vivieron","vivieron"],
  "Simple future":["viviré","vivirás","vivirá","viviremos","vivirán","vivirán"]},
  "examples":{"Present":("Vivo en México.","I live in Mexico."),"Preterite":("Vivimos en Puebla un año.","We lived in Puebla for a year."),"Simple future":("El próximo año viviré cerca del trabajo.","Next year I will live near work.")}},
 "tener":{"meaning":"to have","forms":{
  "Present":["tengo","tienes","tiene","tenemos","tienen","tienen"],
  "Preterite":["tuve","tuviste","tuvo","tuvimos","tuvieron","tuvieron"],
  "Simple future":["tendré","tendrás","tendrá","tendremos","tendrán","tendrán"]},
  "examples":{"Present":("Tengo dos hermanas.","I have two sisters."),"Preterite":("Ayer tuve mucho trabajo.","Yesterday I had a lot of work."),"Simple future":("Mañana tendré tiempo.","Tomorrow I will have time.")}}
}

groups = {
 "Connecting words":[
  ("y","and","Tengo café y pan.","I have coffee and bread."),
  ("o","or","¿Quieres té o café?","Do you want tea or coffee?"),
  ("pero","but","Quiero ir, pero tengo trabajo.","I want to go, but I have work."),
  ("porque","because","Estudio porque me gusta.","I study because I like it."),
  ("con","with","Voy con mi amiga.","I’m going with my friend."),
  ("en","in / on / at","El libro está en la mesa.","The book is on the table."),
  ("para","for / in order to","Este regalo es para ti.","This gift is for you."),
  ("de","of / from","Soy de Chicago.","I’m from Chicago.")],
 "Time and frequency":[
  ("siempre","always","Siempre tomo agua en la mañana.","I always drink water in the morning."),
  ("a menudo","often","A menudo caminamos al parque.","We often walk to the park."),
  ("a veces","sometimes","A veces cocino en casa.","Sometimes I cook at home."),
  ("nunca","never","Nunca tomo café por la noche.","I never drink coffee at night."),
  ("ahora","now","Ahora estoy en casa.","I’m at home now."),
  ("después","after / later","Después vamos al mercado.","Later we’re going to the market.")],
 "Question words":[
  ("qué","what / which","¿Qué quieres comer?","What do you want to eat?"),
  ("por qué","why","¿Por qué estudias español?","Why are you studying Spanish?"),
  ("cuándo","when","¿Cuándo empieza la película?","When does the movie start?"),
  ("cuál","which / what","¿Cuál prefieres?","Which one do you prefer?"),
  ("quién","who","¿Quién viene hoy?","Who is coming today?"),
  ("dónde","where","¿Dónde está la estación?","Where is the station?"),
  ("cómo","how","¿Cómo te llamas?","What is your name?"),
  ("cuánto / cuánta","how much","¿Cuánto cuesta?","How much does it cost?")]
}

defaults = {"card_index":0,"card_revealed":False,"reviewed_cards":set(),"known_cards":set(),
            "verb_prompt":None,"verb_revealed":False,"verb_subject_index":0}
for key,value in defaults.items():
 if key not in st.session_state: st.session_state[key] = value

flashcards_tab, verbs_tab, words_tab = st.tabs(["🗂️ Flashcards","🌱 Verb garden","🔗 Word links"])

with flashcards_tab:
 st.markdown('<div class="eyebrow">Recall first, reveal second</div>',unsafe_allow_html=True)
 index = st.session_state.card_index
 card = cards[index]
 st.markdown('<div class="card">',unsafe_allow_html=True)
 st.markdown(f'<div class="visual" role="img" aria-label="Illustration for {card["en"]}">{card["emoji"]}</div><div class="prompt">How do you say…</div><h2>{card["en"]}</h2></div>',unsafe_allow_html=True)
 st.text_input("Try to remember the Spanish",key=f"guess_{index}",placeholder="Type it here, or just think of it")
 col_a,col_b = st.columns(2)
 with col_a:
  if st.button("Reveal answer",type="primary",use_container_width=True,key="reveal_card"):
   st.session_state.card_revealed = True
 with col_b: st.caption(f"Card {index+1} of {len(cards)}")
 if st.session_state.card_revealed:
  st.markdown(f'<div class="card"><div class="prompt">Mexican Spanish</div><div class="answer">{card["es"]}</div><p class="translation"><i>{card["example"]}</i><br>{card["translation"]}</p><div class="soft-note">{card["note"]}</div></div>',unsafe_allow_html=True)
  col_a,col_b = st.columns(2)
  with col_a:
   if st.button("Still learning",use_container_width=True,key="card_learning"):
    st.session_state.reviewed_cards.add(index); st.session_state.known_cards.discard(index)
    st.session_state.card_index = (index+1)%len(cards); st.session_state.card_revealed = False; st.rerun()
  with col_b:
   if st.button("Got it ✓",type="primary",use_container_width=True,key="card_known"):
    st.session_state.reviewed_cards.add(index); st.session_state.known_cards.add(index)
    st.session_state.card_index = (index+1)%len(cards); st.session_state.card_revealed = False; st.rerun()
 col_a,col_b = st.columns(2)
 col_a.metric("Reviewed this visit",len(st.session_state.reviewed_cards))
 col_b.metric("Got it this visit",len(st.session_state.known_cards))
 st.caption("Practice marks last only for this browser session; they are not saved between visits.")

with verbs_tab:
 st.markdown('<div class="eyebrow">Verb garden</div>',unsafe_allow_html=True)
 st.write("See all six subject forms, then practice one at a time.")
 verb = st.selectbox("Choose a verb",list(verbs),format_func=lambda v:f"{v.title()} — {verbs[v]['meaning']}")
 tense = st.selectbox("Choose a tense",["Present","Preterite","Simple future"])
 st.markdown('<div class="soft-note"><b>Quick tense guide</b><br>Present: now or a usual action. Preterite: a completed past action. Simple future: what will happen. Mexican Spanish uses <i>ustedes</i> for plural “you”; <i>vosotros</i> is not used in everyday Mexican Spanish.</div>',unsafe_allow_html=True)
 current_key = (verb,tense)
 if st.session_state.verb_prompt != current_key:
  st.session_state.verb_prompt = current_key
  st.session_state.verb_revealed = False
  st.session_state.verb_subject_index = random.randrange(6)
 subject_index = st.session_state.verb_subject_index
 subject,english = subjects[subject_index]
 forms = verbs[verb]["forms"][tense]
 st.markdown("#### Try a form")
 st.markdown(f'<div class="card"><div class="prompt">{tense} · {english}</div><div class="answer">{verb}</div></div>',unsafe_allow_html=True)
 if st.button("Reveal this form",type="primary",use_container_width=True,key="reveal_verb"):
  st.session_state.verb_revealed = True
 if st.session_state.verb_revealed:
  st.markdown(f'<div class="card"><div class="prompt">{subject}</div><div class="answer">{forms[subject_index]}</div></div>',unsafe_allow_html=True)
 example_es,example_en = verbs[verb]["examples"][tense]
 st.markdown(f'<div class="soft-note"><b>Example</b><br><i>{example_es}</i><br>{example_en}</div>',unsafe_allow_html=True)
 if st.button("Practice another subject",use_container_width=True,key="new_verb_prompt"):
  st.session_state.verb_prompt = None; st.session_state.verb_revealed = False; st.rerun()
 with st.expander("Show all six forms"):
  for i,(person,gloss) in enumerate(subjects):
   st.markdown(f"**{person}** · {gloss} — **{forms[i]}**")
 st.caption("The preterite is one common past tense. More past tenses can be added as you progress.")

with words_tab:
 st.markdown('<div class="eyebrow">Make the little words useful</div>',unsafe_allow_html=True)
 query = st.text_input("Search words or meanings",placeholder="Try “where”, “often”, “with”…")
 shown = 0
 for group_name,entries in groups.items():
  matches = [item for item in entries if not query or query.casefold() in " ".join(item).casefold()]
  if matches:
   st.markdown(f"#### {group_name}")
   for spanish,meaning,example_es,example_en in matches:
    shown += 1
    with st.container(border=True):
     st.markdown(f'<span class="word-chip">{spanish}</span> &nbsp; <b>{meaning}</b>',unsafe_allow_html=True)
     st.markdown(f"*{example_es}*  \n{example_en}")
 if shown == 0: st.info("No matches yet. Try another word or meaning.")

st.divider()
st.markdown('<p class="footnote">Original sample sentences for practice. Mexican Spanish is the default variety; meanings can depend on context.</p>',unsafe_allow_html=True)
