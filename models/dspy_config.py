# great-ideas/models/dspy_config.py
import os
from dotenv import load_dotenv
import dspy

load_dotenv()

# Configure DSPy
dspy.settings.configure(lm=dspy.OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

# Define a basic prompt template
class BasicPrompt(dspy.Prompt):
    input_description = dspy.InputField()
    output_description = dspy.InputField()
    context = dspy.InputField(desc="Additional context or instructions")
    query = dspy.InputField()
    search_results = dspy.InputField(desc="Web search results related to the query")
    response = dspy.OutputField()

# Define a signature for structured output
class StructuredOutput(dspy.Signature):
    input_description = dspy.InputField()
    query = dspy.InputField()
    search_results = dspy.InputField(desc="Web search results related to the query")
    response = dspy.OutputField(desc="JSON structured response")
