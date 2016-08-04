from coala_utils.string_processing.Core import unescaped_search_for
from coalib.results.AbsolutePosition import AbsolutePosition
from coalib.results.SourceRange import SourceRange


def get_specified_block_range(file,
                              filename,
                              open_specifier,
                              close_specifier,
                              annotation_dict):
    """
    Gets a sourceranges of all the indentation blocks present inside the
    file.

    :param file:            File that needs to be checked in the form of
                            a list of strings.
    :param filename:        Name of the file that needs to be checked.
    :param open_specifier:  A character or string indicating that the
                            block has begun.
    :param close_specifier: A character or string indicating that the block
                            has ended.
    :param annotation_dict: A dictionary containing sourceranges of all the
                            strings and comments within a file.
    :return:                A tuple whith the first source range being
                            the range of the outermost indentation while
                            last being the range of the most
                            nested/innermost indentation.
                            Equal level indents appear in the order of
                            first encounter or left to right.
    """
    ranges = []

    open_pos = list(get_valid_sequences(
        file, open_specifier, annotation_dict))
    close_pos = list(get_valid_sequences(
        file, close_specifier, annotation_dict))

    number_of_encaps = len(open_pos)
    if number_of_encaps != len(close_pos):
        raise UnmatchedIndentError(open_specifier, close_specifier)

    if number_of_encaps == 0:
        return ()

    stack = []
    text = ''.join(file)
    open_counter = close_counter = position = 0
    op_limit = cl_limit = False
    for position in range(len(text)):
        if not op_limit:
            if open_pos[open_counter].position == position:
                stack.append(open_pos[open_counter])
                open_counter += 1
                if open_counter == number_of_encaps:
                    op_limit = True

        if not cl_limit:
            if close_pos[close_counter].position == position:
                try:
                    op = stack.pop()
                except IndexError:
                    raise UnmatchedIndentError(open_specifier,
                                               close_specifier)
                ranges.append(SourceRange.from_values(
                    filename,
                    start_line=op.line,
                    start_column=op.column,
                    end_line=close_pos[close_counter].line,
                    end_column=close_pos[close_counter].column))
                close_counter += 1
                if close_counter == number_of_encaps:
                    cl_limit = True

    return tuple(ranges)


def get_valid_sequences(file,
                        sequence,
                        annotation_dict,
                        encapsulators=None,
                        check_ending=False):
    """
    A vaild sequence is a sequence that is outside of comments or strings.

    :param file:            File that needs to be checked in the form of
                            a list of strings.
    :param sequence:        Sequence whose validity is to be checked.
    :param annotation_dict: A dictionary containing sourceranges of all the
                            strings and comments within a file.
    :param encapsulators:   A tuple of SourceRanges of code regions
                            trapped in between a matching pair of
                            encapsulators.
    :param check_ending:    Check whether sequence falls at the end of the
                            line.
    :return:                A tuple of AbsolutePosition's of all occurances
                            of sequence outside of string's and comments.
    """
    file_string = ''.join(file)
    # tuple since order is important
    sequence_positions = tuple()

    for sequence_match in unescaped_search_for(sequence, file_string):
        valid = True
        sequence_position = AbsolutePosition(
                                file, sequence_match.start())
        sequence_line_text = file[sequence_position.line - 1]

        # ignore if within string
        for string in annotation_dict['strings']:
            if(gt_eq(sequence_position, string.start) and
               lt_eq(sequence_position, string.end)):
                valid = False

        # ignore if within comments
        for comment in annotation_dict['comments']:
            if(gt_eq(sequence_position, comment.start) and
               lt_eq(sequence_position, comment.end)):
                valid = False

            if(comment.start.line == sequence_position.line and
                    comment.end.line == sequence_position.line and
                    check_ending):
                sequence_line_text = sequence_line_text[
                    :comment.start.column - 1] + sequence_line_text[
                    comment.end.column-1:]

        if encapsulators:
            for encapsulator in encapsulators:
                if(gt_eq(sequence_position, encapsulator.start) and
                   lt_eq(sequence_position, encapsulator.end)):
                    valid = False

        if not sequence_line_text.rstrip().endswith(':') and check_ending:
            valid = False

        if valid:
            sequence_positions += (sequence_position,)

    return sequence_positions


# TODO remove these once https://github.com/coala-analyzer/coala/issues/2377
# gets a fix
def lt_eq(absolute, source):
    if absolute.line == source.line:
        return absolute.column <= source.column

    return absolute.line < source.line


def gt_eq(absolute, source):
    if absolute.line == source.line:
        return absolute.column >= source.column

    return absolute.line > source.line


class UnmatchedIndentError(Exception):

    def __init__(self, open_indent, close_indent):
        Exception.__init__(self, "Unmatched " + open_indent + ", " +
                           close_indent + " pair")
