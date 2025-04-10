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
