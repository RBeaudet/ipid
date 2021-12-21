import re
from typing import List

from pydantic import fields

from .template import Ipid

regex_not_new_line = re.compile(r"(\n)([\t\s]?[a-zàâäéèëêùûü])")


class PostProcessing:

    def process(self, template: Ipid) -> Ipid:
        """Perform some post-processing to IPID template:
            - clean punctuation
            - return to line
            etc.
        """
        ## iterate over all Template fields (did not find a way to iterate over BaseModel fields)

        # coverage
        template.coverage.always_covered = self._process(template.coverage.always_covered)
        template.coverage.optionally_covered = self._process(template.coverage.optionally_covered)
        template.coverage.not_covered = self._process(template.coverage.not_covered)
        template.coverage.exclusions = self._process(template.coverage.exclusions)
        template.coverage.services = self._process(template.coverage.services)

        # applicability
        template.applicability.obligations = self._process(template.applicability.obligations)
        template.applicability.localization = self._process(template.applicability.localization)
        template.applicability.payment_options = self._process(template.applicability.payment_options)
        template.applicability.start_date = self._process(template.applicability.start_date)
        template.applicability.termination = self._process(template.applicability.termination)

        # extraction
        template.product.description = self._process(template.product.description)
        template.product.product = self._process(template.product.product)
        template.product.typology = self._process(template.product.typology)

        # extraction
        template.insurer.name = self._process(template.insurer.name)
        template.insurer.siren = [self._process(x) for x in template.insurer.siren]

        return template

    @staticmethod
    def _process(text: str) -> str:
        # clean punctuation
        text = re.sub(r"[\?!✓\uf0fb]+", " - ", text)
        text = re.sub(r":", " ",text)
        text = re.sub(r"[\s\t]+", " ", text)

        # remove new line characters that should not be considered as new lines
        text = re.sub(regex_not_new_line, r"\2", text)
        text = re.sub(r"[\s\t]+", " ", text)

        text = re.sub(r"-+", " \n- ", text)
        text = re.sub(r"(\n-)([\s\t]*\n-)", r"\1", text)
        text = re.sub(r"[\s\t]+", " ", text)
        
        return text.strip()
