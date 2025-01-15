import streamlit as st
import google.generativeai as genai

# Configure the Google AI client
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
# Default settings
st.session_state['model'] = "gemini-1.5-flash"
st.session_state['max_output_tokens'] = 2000
st.session_state['temperature'] = 0.8

model = genai.GenerativeModel(
    st.session_state['model'],
    generation_config=genai.GenerationConfig(
        max_output_tokens=st.session_state['max_output_tokens'],
        temperature=st.session_state['temperature'],
    ))

def initialize_context(allow = False):
    if allow:
        return f"""
            You are a health data chatbot that uses the Gemini 1.5 Flash models to answer questions about your user's health data provided.
            This is the health data currently available about the user:
            
            Sleep Score: {st.session_state['sleep_score']}
            Cardiovascular Age: {st.session_state['cardio_age']}
            Activity Score: {st.session_state['activity_score']}
            Resilience Score: {st.session_state['resilience']}
            Readiness Score: {st.session_state['readiness_score']}
            Average SpO2: {st.session_state['average_spo2']}
            
            Your job is to answer questions about the user's health data based on the information provided.
            You can also provide recommendations for the user based on their health data.
            
            Please try to keep your responses concise and to the point.
        """
    else:
        return f"""
            You are a health chatbot that uses the Gemini 1.5 Flash models to answer questions about health.           
            Your job is to answer questions about health based on the information the user provides.
            
            Please try to keep your responses concise and to the point.           
        """


# Page config
st.set_page_config(page_title="Health Chat", page_icon="💭", layout="wide")
st.title("💭 Health Data Chat Assistant")
st.write("This AI assistant uses open-source language models to help analyze and provide insights about your health data.")
st.warning("Important: While Gemini models are free to use, Google has stated they will use conversations to improve their models.")
allow = st.checkbox(
    "Allow the model access to my personal health data ⚠️", 
    value=False, 
    key="allow_data_use",
    help="Enabling this will allow the AI to analyze your personal health metrics, but be aware that this data may be used to improve Google's models"
)

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    # Display user message
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Build conversation history
            conversation = ""      
            conversation += initialize_context(allow)
            
            for message in st.session_state.messages:
                role = "User" if message["role"] == "user" else "Assistant"
                conversation += f"{role}: {message['content']}\n"
            
            # Add current prompt
            conversation += f"User: {prompt}\n"
            
            # Get response with conversation context
            response = model.generate_content(conversation)
            st.write(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# Sidebar options
with st.sidebar:
    st.title("Chat Options")
    
    # Create a container for buttons with equal width
    button_container = st.container()
    
    # Custom styling for buttons
    button_style = """
        <style>
        div.stButton > button {
            width: 100%;
            height: 50px;
            margin: 0px;
        }
        div.stDownloadButton > button {
            width: 100%;
            height: 50px;
            margin: 0px;
            background-color: #98FB98 !important;
            color: black !important;
            border: none !important;
        }
        div.stDownloadButton > button:hover {
            background-color: #7FCD7F !important;
            color: black !important;
        }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    col1, col2 = button_container.columns([1, 1])
    with col1:
        if st.button("Clear Chat", 
                     type="primary",
                     use_container_width=True,
                     key="clear_chat"):
            st.session_state.messages = []
            st.rerun()
    with col2:
        # Convert to String for .txt file
        conversation_text = ""
        for message in st.session_state.messages:   
            role = message["role"].capitalize()
            content = message["content"]
            conversation_text += f"{role}: {content}\n\n"
                
        st.download_button(
            label="Download",
            data=conversation_text,
            file_name="conversation_history.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_chat"
        )
        
    # Add a dropdown menu for model selection and parameter tuning
    with st.expander("Advanced"):
        # Model selection
        st.info("Will add more free models in the future.")
        selected_model = st.selectbox(
            "Model",
            ["gemini-1.5-flash", "gemini-1.5-flash-8b"],
            index=0
        )
        
        # Temperature slider
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            step=0.1,
            help="Higher values make the output more creative but less focused"
        )
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=100,
            max_value=5000,
            value=2000,
            step=100,
            help="Maximum number of tokens to generate. Higher value allows for longer more detailed responses."
        )

        # Update model configuration when changed
        if st.session_state.model != selected_model:
            st.session_state.model = selected_model
        if st.session_state.temperature != temperature:
            st.session_state.temperature = temperature
        if st.session_state.max_output_tokens != max_tokens:
            st.session_state.max_output_tokens = max_tokens
            
        model = genai.GenerativeModel(
            st.session_state.model,
            generation_config=genai.GenerationConfig(
                max_output_tokens=st.session_state.max_output_tokens,
                temperature=st.session_state.temperature,
            ))

