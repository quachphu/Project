import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import datetime
import os
from dotenv import load_dotenv
import json

# Page configuration
st.set_page_config(
    page_title="Ollama Chat Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .chat-message {
        padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
    }
    .chat-message.user {
        background-color: #EFF6FF;
        border-left: 5px solid #3B82F6;
        text-align: right;
        margin-left: 30%;
    }
    .chat-message.assistant {
        background-color: #F8FAFC;
        border-left: 5px solid #10B981;
        margin-right: 30%;
    }
    .chat-message .avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        object-fit: cover;
        margin-right: 1rem;
    }
    .chat-message .message {
        color: #334155;
        font-size: 1rem;
        padding: 0 1rem;
        flex-grow: 1;
    }
    .chat-message .timestamp {
        color: #94A3B8;
        font-size: 0.75rem;
        padding-top: 0.5rem;
    }
    .stTextInput>div>div>input {
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .system-message {
        background-color: #FEF9C3;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #EAB308;
    }
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .stButton>button:hover {
        background-color: #2563EB;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
        border-right: 1px solid #E2E8F0;
        padding: 2rem 1rem;
    }
    .title-container {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }
    .title-text {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

# Load environment variables
load_dotenv()

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful, friendly assistant. Respond thoughtfully to the user's queries.")
    ]

if "conversation_name" not in st.session_state:
    st.session_state.conversation_name = f"Conversation {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"

# Key fix: Add a flag to prevent multiple processing
if "processing_done" not in st.session_state:
    st.session_state.processing_done = False

# Function to generate response
def generate_response(question, llm_model, temp, max_tok, history):
    # Build prompt with history
    messages = []
    
    # First, add the system message
    for message in history:
        if isinstance(message, SystemMessage):
            messages = [("system", message.content)]
            break
    
    # Then add the conversation history
    for message in history:
        if isinstance(message, HumanMessage):
            messages.append(("user", message.content))
        elif isinstance(message, AIMessage):
            messages.append(("assistant", message.content))
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages(messages)
    
    # Set up LLM
    llm = Ollama(
        model=llm_model,
        temperature=temp
    )
    
    # Create and execute chain
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({})

# === SIDEBAR COMPONENTS ===
with st.sidebar:
    st.markdown('<div class="title-container"><span class="title-text">🤖 Assistant Settings</span></div>', unsafe_allow_html=True)
    
    # Model selection
    available_models = ["mistral", "llama3.2"]
    selected_model = st.selectbox(
        "Select Ollama Model", 
        available_models, 
        index=0
    )
    
    st.divider()
    
    # Advanced Settings
    st.markdown("### Response Settings")
    temperature = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, 
                          help="Higher values make output more random, lower values more deterministic")
    
    max_tokens = st.slider("Max Tokens", min_value=50, max_value=4096, value=500,
                         help="Maximum length of the generated response")
    
    st.divider()
    
    # System message (personality)
    st.markdown("### Assistant Personality")
    system_message = st.text_area(
        "System Message",
        value=st.session_state.messages[0].content,
        help="This defines how the AI assistant behaves",
        key="system_message_input"
    )
    
    if st.button("Update Personality", key="update_personality_button"):
        st.session_state.messages[0] = SystemMessage(content=system_message)
        st.success("Assistant personality updated!")
    
    st.divider()
    
    # Conversation Management
    st.markdown("### Conversation")
    conversation_name = st.text_input(
        "Conversation Name", 
        st.session_state.conversation_name,
        key="conversation_name_input"
    )
    
    # Save/Load conversations
    col1, col2 = st.columns(2)
    
    if col1.button("Save Chat", key="save_chat_button", use_container_width=True):
        # Create conversation data
        conversation_data = {
            "name": conversation_name,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": [
                {"role": "system" if isinstance(msg, SystemMessage) else 
                         "user" if isinstance(msg, HumanMessage) else "assistant", 
                 "content": msg.content} 
                for msg in st.session_state.messages
            ]
        }
        
        # Save to file with sanitized name
        safe_name = ''.join(c if c.isalnum() else '_' for c in conversation_name)
        filename = f"conversation_{safe_name}.json"
        
        with open(filename, "w") as f:
            json.dump(conversation_data, f)
        
        st.success(f"Saved as {filename}")
    
    if col2.button("Clear Chat", key="clear_chat_button", use_container_width=True):
        # Keep only the system message
        system_msg = st.session_state.messages[0]
        st.session_state.messages = [system_msg]
        st.session_state.conversation_name = f"Conversation {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        st.session_state.processing_done = False
        st.rerun()

# Display chat title
st.markdown('<div class="title-container"><span class="title-text">💬 Ollama Chat Assistant</span></div>', unsafe_allow_html=True)

# Display chat messages
for idx, message in enumerate(st.session_state.messages):
    # Skip system messages in the main chat display
    if isinstance(message, SystemMessage):
        continue
        
    if isinstance(message, HumanMessage):
        with st.container():
            st.markdown(f"""
            <div class="chat-message user">
                <div class="message">
                    {message.content}
                </div>
                <div class="timestamp">
                    {message.additional_kwargs.get('timestamp', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"""
            <div class="chat-message assistant">
                <div class="message">
                    {message.content}
                </div>
                <div class="timestamp">
                    {message.additional_kwargs.get('timestamp', '')}
                </div>
            </div>
            """, unsafe_allow_html=True)

# User input area - KEY FIX: Use a form to prevent auto-submission
with st.form(key="message_form"):
    user_input = st.text_input(
        "Message:", 
        placeholder="Type your message here...", 
        label_visibility="collapsed",
        key="user_input_field"
    )
    submit_button = st.form_submit_button("Send")

# Process user input only if the form is submitted
if submit_button and user_input and not st.session_state.processing_done:
    # Set the processing flag
    st.session_state.processing_done = True
    
    # Create timestamp
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    
    # Add user message to history
    user_message = HumanMessage(content=user_input)
    user_message.additional_kwargs['timestamp'] = timestamp
    st.session_state.messages.append(user_message)
    
    # Create a placeholder for response
    response_placeholder = st.empty()
    
    # Display typing indicator
    response_placeholder.markdown(f"""
    <div class="chat-message assistant">
        <div class="message">
            <i>Typing...</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        # Generate response
        response_text = generate_response(
            user_input, selected_model, temperature, max_tokens, st.session_state.messages
        )
        
        # Add assistant response to history
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        assistant_message = AIMessage(content=response_text)
        assistant_message.additional_kwargs['timestamp'] = timestamp
        st.session_state.messages.append(assistant_message)
        
        # Reset processing flag at the end
        st.session_state.processing_done = False
        
        # Rerun to update the UI and clear the form
        st.rerun()
        
    except Exception as e:
        # Handle errors gracefully
        error_message = f"Error: {str(e)}"
        response_placeholder.markdown(f"""
        <div class="chat-message assistant" style="border-left: 5px solid #EF4444;">
            <div class="message">
                <strong>Error:</strong> I encountered a problem while generating a response. 
                Please check if Ollama is running and the selected model is installed.
                <br/><br/>
                <code>{error_message}</code>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reset processing flag even after error
        st.session_state.processing_done = False

# Display the system message at the bottom for reference
with st.expander("Current System Instructions"):
    st.markdown('<div class="system-message">' + st.session_state.messages[0].content + '</div>', unsafe_allow_html=True)