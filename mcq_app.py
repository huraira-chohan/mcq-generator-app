import streamlit as st
import re
from random import sample, shuffle
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk import pos_tag

import nltk
import os

# Set custom download path for nltk_data inside the current directory
NLTK_DATA_DIR = os.path.join(os.path.dirname(__file__), "nltk_data")
nltk.data.path.append(NLTK_DATA_DIR)

# Download required resources if not already present
if not os.path.exists(os.path.join(NLTK_DATA_DIR, "corpora/stopwords")):
    nltk.download('stopwords', download_dir=NLTK_DATA_DIR)

if not os.path.exists(os.path.join(NLTK_DATA_DIR, "taggers/averaged_perceptron_tagger")):
    nltk.download('averaged_perceptron_tagger', download_dir=NLTK_DATA_DIR)

import nltk
nltk.data.path.append("/home/adminuser/.nltk_data")

nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words('english'))

# --- MCQ Generator ---
def generate_mcq_from_text(text, distractors=None):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    mcqs = []

    for sent in sentences:
        words = re.findall(r'\b\w+\b', sent)
        filtered = [w for w in words if w.lower() not in stop_words and len(w) > 4 and w.isalpha()]
        tagged = pos_tag(filtered)
        keywords = [word for word, tag in tagged if tag.startswith('NN')]  # use only nouns

        if not keywords:
            continue

        try:
            answer = sample(keywords, 1)[0]
        except:
            continue

        question = sent.replace(answer, '_____')
        other_words = list(set(filtered) - {answer})
        options = sample(other_words + (distractors or ['planet', 'system', 'light', 'orbit']), 3)
        options.append(answer)
        shuffle(options)

        mcqs.append({
            'question': question,
            'options': options,
            'answer': answer
        })

    return mcqs

# --- Streamlit UI ---
st.title("🧠 Smart MCQ Generator from File")

uploaded_file = st.file_uploader("📁 Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    file_type = uploaded_file.name.split('.')[-1]
    if file_type == "pdf":
        import fitz  # PyMuPDF
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "".join([page.get_text() for page in doc])
    else:
        text = uploaded_file.read().decode('utf-8')

    st.success("✅ File loaded. Click below to generate MCQs.")

    if st.button("🎯 Generate MCQs"):
        mcqs = generate_mcq_from_text(text)
        for i, mcq in enumerate(mcqs):
            st.markdown(f"**Q{i+1}:** {mcq['question']}")
            for j, opt in enumerate(mcq['options']):
                st.markdown(f"- {chr(65+j)}. {opt}")
            st.markdown(f"✅ **Answer:** {mcq['answer']}")
            st.markdown("---")

        # Download button
        df = pd.DataFrame(mcqs)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download MCQs as CSV", csv, "mcqs.csv", "text/csv")


