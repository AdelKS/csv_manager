__all__ = ["replace_unicode", "concatenate", "dict_to_string"]

def replace_unicode(string):
    replacement = string
    replacement_dict = {"α": "$\\alpha$", 
                        "ε": "$\\varepsilon$",
                        "γ": "$\\gamma$",
                        "Δ": "$\\Delta$",
                        "Γ": "$\\Gamma$",
                        "μ": "$\\mu$",
                        "δ": "$\\delta$",
                        "_": ""}

    for key, val in replacement_dict.items():
        replacement = replacement.replace(key, val)

    return replacement

def concatenate(string_list, inter_prepend="", return_prepend="", return_every=None):
    res = return_prepend
    for i, string in enumerate(string_list):
        res += string + "," + inter_prepend
        if return_every and i % return_every == 0 and i != 0:
            res += "\n" + return_prepend
    return res

def dict_to_string(dic, separator = "|"):
    extension = str()
    if dic:
        extension += separator
    for i, (key, val) in enumerate(sorted(dic.items())):
        if isinstance(val, float):
            extension += key + "=" + "{0:.5g}".format(val)
        else:
            extension += key + "=" + str(val)
        if i < len(dic) - 1:
            extension += separator
    return extension