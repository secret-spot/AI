# ❤️‍🔥 S2 (Secret-Spot)
<img src="https://github.com/secret-spot/AI/blob/main/SecretSpot.svg"/>

### Info


S2 is a service designed to solve the increasingly discussed problem of overtourism. Instead of crowded tourist attractions, it helps users introduce and explore their own secret places so that they can find less crowded places.

## 👨‍👩‍👧‍👦Members
### Developer
|FE & Designer|BE & PM|BE|AI|
|:--:|:--:|:--:|:--:|
|![jieun](https://avatars.githubusercontent.com/u/143923436?v=4)|![haneul](https://avatars.githubusercontent.com/u/145983374?v=4)|![gyeongeun](https://avatars.githubusercontent.com/u/167386241?v=4)|![eojin](https://avatars.githubusercontent.com/u/166782787?v=4)|
|GDG on Sookmyung|GDG on Sookmyung|GDG on Sookmyung|GDG on Sookmyung|
|[Jieun Lee](https://github.com/mariewldms)|[Haneul Lee](https://github.com/tishakong)|[Gyeongeun Lee](https://github.com/ruddmslee)|[Eojin Yang](https://github.com/ydjwls)|

---
## 📌Tech Stack
![python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)
<img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=FastAPI&logoColor=green"/>
<img src="https://img.shields.io/badge/GoogleGemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=purple"/>
![gcloud](https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white)

  + **Language:** python
  + **FrameWork:** FastAPI
  + **Deployment Platform:** Google App Engine
  + **AI:** Google gemini
---
## 📌Key Features
### 1️⃣ Keyword Extraction Feature 📍
+ **Description:** Automatically extracts relevant keywords from the user's post.
+ **Key Categories:**
  + **Companion Type:** Solo, Family, Friends, Couple
  + **Travel Style:** Art, Extreme, Photography, Food, Healing, History, Shopping, Experience
  + **Region:** Any mentioned region

### 2️⃣ Local Etiquette Display Feature 😊
+ **Description:** When a user searches for a specific region, the system provides local etiquette guidelines tailored to that area.
+ **Highlights:**
  + Utilizes Gemini to generate region-specific etiquette suggestions.
  + Future updates may involve building a dedicated etiquette dataset per region for even more accurate and localized results.

### 3️⃣ Small City Recommendation Feature 🗺️
+ **Description:** Recommends lesser-known small cities near the user’s selected location to help avoid overcrowded destinations.
+ **Highlights:**
  + Powered by Gemini to identify nearby under-the-radar cities.
  + Can be enhanced in the future to base recommendations on accumulated user-generated posts and data.

### 4️⃣ Chatbot Feature 🤖
+ **Description:** An AI-powered companion that assists users like a real travel buddy.
+ **Highlights:**
  + Provides friendly and personalized travel support, just like a friend on the journey.
  + When asked for travel recommendations, it suggests hidden gems rather than typical tourist spots.
---
## 📂Folder
```
│── app
│   ├── api/v1
│       ├── endpoints/      # Modules that handle actual business logic
│       └── routers.py      # File that registers each endpoint to the FastAPI router
│   ├── config.py           # Configuration file for the API and Gemini API settings
│   └── main.py             # Entry point of the FastAPI application (server startup file)
│── .env                    # File that defines environment variables
│── requirements.txt        # File listing required packages and libraries
│── app.yaml                # Deployment configuration file for Google App Engine
```
## 🌐Deployment & Demo 
+ **Full Deployment URL:** https://secret-spot-22469.web.app/
+ **AI Deployment URL:** https://basic-radius-459414-h8.du.r.appspot.com/
+ **Demo Video:**
---
## Try S2 right now! 
### 👇[Secret Spot](https://secret-spot-22469.web.app/)
