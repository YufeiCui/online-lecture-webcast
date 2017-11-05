import urllib.request
import os

class InvalidValueException(Exception):
    pass

def construct(formula, configuration, concatenator = '/', escape_prefix = '/'):
    '''
    (list, dict, [,str[,str]]) -> str
    '''

    # simple function to concate strings with a concatenator in between
    def concatenate_item(before, item, concatenator = concatenator):
        return before + concatenator + item

    EXTENSION_KEYWORD = 'extension'
    EXTENSION_PREFIX = '.'
    rs = ''

    # look at each term in the formula
    for term in formula:
        # treatment for a string
        if (isinstance(term, str)):
            # if the item starts with the escape prefix, then do not evaulate
            if term.startswith(escape_prefix):
                rs = concatenate_item(rs, term[1:])
            else:
                # if the item belongs in configuration
                if term in configuration:
                    # if it's the extension then only add a '.' in front
                    if term == EXTENSION_KEYWORD:
                        rs = concatenate_item(rs, configuration[term], EXTENSION_PREFIX)
                    else:
                        rs = concatenate_item(rs, configuration[term])
                else:
                    rs = concatenate_item(rs, term)
        # if there's another formula
        elif isinstance(term, list):
            if (len(term[-1]) == 1):
                new_concatenator = term[-1]
            else:
                new_concatenator = concatenator
            # concanate current string and the result string from the new formula
            rs = concatenate_item(rs, construct(term[:-1], configuration, concatenator = new_concatenator))
        # cast ints or floats
        elif isinstance(term, int) or isinstance(term, float):
            rs = concatenate_item(term, str(term))
        else:
            raise InvalidValueException

    # add/remove extra concatenators
    return rs[1:]

def download(where, to, name = None):
    # construct the name that the file will be stored as
    if name:
        constructed_name = to + name
    else:
        constructed_name = to + where[where.rindex("/"):]

    urllib.request.urlretrieve(where, constructed_name)

if __name__ == "__main__":
    import json

    # loads the json configuration file
    config = json.load(open("./config.json", "r"))

    # generates a url given the formula and the configured keys
    url = construct(config["Constrution"]["url"], config["DownloadSettings"], concatenator = '/', escape_prefix = '/')

    # given the url, load the download directory and download the content
    download(url, config["DownloadSettings"]["location"])
