import streamlit as st

# Custom CSS for the login page
st.markdown(
    """
    <style>
    body {
        background-color: #1c1c1c; /* Dark background */
        color: white; /* White text */
    }
    .stButton>button {
        background-color: #1c1c1c; /* Dark button background */
        color: white; /* White button text */
        border: none; /* Remove button border */
        transition: background-color 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: #3d3d3d; /* Darker background on hover */
        color: #ffffff; /* Ensure text stays white */
    }
    .stTextInput input {
        background-color: #3d3d3d; /* Input field background */
        color: white; /* Input field text color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Rest of your login page code...
st.title("DID YOUR DAY SUCK?")
st.text_input("🪄 Choose your magic word to find out...", key="magic_word")
st.button("Open sesame")
import pandas as pd
import altair as alt
from datetime import date

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #1a1a2e;
        color: white;
    }
    .stButton>button {
        color: #ffffff;
        background: transparent;
        border: 2px solid #ff8c42;
        border-radius: 12px;
        padding: 5px 20px;
        font-size: 16px;
        transition: background 0.3s, color 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff8c42;
        color: #000000;
    }
    .emoji-summary {
        font-size: 16px;
        display: flex;
        gap: 10px;
        justify-content: flex-start;
        align-items: center;
        overflow-x: auto;
        white-space: nowrap;
    }
    .emoji-summary span {
        display: inline-block;
        margin-right: 5px;
    }
    .stDataFrame {
        background-color: #222831;
        color: white;
        border: none;
    }
    .aura-display {
        color: orange;
        font-size: 24px;
        font-weight: bold;
    }
    .comment-box input {
        background: #2d2d44;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session states
if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {
        "values": [
            {"question": "Did I spend my time self-directed today?", "emoji": "💨", "value": "freedom", "weight": 1},
            {"question": "Did I invest into my relationships?", "emoji": "🍄‍🟫", "value": "connection", "weight": 2},
            {"question": "Did I connect with my queerness?", "emoji": "💧", "value": "authenticity", "weight": 1},
            {"question": "Did I experience joy or pleasure today?", "emoji": "✨", "value": "pleasure", "weight": 2},
            {"question": "Was I kind to my body?", "emoji": "🍃", "value": "sustainability", "weight": 2},
            {"question": "Did I learn something new or explore something?", "emoji": "☁️", "value": "curiosity", "weight": 1},
            {"question": "Did I move closer to one of my dreams?", "emoji": "🌱", "value": "progress", "weight": 3}
        ]
    }
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Date", "Values", "Total Score", "Comment"])

# Function to render the login page
def login_page():
    st.title("DID YOUR DAY SUCK?")
    st.write("Choose your magic word to find out...")
    magic_word = st.text_input("🪄", type="password", label_visibility="collapsed")
    if st.button("Open sesame"):
        if magic_word:
            st.session_state.logged_in = True
            st.session_state.page = "edit_profile"

# Function to render the edit profile page
def edit_profile_page():
    st.title("What do you actually want?")
    st.write("Enter your personal 7 values and corresponding daily questions")
    
    for i, value_info in enumerate(st.session_state.user_profile["values"]):
        with st.expander(f"Value {i+1}"):
            value_info["value"] = st.text_input(f"Value {i+1}", value_info["value"], key=f"value_{i}")
            value_info["emoji"] = st.selectbox(
                "Symbol", 
                ["🌵", "🌲", "🌳", "🌴", "🪵", "🌱", "🌿", "🍀", "🍃", "🍂", "🍁", "🍄", "🍄‍🟫", "🐚", "🪨", "🌾", 
                 "🌷", "🪻", "🪷", "🌺", "🌸", "🌼", "🌻", "🌕", "🌗", "🌓", "🌑", "🌙", "🪐", "💫", "⭐️", "🌟", "✨",
                 "⚡️", "💥", "🔥", "☀️", "☁️", "🌧️", "❄️", "🧊", "💨", "💧", "💦", "🫧", "🍎", "🍐", "🍊", "🍋", "🍇", 
                 "🍓", "🍒", "🍑", "🥭", "🍍", "🥥", "🍅", "🍆", "🥦", "🌶️", "🥕", "🧄", "🧅", "🥔", "🫚", "🥚", 
                 "🦪", "🌰", "🫘", "🌋", "⛰️", "🏔️", "🩸", "❤️", "💜", "🖤", "💕"],
                index=0,
                key=f"emoji_{i}"
            )
            value_info["weight"] = st.slider("Importance", 1, 3, value_info["weight"], key=f"weight_{i}")
            value_info["question"] = st.text_input(f"Daily question regarding {value_info['value']}", 
                                                   value_info["question"], key=f"question_{i}")
    if st.button("Internalize values"):
        st.session_state.page = "main"

# Function to render the main page
def main_page():
    st.title("DID I HAVE A SHIT DAY?")
    # Display emojis summary line
    if st.session_state.data.shape[0] > 0:
        emoji_summary_html = "<div class='emoji-summary'>"
        value_counts = {info["value"]: 0 for info in st.session_state.user_profile["values"]}
        for info in st.session_state.user_profile["values"]:
            count = st.session_state.data["Values"].str.count(info["emoji"]).sum()
            value_counts[info["value"]] = count
            emoji_summary_html += f"<span style='font-size: {max(16, count * 10 + 16)}px;'>{info['emoji']}</span>"
        emoji_summary_html += "</div>"
        st.markdown(emoji_summary_html, unsafe_allow_html=True)

    # Display questions with toggles
    for q in st.session_state.user_profile["values"]:
        col1, col2 = st.columns([8, 1])
        with col1:
            question = f"{q['emoji']} {q['question']}"
            if st.button(question, key=q["question"]):
                st.session_state.toggles[q["question"]] = not st.session_state.toggles.get(q["question"], False)
        with col2:
            emoji_display = "🌟" if st.session_state.toggles.get(q["question"], False) else "⭐️"
            st.markdown(f"<span style='font-size: 18px;'>{emoji_display}</span>", unsafe_allow_html=True)

    # Display the date and comment box
    st.write(f"Date: {date.today()}")
    comment = st.text_input("Reflect on your day...", placeholder="optional 🫧")

    # Display current score
    total_score = sum(q["weight"] for q in st.session_state.user_profile["values"] 
                      if st.session_state.toggles.get(q["question"], False))
    st.write(f"<div class='aura-display'>Today's Aura: +{total_score}</div>", unsafe_allow_html=True)

    # Submit log
    if st.button("Not so shit ain't it"):
        emojis = "".join([q["emoji"] for q in st.session_state.user_profile["values"] 
                          if st.session_state.toggles.get(q["question"], False)])
        entry = {"Date": date.today(), "Values": emojis, "Total Score": total_score, "Comment": comment}
        st.session_state.data = pd.concat([st.session_state.data, pd.DataFrame([entry])], ignore_index=True)
        st.success("Another day, another slay!")
        st.session_state.toggles = {q["question"]: False for q in st.session_state.user_profile["values"]}

    # Display log and charts
    if not st.session_state.data.empty:
        st.write("### My Life")
        st.dataframe(st.session_state.data[["Date", "Values", "Total Score", "Comment"]])
        st.write("### My Priorities")
        sorted_values = sorted(
            [(info["value"], info["emoji"], st.session_state.data["Values"].str.count(info["emoji"]).sum())
             for info in st.session_state.user_profile["values"]],
            key=lambda x: x[2], reverse=True
        )
        for value, emoji, count in sorted_values:
            st.write(f"{emoji} {value} {emoji}")

        st.write("### My Frequency")
        chart_data = st.session_state.data.set_index("Date")[["Total Score"]]
        line_chart = alt.Chart(chart_data.reset_index()).mark_line(color="orange").encode(
            x='Date:T', y='Total Score:Q'
        )
        avg_line = alt.Chart(pd.DataFrame({'y': [chart_data['Total Score'].mean()]})).mark_rule(color="red").encode(
            y='y:Q'
        )
        st.altair_chart((line_chart + avg_line).interactive(), use_container_width=True)

        st.write(f"<div class='aura-display'>Total Aura Collected: +{st.session_state.data['Total Score'].sum()}</div>", 
                 unsafe_allow_html=True)

    st.button("Reconsider values", on_click=lambda: st.session_state.update(page="edit_profile"))

# Page navigation logic
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "edit_profile":
    edit_profile_page()
elif st.session_state.page == "main":
    main_page()
