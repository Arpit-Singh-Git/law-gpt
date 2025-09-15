import streamlit as st
from openai import OpenAI

# NVIDIA API Key (replace with your actual key)
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
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NVIDIA_API_KEY
        )
        with st.spinner("🔍 Getting answer from NVIDIA LLM..."):
            try:
                # Stream the response for a more interactive UI
                completion = client.chat.completions.create(
                    model="nvidia/nvidia-nemotron-nano-9b-v2",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.6,
                    top_p=0.95,
                    max_tokens=2048,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stream=True,
                    extra_body={
                        "min_thinking_tokens": 1024,
                        "max_thinking_tokens": 2048
                    }
                )
                answer = ""
                answer_placeholder = st.empty()
                for chunk in completion:
                    reasoning = getattr(chunk.choices[0].delta, "reasoning_content", None)
                    content = chunk.choices[0].delta.content
                    if reasoning:
                        answer += reasoning
                    if content:
                        answer += content
                    answer_placeholder.markdown(f"<div class='big-font'>{answer}</div>", unsafe_allow_html=True)
                st.success("✅ Response:")
                st.code(answer, language="markdown")
            except Exception as e:
                st.error(f"❌ Error communicating with NVIDIA API: {str(e)}")
