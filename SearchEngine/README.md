Web App Link: https://search-engine-app.streamlit.app/ 

```mermaid
flowchart LR
  AB["User opens Streamlit app and enters Groq API key in sidebar"] --> C{"Is API key in session_state?"}
  C -- No --> D["Prompt user to enter API key"]
  C -- Yes --> EJ["Load session_state.messages, render chat, get new prompt, display it, and initialize ChatGroq LLM"]
  EJ --> K["Instantiate tools"]
  K --> K1["DuckDuckGoSearchRun"] & K2["ArxivQueryRun"] & K3["WikipediaQueryRun"]
  K1 --> L["Initialize agent"]
  K2 --> L
  K3 --> L
  L --> M["Run agent run with messages and callbacks"]
  M --> N{"Agent decides action"}
  N -- Search --> O["Call DuckDuckGoSearchRun"]
  N -- Arxiv --> P["Call ArxivQueryRun"]
  N -- Wiki --> Q["Call WikipediaQueryRun"]
  O --> R["Fetch web search results"]
  P --> S["Fetch Arxiv abstracts"]
  Q --> T["Fetch Wikipedia summaries"]
  R --> U["Agent ingests tool outputs"]
  S --> U
  T --> U
  U --> V["Agent generates final text response"]
  V --> W["StreamlitCallbackHandler streams “thinking”"]
  W --> X["Append assistant response to session_state.messages"]
  X --> Y["Display assistant response in chat UI"]

