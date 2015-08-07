import os, errno


def silent_remove(filename):
    """
    Remove a file from operation system and omit the error if it's not existing.
    :param filename: name of the file
    :return: None
    """
    try:
        os.remove(filename)
    except OSError as e:
        # errno.ENOENT = no such file or directory
        if e.errno != errno.ENOENT:
            # re-raise exception if a different error occurred
            raise
