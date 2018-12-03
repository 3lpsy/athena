
def only(data, grab, strict=False):
    if not strict:
        return dict((k, data[k]) for k in grab if k in data)
    return dict((k, data[k]) for k in grab)
