from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="Enter you api key"
)

def get_response(prompt):
    """
    Sends a prompt to the OpenAI API and returns the generated content.
    
    Args:
        prompt (str): The user's input question or command.

    Returns:
        str: The generated response content.
    """
    content = ""
    completion = client.chat.completions.create(
        model="meta/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        top_p=1,
        max_tokens=1024,
        stream=True
    )
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            content += chunk.choices[0].delta.content
    return content
