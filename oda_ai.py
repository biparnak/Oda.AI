from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import wikipedia
import random
import numpy as np

# Response templates
response_templates = [
    "Here's what I found: {}",
    "Let me tell you: {}",
    "Based on my knowledge, {}",
    "I looked it up, and {}",
    "From what I know, {}",
]

# Predefined Q&A
qa_pairs = [
    ("hi", "Hello! How can I help you?"),
    ("hello", "Hi there!"),
    ("hey", "Hey! What's up?"),
    ("what's your name?", "I'm your friendly chatbot."),
    ("how are you?", "Doing great, thanks!"),
    ("tell me a joke", "Why did the scarecrow become a motivational speaker? Because he was outstanding in his field!"),
]

# Casual keywords
greetings_and_common_words = {"hi", "hello", "hey", "okay", "ok", "thanks", "thank you", "fine", "great", "cool", "nice"}

# Training data for TF-IDF
questions = [q.lower() for q, a in qa_pairs]
answers = [a for q, a in qa_pairs]
vectorizer = TfidfVectorizer(lowercase=True)
tfidf_matrix = vectorizer.fit_transform(questions)

# Classify the field (medical, engineering, gaming, general)
def classify_field(query):
    medical_keywords = ["doctor", "medicine", "hospital", "symptom", "treatment", "health", "disease"]
    engineering_keywords = ["engineer", "mechanical", "electrical", "civil", "robotics", "technology"]
    gaming_keywords = ["game", "gamer", "console", "multiplayer", "video game", "fps", "rpg", "esports"]

    query = query.lower()
    if any(word in query for word in medical_keywords):
        return "medical"
    elif any(word in query for word in engineering_keywords):
        return "engineering"
    elif any(word in query for word in gaming_keywords):
        return "gaming"
    return "general"

# Wikipedia fetch
def get_wikipedia_summary(search_term):
    try:
        summary = wikipedia.summary(search_term, sentences=2)
        return summary
    except wikipedia.exceptions.DisambiguationError:
        return "Multiple possibilities exist; please clarify."
    except wikipedia.exceptions.PageError:
        return "Sorry, I couldn’t find that on Wikipedia."
    except Exception:
        return "Error fetching Wikipedia data."

# Custom response from summary
def build_own_answer(summary, topic):
    sentences = summary.split(". ")
    if len(sentences) > 1:
        intro = random.choice([
            f"So, basically, {topic} is",
            f"Let me explain {topic} to you:",
            f"Here's the deal with {topic}:",
            f"In simple words, {topic} means",
            f"To put it simply, {topic} is"
        ])
        rest = ". ".join(sentences[:2])
        return f"{intro} {rest}."
    else:
        return f"Here's what I know about {topic}: {summary}"

# Detect factual question
def is_factual_query(query):
    prefixes = [
        "what is", "who is", "where is", "when did", "how does",
        "tell me about", "i need to know about", "explain", "define"
    ]
    q = query.lower().strip()
    for prefix in prefixes:
        if q.startswith(prefix):
            search_term = q[len(prefix):].strip()
            if search_term:
                return True, search_term
    return False, None

# Casual replies
def get_casual_response(user_input):
    casual_responses = {
        "thanks": ["You're welcome!", "No problem!", "Anytime!"],
        "thank you": ["You're welcome!", "Glad I could help."],
        "great": ["Glad to hear that!", "Awesome! Do you have any more questions?"],
        "cool": ["Cool indeed!", "Nice! Want to know more?"],
        "okay": ["Okay! Let me know if you need anything."],
        "ok": ["Alright!", "Cool!"],
        "nice": ["Nice!", "Thanks!"],
        "fine": ["Great!", "Good to know!"],
    }
    cleaned = user_input.strip().lower()
    for keyword in casual_responses:
        if keyword in cleaned:
            return random.choice(casual_responses[keyword])
    return None

# Generate a story
def generate_story():
    characters = ["a young wizard", "an alien explorer", "a curious robot", "a talking cat", "a mischievous fairy", "a brave knight", "a time-traveling historian", "a shapeshifting entity", "a quirky inventor", "a skilled archer with magical abilities", "a cursed pirate seeking redemption", "a mysterious oracle"]
    settings = ["in a magical forest", "on Mars", "inside a haunted castle", "beneath the ocean",  "in a forgotten underground city", "on a distant, mysterious planet", "atop a floating island in the sky", "inside a labyrinth of mirrors", "amidst the ruins of an ancient civilization", "within an enchanted garden that changes with time", "at the edge of a volcano about to erupt", "in a bustling intergalactic marketplace"]
    conflicts = ["discovered a mysterious map", "found a hidden door", "was trapped in a strange dream", "had to solve an ancient riddle", "uncovered a cursed relic"]
    resolutions = ["and became a hero of the land.", "and uncovered the secret of the universe.", "and found a new best friend.", "and saved the day just in time.", "and restored balance to the world."]

    return f"Once upon a time, {random.choice(characters)} {random.choice(settings)} {random.choice(conflicts)}, {random.choice(resolutions)}"

# Chatbot main logic
def get_response(user_input):
    user_input_clean = user_input.strip().lower()
    if not user_input_clean:
        return "Please type something."

    category = classify_field(user_input_clean)
    print(f"(Debug) Detected category: {category}")

    if "tell me a story" in user_input_clean or "make a story" in user_input_clean or user_input_clean == "story":
        return generate_story()

    casual = get_casual_response(user_input_clean)
    if casual:
        return casual

    is_factual, search_term = is_factual_query(user_input_clean)
    if is_factual and search_term:
        summary = get_wikipedia_summary(search_term)
        if "Error" not in summary and "Sorry" not in summary:
            return build_own_answer(summary, search_term)
        return summary

    if len(user_input_clean.split()) == 1 and user_input_clean not in greetings_and_common_words:
        summary = get_wikipedia_summary(user_input_clean)
        if "Error" not in summary and "Sorry" not in summary:
            return build_own_answer(summary, user_input_clean)
        return summary

    user_vector = vectorizer.transform([user_input_clean])
    similarity = cosine_similarity(user_vector, tfidf_matrix)
    best_match_idx = np.argmax(similarity)
    best_score = similarity[0][best_match_idx]
    threshold = 0.3 if len(user_input_clean.split()) > 2 else 0.1
    if best_score > threshold:
        return answers[best_match_idx]

    return "I'm not sure about that. Try asking 'What is [topic]?' or 'Tell me about [topic].'"

# Run the chatbot
def main():
    print("Chatbot: Hi! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower().strip() == "exit":
            print("Chatbot: Goodbye!")
            break
        print("Chatbot:", get_response(user_input))

if __name__ == "__main__":
    main()
