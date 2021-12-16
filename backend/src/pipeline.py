from .parser import Parser
from .reader import read_pdf
from .template import Ipid


def parse_document(path: str) -> Ipid:
    """Parse a document and return extracted information in
    a Ipid template object.

    Args:
        path (str): Path to pdf document.

    Returns:
        Ipid: Ipid template object with extracted fields.
    """

    # 1. open pdf
    document = read_pdf(path)

    # 2. extract content
    parser = Parser()
    template = Ipid()
    #for page in document:
    #    template = parser.parse_document(template, page)
    filled_template = parser.parse_document(template, document[0])

    return filled_template
