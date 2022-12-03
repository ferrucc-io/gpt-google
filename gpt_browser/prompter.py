#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_gpt_command(objective, url, previous_command, browser_content, prompt_template):
		prompt = prompt_template
		prompt = prompt.replace("$objective", objective)
		prompt = prompt.replace("$url", url[:100])
		prompt = prompt.replace("$previous_command", previous_command)
		prompt = prompt.replace("$browser_content", browser_content[:4500])
		response = openai.Completion.create(model="text-davinci-002", prompt=prompt, temperature=0.5, best_of=10, n=3, max_tokens=50)
		return response.choices[0].text