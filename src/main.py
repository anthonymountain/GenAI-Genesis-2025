from src.api.cohere_api import generate_slides
from src.api.gemini_api import generate_image_from_prompt
from src.parser.pptx_parser import create_pptx_from_response
import os


def extract_slide_blocks(response_text):
    slides = response_text.split("Slide")[1:]
    slide_blocks = []

    for raw_slide in slides:
        lines = raw_slide.strip().split("\n")
        title = ""
        bullets = []
        for line in lines:
            if line.startswith("Title:"):
                title = line.replace("Title:", "").strip()
            elif line.startswith("-"):
                bullets.append(line.strip())
        slide_blocks.append((title, bullets))

    return slide_blocks


def main():
    user_input = input("Paste your topic or text: ")
    print("Generating slides with Cohere...")
    response_text = generate_slides(user_input)

    print("Parsing slide structure...")
    slide_blocks = extract_slide_blocks(response_text)

    print("Generating images with Gemini...")
    image_paths = []
    os.makedirs("generated_images", exist_ok=True)

    for i, (title, bullets) in enumerate(slide_blocks):
        prompt = f"Generate a 3D-rendered image for a slide titled '{title}' with context: {', '.join(bullets)}"
        filename = f"generated_images/slide_{i+1}.png"
        print(f"Generating image for slide {i+1}...")
        try:
            image_path = generate_image_from_prompt(prompt, filename)
            image_paths.append(image_path)
        except Exception as e:
            print(f"Failed to generate image for slide {i+1}: {e}")
            image_paths.append(None)

    print("Creating final presentation...")
    output_path = create_pptx_from_response(response_text, slide_images=image_paths)
    print(f"Presentation saved as {output_path}")


if __name__ == "__main__":
    main()
