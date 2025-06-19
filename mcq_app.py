import streamlit as st
import re
from random import sample, shuffle
import pandas as pd

def simple_sent_tokenize(text):
    return re.split(r'(?<=[.!?])\s+', text)

def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text)

def generate_mcq_from_text(text, distractors=None):
    sentences = simple_sent_tokenize(text)
    mcqs = []

    for sent in sentences:
        words = simple_word_tokenize(sent)
        keywords = [w for w in words if w.isalpha() and len(w) > 4]

        if not keywords:
            continue
        
        try:
            answer = sample(keywords, 1)[0]
        except:
            continue

        question = sent.replace(answer, '_____')
        other_words = list(set(keywords) - {answer})
        options = sample(other_words + (distractors or ['sun', 'earth', 'moon', 'star']), 3)
        options.append(answer)
        shuffle(options)

        mcqs.append({
            'question': question,
            'options': options,
            'answer': answer
        })

    return mcqs

st.title("🧠 Automatic MCQ Generator")

uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "pdf":
        import fitz
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
    else:
        text = uploaded_file.read().decode('utf-8')

    if st.button("Generate MCQs"):
        mcqs = generate_mcq_from_text(text)
        for i, mcq in enumerate(mcqs):
            st.markdown(f"**Q{i+1}:** {mcq['question']}")
            for j, opt in enumerate(mcq['options']):
                st.markdown(f"- {chr(65+j)}. {opt}")
            st.markdown(f"✅ **Answer:** {mcq['answer']}")
        
        # Option to download
        df = pd.DataFrame(mcqs)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download MCQs as CSV", csv, "mcqs.csv", "text/csv")


