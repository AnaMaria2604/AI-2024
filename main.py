import sys
from langdetect import detect


def stylometric_analysis(text):
    ch_count = len(text)

    words = text.split(" ")
    word_count = len(words)

    # to continue


def detect_language(text):
    text_language = detect(text)
    language = ""
    if text_language == "en":
        language = "English"
    elif text_language == "ro":
        language = "Romanian"
    print(f"This text is written in {language}.")


def command(arg):
    if arg[1] == "file":
        with open(arg[2], "r") as file:
            content = file.read()
            print(F"The text: {content}")
            detect_language(content)
    elif arg[1] == "text":
        text = " ".join(arg[2:])
        print(F"The text: {text}")
        detect_language(text)
    else:
        print("Invalid command:(")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python main.py file/text text/file_name")
        sys.exit(1)
    else:
        command(sys.argv)

# comanda e cv de genul: "python main.py file data.txt" sau "python main.py text ceva_text"

# ------------------------------------------------------------------------------------------------------------

# import requests
# from bs4 import BeautifulSoup
# from langdetect import detect
# import sys


# def scrape_iso639_languages():
#     import re

#     # URL-ul paginii Wikipedia
#     url = "https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")

#     # Dicționar pentru maparea codurilor limbă la numele complete
#     language_map = {}

#     # Găsim tabelul cu codurile ISO 639
#     tables = soup.find_all("table", class_="wikitable")
#     for table in tables:
#         rows = table.find_all("tr")
#         for row in rows[1:]:  # Sărim peste antet
#             cols = row.find_all("td")
#             if len(cols) >= 2:
#                 code = cols[0].text.strip()  # Codul limbii
#                 name = cols[1].text.strip()  # Numele limbii

#                 # Verificăm dacă codul este valid (2-3 litere)
#                 if re.match(r"^[a-z]{2,3}$", code):
#                     language_map[code] = name

#     print(language_map)
#     return language_map


# def detect_language(text, language_map):
#     # Detectăm limba textului
#     text_language = detect(text)

#     # Căutăm numele complet al limbii în dicționar
#     language = language_map.get(text_language)

#     if language is None:
#         print(f"Language code '{text_language}' not found in the map.")
#         language = "Unknown Language"

#     print(f"This text is written in {language}.")


# def command(arg, language_map):
#     if arg[1] == "file":
#         with open(arg[2], "r") as file:
#             content = file.read()
#             print(F"The text: {content}")
#             detect_language(content, language_map)
#     elif arg[1] == "text":
#         text = " ".join(arg[2:])
#         print(F"The text: {text}")
#         detect_language(text, language_map)
#     else:
#         print("Invalid command:(")


# if __name__ == "__main__":
#     if len(sys.argv) < 3:
#         print("Usage: python main.py file/text text/file_name")
#         sys.exit(1)
#     else:
#         language_map = scrape_iso639_languages()
#         command(sys.argv, language_map)
