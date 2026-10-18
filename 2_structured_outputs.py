from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

client = OpenAI()

# ---- 1. The problem - unstructured output ----
# result = client.responses.create(
#     model="gpt-4o",
#     instructions="You are a helpful assistant.",
#     input="Give me the name, age and city of a fictional person."
# )

# print(result.output_text)

# print(type(result.output_text))
# Output: "Sure! Here's a fictional person: Name: John Smith, Age: 32, City: Chicago"
# You can't reliably parse this in your code

# ---- 2. Naive fix - ask for JSON in the prompt ----
# result = client.responses.create(
#     model="gpt-4o",
#     instructions="You are a helpful assistant. Respond in JSON format.",
#     input="Give me the name, age and city of a fictional person."
# )

# print(result.output_text)
#print(type(result.output_text))
# # Sometimes works, but the model might wrap it in ```json ``` blocks
# # or change the key names, or add extra fields
# # Not reliable enough for production



# ---- What is Pydantic? ----
# Pydantic lets you define the exact "shape" of data you expect.
# Each field has a name and a type (str, int, float, bool, list, etc.)
#
# When you pass text_format=Person, the SDK converts this class into a
# JSON schema and sends it to OpenAI's servers. The model is constrained
# AT THE SERVER LEVEL to only return data that matches this schema.
#
# This is the key difference:
# "Respond in JSON" in the prompt = a suggestion the model can ignore
# text_format=Person = a guarantee enforced before the response reaches you

# ---- 3. Structured output with Pydantic ----
class Person(BaseModel):
    name: str
    age: int
    city: str

result = client.responses.parse(
    model="gpt-4o",
    instructions="You are a helpful assistant.",
    input="Give me the name, age and city of a fictional person.",
    text_format=Person  
)

person = result.output_parsed
print(person)
print(person.name)
print(person.age)
print(person.city)