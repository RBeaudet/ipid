from .parser import Parser
from .post_processing import PostProcessing
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
    for page in document:
        template = parser.parse_document(template, page)

    # 3. post-processing
    post_processor = PostProcessing()
    template = post_processor.process(template)

    return template
