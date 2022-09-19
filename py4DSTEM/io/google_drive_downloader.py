import gdown
from typing import Union
import pathlib
import os


# Built-in sample datasets

# single files
sample_file_ids = {
    'FCU-Net' : '1-KX0saEYfhZ9IJAOwabH38PCVtfXidJi',
    'sample_diffraction_pattern':'1ymYMnuDC0KV6dqduxe2O1qafgSd0jjnU'
}

# collections of files
sample_collection_ids = {
    'unit_test_data' : (
        ('dm_test_file.dm3', '1RxI1QY6vYMDqqMVPt5GBN6Q_iCwHFU4B'),
    ),
    'moretestdata' : (
        ('file3','id'),
        ('file4','id')
    )
}


def download_file_from_google_drive(id_, destination, overwrite=False):
    """
    Downloads a file or collection of files from google drive to the
    destination file path.

    Args:
        id_ (str): File ID for the desired file.  May be:
            - the file id, i.e. for
              https://drive.google.com/file/d/1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM/
              id='1bHv3u61Cr-y_GkdWHrJGh1lw2VKmt3UM'
            - the complete URL,
            - a special string denoting a sample dataset or collection of
              datasets. For a list of sample datasets and their keys, run
              get_sample_data_ids().
        destination (str or Path): path file will be downloaded to. For
            collections of files, this should point to an existing directory;
            a subdirectory will be created inside this directory whose name
            will be given by `id_`, and the colletion of files will be placed
            inside that subdirectory. If a subdirectory of this name already
            exists, aborts or deletes and overwrite the entire subdirectory,
            depending on the value of `overwrite`.
        overwrite (bool): turn overwrite protection on/off
    """
    # handle paths

    # for collections of files
    if id_ in sample_collection_ids.keys():

        # check if directory exists
        assert os.path.exists(destination), "specified directory does not exist; check filepath"

        # update the path with a new sub-directory name
        destination = os.path.join(destination, id_)

        # check if it already exists
        if os.path.exists(destination):

            # check if it contains any files
            paths = os.listdir(destination)
            if len(paths) > 0:

                # check `overwrite`
                if overwrite:
                    for p in paths:
                        os.remove(os.path.join(destination, p))
                else:
                    raise Exception('a populated directory exists at the specified location. to overwrite set `overwrite=True`.')

        # if it doesn't exist, make a new directory
        else:
            os.mkdir(destination)

        # get the files
        for file_name,file_id in sample_collection_ids[id_]:
            if file_id[:4].lower() == 'http':
                gdown.download(
                    url = file_id,
                    output = os.path.join(destination, file_name),
                    fuzzy = True
                )
            else:
                gdown.download(
                    id = file_id,
                    output = os.path.join(destination, file_name),
                    fuzzy = True
                )

        return None


    # for single files

    # Check and handle if a file at the destination filepath exists
    if os.path.exists(destination):

        # check `overwrite`
        if overwrite == True:
            print(f"File already existed, downloading and overwriting")
            os.remove(destination)
        else:
            raise Exception('File already exists; aborting. To overwrite, use `overwrite=True`.')

    # Check if the id_ is a key pointing to a known sample dataset
    if id_ in sample_file_ids.keys():
        id_ = sample_file_ids[id_]

    # Check if `id_` is a file ID or a URL, and download
    if id_[:4].lower()=='http':
        gdown.download(url=id_,output=destination,fuzzy=True)
    else:
        gdown.download(id=id_,output=destination,fuzzy=True)

    return None



def get_sample_data_ids():
    return {'files' : sample_file_ids.keys(),
            'collections' : sample_collection_ids.keys()}



