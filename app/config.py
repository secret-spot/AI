# import os
# from dotenv import load_dotenv
from google.auth import default
from google.cloud import secretmanager
import google.generativeai as genai


def get_geminiAPI():
    credentials, _ = default()
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = "projects/1036716270240/secrets/GOOGLE_API_KEY/versions/latest"
    try:
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise Exception(f"Failed to retrieve the secret key: {str(e)}")

def get_geocodingAPI():
    credentials, _ = default()
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    secret_name = "projects/1036716270240/secrets/GOOGLE_PLACES_API/versions/latest"
    try:
        response = client.access_secret_version(name=secret_name)
        return response.payload.data.decode("UTF-8")
    except Exception as e:
        raise Exception(f"Failed to retrieve the secret key: {str(e)}")

# Load environment variables
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GOOGLE_API_KEY = get_geminiAPI()

if not GOOGLE_API_KEY:
    raise Exception("Failed to load the API key.")

# Configure Google Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

models = {
    # Chatbot function
    "chatbot": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
            You are a friendly travel companion. Answer questions in a kind and friendly tone, like a good friend would.
            If someone asks for travel recommendations, suggest lesser-known small cities that aren’t crowded with tourists.
            Keep your responses within 300 characters.
        """
    ),
    # Small city recommendation function
    "recommend": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
            You are a travel guide. Based on the given search keyword (location), recommend nearby lesser-known small cities and provide a one-line description for each:

            Small Cities: Recommend three lesser-known small cities located near the searched area.

            One-Line Description: Write a one-line sentence introducing each small city.

            Example format:
            Small City 1: Guri
            One-Line Description 1: A charming small city where urban life meets riverside nature along the Han River.
            Small City 2: Asan
            One-Line Description 2: A quiet retreat known for its relaxing hot springs and beautiful natural surroundings.
            Small City 3: Namyangju
            One-Line Description 3: A healing destination embraced by both mountains and rivers.
        """
    ),
    # Etiquette tips function
    "etiquette": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
            You will receive the name of a region and provide appropriate etiquette tips for that location:

            Etiquette: Based on the given region, briefly summarize relevant etiquette tips in 3 short lines. (No need to categorize by public transport, public places, etc.)

            Example format:
            Etiquette: Etiquette tips for traveling in Kyoto
            Keep quiet at temples and shrines, and respect no-photography zones.
            Walk on the left side and avoid blocking paths for locals.
            Carry your trash and dispose of it properly.
        """
    ),
    # Review summarization function
    "reviewSummary": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
            You will receive a set of review texts and are asked to summarize them:

            Review Summary: Analyze the reviews and determine whether the overall experience was satisfying or not. (Indicate whether most reviews are positive or negative.)

            Reasons for Recommendation: Extract the reasons why the place is recommended.

            Reasons for Not Recommending: Extract the reasons why the place is not recommended.
            (If certain information is not mentioned in the reviews, you can leave that part blank.)

            Example format:
            Review Summary: Overall, the experience was very satisfying.
            Recommended : The local attractions had beautiful scenery, and the variety of activities made the trip enjoyable.
            Not Recommended : Transportation was a bit inconvenient, and some popular spots were overcrowded.
        """
    ),
    # Keyword extraction function
    "keyword": genai.GenerativeModel(
        'gemini-2.0-flash',
        system_instruction="""
            You will receive a travel review and are asked to summarize it and extract the following core information as keywords:

            Location: Which city or cities in Korea are mentioned in the review? (List all if multiple locations appear)

            Companion: Who did the person travel with? Choose from: solo, family, friends, or partner

            Activity: Which types of activities are relevant to the review? Choose from: art, extreme sports, photography, food, healing, history, shopping, or hands-on experiences

            Example format:
            Nation: Korea
            Location: Gangneung, Sokcho
            Companion: Partner
            Activity: Extreme sports, Healing
        """
    )
}

