# 🌍 Travel Itinerary Planner

An AI-powered travel planner that generates a complete trip itinerary using a multi-agent pipeline.

## 🛠️ Tech Stack
LangChain · LangGraph · Groq (LLaMA 3.3-70B) · Streamlit · Python

## ⚙️ Setup
1. Clone the repo and run `pip install -r requirements.txt`
2. Create a `.env` file and add your `GROQ_API_KEY=your_key_here`
3. Run the app with `streamlit run app.py`

## 🤖 Agents
Validator → Hotels → Meals → Activities → Transport → Budget → Final Itinerary

## 📌 Input
Enter your destination, trip duration, budget (low/medium/high), and interests to get started.
