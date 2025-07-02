from openai import OpenAI

client = OpenAI()


def summarize_email(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're an email digest assistant. "
                    "Summarize in 3-7 bullets only the most important ideas, with each point concise."
                    "Avoid assistant-style intros and don't include markdown formatting like bold or italics."
                ),
            },
            {"role": "user", "content": f"{text}"},
        ],
    )
    return response.choices[0].message.content.strip()
