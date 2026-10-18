from openai import OpenAI   
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

# ---- 1. Simplest possible API call ----
# result = client.responses.create(
#     model="gpt-4o",
#     input="What is the square root of 49? and how is hyderabad"
# )

# ---- 2. What does the full response object look like? ----
#print(result)

# ---- 2.5. What does the raw JSON OpenAI response look like? ----
#print(json.dumps(result.to_dict(), indent=2))

# # ---- 3. Extract just the text ----
#print(result.output_text)

# ---- 4. Multi-turn conversation (passing a list of messages) ----
# result = client.responses.create(
#     model="gpt-4o",
#     instructions="You are a helpful assistant.",
#     input=[
#         {"role": "user", "content": "My name is denanath chohan"},
#         {"role": "assistant", "content": "Nice to meet you Harish!"},
#         {"role": "user", "content": "What is my name?"}
#     ]
# )

# print(result.output_text)

# ---- 5. Now add system prompt, temperature, max_tokens ----
# result = client.responses.create(
#     model="gpt-4o",
#     instructions="You are a helpful assistant who makes jokes.",
#     input="What is the square root of 49?",
#     temperature=0.7,
#     max_output_tokens=100
# )

# print(result.output_text)

# # # # ---- 6. Token usage ----
# print(f"Input tokens: {result.usage.input_tokens}")
# print(f"Output tokens: {result.usage.output_tokens}")
# print(f"Total tokens: {result.usage.total_tokens}")

# # ---- 7. Streaming ----
stream = client.responses.create(
    model="gpt-4o",
    instructions="You are a helpful assistant.",
    input="Tell me a short story about a robot.",
    stream=True
)

for event in stream:
    if hasattr(event, 'delta'):
        print(event.delta, end="", flush=True)