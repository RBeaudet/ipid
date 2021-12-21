import copy
import re
from typing import List

from fitz.fitz import Page

from .template import Ipid

## regex

regex_field = {
    # applicability
    "localization": re.compile(r"où[\t\s\n]suis-je[\t\s\n]couvert", re.IGNORECASE),
    "obligations": re.compile(r"quelles[\t\s\n]sont[\t\s\n]mes[\t\s\n]obligations", re.IGNORECASE),
    "payment_options": re.compile(r"effectuer[\t\s\n]les[\t\s\n]paiements", re.IGNORECASE),
    "start_date": re.compile(r"quand[\t\s\n]commence[\t\s\n]la[\t\s\n]couverture[\t\s\n]et[\t\s\n]quand[\t\s\n]prend-elle[\t\s\n]fin", re.IGNORECASE),
    "termination": re.compile(r"comment[\t\s\n]puis-je[\t\s\n]résilier[\t\s\n]le[\t\s\n]contrat", re.IGNORECASE),

    # coverage
    "always_covered": re.compile(r"les[\t\s\n]garanties[\t\s\n]systématiquement[\t\s\n]prévues", re.IGNORECASE),
    "optionally_covered": re.compile(r"les[\t\s\n]garanties[\t\s\n]optionnelles", re.IGNORECASE),
    "not_covered": re.compile(r"qu[’']est-ce[\t\s\n]qui[\t\s\n]n[’']est[\t\s\n]pas[\t\s\n]assuré", re.IGNORECASE),
    "exclusions": re.compile(r"y-a-t-il[\t\s\n]des[\t\s\n]exclusions[\t\s\n]à[\t\s\n]la[\t\s\n]couverture", re.IGNORECASE),
    "services": re.compile(r"les[\t\s\n]services[\t\s\n]et[\t\s\n]avantages", re.IGNORECASE),

    # product
    "description": re.compile(r"type[\t\s\n]d[’']assurance", re.IGNORECASE)
}

siren_regex = re.compile(r"\b(?:\d\s?){9}\b", re.IGNORECASE)
typology_regex = re.compile(r"([^\n]+)\n", re.IGNORECASE)
product_regex = re.compile(r"produit\s?:([^\n]+)\n", re.IGNORECASE)

# non-exhaustive list
insurer_name_regex = re.compile(r"\b(axa|ag2r|matmut|groupama)\b", re.IGNORECASE)


class Parser:

    def parse_document(self, template: Ipid, page: Page) -> Ipid:

        # process page
        text = page.get_text("text")

        # extract coverage
        template.coverage.always_covered += self.parse_field(text, "always_covered")
        template.coverage.optionally_covered += self.parse_field(text, "optionally_covered")
        template.coverage.not_covered += self.parse_field(text, "not_covered")
        template.coverage.exclusions += self.parse_field(text, "exclusions")
        template.coverage.services += self.parse_field(text, "services")

        # extract applicability
        template.applicability.obligations += self.parse_field(text, "obligations")
        template.applicability.localization += self.parse_field(text, "localization")
        template.applicability.payment_options += self.parse_field(text, "payment_options")
        template.applicability.start_date += self.parse_field(text, "start_date")
        template.applicability.termination += self.parse_field(text, "termination")

        # product extraction
        template.product.description += self.parse_field(text, "description")
        template.product.product += self.product_search(text)
        template.product.typology = self.typology_search(text=text, existing_field=template.product.typology)

        # insurer extraction
        template.insurer.name = self.insurer_name_search(text=text, existing_field=template.insurer.name)
        template.insurer.siren.extend(self.siren_search(text))

        return template

    @staticmethod
    def parse_field(text: str, starting_field: str) -> str:
        """Extract relevant paragraph from `text`. First, detect beginning of text
        to extract by looking for `starting_field`, and then stops when any other field
        is detected. If no starting nor ending field is detected, return empty string.
        """
        # starting field
        match_start = regex_field[starting_field].search(text)

        # ending fields
        remaining_regex = copy.deepcopy(regex_field)
        del remaining_regex[starting_field]
        ending_regex = re.compile('|'.join([x.pattern for x in list(remaining_regex.values())]), re.IGNORECASE)
        
        matches_end = [(text[x.span()[0]:x.span()[1]], x.span()[0], x.span()[1]) for x in re.finditer(ending_regex, text)]
        matches_end = sorted(matches_end, key = lambda x: x[1])
        
        if not match_start:
            return ""
        
        if not matches_end:
            return text[match_start.span()[1]:]
        
        for match_end in matches_end:
            
            if match_start.span()[1] < match_end[1]:
                parsed_text = text[match_start.span()[1]:match_end[1]]
                return parsed_text

        return text[match_start.span()[1]:]

    @staticmethod
    def product_search(text: str) -> str:
        """Parse product name using a regex search. If nothing is found,
        return an empty string.
        """
        match = re.search(product_regex, text)
        if match:
            output = match.group(1).strip()
        else:
            output = ""
        return output

    @staticmethod
    def siren_search(text: str) -> List[str]:
        """Parse SIREN number by simple regex search. There can be several SIREN
        numbers, thus we return a list.
        """
        match = re.finditer(siren_regex, text)
        if not match:
            sirens = []
        else:
            sirens = [text[x.span()[0]:x.span()[1]] for x in match]
        return sirens

    @staticmethod
    def typology_search(text: str, existing_field: str) -> str:
        """Parse typology of insurance product. This is typically the first piece of text 
        in the first page of the document. If `existing_field` is already filled, then it means
        typology has already been extracted in the previous page. Otherwise, we look for typology
        by regex search.
        """
        if len(existing_field) > 0:
            return existing_field
        else:
            match = re.search(typology_regex, text)
            if match:
                output = match.group(1).strip()
            else:
                output = ""
        return output

    @staticmethod
    def insurer_name_search(text: str, existing_field: str) -> str:
        """Parse name of insurer, and return it in uppercase letters.
        """
        if len(existing_field) > 0:
            return existing_field
        else:
            match = re.search(insurer_name_regex, text)
            if match:
                output = match.group(0).strip().upper()
            else:
                output = ""
        return output
