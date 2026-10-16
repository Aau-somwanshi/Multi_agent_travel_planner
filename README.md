# ✈️ VoyageAI — Multi-Agent Travel Planning System

An autonomous multi-agent travel orchestration network built using **LangGraph**, **Groq LLM Engine**, **Tavily Search**, and **AviationStack API**, featuring a custom Cyberpunk Glassmorphism **Streamlit** dashboard.

---

## 🌟 Key Features

- **Multi-Agent Orchestration**: Specialized nodes (`flight_agent`, `hotel_agent`, `itinerary_agent`, and `final_agent`) coordinate state seamlessly using LangGraph.
- **Real-Time Data Extraction**: Live flight lookups via AviationStack API and live hotel/attraction search using Tavily Web Search.
- **Fast LLM Synthesis**: Powered by Groq LLM Engine for high-speed agentic reasoning.
- **Interactive Cyberpunk UI**: Custom glassmorphism Streamlit dashboard with live workflow status tracking and expandable raw tool logs.
- **Full Report Export**: One-click download of generated itineraries and tool findings as structured reports.

---

## 🏗️ System Architecture

```text
               +----------------------+
               |    User Request      |
               +----------+-----------+
                          |
                          v
               +----------------------+
               |    Flight Agent      | (AviationStack API)
               +----------+-----------+
                          |
                          v
               +----------------------+
               |     Hotel Agent      | (Tavily Search API)
               +----------+-----------+
                          |
                          v
               +----------------------+
               |   Itinerary Agent    | (Groq LLM Engine)
               +----------+-----------+
                          |
                          v

# ✈️ VoyageAI — Multi-Agent Travel Planning System

An autonomous multi-agent travel orchestration network built using **LangGraph**, **Groq LLM Engine**, **Tavily Search**, and **AviationStack API**, featuring a custom Cyberpunk Glassmorphism **Streamlit** dashboard.

---

## 🌟 Key Features

- **Multi-Agent Orchestration**: Specialized nodes (`flight_agent`, `hotel_agent`, `itinerary_agent`, and `final_agent`) coordinate state seamlessly using LangGraph.
- **Real-Time Data Extraction**: Live flight lookups via AviationStack API and live hotel/attraction search using Tavily Web Search.
- **Fast LLM Synthesis**: Powered by Groq LLM Engine for high-speed agentic reasoning.
- **Interactive Cyberpunk UI**: Custom glassmorphism Streamlit dashboard with live workflow status tracking and expandable raw tool logs.
- **Full Report Export**: One-click download of generated itineraries and tool findings as structured reports.

---

## 🏗️ System Architecture

```text
               +----------------------+
               |    User Request      |
               +----------+-----------+
                          |
                          v
               +----------------------+
               |    Flight Agent      | (AviationStack API)
               +----------+-----------+
                          |
                          v
               +----------------------+
               |     Hotel Agent      | (Tavily Search API)
               +----------+-----------+
                          |
                          v
               +----------------------+
               |   Itinerary Agent    | (Groq LLM Engine)
               +----------+-----------+
                          |
                          v
               +----------------------+
               |   Final Synthesizer  |
               +----------------------+
               +----------------------+
               |   Final Synthesizer  |
               +----------------------+
