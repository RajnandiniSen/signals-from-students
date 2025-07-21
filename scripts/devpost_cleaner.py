import pandas as pd
import re

# Load enriched data
df = pd.read_csv("data/devpost_projects_enriched.csv")
df = df.dropna(subset=["title", "url", "short_description"])

# --- CLEANING TEXT FIELDS ---

# Clean and title-case short_description
df["short_description"] = df["short_description"].astype(str).str.strip().str.title()

# Normalize submitted_to
def normalize_submitted_to(value):
    if not isinstance(value, str):
        return ""
    value = value.strip()
    value = re.sub(r'\b(Hackathon|Hack)\b', '', value).strip()
    value = re.sub(r'\s+\d{4}$', '', value)  # Remove trailing year
    return value

df["submitted_to"] = df["submitted_to"].apply(normalize_submitted_to)

# Normalize and clean built_with
def clean_built_with(tags):
    if isinstance(tags, str):
        tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
    if not isinstance(tags, list):
        return []
    return [re.sub(r"[^a-zA-Z0-9+#]", "", tag.strip().lower()) for tag in tags if isinstance(tag, str)]

df["built_with"] = df["built_with"].apply(clean_built_with)

# --- SIGNAL EXTRACTION ---

def check_any_keywords(texts, keywords):
    text = " ".join([str(t).lower() for t in texts if isinstance(t, str)])
    return any(kw in text for kw in keywords)

# Keyword definitions
AI_ML_KEYWORDS = ["machine learning", "deep learning", "neural network", "tensorflow", "pytorch", "nlp", "ai", "artificial intelligence", "gpt", "transformer"]
FINTECH_KEYWORDS = ["finance", "banking", "crypto", "blockchain", "ethereum", "bitcoin", "trading", "stock"]
HARDWARE_KEYWORDS = ["arduino", "raspberry pi", "sensor", "iot", "esp32", "hardware", "robot"]
HEALTHCARE_KEYWORDS = ["health", "medical", "diagnosis", "disease", "patient", "hospital", "therapy", "wearable"]
WEB_APP_KEYWORDS = ["react", "flask", "django", "next.js", "webapp", "api", "frontend", "backend"]
OPENAI_KEYWORDS = ["gpt", "openai", "chatgpt", "dall-e", "whisper"]

# Add signal columns
df["uses_ai_ml"] = df.apply(lambda row: check_any_keywords(
    [row.get("built_with"), row.get("what_it_does"), row.get("how_we_built_it")], AI_ML_KEYWORDS), axis=1)

df["is_fintech"] = df.apply(lambda row: check_any_keywords(
    [row.get("built_with"), row.get("what_it_does"), row.get("inspiration")], FINTECH_KEYWORDS), axis=1)

df["has_hardware_component"] = df.apply(lambda row: check_any_keywords(
    [row.get("built_with"), row.get("how_we_built_it")], HARDWARE_KEYWORDS), axis=1)

df["is_healthcare"] = df.apply(lambda row: check_any_keywords(
    [row.get("inspiration"), row.get("what_it_does")], HEALTHCARE_KEYWORDS), axis=1)

df["has_web_app"] = df.apply(lambda row: check_any_keywords(
    [row.get("built_with"), row.get("how_we_built_it")], WEB_APP_KEYWORDS), axis=1)

df["is_openai_related"] = df.apply(lambda row: check_any_keywords(
    [row.get("built_with"), row.get("inspiration"), row.get("what_it_does")], OPENAI_KEYWORDS), axis=1)

# --- SAVE ---

df.to_csv("data/devpost_projects_cleaned.csv", index=False)
print("✅ Cleaned data with signal columns saved to data/devpost_projects_cleaned.csv")
