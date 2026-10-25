import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from pathlib import Path
from datetime import datetime

st.set_page_config(
    page_title="FloodSafe",
    page_icon="🌊",
    layout="wide"
)

# ---------- DATA STORAGE ----------
Path("data").mkdir(exist_ok=True)
REPORTS = Path("data/reports.csv")

# ---------- COLOURFUL UI ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&display=swap');

.stApp {
 background:radial-gradient(circle at top left,#164c70,#10152f 48%,#070d1b);
 color:#f4f8ff;
 font-family:'Manrope',sans-serif;
}
[data-testid="stSidebar"] {
 background:linear-gradient(180deg,#111c38,#071321);
 border-right:1px solid #35456d;
}
.block-container {max-width:1450px;padding-top:1.5rem;}
.hero {
 padding:30px;border-radius:24px;margin-bottom:22px;
 background:linear-gradient(120deg,#00a6c7,#3559bd,#853ac6,#00a6c7);
 background-size:300% 300%;
 animation:flow 9s ease infinite;
 border:1px solid #80eaff;
 box-shadow:0 8px 35px #00d9ff25;
}
.hero h1 {font-size:38px;color:white;}
.hero p {color:#f0f6ff;}
@keyframes flow {
 0% {background-position:0% 50%}
 50% {background-position:100% 50%}
 100% {background-position:0% 50%}
}
.metric {
 padding:20px;border-radius:18px;
 background:linear-gradient(140deg,#182d50,#172039);
 border:1px solid #40547a;
 transition:all .25s ease;
 min-height:120px;
}
.metric:hover {
 transform:translateY(-5px);
 border-color:#36e7f5;
 box-shadow:0 8px 25px #19d9ef25;
}
.value {font-size:29px;font-weight:800;color:white;margin:8px 0;}
.label {color:#bacbe7;font-size:13px;}
.note {color:#4de7d3;font-size:12px;}
.stButton>button,.stDownloadButton>button {
 background:linear-gradient(100deg,#008ba8,#7445bd);
 color:white;border:1px solid #60d9f3;
 border-radius:10px;font-weight:700;
 transition:all .2s;
}
.stButton>button:hover {
 transform:translateY(-2px);
 box-shadow:0 5px 18px #00c8ff55;
 color:white;
}
div[data-testid="stForm"] {
 background:#14213bcc;
 border:1px solid #394d70;
 border-radius:16px;padding:18px;
}
</style>
""", unsafe_allow_html=True)


# ---------- DEMO LOCATIONS ----------
@st.cache_data
def get_data():
    rng = np.random.default_rng(42)
    places = [
        ("Guntur",16.3067,80.4365),
        ("Vijayawada",16.5062,80.6480),
        ("Amaravati",16.5417,80.5150),
        ("Tenali",16.2430,80.6400),
        ("Mangalagiri",16.4300,80.5600),
        ("Bapatla",15.9040,80.4670),
        ("Repalle",16.0190,80.8300),
        ("Ongole",15.5057,80.0499),
        ("Eluru",16.7107,81.0952),
        ("Nandigama",16.7710,80.2850)
    ]

    rows = []
    for name,lat,lon in places:
        rain = int(rng.integers(5,145))
        water = int(rng.integers(10,190))
        score = min(100,int(rain*.42+water*.32+rng.integers(0,22)))
        risk = "High" if score>=70 else "Moderate" if score>=42 else "Low"

        rows.append({
            "Location":name,
            "Latitude":lat,
            "Longitude":lon,
            "Rainfall (mm)":rain,
            "Water level (cm)":water,
            "Risk score":score,
            "Risk level":risk
        })

    return pd.DataFrame(rows)


def read_reports():
    if REPORTS.exists():
        try:
            return pd.read_csv(REPORTS)
        except Exception:
            pass
    return pd.DataFrame(columns=[
        "Report ID","Time","Reporter","Location",
        "Latitude","Longitude","Water depth (cm)",
        "Severity","Description"
    ])


def card(title,value,subtitle,emoji):
    st.markdown(f"""
    <div class="metric">
      <div class="label">{emoji} {title}</div>
      <div class="value">{value}</div>
      <div class="note">{subtitle}</div>
    </div>
    """,unsafe_allow_html=True)


# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("# 🌊 FloodSafe")
    st.caption("SMART FLOOD AWARENESS")
    page = st.radio("MENU",[
        "🏠 Dashboard",
        "🗺️ Risk Map",
        "📊 Analytics",
        "📣 Reports",
        "🛟 Safety Quiz"
    ])
    st.divider()

    location = st.selectbox("Filter location",[
        "All locations","Guntur","Vijayawada","Amaravati",
        "Tenali","Mangalagiri","Bapatla","Repalle",
        "Ongole","Eluru","Nandigama"
    ])

    if st.button("🔄 Refresh dashboard"):
        st.cache_data.clear()
        st.rerun()

    st.caption("Sample data is illustrative, not official alerts.")


df = get_data()
if location != "All locations":
    df = df[df["Location"] == location]

reports = read_reports()

st.markdown("""
<div class="hero">
 <h1>🌊 FloodSafe Intelligence</h1>
 <p>Explore flood-risk indicators, interactive maps, community reports
 and safety information in one place.</p>
 <b>📍 Regional insights &nbsp; • &nbsp; 📈 Live interactions &nbsp; • &nbsp; 🛡️ Preparedness</b>
</div>
""",unsafe_allow_html=True)

st.caption(f"Dashboard opened: {datetime.now():%d %b %Y, %I:%M %p}")


# ========== DASHBOARD ==========
if page == "🏠 Dashboard":
    st.subheader("✨ Situation Overview")

    high = int((df["Risk level"]=="High").sum())
    avg_rain = int(df["Rainfall (mm)"].mean())
    avg_water = int(df["Water level (cm)"].mean())

    a,b,c,d = st.columns(4)
    with a:
        card("Community Reports",len(reports),"Saved on this computer","📣")
    with b:
        card("High-risk sample areas",high,"Demo calculation only","🔴")
    with c:
        card("Average Rainfall",f"{avg_rain} mm","Illustrative data","🌧️")
    with d:
        card("Average Water Level",f"{avg_water} cm","Illustrative data","🌊")

    left,right = st.columns([1.2,1])

    with left:
        st.markdown("### 🌈 Rainfall by location")
        fig = px.bar(
            df.sort_values("Rainfall (mm)"),
            x="Rainfall (mm)",y="Location",
            orientation="h",color="Risk level",
            color_discrete_map={
                "Low":"#36dfae",
                "Moderate":"#ffbd59",
                "High":"#ff5577"
            },template="plotly_dark",
            hover_data=["Water level (cm)","Risk score"]
        )
        fig.update_layout(
            height=420,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig,use_container_width=True)

    with right:
        st.markdown("### 🎯 Risk distribution")
        counts = df["Risk level"].value_counts().reindex(
            ["Low","Moderate","High"],fill_value=0
        ).rename_axis("Risk").reset_index(name="Areas")

        fig = px.pie(
            counts,names="Risk",values="Areas",hole=.62,
            color="Risk",
            color_discrete_map={
                "Low":"#36dfae",
                "Moderate":"#ffbd59",
                "High":"#ff5577"
            },template="plotly_dark"
        )
        fig.update_layout(
            height=420,paper_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig,use_container_width=True)

    st.markdown("### 📍 Location overview")
    st.dataframe(df,use_container_width=True,hide_index=True)

    st.markdown("### 📣 Recent reports")
    if reports.empty:
        st.info("No reports submitted yet.")
    else:
        st.dataframe(
            reports.tail(5).iloc[::-1],
            use_container_width=True,hide_index=True
        )


# ========== RISK MAP ==========
elif page == "🗺️ Risk Map":
    st.subheader("🗺️ Interactive Regional Risk Map")
    st.caption("Map needs internet. All marker values are demo data.")

    fig = px.scatter_map(
        df,lat="Latitude",lon="Longitude",
        hover_name="Location",
        hover_data=[
            "Rainfall (mm)","Water level (cm)",
            "Risk score","Risk level"
        ],
        color="Risk level",size="Risk score",size_max=30,
        zoom=7,center={"lat":16.25,"lon":80.55},
        map_style="carto-darkmatter",
        color_discrete_map={
            "Low":"#c6df36",
            "Moderate":"#5977ff",
            "High":"#811927"
        }
    )
    fig.update_layout(
        height=600,margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig,use_container_width=True)

    chosen = st.selectbox("Explore an area",df["Location"].tolist())
    item = df[df["Location"]==chosen].iloc[0]
    x,y,z = st.columns(3)
    with x:
        card("Rainfall",f"{item['Rainfall (mm)']} mm","Sample value","🌧️")
    with y:
        card("Water level",f"{item['Water level (cm)']} cm","Sample value","🌊")
    with z:
        card("Risk score",f"{item['Risk score']}/100",item["Risk level"],"📍")


# ========== ANALYTICS ==========
elif page == "📊 Analytics":
    st.subheader("📊 Interactive Analytics Studio")

    measure = st.selectbox("Select metric",[
        "Rainfall (mm)","Water level (cm)","Risk score"
    ])
    style = st.radio(
        "Chart style",["Bar","Line","Area"],
        horizontal=True
    )

    if style == "Bar":
        fig = px.bar(
            df,x="Location",y=measure,color="Risk level",
            color_discrete_map={
                "Low":"#36dfae",
                "Moderate":"#ffbd59",
                "High":"#ff5577"
            },template="plotly_dark"
        )
    elif style == "Line":
        fig = px.line(
            df,x="Location",y=measure,markers=True,
            color_discrete_sequence=["#48e5f2"],
            template="plotly_dark"
        )
    else:
        fig = px.area(
            df,x="Location",y=measure,
            color_discrete_sequence=["#9c7cff"],
            template="plotly_dark"
        )

    fig.update_layout(
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("### 🌧️ Rainfall vs Water Level")
    scatter = px.scatter(
        df,x="Rainfall (mm)",y="Water level (cm)",
        size="Risk score",color="Risk level",
        hover_name="Location",
        color_discrete_map={
            "Low":"#36dfae",
            "Moderate":"#ffbd59",
            "High":"#ff5577"
        },template="plotly_dark"
    )
    scatter.update_layout(
        height=420,paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(scatter,use_container_width=True)

    st.download_button(
        "⬇️ Download location data",
        df.to_csv(index=False).encode("utf-8"),
        "floodsafe_data.csv","text/csv"
    )


# ========== COMMUNITY REPORTS ==========
elif page == "📣 Reports":
    st.subheader("📣 Community Flood Report")
    st.write("Report an observation. Avoid entering private details.")

    with st.form("report_form",clear_on_submit=True):
        a,b = st.columns(2)

        with a:
            reporter = st.text_input("Name or alias (optional)")
            place = st.text_input("Location / landmark *")
            lat = st.number_input(
                "Latitude",min_value=-90.0,max_value=90.0,
                value=16.3067,format="%.5f"
            )
            lon = st.number_input(
                "Longitude",min_value=-180.0,max_value=180.0,
                value=80.4365,format="%.5f"
            )

        with b:
            depth = st.number_input(
                "Water depth (cm)",min_value=0,max_value=500,
                value=0,step=5
            )
            severity = st.selectbox("Situation",[
                "Low - water on road",
                "Moderate - difficult to pass",
                "High - unsafe or fast-moving water"
            ])
            description = st.text_area("What did you observe?")

        submit = st.form_submit_button("🚀 Submit report")

    if submit:
        if not place.strip():
            st.error("Please enter a location.")
        else:
            row = {
                "Report ID":datetime.now().strftime("FS%Y%m%d%H%M%S%f"),
                "Time":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Reporter":reporter.strip() or "Anonymous",
                "Location":place.strip(),
                "Latitude":lat,
                "Longitude":lon,
                "Water depth (cm)":depth,
                "Severity":severity,
                "Description":description.strip()
            }
            new = pd.concat(
                [read_reports(),pd.DataFrame([row])],
                ignore_index=True
            )
            new.to_csv(REPORTS,index=False)
            st.success("Report saved successfully on this computer!")
            st.rerun()

    st.markdown("### 📋 Saved reports")
    reports = read_reports()

    if reports.empty:
        st.info("No reports yet.")
    else:
        st.dataframe(
            reports.iloc[::-1],
            use_container_width=True,hide_index=True
        )
        st.download_button(
            "⬇️ Export reports to CSV",
            reports.to_csv(index=False).encode("utf-8"),
            "floodsafe_reports.csv","text/csv"
        )


# ========== SAFETY QUIZ ==========
elif page == "🛟 Safety Quiz":
    st.subheader("🛟 Flood Safety Challenge")
    st.write("Test your flood-safety knowledge!")

    questions = [
        (
            "What should you do if floodwater covers a road?",
            ["Drive through quickly","Avoid crossing and find a safe route","Walk through it"],
            1,
            "Never walk or drive through floodwater."
        ),
        (
            "Where should you move if officials advise evacuation?",
            ["Higher, safer ground","A basement","Near a river"],
            0,
            "Follow official evacuation advice and move to safer ground."
        ),
        (
            "What should be ready in an emergency kit?",
            ["Only snacks","Water, torch, medicines and phone","Heavy furniture"],
            1,
            "Keep essential supplies ready in advance."
        ),
        (
            "When should you return after a flood?",
            ["As soon as rain stops","When authorities say it is safe","Whenever the road looks dry"],
            1,
            "Wait for official safety guidance."
        )
    ]

    answers = []
    with st.form("quiz"):
        for i,(question,options,correct,explanation) in enumerate(questions):
            st.markdown(f"#### {i+1}. {question}")
            answer = st.radio(
                "Choose an answer",
                options,key=f"q{i}"
            )
            answers.append(options.index(answer))
        check = st.form_submit_button("✨ Check my score")

    if check:
        score = sum(
            answers[i] == q[2]
            for i,q in enumerate(questions)
        )
        st.markdown(f"## 🏆 Your score: {score}/{len(questions)}")
        if score == len(questions):
            st.balloons()
            st.success("Excellent! You know these safety basics.")
        elif score >= 2:
            st.success("Good work! Review the explanations below.")
        else:
            st.info("Keep learning! Review the safety tips below.")

        for i,q in enumerate(questions):
            if answers[i] == q[2]:
                st.write(f"✅ {i+1}. {q[3]}")
            else:
                st.write(f"📘 {i+1}. Correct answer: {q[1][q[2]]}. {q[3]}")


# ========== FOOTER ==========
st.divider()
st.caption(
    "🌊 FloodSafe prototype | Sample readings are simulated, "
    "not live sensor data or official flood predictions. "
    "Follow local authorities for real emergency warnings."
)