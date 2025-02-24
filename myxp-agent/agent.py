# First we initialize the model we want to use.
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from langchain_core.tools import tool

load_dotenv()
model = ChatOpenAI(model="gpt-4o", temperature=0)


# For this tutorial we will use custom tool that returns pre-defined values for weather in two cities (NYC & SF)

from typing import Literal



@tool
def get_weather(city: str):
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


graph = create_react_agent(model, tools=tools)

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "what is the population of New York")]}
print_stream(graph.stream(inputs, stream_mode="values"))