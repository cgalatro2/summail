from openai import OpenAI

client = OpenAI()


def summarize_email(text):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You summarize newsletters into 3 bullet points.",
            },
            {"role": "user", "content": f"Summarize this newsletter:\n\n{text}"},
        ],
    )
    return response.choices[0].message.content
