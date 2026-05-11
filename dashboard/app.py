import streamlit as st
import requests
import pandas as pd
from src.core.database import db_manager

st.set_page_config(page_title="LinkedIn Agent Dashboard", layout="wide")

# API URL (Local default)
API_URL = "http://localhost:8000/api"

st.sidebar.title("🚀 LinkedIn AI Agent")
page = st.sidebar.selectbox("Navigate", ["📊 Home", "📝 Review Drafts", "📜 History"])

def get_stats():
    try:
        return requests.get(f"{API_URL}/stats").json()
    except:
        return {"pending": 0, "approved": 0, "posted": 0, "rejected": 0}

def get_pending():
    try:
        return requests.get(f"{API_URL}/drafts/pending").json()
    except:
        return []

def approve_draft(draft_id):
    requests.post(f"{API_URL}/drafts/{draft_id}/approve")

def reject_draft(draft_id):
    requests.post(f"{API_URL}/drafts/{draft_id}/reject", json={"status": "rejected"})

if page == "📊 Home":
    st.header("System Statistics")
    stats = get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pending Review", stats['pending'])
    col2.metric("Approved", stats['approved'])
    col3.metric("Posted Live", stats['posted'])
    col4.metric("Rejected", stats['rejected'])

elif page == "📝 Review Drafts":
    st.header("Review & Approve Drafts")
    drafts = get_pending()
    
    if not drafts:
        st.info("No pending drafts. Run the agent to generate some!")
    else:
        for d in drafts:
            with st.container():
                st.subheader(f"{d['post_type']} Draft for: {d['signals']['title']}")
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.text_area("Post Content", d['content'], height=200, disabled=True)
                    st.write(f"🔗 Source: [Link]({d['signals']['url']})")
                
                with col2:
                    if d.get('visual_url'):
                        st.image(d['visual_url'], caption="Genuine Visual (macOS Frame)")
                    else:
                        st.warning("No visual generated for this draft.")
                
                b1, b2, _ = st.columns([1, 1, 4])
                if b1.button("✅ Approve", key=f"app_{d['id']}"):
                    approve_draft(d['id'])
                    st.success("Draft Approved!")
                    st.rerun()
                
                if b2.button("❌ Reject", key=f"rej_{d['id']}"):
                    reject_draft(d['id'])
                    st.error("Draft Rejected.")
                    st.rerun()
            st.divider()

elif page == "📜 History":
    st.header("Draft History")
    try:
        history = requests.get(f"{API_URL}/drafts/history").json()
        if history:
            df = pd.DataFrame(history)
            # Flatten signals title
            df['signal_title'] = df['signals'].apply(lambda x: x['title'] if x else 'N/A')
            st.table(df[['created_at', 'signal_title', 'post_type', 'status']])
        else:
            st.info("No history yet.")
    except:
        st.error("Failed to fetch history. Is the API running?")
