from quote_bank import QuoteContainer
from datetime import datetime as dt
import re

class ResponseBot():
    def __init__(self, quote_tsv_path: str, time_fmt: str = "%H:%M:%S"):
        self.quotes = QuoteContainer()
        self.quotes.load_from_tsv(quote_tsv_path, log=True)
        self.time_fmt = time_fmt
                 

    def get_response(self, msg: str = "", require_match: bool = False):
        self.log(f"Getting response for \"{msg}\"")
        msg_lower = msg.lower()
        
        # If there is a message to be searched
        if not msg or not msg.strip():
            self.log(f"Message isn't searchable.")

        self.log(f"Searching through message...")
        # Search through all keys
        for key in self.quotes.keys():
            
            # Skip the blank key
            if not key or not key.strip() : continue
            
            # If key found in msg, get a quote
            if re.search(r"\b" + key + r"\b", msg_lower): 
                self.log(f"Matched key {key}.")
                return self.quotes.get_quote(key)
        
                
        
        # Otherwise, simply return a quote with the empty key
        if not require_match:
            self.log(f"No match, getting unspecified quote.")
            return self.quotes.get_quote()
        
        return ""
    
                
    def time_stamp(self):
        return dt.now().strftime(self.time_fmt)

    def log(self, msg: str):
        print(f"[{self.time_stamp()}] " + msg)