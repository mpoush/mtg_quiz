allowed_letters = set('abcdefghijklmnopqrstuvwxyz ')
replacement = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'æ': 'ae', 'ç': 'c', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ð': 'o', 'ñ': 'n', 'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ø': 'o', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ý': 'y', '-': ' '}
bad_letters = set('\'!"+,.0213456789:')

def _sanitize_letter(letter):
    if letter in bad_letters:
        return ''
    if letter in replacement:
        return replacement[letter]
    if letter.lower() not in allowed_letters:
        raise RuntimeError(f'Could not sanitize character "{letter}"')
    return letter

def _remove_extra_whitespace(text):
    words = text.strip().split(' ')
    return ' '.join(words)

def sanitize_text(text):
    text = ''.join(map(_sanitize_letter, text))
    return _remove_extra_whitespace(text)
