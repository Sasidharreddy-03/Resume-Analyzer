import PyPDF2 
from google import genai 
import os 
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()
    return text.lower()

def analyse(resume_text, job_desc):
    job_words = set(job_desc.lower().split())
    resume_words = set(resume_text.split())
    stopwords = {'and','the','to','of','a','in','is','for','with','on','at','an','be','as','by'}
    job_words = job_words - stopwords
    matched = job_words & resume_words
    missing = job_words - resume_words
    score = int((len(matched) / len(job_words)) * 100) if job_words else 0
    return {
        'score': score,
        'matched': sorted(list(matched))[:15],
        'missing': sorted(list(missing))[:15]
    }

def get_ai_suggestions(resume_text, job_desc, missing_keywords):
    try:
        prompt = f"""
You are a resume coach helping an Indian engineering student get placed.
Resume: {resume_text[:1500]}
Job description: {job_desc[:800]}
Missing keywords: {', '.join(missing_keywords)}
Give exactly 4 specific actionable tips numbered like:
1. tip
2. tip
3. tip
4. tip
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        tips = response.text.strip().split('\n')
        tips = [t.strip() for t in tips if t.strip() and len(t) > 3 and t[0].isdigit()]
        return tips[:4]
    except BaseException as e:
        print("AI tips error:", e)
        return [
            "1. Add missing keywords naturally into your experience section",
            "2. Quantify your achievements with numbers where possible",
            "3. Tailor your resume summary to match this specific role",
            "4. Add a skills section that mirrors the job description language"
        ]

def get_interview_questions(job_desc, resume_text):
    try:
        prompt = f"""
You are a technical interviewer at an Indian tech company.
Job description: {job_desc[:800]}
Candidate resume: {resume_text[:800]}
Generate exactly 5 technical interview questions numbered like:
1. question
2. question
3. question
4. question
5. question
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        questions = response.text.strip().split('\n')
        questions = [q.strip() for q in questions if q.strip() and len(q) > 3 and q[0].isdigit()]
        return questions[:5]
    except BaseException as e:
        print("AI questions error:", e)
        return [
            "1. Explain the difference between REST and SOAP APIs",
            "2. How does JWT authentication work?",
            "3. What is ORM and why do we use it?",
            "4. Explain the difference between SQL and NoSQL databases",
            "5. How would you optimize a slow database query?"
        ]
