from phi.agent import Agent, RunResponse
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.crawl4ai_tools import Crawl4aiTools
from phi.storage.agent.sqlite import SqlAgentStorage

import streamlit as st
import os
os.environ['GOOGLE_API_KEY']="AIzaSyCVCopeMcTMZQ09I4eYopdvTC60vPtxXF0"

storage = SqlAgentStorage(
    table_name="agent_sessions",
    db_file="tmp/data.db",
)

# Define the AI agent
agent = Agent(
    model=Gemini(id="gemini-1.5-pro"),
    description="You are an expert in geopolitics.",
    instruction=[
        "Whenever a user query requires external data, use DuckDuckGo to search for relevant information.",
        "Retrieve the top 5 links and provide them to the webcrawler.",
        "Summarize the extracted information in the style of a geopolitical expert.",
        "Include URLs of sources in the summary.",
        "Use charts to explain comparisons when requested."
    ],
    markdown=True,
    tools=[DuckDuckGo(), Crawl4aiTools(max_length=200)],
    show_tool_calls=True,
    num_history_responses=5,
    storage=storage
)

# Streamlit UI
st.title("GeoPolitics Guru",)

# Display chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# User input
user_input = st.chat_input("Ask anything to Geo Politics Guru")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Run AI agent and get response
    run: RunResponse = agent.run(user_input)
    bot_response = run.content

    st.session_state.messages.append({"role": "bot", "content": bot_response})

# Display messages in the chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])