from utils.llm_utils import LLaMAHelper 
import spacy
from geotext import GeoText
import spacy
import spacy.cli

# Initialize LLaMA and spaCy
llm = LLaMAHelper()

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def extract_location(text, method="spacy"):
    if method == "spacy":
        doc = nlp(text)
        locations = [ent.text for ent in doc.ents if ent.label_ == "GPE"]
        return locations[0] if locations else ""
    elif method == "geotext":
        geo = GeoText(text)
        locations = geo.countries + geo.cities
        return locations[0] if locations else ""
    return ""

def get_cached_location_from_history(history, method="spacy"):
    for question, _ in reversed(history):
        location = extract_location(question, method)
        if location:
            return location
    return ""

def handle_tenancy_query(user_query, user_context, history=[], location_method="spacy"):
    # Use stored location if available
    location = user_context.get("location", "")

    # Otherwise, extract from current or previous queries
    if not location:
        location = extract_location(user_query, location_method)
        if not location:
            location = get_cached_location_from_history(history, location_method)

        if location:
            user_context["location"] = location 

    system_prompt = "You are a legal assistant specializing in tenancy laws."
    prompt=""
    if location:
        prompt += f" The user is from {location}."

    if history:
        chat_context = "\n".join(f"User: {q}\nBot: {a}" for q, a in history)
        prompt += f"\n\nPrevious conversation:\n{chat_context}"

    prompt += f"\n\nUser's current question: {user_query}\n\nGive a concise and helpful answer. If needed, ask a follow-up question to clarify."
    print(f'prompt for tenacy faq is {prompt}')
    reply = llm.chat(system_prompt, prompt, temperature=0.7)
    return reply
