import streamlit as st
import requests

# 🔐 Embedded NVIDIA API Key (replace with your actual key)
NVIDIA_API_KEY = "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"

# Streamlit UI
st.set_page_config(page_title="LawGPT - Legal Q&A", layout="centered")
st.title("🧠 LawGPT - Legal Question Answering")
st.markdown(
    """
    <style>
    .big-font {font-size:22px !important;}
    .stTextArea textarea {font-size:18px;}
    </style>
    """, unsafe_allow_html=True
)
st.markdown("Ask law-based questions and get intelligent answers powered by NVIDIA's LLM.")

# Example questions for quick selection
with st.expander("💡 Example Questions"):
    cols = st.columns(2)
    examples = [
        "What are my rights if I am arrested in the US?",
        "How does intellectual property law protect inventions?",
        "What is the process for filing for divorce in California?",
        "Can an employer fire someone without notice?",
        "What are the GDPR requirements for data privacy?"
    ]
    for i, ex in enumerate(examples):
        if cols[i % 2].button(ex, key=f"ex_{i}"):
            st.session_state['question'] = ex

# Input field for the legal question
question = st.text_area("📜 Enter your legal question", value=st.session_state.get('question', ''))

# Option to select answer detail level
detail_level = st.radio(
    "How detailed should the answer be?",
    ["Brief", "Standard", "In-depth"],
    horizontal=True
)

# Option to select language
language = st.selectbox(
    "Select answer language",
    ["English", "Spanish", "French", "German", "Chinese"]
)

# Submit button
if st.button("Ask"):
    if not question.strip():
        st.warning("⚠️ Please enter a legal question before submitting.")
    else:
        # Add instructions for detail level and language
        system_prompt = f"Answer as a legal expert. Detail level: {detail_level}. Language: {language}."
        payload = {
            "model": "meta/llama3-70b-instruct",  # Use a known valid model name
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            "max_tokens": 1024,
            "temperature": 0.2
        }
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        with st.spinner("🔍 Getting answer from NVIDIA LLM..."):
            try:
                response = requests.post(
                    "https://integrate.api.nvidia.com/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                response.raise_for_status()
                result = response.json()
                answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                st.success("✅ Response:")
                st.markdown(f"<div class='big-font'>{answer}</div>", unsafe_allow_html=True)
                st.code(answer, language="markdown")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error communicating with NVIDIA API: {str(e)}")
