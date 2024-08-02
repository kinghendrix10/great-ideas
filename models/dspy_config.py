# great-ideas/models/dspy_config.py
import os
from dotenv import load_dotenv
import dspy
import json

load_dotenv()

# Configure DSPy
dspy.configure(api_key=os.getenv("OPENAI_API_KEY"))

# Define a basic signature for prompts
class BasicPrompt(dspy.Signature):
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

# Define a basic ChainOfThought module
class BasicChainOfThought(dspy.Module):
    def __init__(self, signature):
        super().__init__()
        self.signature = signature
        self.lm = dspy.OpenAI(model="gpt-3.5-turbo")

    def forward(self, **kwargs):
        # Convert SignatureMeta objects to dictionaries
        serializable_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, dspy.Signature):
                serializable_kwargs[key] = {field: getattr(value, field) for field in value.__fields__}
            else:
                serializable_kwargs[key] = value
        
        return self.lm(self.signature, **serializable_kwargs)

    def to_json(self):
        return json.dumps({
            "signature": str(self.signature),
            "lm": str(self.lm)
        })

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        instance = cls(eval(data["signature"]))
        instance.lm = eval(data["lm"])
        return instance
