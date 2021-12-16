from fitz import Document


def read_pdf(path) -> Document:
    try:
        pdf = Document(stream=path, filetype="pdf")
        assert pdf.is_pdf
    except (AssertionError, RuntimeError):
        raise
    return pdf


def get_pdf_metadata(pdf: Document) -> dict:
    metadata = {
        "year": "None"
    }
    if not pdf.is_encrypted:
        metadata = pdf.metadata
        if metadata["creationDate"]:
            metadata["year"] = metadata["creationDate"][2:6]  # get year
        else:
            metadata["year"] = "None"
    return metadata
