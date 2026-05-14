import ollama

print("=== Local AI DevOps Assistant ===")

while True:
    user_input = input("\nAsk something: ")

    if user_input.lower() == "exit":
        break

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful DevOps assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        )

        print("\nAI:", response["message"]["content"])

    except Exception as e:
        print("\nError:", e)