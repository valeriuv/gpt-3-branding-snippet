
import os
import openai
from decouple import config
import argparse
from typing import List
import re

MAX_INPUT_LENGTH = 32


def main():
	parser = argparse.ArgumentParser() # add CLI argument for prompt
	parser.add_argument('--input', '-i', type=str, required=True)
	args = parser.parse_args()
	user_input = args.input

	print(f"User input: {user_input}")

	if validate_length(user_input):
		generate_branding_snippet(user_input)
		generate_keywords(user_input)
	else:
		raise ValueError(
			f"Input is too large. Must be under {MAX_INPUT_LENGTH} characters. Submitted input is {len(user_input)} characters."
			)


def validate_length(prompt: str) -> bool:
	return len(prompt) <= MAX_INPUT_LENGTH


def generate_branding_snippet(prompt: str) -> str:
	openai.api_key = config("OPENAI_API_KEY")
	enriched_prompt = f"Generate upbeat branding snippet for {prompt}: "
	print(enriched_prompt)

	response = openai.Completion.create(
		model="text-curie-001",
		prompt=enriched_prompt,
		max_tokens=32,
		temperature=0.8
	)

	branding_text: str = response["choices"][0]["text"] 	#Get the output text.
	branding_text = branding_text.strip() 					#Strip whitespace

	last_char = branding_text[-1]		# If the text doesn't have a sentence end, add "..." 
	if last_char not in {".", "!", "?"}:  
		branding_text += "..."

	print(f"Branding snippet: {branding_text}")
	return branding_text


def generate_keywords(prompt: str) -> List[str]:
	openai.api_key = config("OPENAI_API_KEY")
	enriched_prompt = f"Generate related branding keywords for {prompt}: "
	print(enriched_prompt)

	response = openai.Completion.create(
		model="text-curie-001",
		prompt=enriched_prompt,
		max_tokens=32,
		temperature=0.8
	)

	keywords_text: str = response["choices"][0]["text"] 	#Get the output text.
	keywords_text = keywords_text.strip() 					#Strip whitespace

	keywords_array = re.split(",|\n|;|\\||\*|\·|-", keywords_text)
	keywords_array = [k.lower().strip() for k in keywords_array]
	keywords_array = [k for k in keywords_array if len(k) > 0]

	print(f"Keywords: {keywords_array}")
	return keywords_array





if __name__ == '__main__':
	main()