from openai import OpenAI

client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="openai/gpt-3.5-turbo",  # You can also try "mistralai/mixtral-8x7b", "google/gemini-pro"
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# Chat loop
while True:
    user_input = input("You: ")
    reply = chat_with_gpt(user_input)
    print("Bot:", reply)
