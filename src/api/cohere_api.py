import os
import cohere
from dotenv import load_dotenv

load_dotenv()
co = cohere.ClientV2(os.getenv("COHERE_API_KEY"))


def generate_slides(text: str) -> str:
    prompt = f"""
Create a presentation based on the following content. Break it into slides with 
clear titles and 3–5 bullet points each. Also write a short presenter script for
 each slide.

Content:
{text}

Output format:
Slide 1:
Title: ...
Bullet Points:
- ...
- ...
- ...
Presenter Script: ...
"""
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content[0].text.strip()

