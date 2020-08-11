import difflib
import Levenshtein#python-Levenshtein
import jaro

def similarity(str1, str2):
    seq = difflib.SequenceMatcher(None, str1, str2)
    ratio = seq.ratio()
    sim3 = Levenshtein.jaro(str1, str2)
    sim4 = jaro.jaro_metric(str1, str2)
    if ratio > 0.731104540194254 and (sim3 + sim4) / 2 > 0.7890962851907381:
        return True
