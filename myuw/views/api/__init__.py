import re


SPACE_PATTERN = r'%20'
AMP_PATTERN = r'%26'


def unescape_curriculum_abbr(cur_abb):
    if re.search(SPACE_PATTERN, cur_abb):
        cur_abb = re.sub(SPACE_PATTERN, ' ', cur_abb)
    if re.search(AMP_PATTERN, cur_abb):
        cur_abb = re.sub(AMP_PATTERN, '&', cur_abb)
    return cur_abb
