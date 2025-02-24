# LangGraph Agent Setup Guide

This guide will walk you through setting up a LangGraph agent locally. The agent is designed to interact with a user, process queries, and use custom tools to provide responses. The agent leverages OpenAI's GPT-4o model and custom tools to fetch weather information, population data, and verify facts.

## What is an Agent?

An **agent** in the context of LangGraph is an AI-powered system that can interact with users, process natural language queries, and use predefined tools to fetch or verify information. The agent is built using the LangGraph framework, which allows for the creation of reactive agents that can handle complex workflows.

In this example, the agent is equipped with three custom tools:
1. **get_weather**: Fetches weather information for specific cities (NYC, SF, Toronto).
2. **get_population**: Returns the population of a given city (currently returns a placeholder value).
3. **verify_fact**: Verifies the truthfulness of a statement (currently returns a placeholder value).

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- `pip` (Python package manager)

## Setting Up the Environment

1. **Clone the Repository**:
   Clone the repository containing the `agent.py` and `requirements.txt` files to your local machine.

2. **Install Dependencies**:
   Navigate to the directory where the repository is cloned and install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up `.env` File**:
   The agent requires an OpenAI API key to function. Create a `.env` file in the same directory as `agent.py` and add your OpenAI API key as follows:
   ```plaintext
   OPENAI_API_KEY=your_openai_api_key_here
   ```
   Replace `your_openai_api_key_here` with your actual OpenAI API key.

   **Note**: If you don't have an OpenAI API key, you can obtain one by signing up at [OpenAI's website](https://platform.openai.com/signup).

## Running the Agent

Once the environment is set up, you can run the agent by executing the following command in your terminal:
```bash
python agent.py
```

### What Happens When You Run the Agent?

When you run `agent.py`, the script will:
1. Initialize the GPT-4 model with a temperature of 0 (deterministic responses).
2. Load the custom tools (`get_weather`, `get_population`, `verify_fact`).
3. Create a reactive agent using the LangGraph framework.
4. Process two example queries:
   - "What is the weather of New York?"
   - "What is the population of New York?"
5. Print the agent's responses to the terminal.

### Example Output

When you run the script, you should see output similar to the following:

```plaintext
Thought: I need to find the weather in New York.
Action: get_weather
Observation: It might be cloudy in nyc
Thought: I have the weather information for New York.
Final Answer: It might be cloudy in nyc

============================================================

Thought: I need to find the population of New York.
Action: get_population
Observation: {'city': 'New York', 'population': 1000000, 'verified': 'False, needs verification'}
Thought: I have the population information for New York.
Final Answer: The population of New York is 1000000, but this needs verification.
```

## Customizing the Agent

You can customize the agent by adding more tools or modifying the existing ones. For example, you could add a tool to fetch real-time data from an API or modify the `get_population` tool to return actual population data.

To add a new tool, define a function with the `@tool` decorator and add it to the `tools` list in `agent.py`.

## Troubleshooting

- **Missing API Key**: If you forget to add the OpenAI API key to the `.env` file, the script will fail with an error. Ensure the `.env` file is correctly set up.
- **Dependency Issues**: If you encounter issues with dependencies, ensure you have the correct versions installed by running `pip install -r requirements.txt`.