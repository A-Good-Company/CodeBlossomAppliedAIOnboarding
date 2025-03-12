# First we initialize the model we want to use.
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.tools import tool
import os
import openai
from langchain.prompts import ChatPromptTemplate
from typing import Literal

openai.api_key = os.getenv("OPENAI_API_KEY")

load_dotenv()

@tool
def get_weather(city: Literal["nyc", "sf", "toronto"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    elif city == "toronto":
        return "Its full of snow!"
    else:
        raise AssertionError("Unknown city")
    
@tool
def get_population(city: str):
    """Returns the population of a city"""
    return {"city": city, "population": 1000000, "verified": "False, needs verification"}
    


@tool
def verify_fact(statement: str):
    """Verifies facts before sharing with human"""
    return  "This statement is True"

tools = [get_weather, get_population, verify_fact]

# Define a custom prompt template
custom_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant specialized in providing accurate information about weather and population statistics.And you only talk in chichewa or English
    When using tools, always:
    1. Think carefully about which tool is most appropriate
    2. Use the exact city names as specified in the tool descriptions
    3. Verify important facts before stating them
    4. Provide clear, concise responses
    
    Available tools:
    - get_weather: Get weather for nyc, sf, or toronto
    - get_population: Get population statistics
    - verify_fact: Verify information before sharing
    
    Format your responses professionally and always cite your sources."""),
    
    ("assistant", "I'll help you with that request. Let me think about this step by step."),
])

model = ChatOpenAI(model="gpt-4o", temperature=0)

# Rest of your code remains the same until creating the graph
# When creating the graph, add the custom prompt

graph = create_react_agent(
    model, 
    tools=tools,
    prompt=custom_prompt
)

# Rest of your code remains unchanged
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "what is the weather of New York")]}
print_stream(graph.stream(inputs, stream_mode="values"))


print(f"\n\n{"==="*20}\n\n")

inputs = {"messages": [("user", "what is the population of New York")]}
print_stream(graph.stream(inputs, stream_mode="values"))