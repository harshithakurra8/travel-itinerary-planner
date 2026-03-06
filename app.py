import streamlit as st
import sys, os, time

# ── Page config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="✈️ Travel Itinerary Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Background ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #1a1060 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, #0d2640 0%, transparent 50%),
                #0a0e1a !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* ── Typography ── */
* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3 { font-family: 'Playfair Display', serif !important; }

/* ── Hero Section ── */
.hero-wrapper {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.3em;
    text-transform: uppercase;
    color: #f0a500;
    margin-bottom: 0.8rem;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: clamp(2.4rem, 6vw, 4.2rem);
    font-weight: 900;
    line-height: 1.1;
    color: #ffffff;
    margin: 0 0 1rem;
}
.hero-title span {
    background: linear-gradient(135deg, #f0a500 0%, #ff6b35 50%, #e91e8c 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 1.05rem;
    font-weight: 300;
    color: #8899bb;
    max-width: 520px;
    margin: 0 auto 2rem;
    line-height: 1.65;
}
.hero-divider {
    width: 60px; height: 3px;
    background: linear-gradient(90deg, #f0a500, #e91e8c);
    border-radius: 2px;
    margin: 0 auto 2.5rem;
}

/* ── Form Card ── */
.form-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 2rem 2.2rem;
    backdrop-filter: blur(12px);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    margin-bottom: 1.5rem;
}
.form-section-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #f0a500;
    margin-bottom: 1rem;
}

/* ── Streamlit input overrides ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div,
[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.92) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 10px !important;
    color: #111111 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: #f0a500 !important;
    box-shadow: 0 0 0 2px rgba(240,165,0,0.2) !important;
}
label, .stTextInput label, .stSelectbox label {
    color: #aabbdd !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}

/* ── Budget Pills ── */
.budget-row { display: flex; gap: 0.7rem; margin-top: 0.5rem; }
.budget-pill {
    flex: 1; text-align: center; padding: 0.6rem 0.5rem;
    border-radius: 10px; font-size: 0.85rem; font-weight: 600;
    cursor: pointer; transition: all 0.2s;
    border: 1px solid rgba(255,255,255,0.1);
}

/* ── CTA Button ── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #f0a500 0%, #ff6b35 50%, #e91e8c 100%) !important;
    color: #fff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.5rem !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(240,107,53,0.35) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(240,107,53,0.5) !important;
}
.stButton > button:active { transform: translateY(0px) !important; }

/* ── Agent Step Cards ── */
.step-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-left: 3px solid;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.9rem;
    transition: all 0.3s;
}
.step-card.running  { border-left-color: #f0a500; background: rgba(240,165,0,0.06); }
.step-card.done     { border-left-color: #22c55e; background: rgba(34,197,94,0.05); }
.step-card.idle     { border-left-color: rgba(255,255,255,0.15); }
.step-card.error    { border-left-color: #ef4444; background: rgba(239,68,68,0.06); }
.step-title {
    font-weight: 600; font-size: 0.9rem; color: #e8eeff; margin-bottom: 0.2rem;
}
.step-status { font-size: 0.78rem; color: #6677aa; }
.step-status.running { color: #f0a500; }
.step-status.done    { color: #22c55e; }
.step-status.error   { color: #ef4444; }

/* ── Result Sections ── */
.result-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    margin: 1.5rem 0 0.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.result-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    color: #c8d8f0;
    font-size: 0.92rem;
    line-height: 1.75;
    white-space: pre-wrap;
    margin-bottom: 1rem;
}
.result-box.highlight {
    border-color: rgba(240,165,0,0.3);
    background: rgba(240,165,0,0.05);
}

/* ── Error Banner ── */
.error-banner {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    color: #fca5a5;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* ── Stats Row ── */
.stats-row {
    display: flex; gap: 1rem; margin: 1.5rem 0;
    flex-wrap: wrap;
}
.stat-chip {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    padding: 0.45rem 1rem;
    font-size: 0.8rem;
    color: #aabbdd;
    font-weight: 500;
}
.stat-chip span { color: #f0a500; font-weight: 600; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(10,14,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}

/* ── Misc ── */
.divider { height: 1px; background: rgba(255,255,255,0.07); margin: 1.5rem 0; }
hr { border-color: rgba(255,255,255,0.07) !important; }
[data-testid="stMarkdownContainer"] p { color: #8899bb; }
</style>
""", unsafe_allow_html=True)

# ── Lazy imports (after env is loaded) ────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

# ── Session state init ────────────────────────────────────────────────────────
for key in ["result", "running", "error"]:
    if key not in st.session_state:
        st.session_state[key] = None
if "running" not in st.session_state:
    st.session_state.running = False

# ══════════════════════════════════════════════════════════════════════════════
# HERO
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-wrapper">
  <div class="hero-eyebrow">✈️ AI-Powered Travel Planning</div>
  <h1 class="hero-title">Plan Your Dream Trip<br>with <span>Intelligent Agents</span></h1>
  <p class="hero-sub">
    A multi-agent pipeline powered by LLaMA 3.3 · 70B — each specialist crafts
    hotels, meals, activities, transport & budget tailored to your journey.
  </p>
  <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LAYOUT
# ══════════════════════════════════════════════════════════════════════════════
left_col, right_col = st.columns([1, 1.4], gap="large")

# ─────────────────────────────────────────────────────────────────────────────
# LEFT — INPUT FORM
# ─────────────────────────────────────────────────────────────────────────────
with left_col:
    st.markdown('<div class="form-section-label">🗺️ Trip Details</div>', unsafe_allow_html=True)

    destination = st.text_input(
        "Destination",
        placeholder="e.g. Tokyo, Paris, New York…",
        help="Enter any city, country, or region"
    )
    duration = st.text_input(
        "Trip Duration",
        placeholder="e.g. 5 days, 1 week, 10 days…"
    )

    st.markdown('<div class="form-section-label" style="margin-top:1.2rem">💰 Budget Level</div>', unsafe_allow_html=True)
    budget = st.selectbox(
        "Budget",
        options=["medium", "low", "high"],
        format_func=lambda x: {"low": "🟢 Low — Budget-friendly", "medium": "🟡 Medium — Comfort", "high": "🔴 High — Luxury"}[x],
        label_visibility="collapsed"
    )

    st.markdown('<div class="form-section-label" style="margin-top:1.2rem">🎯 Travel Interests</div>', unsafe_allow_html=True)

    # Interest tag checkboxes
    interest_options = {
        "🎨 Art & Culture": "art, culture",
        "🍜 Food & Dining": "food, dining",
        "🏛️ History": "history",
        "🏞️ Nature": "nature, outdoors",
        "🛍️ Shopping": "shopping",
        "🎵 Music & Nightlife": "music, nightlife",
        "🧘 Wellness & Spa": "wellness, spa",
        "🏄 Adventure": "adventure, sports",
    }
    cols_a, cols_b = st.columns(2)
    selected_interests = []
    items = list(interest_options.items())
    for i, (label, val) in enumerate(items):
        col = cols_a if i % 2 == 0 else cols_b
        if col.checkbox(label, key=f"interest_{i}"):
            selected_interests.append(val)

    custom_interest = st.text_input(
        "Or type your own interests",
        placeholder="e.g. photography, architecture…"
    )

    interests_final = ", ".join(selected_interests)
    if custom_interest.strip():
        interests_final = (interests_final + ", " + custom_interest.strip()).strip(", ")

    st.markdown('<div style="margin-top:1.5rem"></div>', unsafe_allow_html=True)
    generate_btn = st.button("🚀 Generate My Itinerary", use_container_width=True)

    # ── Quick example chips ────────────────────────────────────────────────
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="form-section-label">✨ Quick Examples</div>', unsafe_allow_html=True)
    ex_col1, ex_col2, ex_col3 = st.columns(3)
    if ex_col1.button("🗼 Paris", use_container_width=True):
        st.session_state["_ex"] = ("Paris", "5 days", "medium", "art, food, history")
    if ex_col2.button("🗾 Tokyo", use_container_width=True):
        st.session_state["_ex"] = ("Tokyo", "7 days", "medium", "food, culture, technology")
    if ex_col3.button("🏝️ Bali", use_container_width=True):
        st.session_state["_ex"] = ("Bali", "6 days", "low", "nature, wellness, adventure")

    # Apply quick example pre-fill hint
    if "_ex" in st.session_state:
        ex = st.session_state["_ex"]
        st.info(f"💡 **{ex[0]}** — {ex[1]} · {ex[2]} budget · {ex[3]}\n\nFill the form above with these values and click Generate!")


# ─────────────────────────────────────────────────────────────────────────────
# RIGHT — PIPELINE STATUS + RESULTS
# ─────────────────────────────────────────────────────────────────────────────
with right_col:

    AGENTS = [
        ("🔍", "Validator",  "Checking your travel details"),
        ("🏨", "Hotels",     "Finding the best stays"),
        ("🍽️", "Meals",      "Crafting daily food plan"),
        ("🎯", "Activities", "Scheduling experiences"),
        ("🚌", "Transport",  "Mapping local transit"),
        ("💰", "Budget",     "Calculating trip costs"),
        ("📋", "Itinerary",  "Compiling your report"),
    ]

    # ── Generate on click ─────────────────────────────────────────────────
    if generate_btn:
        if not destination.strip():
            st.error("⚠️ Please enter a destination.")
        elif not duration.strip():
            st.error("⚠️ Please enter trip duration.")
        elif not interests_final.strip():
            st.error("⚠️ Please select or type at least one interest.")
        else:
            st.session_state.result = None
            st.session_state.error  = None

            user_input = {
                "destination": destination.strip(),
                "duration":    duration.strip(),
                "budget":      budget,
                "interests":   interests_final,
            }

            # ── Live pipeline status ───────────────────────────────────────
            st.markdown('<div class="form-section-label">⚙️ Pipeline Status</div>', unsafe_allow_html=True)
            status_slots = [st.empty() for _ in AGENTS]

            def render_agents(active_idx, statuses):
                for i, (icon, name, desc) in enumerate(AGENTS):
                    s = statuses.get(i, "idle")
                    status_label = {"idle": "Waiting…", "running": "Running…", "done": "Complete ✓", "error": "Error ✗"}.get(s, "")
                    status_slots[i].markdown(f"""
                    <div class="step-card {s}">
                      <div class="step-title">{icon} {name}</div>
                      <div class="step-status {s}">{status_label} — {desc}</div>
                    </div>""", unsafe_allow_html=True)

            statuses = {i: "idle" for i in range(len(AGENTS))}
            render_agents(-1, statuses)

            # ── Patch agents to update UI live ────────────────────────────
            import agents.validator_agent  as va_mod
            import agents.hotel_agent      as ha_mod
            import agents.meal_agent       as ma_mod
            import agents.activity_agent   as aa_mod
            import agents.transport_agent  as ta_mod
            import agents.budget_agent     as ba_mod
            import agents.final_agent      as fa_mod

            orig_validate   = va_mod.validate_input
            orig_hotel      = ha_mod.hotel_agent
            orig_meal       = ma_mod.meal_agent
            orig_activity   = aa_mod.activity_agent
            orig_transport  = ta_mod.transport_agent
            orig_budget     = ba_mod.budget_agent
            orig_final      = fa_mod.final_agent

            def make_wrapper(fn, idx):
                def wrapper(state):
                    statuses[idx] = "running"
                    render_agents(idx, statuses)
                    try:
                        result = fn(state)
                        statuses[idx] = "done"
                    except Exception as e:
                        statuses[idx] = "error"
                        render_agents(idx, statuses)
                        raise e
                    render_agents(idx, statuses)
                    return result
                return wrapper

            va_mod.validate_input  = make_wrapper(orig_validate,  0)
            ha_mod.hotel_agent     = make_wrapper(orig_hotel,     1)
            ma_mod.meal_agent      = make_wrapper(orig_meal,      2)
            aa_mod.activity_agent  = make_wrapper(orig_activity,  3)
            ta_mod.transport_agent = make_wrapper(orig_transport, 4)
            ba_mod.budget_agent    = make_wrapper(orig_budget,    5)
            fa_mod.final_agent     = make_wrapper(orig_final,     6)

            # Re-import workflow so it picks up patched agents
            import importlib
            import graph.workflow as wf_mod
            importlib.reload(wf_mod)

            try:
                result = wf_mod.graph.invoke({"input": user_input})
                st.session_state.result = result
                if result.get("error") and not result.get("final_itinerary"):
                    st.session_state.error = result["error"]
            except Exception as e:
                st.session_state.error = str(e)
            finally:
                # Restore originals
                va_mod.validate_input  = orig_validate
                ha_mod.hotel_agent     = orig_hotel
                ma_mod.meal_agent      = orig_meal
                aa_mod.activity_agent  = orig_activity
                ta_mod.transport_agent = orig_transport
                ba_mod.budget_agent    = orig_budget
                fa_mod.final_agent     = orig_final

    # ── Show error ────────────────────────────────────────────────────────
    if st.session_state.error:
        st.markdown(f"""
        <div class="error-banner">
          <strong>🚨 Could not generate itinerary</strong><br><br>
          {st.session_state.error}
        </div>""", unsafe_allow_html=True)

    # ── Show results ──────────────────────────────────────────────────────
    elif st.session_state.result and st.session_state.result.get("final_itinerary"):
        r = st.session_state.result
        vi = r.get("validated_input", {})

        # Trip overview chips
        st.markdown(f"""
        <div class="stats-row">
          <div class="stat-chip">📍 <span>{vi.get('destination','')}</span></div>
          <div class="stat-chip">📅 <span>{vi.get('duration','')}</span></div>
          <div class="stat-chip">💵 <span>{vi.get('budget','').title()} Budget</span></div>
          <div class="stat-chip">🎯 <span>{vi.get('interests','')}</span></div>
        </div>
        """, unsafe_allow_html=True)

        # Tabs for each section
        tabs = st.tabs(["🗺️ Full Itinerary", "🏨 Hotels", "🍽️ Meals", "🎯 Activities", "🚌 Transport", "💰 Budget"])

        with tabs[0]:
            st.markdown('<div class="result-box highlight">' + r.get("final_itinerary","").replace("\n","<br>") + '</div>', unsafe_allow_html=True)
            # Download button
            st.download_button(
                label="⬇️ Download Itinerary (.txt)",
                data=r.get("final_itinerary",""),
                file_name=f"itinerary_{vi.get('destination','trip').lower().replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with tabs[1]:
            st.markdown('<div class="result-box">' + (r.get("hotels","") or "N/A").replace("\n","<br>") + '</div>', unsafe_allow_html=True)

        with tabs[2]:
            st.markdown('<div class="result-box">' + (r.get("meals","") or "N/A").replace("\n","<br>") + '</div>', unsafe_allow_html=True)

        with tabs[3]:
            st.markdown('<div class="result-box">' + (r.get("activities","") or "N/A").replace("\n","<br>") + '</div>', unsafe_allow_html=True)

        with tabs[4]:
            st.markdown('<div class="result-box">' + (r.get("transport","") or "N/A").replace("\n","<br>") + '</div>', unsafe_allow_html=True)

        with tabs[5]:
            st.markdown('<div class="result-box">' + (r.get("budget_estimate","") or "N/A").replace("\n","<br>") + '</div>', unsafe_allow_html=True)

    else:
        # Empty state illustration
        st.markdown("""
        <div style="text-align:center; padding: 4rem 2rem; color: #445577;">
          <div style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.4;">🗺️</div>
          <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #334466; margin-bottom: 0.5rem;">
            Your itinerary will appear here
          </div>
          <div style="font-size: 0.85rem; color: #334466;">
            Fill in your trip details and click <strong style="color:#f0a500">Generate My Itinerary</strong>
          </div>
        </div>
        """, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:3rem; padding: 1.5rem; border-top: 1px solid rgba(255,255,255,0.06);">
  <p style="color:#334466; font-size:0.8rem; margin:0;">
    Powered by <strong style="color:#f0a500">LLaMA 3.3 · 70B</strong> via Groq &nbsp;·&nbsp;
    Built with <strong style="color:#f0a500">LangGraph</strong> multi-agent pipeline &nbsp;·&nbsp;
    UI by <strong style="color:#f0a500">Streamlit</strong>
  </p>
</div>
""", unsafe_allow_html=True)
