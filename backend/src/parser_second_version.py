import copy
import re
from typing import Union

from fitz.fitz import Page

from .template import Ipid

# regex

regex = {
    # applicability
    "localization": re.compile(r"où suis-je couvert", re.IGNORECASE),
    "obligations": re.compile(r"quelles sont mes obligations", re.IGNORECASE),
    "payment_options": re.compile(r"quand et comment effectuer les paiements", re.IGNORECASE),
    "start_date": re.compile(r"quand commence la couverture", re.IGNORECASE),
    "termination": re.compile(r"comment puis-je résilier le contrat", re.IGNORECASE),

    # coverage
    "always_covered": re.compile(r"les garanties systématiquement prévues", re.IGNORECASE),
    "optionally_covered": re.compile(r"les garanties optionnelles", re.IGNORECASE),
    "not_covered": re.compile(r"qu’est-ce qui n’est pas assuré", re.IGNORECASE),
    "exclusions": re.compile(r"y-a-t-il des exclusions à la couverture", re.IGNORECASE),
    "services": re.compile(r"les services et avantages", re.IGNORECASE)
}


class Parser:

    def parse_document(self, template: Ipid, page: Page) -> Ipid:

        # process page
        text = page.get_text("text")

        # extract content
        template.coverage.always_covered = self.parse_field(text, "always_covered")
        template.coverage.optionally_covered = self.parse_field(text, "optionally_covered")
        template.coverage.not_covered = self.parse_field(text, "not_covered")
        template.coverage.exclusions = self.parse_field(text, "exclusions")
        template.coverage.services = self.parse_field(text, "services")

        return template

    @staticmethod
    def parse_field(text: str, starting_field: str) -> Union[str, None]:
        """Extract relevant paragraph from `text`. First, detect beginning of text
        to extract by looking for `starting_field`, and then stops when any other field
        is detected. If no starting nor ending field is detected, return None.
        """
        # starting field
        match_start = regex[starting_field].search(text)

        # ending fields
        remaining_regex = copy.deepcopy(regex)
        del remaining_regex[starting_field]
        ending_regex = re.compile('|'.join([x.pattern for x in list(remaining_regex.values())]), re.IGNORECASE)
        
        matches_end = [(text[x.span()[0]:x.span()[1]], x.span()[0], x.span()[1]) for x in re.finditer(ending_regex, text)]
        matches_end = sorted(matches_end, key = lambda x: x[1])
        
        if not match_start:
            return "None"
        
        if not matches_end:
            return text[match_start.span()[1]:]
        
        for match_end in matches_end:
            
            if match_start.span()[1] < match_end[1]:
                parsed_text = text[match_start.span()[1]:match_end[1]]
                return parsed_text

        return text[match_start.span()[1]:]
