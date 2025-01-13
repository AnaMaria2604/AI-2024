import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.probability import FreqDist
from langdetect import detect
import random
from collections import Counter
import spacy
from rake_nltk import Rake
from nltk.corpus import wordnet as wn
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

class StylometricAnalyzer:
    def __init__(self):
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)

    def analyze(self, text):
        words = word_tokenize(text)
        filtered_words = [word for word in words if word.isalnum()]
        chars = len(text)
        word_count = len(filtered_words)

        freq_dist = FreqDist(filtered_words)
        most_common = freq_dist.most_common(10)

        avg_word_length = sum(len(word) for word in filtered_words) / word_count if word_count > 0 else 0

        sentences = sent_tokenize(text)
        sentence_count = len(sentences)

        return {
            'character_count': chars,
            'word_count': word_count,
            'sentence_count': sentence_count,
            'average_word_length': round(avg_word_length, 2),
            'most_common_words': most_common
        }
class TextGenerator:
    def __init__(self):
        nltk.download('wordnet', quiet=True)
        nltk.download('omw-1.4', quiet=True)
        self.nlp_ro = spacy.load('ro_core_news_sm')

    def generate_alternative(self, text, language='ro'):
        doc = self.nlp_ro(text)
        tokens = [token for token in doc if not token.is_punct and not token.is_space]

        content_tokens = [token for token in tokens if token.pos_ in ['NOUN', 'VERB', 'ADJ']]

        words_to_replace = max(1, int(len(content_tokens) * random.uniform(0.7, 0.8)))
        tokens_to_replace = random.sample(content_tokens, words_to_replace)

        changes = {}
        new_text = text

        for token in tokens_to_replace:
            word = token.text
            pos = token.pos_

            alternatives = self._get_alternatives(word, pos, language)

            if alternatives:
                filtered_alternatives = [alt for alt in alternatives
                                      if 0.5 * len(word) <= len(alt) <= 2 * len(word)]

                if filtered_alternatives:
                    new_word = self._select_contextual_replacement(
                        filtered_alternatives,
                        token,
                        doc
                    )

                    if word[0].isupper():
                        new_word = new_word.capitalize()

                    new_text = new_text.replace(word, new_word)
                    changes[word] = new_word

        return new_text, changes

    def _get_alternatives(self, word, pos, language):
        alternatives = set()

        synsets = wn.synsets(word, lang='ron' if language == 'ro' else 'eng')
        if not synsets:
            synsets = wn.synsets(word)

        for synset in synsets:
            alternatives.update(lemma.name().replace('_', ' ')
                             for lemma in synset.lemmas(lang='ron' if language == 'ro' else 'eng'))

            if pos == 'NOUN':
                for hypernym in synset.hypernyms():
                    alternatives.update(lemma.name().replace('_', ' ')
                                     for lemma in hypernym.lemmas(lang='ron' if language == 'ro' else 'eng'))

            if pos == 'ADJ':
                for lemma in synset.lemmas(lang='ron' if language == 'ro' else 'eng'):
                    if lemma.antonyms():
                        alternatives.update(ant.name().replace('_', ' ')
                                         for ant in lemma.antonyms())

        return list(alternatives)

    def _select_contextual_replacement(self, alternatives, token, doc):
        context_start = max(0, token.i - 2)
        context_end = min(len(doc), token.i + 3)
        context = doc[context_start:context_end]

        best_alternative = alternatives[0]
        best_score = float('-inf')

        for alternative in alternatives:
            score = 0
            alt_doc = self.nlp_ro(alternative)
            if len(alt_doc) > 0:
                alt_token = alt_doc[0]

                if token.pos_ == 'NOUN' and token.morph.get('Number'):
                    if token.morph.get('Number') == alt_token.morph.get('Number'):
                        score += 1

                if token.morph.get('Gender') and alt_token.morph.get('Gender'):
                    if token.morph.get('Gender') == alt_token.morph.get('Gender'):
                        score += 1

            if score > best_score:
                best_score = score
                best_alternative = alternative

        return best_alternative
class KeywordExtractor:
    def __init__(self):
        self.nlp_ro = spacy.load('ro_core_news_sm')
        self.rake = Rake()

    def extract_keywords(self, text, language='ro'):
        if language == 'ro':
            return self._extract_keywords_romanian(text)
        return self._extract_keywords_english(text)

    def _extract_keywords_romanian(self, text):
        doc = self.nlp_ro(text)

        keywords = []
        for token in doc:
            if token.pos_ in ['NOUN', 'VERB'] and not token.is_stop:
                keywords.append(token.text)

        keyword_freq = Counter(keywords)
        top_keywords = [word for word, freq in keyword_freq.most_common(5)]

        sentences = []
        for sent in doc.sents:
            for keyword in top_keywords:
                if keyword in sent.text:
                    sentences.append(f"Cuvânt cheie '{keyword}': {sent.text.strip()}")
                    break

        return top_keywords, sentences

    def _extract_keywords_english(self, text):
        self.rake.extract_keywords_from_text(text)
        keywords = self.rake.get_ranked_phrases()[:5]

        sentences = []
        doc = self.nlp_ro(text)
        for keyword in keywords:
            for sent in doc.sents:
                if keyword.lower() in sent.text.lower():
                    sentences.append(f"Keyword '{keyword}': {sent.text.strip()}")
                    break

        return keywords, sentences
def main():
    reader = TextReader()
    detector = LanguageDetector()
    analyzer = StylometricAnalyzer()
    generator = TextGenerator()
    extractor = KeywordExtractor()

    filenames = [
        "input_en.txt",
        "input_ro.txt",
    ]

    results = []
    for filename in filenames:
        try:
            text = reader.read_text(filename)
            language = detector.detect_language(text)
            print(f"\nDetected Language: {language}")

            style_info = analyzer.analyze(text)
            print("\nStylometric Information:")
            for key, value in style_info.items():
                print(f"{key}: {value}")

            alt_text, changes = generator.generate_alternative(text, language[:2].lower())
            print("\nAlternative Version and Changes:")
            print(alt_text)
            print("\nChanges Made:")
            for original, alternative in changes.items():
                print(f"{original} -> {alternative}")

            keywords, sentences = extractor.extract_keywords(text, language[:2].lower())
            print("\nKeywords and Associated Sentences:")
            print("Keywords:", keywords)
            print("\nGenerated Sentences:")
            for sentence in sentences:
                print(sentence)

        except Exception as e:
            print(f"Error processing {filename}: {str(e)}")

if __name__ == "__main__":
    main()