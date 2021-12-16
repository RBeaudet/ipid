from itertools import groupby
from operator import itemgetter

from fitz import Rect


class WordRecovery:

    def __call__(self, words: list, rect: Rect) -> list:
        return self.recover_words(words, rect)

    def recover_words(self, words: list, rect: Rect) -> list:
        """Order words in `rect`, and compute new word lines.
        """
        new_words = self.order_words(words, rect)
        recovered_words = self.get_new_word_lines(new_words)
        return recovered_words

    @staticmethod
    def get_new_word_lines(words: list) -> list:
        """Compute line numbers for each word in `words`.
        Here, `words` is the output of the method `recover_words`.

        Output is a list where each item will have the following format:
        [x0, y0, x1, y1, "word", line]
        """
        words_out = []  # we will return this
        if len(words) == 0:
            return words_out

        # sort words by y coordinates
        words = sorted(words, key=lambda x: Rect(x[:4]).y1)

        # get y coord of first word
        line = 0
        height = Rect(words[0][:4]).y1

        for w in words:
            # if word has a different y coord than previous word, then add a new line
            if Rect(w[:4]).y1 != height:
                height = Rect(w[:4]).y1
                line += 1
            words_out.append(w + [line])

        return words_out

    @staticmethod
    def order_words(words: list, rect: Rect) -> list:
        """ Word recovery.

        Notes:
            Method 'get_textWords()' from PyMuPDF does not try to recover words, if their single
            letters do not appear in correct lexical order. This function steps in
            here and creates a new list of recovered words.
        Args:
            words: list of words as created by 'get_textWords()' or a similar function from PyMuPDF
            rect: rectangle to consider (usually the full page)
        Returns:
            List of recovered words. Same format as 'get_text_words', but left out
            block, line and word number - a list of items of the following format:
            [x0, y0, x1, y1, "word"]
        """
        # build sublist of words contained in given rectangle
        words = [w for w in words if Rect(w[:4]) in rect]  # w[:4] = x0, y0, x1, y1

        # sort the words by lower line, then by word start coordinate
        words.sort(key=itemgetter(3, 0))  # sort by y1, x0 of word rectangle

        # build word groups on same line
        grouped_lines = groupby(words, key=itemgetter(3))

        words_out = []  # we will return this

        # iterate through the grouped lines
        # for each line coordinate ("_"), the list of words is given
        for _, words_in_line in grouped_lines:
            for i, w in enumerate(words_in_line):
                if i == 0:  # store first word
                    x0, y0, x1, y1, word = w[:5]
                    continue

                r = Rect(w[:4])  # word rect

                # Compute word distance threshold as 20% of width of 1 letter.
                # So we should be safe joining text pieces into one word if they
                # have a distance shorter than that.
                threshold = r.width / len(w[4]) / 5
                if r.x0 <= x1 + threshold:  # join with previous word
                    word += w[4]  # add string
                    x1 = r.x1  # new end-of-word coordinate
                    y0 = max(y0, r.y0)  # extend word rect upper bound
                    continue

                # now have a new word, output previous one
                words_out.append([x0, y0, x1, y1, word])

                # store the new word
                x0, y0, x1, y1, word = w[:5]

            # output word waiting for completion
            words_out.append([x0, y0, x1, y1, word])

        return words_out


def search_for(text: str, words: list) -> list:
    """ Search for text in items of list of words.
    TODO: add regular expressions.
    TODO: currently, words is a list of words, check if it could be entire text and how to derive bounding box

    Args:
        text: string to be searched for 
        words: list of items in format delivered by 'get_text_words()'.
    Returns:
        List of rectangles, one for each found locations.
    """
    rect_list = []
    for w in words:
        if text in w[4]:
            rect_list.append(Rect(w[:4]))
    return rect_list
