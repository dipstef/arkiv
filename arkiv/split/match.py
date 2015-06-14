from arkiv.split.digit import digit_split, substitute_digit_split_file
from arkiv.split.letter import letter_split, substitute_letter_split_file


def match_split_extension(file_name):
    split_file = (digit_split(file_name) or letter_split(file_name)) if file_name else None
    return split_file


def match_split_file(file_name):
    from arkiv.util.files import is_known_file_type

    return match_valid_split_file(file_name, archive_filter=is_known_file_type)


def match_valid_split_file(file_name, archive_filter=None):
    # Archive filter should be used to select give file names with a valid exception
    split_file = match_split_extension(file_name)
    if split_file:
        return split_file if not archive_filter or archive_filter(split_file.archive) else None


def substitute_split_file_name(file_name, missing_part):
    split_digit = digit_split(file_name)

    if split_digit:
        return substitute_digit_split_file(file_name, split_digit.number, missing_part)
    else:
        split_letter = letter_split(file_name)
        if split_letter:
            return substitute_letter_split_file(file_name, split_letter.number, missing_part)
