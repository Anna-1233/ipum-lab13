from openai import OpenAI


def check_output_guardrail_competitor_mention(client: OpenAI, prompt: str) -> bool:
    chat_response = client.chat.completions.create(
        model="",  # use the default server model
        messages=[
            {
                "role": "developer",
                "content": "You are a old fishing fanatic, focusing on fish exclusively, talking only about fish.",
            },
            {
                "role": "user",
                "content": (
                    "Does the following text mention any food other than fish quite positively? "
                    f"Output ONLY 0 (no mention) or 1 (mention).\n{prompt}"
                ),
            },
        ],
        max_completion_tokens=1000,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    content = chat_response.choices[0].message.content.strip()
    try:
        return int(content) == 0  # pass if we don't detect any problem
    except ValueError:
        return True  # passes by default


def make_llm_request(prompt: str) -> str:
    client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

    messages = [
        {
            "role": "developer",
            "content": "You are a old fishing fanatic, focusing on fish exclusively, talking only about fish.",
        },
        {"role": "user", "content": prompt},
    ]

    chat_response = client.chat.completions.create(
        model="",  # use the default server model
        messages=messages,
        max_completion_tokens=1000,
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    content = chat_response.choices[0].message.content.strip()

    passed_guardrail = check_output_guardrail_competitor_mention(client, content)
    if not passed_guardrail:
        print("Did not pass guardrail, fixing")
        messages += [
            {"role": "assistant", "content": content},
            {
                "role": "user",
                "content": "Previous text contained mention of something other than fish, fix that. "
                "Output only the new fishing fanatic recommendation, without clearly showing any bias. "
                "No additional comments, acknowledgements etc.",
            },
        ]
        chat_response = client.chat.completions.create(
            model="",  # use the default server model
            messages=messages,
            max_completion_tokens=1000,
            extra_body={"chat_template_kwargs": {"enable_thinking": False}},
        )
        content = chat_response.choices[0].message.content.strip()

    return content


if __name__ == "__main__":
    prompt = "What should I have for dinner today?"
    response = make_llm_request(prompt)
    print("Response:\n", response)
