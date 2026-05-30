"""Streamlit dashboard with role-based student / educator views.

Run with:  streamlit run frontend/streamlit_app.py
Talks to the FastAPI backend (default http://localhost:8000).
"""
import os
import requests
import pandas as pd
import plotly.express as px
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="AI Learning Assistant",
                   page_icon="U0001F393", layout="wide")


# --------------------------- API helpers ---------------------------
def login(username, password):
    resp = requests.post(f"{API}/auth/login",
                         data={"username": username, "password": password})
    if resp.status_code == 200:
        return resp.json()
    return None


def api_get(path, token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(f"{API}{path}", headers=headers)
    resp.raise_for_status()
    return resp.json()


# --------------------------- Auth state ---------------------------
if "auth" not in st.session_state:
    st.session_state.auth = None


def login_view():
    st.title("U0001F393 AI Personalized Learning Assistant")
    st.caption("Sign in to your student or educator account.")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")
    if submitted:
        result = login(username, password)
        if result:
            st.session_state.auth = result
            st.session_state.username = username
            st.rerun()
        else:
            st.error("Invalid credentials. Try educator/educator123.")


# --------------------------- Student view ---------------------------
def student_dashboard(token, student_id):
    st.header("U0001F4DA My Learning Dashboard")
    progress = api_get(f"/students/{student_id}/progress", token)
    prediction = api_get(f"/analytics/predict/{student_id}", token)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Overall Progress", f"{progress['overall_progress']*100:.0f}%")
    c2.metric("Mastery Score", f"{progress['mastery_score']:.0f}")
    c3.metric("Projected Score", f"{prediction['projected_score']:.0f}")
    c4.metric("Pass Probability", f"{prediction['pass_probability']*100:.0f}%")

    risk = prediction["risk_level"]
    color = {"low": "green", "medium": "orange", "high": "red"}[risk]
    st.markdown(f"**Risk level:** :{color}[{risk.upper()}]")

    if progress["weak_topics"]:
        st.warning("Topics to focus on: " + ", ".join(progress["weak_topics"]))

    st.subheader("✨ Recommended Courses")
    recs = api_get(f"/recommendations/{student_id}", token)
    if recs:
        df = pd.DataFrame(recs)
        st.dataframe(df[["title", "subject", "score", "reason"]],
                     use_container_width=True, hide_index=True)

    st.subheader("U0001F5FA️ Your Optimized Learning Path")
    path = api_get(f"/recommendations/{student_id}/path", token)
    for step in path:
        st.write(f"**{step['order']}. {step['title']}** — "
                 f"difficulty {step['predicted_difficulty']:.2f}. {step['rationale']}")


# --------------------------- Educator view ---------------------------
def educator_dashboard(token):
    st.header("U0001F4CA Educator Analytics")
    cohort = api_get("/analytics/cohort", token)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Students", cohort.get("count", 0))
    c2.metric("Avg Score", f"{cohort.get('avg_score_mean', 0):.1f}")
    c3.metric("Avg Engagement", f"{cohort.get('engagement_mean', 0):.1f}")
    c4.metric("At Risk", cohort.get("at_risk_count", 0))

    dist = cohort.get("risk_distribution", {})
    if dist:
        fig = px.pie(names=list(dist.keys()), values=list(dist.values()),
                     title="Risk Distribution",
                     color=list(dist.keys()),
                     color_discrete_map={"low": "#2ecc71", "medium": "#f39c12",
                                         "high": "#e74c3c"})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("U0001F6A8 Intervention Recommendations")
    interventions = api_get("/analytics/interventions", token)
    if interventions:
        df = pd.DataFrame(interventions)
        st.dataframe(df[["name", "risk_level", "risk_score",
                         "recommended_action"]],
                     use_container_width=True, hide_index=True)


# --------------------------- Router ---------------------------
def main():
    if not st.session_state.auth:
        login_view()
        return

    auth = st.session_state.auth
    token = auth["access_token"]
    role = auth["role"]

    with st.sidebar:
        st.write(f"Signed in as **{st.session_state.get('username')}** ({role})")
        if st.button("Sign out"):
            st.session_state.auth = None
            st.rerun()

    if role == "educator":
        educator_dashboard(token)
        st.divider()
        st.subheader("Inspect an individual student")
        students = api_get("/students", token)
        if students:
            options = {f"{s['name']} (#{s['id']})": s['id'] for s in students}
            choice = st.selectbox("Student", list(options.keys()))
            student_dashboard(token, options[choice])
    else:
        students = api_get("/students", token)
        sid = students[0]["id"] if students else 1
        student_dashboard(token, sid)


if __name__ == "__main__":
    main()
