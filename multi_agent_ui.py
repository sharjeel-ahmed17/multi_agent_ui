import os
import streamlit as st
from agents import Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from my_agents import get_agent
from agents import RunConfig
import asyncio

load_dotenv()

gemini_api_key=os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("❌ no gimini key set in your .env file.")
    st.stop()

external_client= AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
) 

model=OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config= RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent=get_agent(model)

agent_descriptions={
    "assistant": "🧠 General-purpose assistant",
    "coder": "💻 Code generator & explainer",
    "teacher": "📚 Educational tutor",
    "poet": "✍️ Creative writer & poet"
}

st.title("💥 Gemini Multi AI Agent App")
st.write("Choose and Agent and Enter Your Prompt")


agent_choice=st.selectbox(
    "Select an Agent",
    options=list(agent_descriptions.keys()),
    format_func=lambda name: f"{name.title()}- {agent_descriptions[name]}"
)

prompt = st.text_area("Enter your question or task:")

async def run_with_retries(agent, prompt, config, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return await Runner.run(agent, prompt, run_config=config)
        except Exception as e:
            if "503" in str(e) and attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                raise


if st.button("Run Agent"):
    if not prompt.strip():
        st.warning("⚠ Please enter a valid prompt.")
    else:
        selected_agent=agent[agent_choice]
        with st.spinner("Generating Response....."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(Runner.run(selected_agent, prompt, run_config=config))
                st.success(f"✅ {agent_choice.title()} Response")
                st.markdown(result.final_output)
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")