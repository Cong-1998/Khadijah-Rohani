from .analyzer import Analyzer
from .khadijah_rohani import KhadijahRohani

class Readability:
    def __init__(self, text):
        self._analyzer = Analyzer()
        self._statistics = self._analyzer.analyze(text)

    def khadijah_rohani(self):
        """Calculate Khadijah Rohani Readability Level."""
        return KhadijahRohani(self._statistics).score()

    def statistics(self):
        return {
            'num_words': self._statistics.num_words,
            'num_sentences': self._statistics.num_sentences,
            'num_syllables': self._statistics.num_syllables,
            'avg_words_per_sentence': self._statistics.avg_words_per_sentence,
            'avg_syllables_per_word': self._statistics.avg_syllables_per_word,
        }

    # syllable
    def syll_count(self):
        return self._statistics.num_syllables

#text = "sangat benci"
#r = Readability(text)
#kr = r.khadijah_rohani()
#kr.score

