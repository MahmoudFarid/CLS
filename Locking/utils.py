

def get_details_from_message(full_message):
    """
        split the full message to return the url and resource
        :param full_message: full_message that sending from LockerClient
        :return: - url: that we request on
                 - resource: that we want to lock it
    """
    url_with_resource = full_message.split('url is:')[1].split('and resource is:')
    url = url_with_resource[0].strip()
    resource = url_with_resource[1].strip()
    return url, resource
