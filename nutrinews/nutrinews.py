# Copyright Dave Vandenbout
# MIT license.

import argparse
import requests
import sys
import os
import openai
import pyperclip as clipbrd
import tempfile
import bs4


def get_args():
    parser = argparse.ArgumentParser(
        prog="nutrinews", description="Remove bias from some text."
    )
    parser.add_argument(
        "-m", "--model", choices=["3.5", "4"], default="3.5", help="GPT model to use."
    )
    parser.add_argument(
        "-p",
        "--prompt",
        default="",
        help="File containing instructions for removing bias.",
    )
    parser.add_argument("--url", metavar="URL", help="Get text from this URL.")
    parser.add_argument("-f", "--file", help="Get text from this file.")
    parser.add_argument(
        "-c", "--clipboard", action="store_true", help="Get text from the clipboard."
    )
    parser.add_argument(
        "-d", "--diff", help="Specify tool to diff the original and nutritious text."
    )
    return parser.parse_args()


def get_text_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return bs4.BeautifulSoup(response.text, "html.parser").get_text()
    else:
        print(f"Error getting text from {url}.")
        sys.exit()


def remove_bias(text, model, prompt):
    """Send text and prompt to LLM."""

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        print(
            "Create an account at OpenAI and get an API key here: https://platform.openai.com/account/api-keys"
        )
        sys.exit()

    msg = {"role": "user", "content": prompt + "\n\n" + text}
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[msg])
    return response.choices[0].message.content


def limit_line_length(text):
    """Limit text lines to 72 characters (more or less)."""
    l = 72

    def split_text(txt):
        while txt:
            for i in range(0, len(txt)):
                if txt[i] in "\n":
                    yield txt[0 : i + 1]
                    txt = txt[i + 1 :]
                    break
                elif i >= l and txt[i] in " \t":
                    yield txt[0:i]
                    txt = txt[i + 1 :]
                    break
            else:
                yield txt
                return
        yield txt
        return

    splits = split_text(text)
    return "\n".join([line for line in splits])


def main():
    args = get_args()

    # Get the LLM model.
    model = {"3.5": "gpt-3.5-turbo", "4": "gpt-4"}[args.model]

    # Get the prompt to enforce fairness.
    if args.prompt:
        try:
            with open(args.prompt, "r") as fp:
                fairness_prompt = fp.read()
        except FileNotFoundError:
            print(f"Could not find file with the fairness prompt: {args.prompt}")
            sys.exit()
    else:
        fairness_prompt = "[1] - Rewrite the article below to make it more informative, truth-focused, and neutral.\n[2] - Compare the original article to the rewrite, and describe the bias of the original, use a numbered list if needed."

    # Get the original text.
    if args.url:
        # From a URL.
        article_text = get_text_from_url(args.url)
        # From the clipboard.
    elif args.clipboard:
        article_text = clipbrd.paste()
    elif args.file:
        # From a file.
        try:
            with open(args.file, "r") as fp:
                article_text = fp.read()
        except FileNotFoundError:
            print(f"No such file: {args.file}")
            sys.exit()
    else:
        print("There's no text to nutrify. Feed me!")
        sys.exit()

    # Pass the article text and prompt to the LLM.
    article_text = limit_line_length(article_text)
    nutritious_text = remove_bias(article_text, model, fairness_prompt)
    nutritious_text = limit_line_length(nutritious_text)

    # Print the article with bias removed.
    print(nutritious_text)

    # Show the differences between the original and the unbiased text.
    if args.diff:
        with tempfile.TemporaryDirectory() as tmpd:
            original_name = os.path.join(tmpd, "original")
            nutritious_name = os.path.join(tmpd, "nutritious")
            with open(original_name, "w") as fp:
                fp.write(article_text)
            with open(nutritious_name, "w") as fp:
                fp.write(nutritious_text)
            os.system(f"{args.diff} {original_name} {nutritious_name}")
