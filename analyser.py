import PyPDF2

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