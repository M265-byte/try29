import streamlit as st
from PIL import Image
import os
import time

st.set_page_config(page_title="Ancient Tale", layout="wide")

# -----------------------
# Utilities
# -----------------------
def load_img(path):
    try:
        return Image.open(path).convert("RGBA")
    except:
        st.warning(f"Missing or unreadable image: {path}")
        return None

def show(img):
    if img: st.image(img, use_container_width=True)

def next_scene(name):
    st.session_state.scene = name

def layout(cols=[4,1]):
    return st.columns(cols)

# -----------------------
# Session Defaults
# -----------------------
defaults = {
    "scene": "menu",
    "character": None,
    "kids_q": 0,
    "ship_q": 0,
    "pearls_answered": 0,
    "pearl_start": None,
    "hearts": 4,
    "current_pearl": None,
    "congrats_time": None
}
for k,v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------
# Static Data
# -----------------------
KIDS_QUESTIONS = [
    ("Which game are they playing?", ["Tila", "Qubba", "Salam bil Aqaal", "Khosah Biboosah"], "Tila"),
    ("And the second game?", ["Khosah Biboosah", "Tila", "Mawiyah", "Alghimayah"], "Khosah Biboosah"),
]
PEARL_QUESTIONS = [
    ("What is the knife used to open oysters called?", ["Sakaria", "Mafak", "Tasa"], "Sakaria"),
    ("Large white/pinkish pearl?", ["Danah", "Yaqooti", "Jiwan"], "Danah"),
    ("Smaller white shiny pearl?", ["Yaqooti", "Yika", "Mauz"], "Yaqooti"),
    ("Yellowish/blueish pearl?", ["Batniyah", "Qimashi", "Rasiyah"], "Qimashi"),
]
SHIP_QUESTIONS = [
    ("What is the Naukhada's role?", ["Captain / Chief", "Main diver", "Assistant diver"], "Captain / Chief"),
    ("What is Naham's role?", ["Motivator and singer", "Main diver", "Pearl inspector"], "Motivator and singer"),
    ("Who steers the ship?", ["Skuni", "Seeb", "Naham"], "Skuni"),
]

# Pearl image positions not needed now (they are in right column)
PEARL_SIZE = (100,100)

# -----------------------
# Helper Function
# -----------------------
def single_scene(image_path, next_name, key):
    main, side = layout()
    with main:
        show(load_img(image_path))
    with side:
        if st.button("Next ▶", key=f"next_{key}"):
            next_scene(next_name)

# -----------------------
# SCENES
# -----------------------
suf = st.session_state.character or "girl"

# --- MENU ---
if st.session_state.scene == "menu":
    main, side = layout()
    with main:
        show(load_img("menu.png"))
        st.markdown("<h1 style='text-align:center; color:white;'>Ancient Tales</h1>", unsafe_allow_html=True)
    with side:
        if st.button("Sign In"):
            next_scene("signin")
        if st.button("Enter as Guest"):
            next_scene("character_select")

# --- SIGNIN ---
elif st.session_state.scene == "signin":
    main, side = layout()
    with main:
        show(load_img("menu.png"))
        st.markdown("<h2 style='text-align:center; color:white;'>Sign In</h2>", unsafe_allow_html=True)
        st.session_state._email = st.text_input("Enter Email")
        st.session_state._pwd = st.text_input("Enter Password", type="password")
    with side:
        if st.button("Submit"):
            if st.session_state._email and st.session_state._pwd:
                next_scene("character_select")
            else:
                st.warning("Please enter email and password")

# --- CHARACTER SELECT ---
elif st.session_state.scene == "character_select":
    main, side = layout()
    with main:
        show(load_img("character.png"))
    with side:
        if st.button("Play as Dhabia (girl)"):
            st.session_state.character = "girl"
            st.session_state.kids_q = st.session_state.ship_q = 0
            st.session_state.pearls_answered = 0
            st.session_state.pearl_start = None
            st.session_state.hearts = 4
            st.session_state.current_pearl = None
            st.session_state.congrats_time = None
            next_scene("dubainew1")
        if st.button("Play as Nahyan (boy)"):
            st.session_state.character = "boy"
            st.session_state.kids_q = st.session_state.ship_q = 0
            st.session_state.pearls_answered = 0
            st.session_state.pearl_start = None
            st.session_state.hearts = 4
            st.session_state.current_pearl = None
            st.session_state.congrats_time = None
            next_scene("dubainew1")

# --- STORY SCENES ---
if st.session_state.scene == "dubainew1":
    single_scene(f"dubainew1{suf}.png", "dubainew2", "dubainew1")
elif st.session_state.scene == "dubainew2":
    single_scene(f"dubainew2{suf}.png", f"welcome1_{suf}", "dubainew2")
elif st.session_state.scene.startswith("welcome1"):
    single_scene(f"welcome1{suf}.png", f"welcome2_{suf}", f"welcome1_{suf}")
elif st.session_state.scene.startswith("welcome2"):
    single_scene(f"welcome2{suf}.png", f"kid1{suf}", f"welcome2_{suf}")
elif st.session_state.scene.startswith("kid1"):
    single_scene(f"kid1{suf}.png", f"kid2{suf}", f"kid1_{suf}")
elif st.session_state.scene.startswith("kid2"):
    main, side = layout()
    with main: show(load_img(f"kid2{suf}.png"))
    with side:
        q, opts, ans = KIDS_QUESTIONS[0]
        choice = st.radio(q, opts, key="kids2_q")
        if st.button("Submit Answer"):
            if choice == ans: st.success("Correct!")
            else: st.error(f"Wrong! Correct: {ans}")
            next_scene(f"kid3{suf}")
elif st.session_state.scene.startswith("kid3"):
    main, side = layout()
    with main: show(load_img(f"kid3{suf}.png"))
    with side:
        q, opts, ans = KIDS_QUESTIONS[1]
        choice = st.radio(q, opts, key="kids3_q")
        if st.button("Submit Answer"):
            if choice == ans: st.success("Correct!")
            else: st.error(f"Wrong! Correct: {ans}")
            next_scene(f"kid4{suf}")
elif st.session_state.scene.startswith("kid4"):
    single_scene(f"kid4{suf}.png", f"crew1{suf}", f"kid4_{suf}")

# --- CREW SCENES 1..9 ---
for i in range(1,10):
    if st.session_state.scene == f"crew{i}{suf}":
        next_name = f"crew{i+1}{suf}" if i<9 else "pearlgame"
        single_scene(f"crew{i}{suf}.png", next_name, f"crew{i}_{suf}")

# --- PEARL GAME (pearls clickable on right) ---
if st.session_state.scene == "pearlgame":
    bg = load_img(f"pearlgame{suf}1.png")
    pearl_imgs = [load_img(f"pearl{i+1}.png") for i in range(4)]

    left, right = st.columns([4,1])

    # Left: main background + question
    with left:
        if bg: st.image(bg, use_container_width=True)

        # Hearts timer
        if st.session_state.pearl_start is None:
            st.session_state.pearl_start = time.time()
        elapsed = int(time.time() - st.session_state.pearl_start)
        st.session_state.hearts = max(4 - elapsed//30,0)
        st.markdown(f"<div style='color:red; font-size:20px;'>{'❤️ '*st.session_state.hearts}</div>", unsafe_allow_html=True)

        # Show question for clicked pearl
        if st.session_state.current_pearl is not None:
            p = st.session_state.current_pearl
            q, opts, ans = PEARL_QUESTIONS[p]
            st.markdown(f"### Pearl {p+1} Question")
            choice = st.radio(q, opts, key=f"pearl_radio_{p}")
            if st.button("Submit Pearl Answer", key=f"pearl_submit_{p}"):
                if choice == ans: st.success("Correct!")
                else: st.error(f"Wrong! Correct: {ans}")
                st.session_state.pearls_answered += 1
                st.session_state.current_pearl = None

    # Right: clickable pearl PNGs
    with right:
        for idx, p_img in enumerate(pearl_imgs):
            disabled = idx < st.session_state.pearls_answered
            if p_img:
                if st.button("", key=f"pearl_btn_{idx}", disabled=disabled):
                    st.session_state.current_pearl = idx
                st.image(p_img, width=80)

    # Proceed / fail
    if st.session_state.pearls_answered >= 4:
        if st.button("Proceed to Ship"): next_scene("ship")
    elif st.session_state.hearts <=0:
        st.error("All hearts lost.")
        if st.button("Proceed to Ship (continue)"): next_scene("ship")

# --- SHIP ---
if st.session_state.scene == "ship":
    main, side = st.columns([4,1])
    with main: show(load_img(f"ship{suf}1.png"))
    with side:
        idx = st.session_state.ship_q
        if idx < len(SHIP_QUESTIONS):
            q, opts, ans = SHIP_QUESTIONS[idx]
            choice = st.radio(q, opts, key=f"ship_radio_{idx}")
            if st.button("Submit Ship Answer", key=f"ship_submit_{idx}"):
                if choice == ans: st.success("Correct!")
                else: st.error(f"Wrong! Correct: {ans}")
                st.session_state.ship_q += 1
        else:
            if st.button("Finish Ship Questions"):
                st.session_state.congrats_time = time.time()+5
                next_scene("congrats1")

# --- CONGRATS ---
if st.session_state.scene == "congrats1":
    main, side = st.columns([4,1])
    with main: show(load_img(f"congrats{suf}1.png"))
    if st.session_state.congrats_time is None:
        st.session_state.congrats_time = time.time()+5
    if time.time() >= st.session_state.congrats_time:
        next_scene("congrats2")
elif st.session_state.scene == "congrats2":
    main, side = st.columns([4,1])
    with main:
        show(load_img(f"congrats{suf}2.png"))
        st.markdown("<h2 style='text-align:center; color:white;'>Adventure Complete</h2>", unsafe_allow_html=True)
    with side:
        if st.button("Play Again"):
            for k in defaults.keys():
                st.session_state[k] = defaults[k]
