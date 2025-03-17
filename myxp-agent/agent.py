# First we initialize the model we want to use.
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

from langchain_core.tools import tool

load_dotenv()
model = ChatOpenAI(model="gpt-4o", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal

system_prompt = """
You are a helpful bot, which only replies in English, Swahili and Chichewa

For example, 
Q: How are you?
A:
English: I am doing well, thank you
Chichewa: Ndili bwino, zikomo
Swahili: Niko vizuri, asante

"""




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


# Define the graph


graph = create_react_agent(model, tools=tools, prompt=system_prompt)

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


