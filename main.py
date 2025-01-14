import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from langdetect import detect
import random
from collections import Counter
import spacy
from rake_nltk import Rake
from nltk.corpus import wordnet as wn
import json
import tkinter as tk
from tkinter import messagebox
from read_and_classification import predict_and_generate_output
from PIL import Image, ImageTk
import os


attributes_dict = {
    "Sex": [
        ("M", "male", 0.0),
        ("F", "female", 1.0)
    ],
    "Age": [
        ("Moinsde1", "Less than 1 year", 0.0),
        ("1a2", "1-2 years", 1.0),
        ("2a10", "2-10 years", 2.0),
        ("Plusde10", "More than 10 years", 3.0)
    ],
    "Number": [
        ("1", "one cat in the household", 1.0),
        ("2", "two cats in the household", 2.0),
        ("3", "three cats in the household", 3.0),
        ("4", "four cats in the household", 4.0),
        ("5", "five cats in the household", 5.0),
        ("Plusde5", "more than five cats in the household", 0.0),
    ],
    "Home": [
        ("ASB", "Apartment without balcony", 0.0),
        ("AAB", "Apartment with balcony or terrace", 1.0),
        ("ML", "House in a subdivision", 2.0),
        ("MI", "Individual house", 3.0)
    ],
    "Zone": [
        ("U", "Urban", 0.0),
        ("PU", "Periurban", 1.0),
        ("R", "Rural", 2.0)
    ],
    "Ext": [
        ("1", "no time outside", 0.0),
        ("2", "less than one hour outside", 1.0),
        ("3", "1 to 5 hours outside", 2.0),
        ("4", "more than 5 hours outside", 3.0),
        ("5", "All the time outside", 4.0)
    ],
    "Obs": [
        ("1", "None", 0.0),
        ("2", "Limited (less than one hour)", 1.0),
        ("3", "Moderate (1 to 5 hours)", 2.0),
        ("4", "Long (more than 5 hours)", 3.0)
    ],
    "Shy": [
        ("1", "reclusive", 1.0),
        ("2", "introverted", 2.0),
        ("3", "reserved", 3.0),
        ("4", "timid", 4.0),
        ("5", "bold", 5.0)
    ],
    "Calm": [
        ("1", "tense", 1.0),
        ("2", "serene", 2.0),
        ("3", "composed", 3.0),
        ("4", "tranquil", 4.0),
        ("5", "peaceful", 5.0)
    ],
    "Frightened": [
        ("1", "petrified", 1.0),
        ("2", "terrified", 2.0),
        ("3", "alarmed", 3.0),
        ("4", "anxious", 4.0),
        ("5", "brave", 5.0)
    ],
    "Intelligent": [
        ("1", "dull", 1.0),
        ("2", "smart", 2.0),
        ("3", "clever", 3.0),
        ("4", "bright", 4.0),
        ("5", "brilliant", 5.0)
    ],
    "Vigilant": [
        ("1", "careless", 1.0),
        ("2", "alert", 2.0),
        ("3", "attentive", 3.0),
        ("4", "watchful", 4.0),
        ("5", "observant", 5.0)
    ],
    "Persevering": [
        ("1", "lazy", 1.0),
        ("2", "determined", 2.0),
        ("3", "persistent", 3.0),
        ("4", "dedicated", 4.0),
        ("5", "resolute", 5.0)
    ],
    "Affectionate": [
        ("1", "cold", 1.0),
        ("2", "warm", 2.0),
        ("3", "loving", 3.0),
        ("4", "tender", 4.0),
        ("5", "devoted", 5.0)
    ],
    "Friendly": [
        ("1", "hostile", 1.0),
        ("2", "cordial", 2.0),
        ("3", "kind", 3.0),
        ("4", "pleasant", 4.0),
        ("5", "amiable", 5.0)
    ],
    "Solitary": [
        ("1", "social", 1.0),
        ("2", "lonely", 2.0),
        ("3", "isolated", 3.0),
        ("4", "introverted", 4.0),
        ("5", "reclusive", 5.0)
    ],
    "Brutal": [
        ("1", "gentle", 1.0),
        ("2", "rough", 2.0),
        ("3", "harsh", 3.0),
        ("4", "fierce", 4.0),
        ("5", "savage", 5.0)
    ],
    "Dominant": [
        ("1", "submissive", 1.0),
        ("2", "controlling", 2.0),
        ("3", "assertive", 3.0),
        ("4", "commanding", 4.0),
        ("5", "overbearing", 5.0)
    ],
    "Aggressive": [
        ("1", "calm", 1.0),
        ("2", "pushy", 2.0),
        ("3", "forceful", 3.0),
        ("4", "hostile", 4.0),
        ("5", "violent", 5.0)
    ],
    "Impulsive": [
        ("1", "cautious", 1.0),
        ("2", "hasty", 2.0),
        ("3", "reckless", 3.0),
        ("4", "spontaneous", 4.0),
        ("5", "unrestrained", 5.0)
    ],
    "Predictable": [
        ("1", "erratic", 1.0),
        ("2", "regular", 2.0),
        ("3", "steady", 3.0),
        ("4", "reliable", 4.0),
        ("5", "consistent", 5.0)
    ],
    "Distracted": [
        ("1", "focused", 1.0),
        ("2", "diverted", 2.0),
        ("3", "preoccupied", 3.0),
        ("4", "unfocused", 4.0),
        ("5", "scattered", 5.0)
    ],
    "Abundance": [
        ("1", "Low", 0.0),
        ("2", "Moderate", 1.0),
        ("3", "High", 2.0),
        ("NSP", "I don’t know", 3.0)
    ],
    "PredBird": [
        ("1", "Never", 0),
        ("2", "Rarely (1 to 5 times a year)", 1.0),
        ("3", "Sometimes (5 to 10 times a year)", 2.0),
        ("4", "Often (1 to 3 times a month)", 3.0),
        ("5", "Very often (once a week or more)", 4.0)
    ],
    "PredMamm": [
        ("1", "Never", 0),
        ("2", "Rarely (1 to 5 times a year)", 1.0),
        ("3", "Sometimes (5 to 10 times a year)", 2.0),
        ("4", "Often (1 to 3 times a month)", 3.0),
        ("5", "Very often (once a week or more)", 4.0)
    ]
}

class TextReader:
    @staticmethod
    def read_text(source):
        if source.endswith('.txt'):
            try:
                with open(source, 'r', encoding='utf-8') as file:
                    return file.read()
            except FileNotFoundError:
                raise Exception(f"File not found: {source}")
            except Exception as e:
                raise Exception(f"Error reading file: {str(e)}")
        return source


class LanguageDetector:
    @staticmethod
    def detect_language(text):
        try:
            lang = detect(text)
            lang_names = {
                'ro': 'Romanian',
                'en': 'English',
                'fr': 'French',
                'de': 'German',
                'es': 'Spanish',
                'it': 'Italian',
                'pt': 'Portuguese',
                'nl': 'Dutch',
                'pl': 'Polish',
                'hu': 'Hungarian',

            }
            return lang_names.get(lang, lang)
        except:
            return "Could not detect language"

class AttributeMatcher:
    def __init__(self, attributes):
        self.attributes = attributes
        self.nlp = spacy.load("en_core_web_sm")

    def match_attributes(self, text):
        characteristics = {key: None for key in self.attributes.keys()}
        sentences = sent_tokenize(text)

        for sentence in sentences:
            print(f"Analyzing sentence: {sentence}")
            words = word_tokenize(sentence)
            for key, values in self.attributes.items():
                for _, word, value in values:
                    if word in words:
                        characteristics[key] = value
                        print(f"Found attribute match: {word} -> {key}: {value}")

            doc = self.nlp(sentence)
            important_words = [token.text for token in doc if token.pos_ in ["NOUN", "VERB", "ADJ"]]

            for key, values in self.attributes.items():
                for _, word, value in values:
                    if word in important_words:
                        characteristics[key] = value
                        print(f"Found attribute match in important words: {word} -> {key}: {value}")

        characteristics = {k: (v if v is not None else 3.0) for k, v in characteristics.items()}
        return characteristics

def predict_attributes():
    user_input = text_entry.get("1.0", tk.END).strip()
    if user_input:
        matcher = AttributeMatcher(attributes_dict)
        characteristics = matcher.match_attributes(user_input)
        
        # Adding "More": "0.0" to the characteristics dictionary
        characteristics["More"] = 0.0

        print("\nExtracted Characteristics:")
        for key, value in characteristics.items():
            print(f"{key}: {value}")

        output_path = "predict_data.json"
        with open(output_path, "w") as json_file:
            json.dump([characteristics], json_file, indent=4)
        print(f"\nResults saved to {output_path}")

        output = json.dumps(characteristics, indent=4)
        messagebox.showinfo("Predicted Attributes", output)
    else:
        messagebox.showwarning("Warning", "Please enter some text before predicting.")

def display_results():
    try:
        output = predict_and_generate_output()

        # Extract predicted race from the output
        predicted_race = output.split(": ")[1].strip() 

        image_path = os.path.join("images", f"{predicted_race}.jpg")
        if not os.path.exists(image_path):
            image_path = os.path.join("images", "other.jpg")  

        # Open and resize the image while preserving aspect ratio
        image = Image.open(image_path)
        max_size = (500, 500)  # Maximum width and height
        image.thumbnail(max_size, Image.Resampling.LANCZOS)

        img = ImageTk.PhotoImage(image)

        # Create a new window for the result
        result_window = tk.Toplevel(root)
        result_window.title("Prediction Results")

        # Add the image to the new window
        img_label = tk.Label(result_window, image=img)
        img_label.image = img
        img_label.pack()

        # add text
        text_label = tk.Label(
        result_window, 
        text=f"Predicted Race: {predicted_race}", 
        font=("Arial", 14, "bold"),  
        fg="#333333",               
        bg="#f0f0f0"                
        )
        text_label.pack(pady=10)  

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while displaying results: {str(e)}")



# Creează fereastra principală
root = tk.Tk()
root.title("Attribute Matcher")
root.geometry("600x400")

# Label
label = tk.Label(root, text="Enter text to match attributes:")
label.pack(pady=10)

# Frame pentru text și scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=10, fill=tk.BOTH, expand=True)

# Text widget
text_entry = tk.Text(text_frame, wrap=tk.WORD, height=10)
text_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar
scrollbar = tk.Scrollbar(text_frame, command=text_entry.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Asociază scrollbar-ul cu widget-ul Text
text_entry.config(yscrollcommand=scrollbar.set)

# Predict Attributes Button
predict_button = tk.Button(root, text="Predict Attributes", command=predict_attributes)
predict_button.pack(pady=10)

# Predict Race Button
race_button = tk.Button(root, text="Predict Race", command=display_results)
race_button.pack(pady=10)

# Rulează aplicația GUI
root.mainloop()
