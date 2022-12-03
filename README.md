# Let GPT-3 answer questions using Google for you

## What is this?

Use GPT-3 to answer questions using Google for you. This is a simple script that uses the OpenAI API to generate a question and then uses Google to answer it. It's a fun way to play with GPT-3 and see what it can do.

## How to use

1. Create an [OpenAI API](https://openai.com/api/) key and save it your environment variables as `OPENAI_API_KEY` - See (`.env.example`)[.env.example] for an example.
2. Run `pip install -r requirements.txt` to install the dependencies.
3. Run `python main.py` to run the script.
4. Write your question and keep pressing enter to see GPT-3 making steps to answer it.

## Credits

This script is almost entirely based on [this](https://github.com/nat/natbot/blob/main/natbot.py). Just focused on answering questions using Google and with easier to install dependencies.
