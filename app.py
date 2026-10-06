import os
import requests
import streamlit as st
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI Question Paper Generator",
    page_icon="📝",
    layout="wide"
)

# -----------------------------
# Pydantic Models
# -----------------------------
class Question(BaseModel):
    number: int
    question: str
    marks: int = Field(gt=0)


class QuestionPaper(BaseModel):
    subject: str
    topic: str
    difficulty: str
    questions: list[Question]
    total_marks: int


# -----------------------------
# Question Generator
# -----------------------------
def generate_question_paper(subject, topic, difficulty, count, marks):

    question_templates = [
        f"What is {topic}? Explain with a suitable example.",
        f"Explain the important concepts of {topic}.",
        f"Discuss the applications of {topic}.",
        f"Explain the working of {topic} in detail.",
        f"What are the advantages and limitations of {topic}?",
        f"Compare the different concepts related to {topic}.",
        f"Write short notes on {topic}.",
        f"Explain {topic} with a suitable example.",
        f"Discuss the real-world applications of {topic}.",
        f"Describe the importance of {topic}."
    ]

    questions = []

    for i in range(count):
        question = Question(
            number=i + 1,
            question=question_templates[i % len(question_templates)],
            marks=marks
        )
        questions.append(question)

    paper = QuestionPaper(
        subject=subject,
        topic=topic,
        difficulty=difficulty,
        questions=questions,
        total_marks=count * marks
    )

    return paper


# -----------------------------
# Header
# -----------------------------
st.title("📝 AI Question Paper Generator")
st.write(
    "Generate a structured question paper based on subject, topic, "
    "difficulty level and marks."
)

st.divider()

# -----------------------------
# Input Section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    subject = st.text_input(
        "📚 Subject Name",
        placeholder="Example: Python Programming"
    )

    topic = st.text_input(
        "📖 Topic / Unit",
        placeholder="Example: Functions and Loops"
    )

with col2:
    difficulty = st.selectbox(
        "🎯 Difficulty Level",
        ["Easy", "Medium", "Hard"]
    )

    count = st.number_input(
        "🔢 Number of Questions",
        min_value=1,
        max_value=20,
        value=5
    )

marks = st.selectbox(
    "💯 Marks per Question",
    [2, 5, 10, 15]
)

st.divider()

# -----------------------------
# Generate Button
# -----------------------------
if st.button(
    "✨ Generate Question Paper",
    use_container_width=True
):

    if not subject.strip():
        st.error("Please enter the subject name.")

    elif not topic.strip():
        st.error("Please enter the topic.")

    else:

        with st.spinner("Generating question paper..."):

            paper = generate_question_paper(
                subject,
                topic,
                difficulty,
                count,
                marks
            )

        st.success("Question paper generated successfully!")

        # -----------------------------
        # Paper Information
        # -----------------------------
        st.subheader("📄 Generated Question Paper")

        info1, info2, info3, info4 = st.columns(4)

        with info1:
            st.metric("Subject", paper.subject)

        with info2:
            st.metric("Topic", paper.topic)

        with info3:
            st.metric("Difficulty", paper.difficulty)

        with info4:
            st.metric("Total Marks", paper.total_marks)

        st.divider()

        # -----------------------------
        # Questions
        # -----------------------------
        for q in paper.questions:

            st.write(
                f"**{q.number}. {q.question}**"
            )

            st.caption(f"Marks: {q.marks}")

            st.divider()

        # -----------------------------
        # Download Text File
        # -----------------------------
        paper_text = f"""
AI GENERATED QUESTION PAPER

Subject: {paper.subject}
Topic: {paper.topic}
Difficulty: {paper.difficulty}
Total Marks: {paper.total_marks}

QUESTIONS
"""

        for q in paper.questions:
            paper_text += (
                f"\n{q.number}. {q.question} "
                f"({q.marks} Marks)\n"
            )

        st.download_button(
            label="📥 Download Question Paper",
            data=paper_text,
            file_name="AI_Question_Paper.txt",
            mime="text/plain",
            use_container_width=True
        )

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "AI Question Paper Generator | Built with Python, Streamlit, "
    "Pydantic, Requests and python-dotenv"
)