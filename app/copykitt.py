from multiprocessing.sharedctypes import Value
import os
from typing import List
import openai
import argparse
import re

MAX_INPUT_LENGTH = 12

def main():
    print("Running Copy Kitt!")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True)
    args = parser.parse_args()
    user_input = args.input

    print(f"User input: {user_input}")

    if validate_length(user_input):
        branding_result = generate_branding_snippet(user_input)
        keywords_result = generate_keywords(user_input)
        print(branding_result)
        print(keywords_result)
    else:
        raise ValueError(f"Input length is too long. Must be under {MAX_INPUT_LENGTH}. Submitted input is {user_input}")


def validate_length(prompt: str) -> bool:
    return len(prompt) <= MAX_INPUT_LENGTH


def generate_branding_snippet(prompt: str) -> str:
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"Generate upbeat branding snippet for {prompt}: "

    response = openai.Completion.create(
        model="text-davinci-002", 
        prompt=enriched_prompt, 
        temperature=0.6, 
        max_tokens=32)

    #Get the output text.
    branding_text: str = response["choices"][0]["text"]

    #Strip whitespace
    branding_text = branding_text.strip()

    # Check if the last character is a full stop "."
    last_char = branding_text[-1]
    if last_char not in {".", "!", "?"}:
        branding_text += "..."

    return branding_text


def generate_keywords(prompt: str) -> List[str]: #function takes a str prompt and returns a list of strings
    # Load your API key from an environment variable or secret management service
    openai.api_key = os.getenv("OPENAI_API_KEY")

    enriched_prompt = f"Generate related branding keywords for {prompt}: "

    response = openai.Completion.create(
        model="text-davinci-002", 
        prompt=enriched_prompt, 
        temperature=0.6, 
        max_tokens=32)

    #Get the output text.
    keywords_text: str = response["choices"][0]["text"]

    #Strip whitespace
    keywords_text = keywords_text.strip()
    keywords_array = re.split(",|\n|;|-", keywords_text)
    keywords_array = [k.lower().strip() for k in keywords_array] #remove whitespaces from each keyword in array
    keywords_array = [k for k in keywords_array if len(k) > 0] #only keep keywords that are not empty

    return keywords_array



if __name__ == "__main__":
    main()