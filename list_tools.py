def read_list(list_fname):
    """Takes a flat file list where each item is on a separate line and returns in list format.

    Parameters
    ----------
    list_fname : str
        Filename of the list

    Returns
    -------
    final_list : list
        List generated from file

    """
    list_file = open(list_fname)
    split_list = list_file.read().split('\n')
    list_file.close()

    final_list = []

    for item in split_list:
        if not len(item) == 0:
            final_list.append(item)

    return final_list
