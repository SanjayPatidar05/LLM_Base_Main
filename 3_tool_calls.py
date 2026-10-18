from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()


# ---- 0. The problem - model has no access to real-time data ----
# result = client.responses.create(
#     model="gpt-4o",
#     input="What is the current weather in Bangalore?"
# )
# print(result.output_text)
# # Output: "I don't have access to real-time weather data."


# ---- 1. Define the actual Python function ----
def get_weather(city: str):
    return {
        "city": city,
        "temperature": 28,
        "unit": "celsius",
        "condition": "sunny"
    }

# # ---- 2. Describe the function to the model (the tool definition) ----
tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get the current weather for a given city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city to get weather for"
                } 
            },
            "required": ["city"]
        }
    }
]


# # ---- 3. Step 1 - Send the question and tools to the model ----
input_messages = [{"role": "user", "content": "What is the current weather in Hyderabad?"}]

result = client.responses.create(
    model="gpt-4o",
    input=input_messages,
    tools=tools
)

# print(json.dumps(result.to_dict(), indent=2))


# # # ---- 4. Extract the function name and arguments ----
tool_call = result.output[0]
function_name = tool_call.name
function_args = json.loads(tool_call.arguments)

#print(tool_call)


# # # ---- 5. Run the function ourselves ----
function_result = get_weather(function_args["city"])

# print(f"🔧 Tool called: {function_name}({', '.join(f'{k}={v}' for k, v in function_args.items())})")
# print(f"📦 Raw result: {function_result}")


# # # ---- 6. Build the full history and send everything back ----
input_messages.append(tool_call)
input_messages.append({
    "type": "function_call_output",
    "call_id": tool_call.call_id,
    "output": json.dumps(function_result)
})

# print(input_messages)

final_result = client.responses.create(
    model="gpt-4o",
    input=input_messages,
    tools=tools
)

print(f"\n💬 Final answer: {final_result.output_text}")