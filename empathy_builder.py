import streamlit as st
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Empathy Builder | Sishya School",
    layout="centered"
)

# ---------------- SESSION STATE INIT ----------------
if "started" not in st.session_state:
    st.session_state.started = False

if "story" not in st.session_state:
    st.session_state.story = None

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=90)
with col2:
    st.markdown("## **Sishya School, Hosur**")
    st.markdown("### 📖 Empathy Builder – Story Completion Game")
    st.markdown("**Social Emotional Learning Activity**")

st.divider()

# ---------------- STUDENT DETAILS (SHOW ONLY ONCE) ----------------
if not st.session_state.started:
    with st.form("student_form"):
        st.subheader("👤 Student Information")
        name = st.text_input("Student Name")
        clas = st.text_input("Class / Section")
        start = st.form_submit_button("Start Activity")

    if start:
        st.session_state.name = name
        st.session_state.clas = clas
        st.session_state.started = True
        st.session_state.story = None
        st.rerun()
    else:
        st.stop()

# ---------------- STORY BANK ----------------
stories = [
    {
        "title": "The Broken Toy",
        "text": """
Ravi brought his favourite toy to school.  
During lunch break, he noticed that the toy was broken.  
Some of his classmates were standing nearby and laughing.

The story stops here.
"""
    },
    {
        "title": "Left Out",
        "text": """
Meena wanted to join a group game during recess.  
When she went near her classmates, they said the teams were full  
and continued playing without her.

Meena stood quietly at the corner of the playground.

The story stops here.
"""
    },
    {
        "title": "New Student",
        "text": """
Arjun is new to the school.  
During class activities, he doesn’t know where to sit  
and hesitates to ask anyone for help.

Some students notice him sitting alone.

The story stops here.
"""
    },
    {
        "title": "Mistake in Class",
        "text": """
During a reading activity, Sana made a mistake while reading aloud.  
A few students giggled when they heard her.

Sana suddenly became very quiet.

The story stops here.
"""
    }
]

# ---------------- SELECT STORY ONCE ----------------
if st.session_state.story is None:
    st.session_state.story = random.choice(stories)

story = st.session_state.story

# ---------------- DISPLAY STORY ----------------
st.success(f"Welcome {st.session_state.name} 👋")

st.markdown(f"### 🧩 Story: *{story['title']}*")
st.write(story["text"])

st.divider()

# ---------------- OPEN-ENDED RESPONSES ----------------
st.markdown("### ✍️ Your Response")

feelings_text = st.text_area(
    "How do you think the character is feeling? Why?",
    key="feelings",
    height=120
)

action_text = st.text_area(
    "What should the character do next? Explain your reason.",
    key="action",
    height=120
)

submit = st.button("Submit Response")

# ---------------- EMPATHY SCORING ----------------
def empathy_score(feelings, action):
    score = 0

    emotion_words = ["sad", "upset", "hurt", "embarrassed", "lonely", "nervous", "angry"]
    support_words = ["help", "teacher", "friend", "talk", "calm", "include", "support"]
    negative_words = ["hit", "shout", "fight", "revenge", "ignore"]

    text = (feelings + " " + action).lower()

    if any(word in feelings.lower() for word in emotion_words):
        score += 2

    if "because" in feelings.lower() or "when" in feelings.lower():
        score += 2

    if any(word in action.lower() for word in support_words):
        score += 2

    if not any(word in text for word in negative_words):
        score += 2

    if len(feelings.split()) + len(action.split()) > 40:
        score += 2

    return score

# ---------------- FEEDBACK ----------------
if submit:
    st.divider()
    st.markdown("### 🧠 Empathy Reflection")

    score = empathy_score(feelings_text, action_text)

    if score >= 8:
        level = "High Empathy"
        remark = "🌟 You clearly understood the emotions and responded with kindness."
    elif score >= 5:
        level = "Developing Empathy"
        remark = "🙂 Good understanding. With deeper reflection, your response can improve."
    else:
        level = "Emerging Empathy"
        remark = "🧠 A good start. Try to think more about emotions and support."

    st.write(f"**Student Name:** {st.session_state.name}")
    st.write(f"**Class:** {st.session_state.clas}")
    st.write(f"**Empathy Score:** {score} / 10")
    st.write(f"**Empathy Level:** {level}")
    st.info(f"**SEL Remark:** {remark}")

    if st.button("🔄 New Story"):
        st.session_state.story = None
        st.session_state.feelings = ""
        st.session_state.action = ""
        st.rerun()
