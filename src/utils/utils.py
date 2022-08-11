def clean_s(s):
    """
    Cleans the string s for a dbpedia entry reference
    :param s: the string to clean
    :return: the cleaned string
    """
    return s.split('/')[-1]
