def get_serach_term(search_term):
    """
    to get serach term
    @:param: string
    ''
    """
    search_term = search_term.replace("\\", "")
    search_term = search_term.replace('\"', "")

    print('search_term===>', search_term)
    return search_term


def p_print(title, data=None):
    """
    function for pretty print
    @:param: title, data
    ''
    """
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    print("\n===================================\n")
    print("{} :\n".format(title))
    pp.pprint(data)
    print("\n===================================\n")


# function to get unique id
def get_unique_id():
    import uuid
    return uuid.uuid4()


def save_file(myfile):
    from django.core.files.storage import FileSystemStorage
    fs = FileSystemStorage() #defaults to   MEDIA_ROOT  
    filename = fs.save(myfile.name, myfile)
    file_url = fs.url(filename)
    print("file_url: ", file_url)
    return file_url

