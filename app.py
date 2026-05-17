import ollama

print("=== AI DevOps Agent ===")

messages = [
    {
        "role": "system",
        "content": """
        You are a DevOps AI assistant.

        If the user says:
        analyze <filename>

        then analyze that log file.

        Otherwise answer normally.
        """
    }
]

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    # LOG ANALYSIS FEATURE
    if user_input.startswith("analyze "):

        file_name = user_input.replace("analyze ", "")

        try:

            with open(file_name, "r") as file:

                lines = file.readlines()

            # Extract only important logs
            important_logs = []

            for line in lines:

                if "ERROR" in line or "WARNING" in line:
                    important_logs.append(line)

            logs = "".join(important_logs)

            # If no important logs found
            if logs.strip() == "":
                logs = "No ERROR or WARNING logs found."

            prompt = f"""
            Analyze these logs.

            Logs:
            {logs}

            Tasks:
            1. Find issues
            2. Explain problems
            3. Suggest fixes
            4. Give severity level
            """

            response = ollama.chat(
                model="llama3",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            answer = response["message"]["content"]

            # Print analysis
            print("\nAI Analysis:\n")
            print(answer)

            # Save report automatically
            with open("report.txt", "w") as report_file:
                report_file.write(answer)

            print("\nReport saved as report.txt")

        except FileNotFoundError:

            print("\nAI: File not found.")

    # NORMAL CHAT FEATURE
    else:

        messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = ollama.chat(
            model="llama3",
            messages=messages
        )

        answer = response["message"]["content"]

        messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        print("\nAI:", answer)