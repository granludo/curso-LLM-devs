# Simple file translator using gpt-3.5_turbo 
from openai import OpenAI
import argparse
import os


api_key = os.getenv('OPENAI_API_KEY')
# your api key should be stored in an environment variable or the .env file
client = OpenAI()

def translate_text(text, target_language="Spanish"):
    completion =client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust the model as necessary
        messages=[
            {"role": "system", "content": f"Translate the following text to {target_language}:"},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=120  # Adjust based on expected length of translation
    )
    return completion.choices[0].message.content 


def is_timestamp_line(line):
    # A basic check for timestamp lines in the SRT format: "00:00:01,000 --> 00:00:04,000"
    return '-->' in line

def process_srt_file(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding='utf-8') as input_file, open(output_file_path, 'w', encoding='utf-8') as output_file:
        content_lines = []  # Store subtitle text lines to be translated

        for line in input_file:
            # Write empty lines and numeric identifiers as is
            if line.strip() == '' or line.strip().isdigit():
                if content_lines:  # Translate and write collected content lines before a new subtitle block
                    translated_text = translate_text(' '.join(content_lines))
                    output_file.write(translated_text + '\n')
                    content_lines = []  # Reset content lines
                output_file.write(line)
            elif is_timestamp_line(line.strip()):  # Timestamp lines are written as is
                output_file.write(line)
            else:  # Collect subtitle text lines
                content_lines.append(line.strip())

        # Translate and write any remaining content lines at the end of the file
        if content_lines:
            translated_text = translate_text(' '.join(content_lines))
            output_file.write(translated_text + '\n')

# Example usage
process_srt_file('example.srt', 'ejemplo.srt')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Translate SRT Subtitle Files.')
    parser.add_argument('input_file', type=str, help='The path to the input .srt file')
    parser.add_argument('output_file', type=str, help='The path to the output .srt file')

    args = parser.parse_args()

    process_srt_file(args.input_file, args.output_file)