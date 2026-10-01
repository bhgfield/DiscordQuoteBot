from sortedcontainers import SortedDict
from re import split
import random

# Container to store key phrases and their corresponding quotes.
# each key is paired with a list of possible resulting quotes,
# -- this causes a lot of duplicate results, when multiple keys are
# given for each 
class QuoteContainer():
    def __init__(self):
        self.dict = SortedDict()
        
        
    def add_quote(self, quote: str, key: str = ""):
        if key in self.dict:
            self.dict[key].append(quote)
        else:
            self.dict[key] = [quote]
        
        if key and key.strip():
            print(f"[\"{key}\" : \"{quote}\"]")
        
            
    def keys(self):
        return self.dict.keys()
            
            
    def get_quote(self, key: str = ""):
        quotes = self.dict[key]
        
        # Return the only value
        if len(quotes) == 1:
            return quotes[0]
        
        # Otherwise, get a random value from the list
        else:
            return quotes[random.randint(0, len(quotes))]
            

    def load_from_tsv(self, path: str, log: bool = False):
        if log: print(f"Loading quotes from \'{path}\'")

        line_count = 0
        try:
            with open(path, "r") as file:
                for line in file:
                    split_line = [token.strip() for token in split(r'\t', line.strip()) if token]
                
                    quote = split_line[0]
                    
                     # Specified keys
                    if len(split_line) > 1:
                        line_count += 1
                        for i in range(1, len(split_line)):
                            self.add_quote(quote, split_line[i])

                    # No specific keys
                    elif len(split_line) == 1:
                        line_count += 1
                        self.add_quote(quote)
                    
                    # Invalid or empty line, just continue for now
                    else: 
                        continue

                    
        except OSError:
            if log: print(f"OSError occured while reading file {path}")
        
        except:
            if log: print(f"Unknown error occured while reading file {path}")
            
        if log: print(f"Load finished. Successfully read {line_count} lines, {len(self.dict.keys())} keys")