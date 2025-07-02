from wordfreq import top_n_list
from app.models.wordfreq import WordByRankResponse, WordFrequencySelection, MostUsedWordsResponse

# Module-level cache (shared across all requests)
_word_list_cache = {}

def get_most_used_words(selection: WordFrequencySelection) -> MostUsedWordsResponse:
    n = int(selection.value)
    try:
        if n in _word_list_cache:
            words = _word_list_cache[n]
        else:
            words = top_n_list('de', n)
            _word_list_cache[n] = words
        return MostUsedWordsResponse(count=n, words=words)
    except Exception as e:
        return MostUsedWordsResponse(count=0, words=[], error=str(e))

def get_word_by_rank(selection: WordFrequencySelection, rank: int) -> WordByRankResponse:
    most_used = get_most_used_words(selection)
    if most_used.error:
        raise ValueError(most_used.error)
    if not (1 <= rank <= most_used.count):
        raise IndexError("Rank out of range for this selection.")
    return WordByRankResponse(rank=rank, word=most_used.words[rank - 1], selection=selection)