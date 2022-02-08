"""
MTG Card Quiz
(c) 2022 Matthew E Poush
"""

from collections import defaultdict
import json
import gzip

from sanitize_text import sanitize_text
            
class CardGenerator:
    colors = {
        'B': 'Black',
        'G': 'Green',
        'R': 'Red',
        'W': 'White',
        'U': 'Blue',
    }
    
    def __init__(self, input_file, approved_types):
        with gzip.open(input_file) as a:
            self.contents = json.load(a)
        self.approved_types = approved_types
        self.data = None
            
    def all_cards_in(self, approved_types, type, cards, name, **_):
        colors = self.colors
        if type not in approved_types:
            return
        for card in cards:
            name = card['name']
            card_color = ' / '.join(colors[c] for c in sorted(card['colors'])) or 'Colorless'
            card_type = ' / '.join(card['types'])

            if '//' in name:
                a, b = name.split('//')
                if card['side'] == 'a':
                    name = a.strip()
                else:
                    name = b.strip()
            sanitized_name = sanitize_text(name)

            if ' ' in sanitized_name:
                yield sanitized_name, (name, card_color, card_type)
        
    def cards_from_approved_sets(self):
        for collection_name, collection in self.contents['data'].items():
            yield from self.all_cards_in(self.approved_types, **collection)

    def possible_starts(self, card_name):
        words = [x.upper() for x in card_name.split() if len(x) > 2 and x[0]]
        while len(words) > 1:
            first, *words = words
            for second in words:
                if len(first) == 3 == len(second):
                    continue
                yield first[:3] + ' ' + second[:3]
        
    def generate(self):
        card_names = set(self.cards_from_approved_sets())
    
        possibles = defaultdict(list)
        for name, value in card_names:
            for hint in self.possible_starts(name):
                possibles[hint].append(value)

        singles = {k: v[0] for k, v in possibles.items() if len(v) == 1}
        
        _, colors, types = zip(*singles.values())
        colors = sorted(set(colors))
        types = sorted(set(types))
        
        in_order = sorted(singles.items())
        compacted = {k: (n, colors.index(c), types.index(t)) for k, (n, c, t) in in_order}
        self.data = {
            'clues': compacted,
            'colors': colors,
            'types': types
        }
        
    def save_to(self, output_file):
        with open(output_file, 'w') as f:
            json.dump(self.data, f, separators=(',', ':'))
    

def main():
    input_file = 'AllPrintings.json.gz'
    output_file = 'cards.json'
    approved_types = {'commander', 'core', 'draft_innovation', 'expansion'}
    generator = CardGenerator(input_file, approved_types)
    generator.generate()
    generator.save_to(output_file)
    # create_cards(input_file, output_file, approved_types)

if __name__ == '__main__':
    main()