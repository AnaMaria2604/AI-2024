import sys
from langdetect import detect
from bs4 import BeautifulSoup
import requests
import re
from collections import Counter


def stylometric_analysis(text):
    clean_text = re.sub(r'[^\w\s]', '', text).lower()
    words = clean_text.split()
    word_frequency = Counter(words)

    ch_count = len(text)
    word_count = len(words)
    sentence_count = len(re.split(r'[.!?]', text)) - 1
    avg_word_length = sum(len(word) for word in words) / \
        word_count if word_count else 0
    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    results = {
        "Character Count": ch_count,
        "Word Count": word_count,
        "Sentence Count": sentence_count,
        "Average Word Length": avg_word_length,
        "Average Sentence Length (in words)": avg_sentence_length,
        "Word Frequency": word_frequency
    }

    return results


def get_supported_languages():
    url = "https://libretranslate.com/languages"  # API pentru limbile suportate
    try:
        response = requests.get(url)
        response.raise_for_status()
        languages = response.json()
        # languages contine JSON de forma
        # [
        #     {"code": "en", "name": "English"},
        #     {"code": "fr", "name": "French"}
        # ]

        # Mapez codurile limbilor (en) cu numele complet al limbii (English)
        language_map = {lang["code"]: lang["name"] for lang in languages}
        # language_map va fi un dictionar de forma
        # {
        #     "en": "English",
        #     "fr": "French",
        #     "es": "Spanish"
        # }

        return language_map

    except requests.exceptions.RequestException as e:
        print(f"Error fetching supported languages: {e}")
        sys.exit(1)


def detect_language(text, language_map):
    # Detectăm limba textului
    text_language = detect(text)

    # Căutăm numele complet al limbii în dicționar
    language = language_map.get(text_language)

    if language is None:
        print(f"Language code '{text_language}' not found in the map.")
        language = "Unknown Language"

    print(f"This text is written in {language}.")


def display_results(results):
    print("\nStylometric Analysis Results:")
    print(f"Character Count: {results['Character Count']}")
    print(f"Word Count: {results['Word Count']}")
    print(f"Sentence Count: {results['Sentence Count']}")
    print(f"Average Word Length: {results['Average Word Length']:.2f}")
    print(f"Average Sentence Length (in words): {
          results['Average Sentence Length (in words)']:.2f}")

    print("\nWord Frequency:")

    for word, freq in results["Word Frequency"].items():
        print(f"  {word}: {freq}")


def command(arg, language_map):
    if arg[1] == "file":
        with open(arg[2], "r") as file:
            content = file.read()
            print(F"The text: {content}")
            detect_language(content, language_map)
            results = stylometric_analysis(content)
            display_results(results)
    elif arg[1] == "text":
        text = " ".join(arg[2:])
        print(F"The text: {text}")
        detect_language(text, language_map)
        results = stylometric_analysis(text)
        display_results(results)

    else:
        print("Invalid command:(")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py file/text text/file_name")
        sys.exit(1)
    else:
        language_map = get_supported_languages()
        command(sys.argv, language_map)


# comanda e cv de genul: "python main.py file data.txt" sau "python main.py text ceva_text"
# ex: python main.py file phrase.txt
