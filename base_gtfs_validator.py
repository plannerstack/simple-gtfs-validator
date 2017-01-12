#!/usr/bin/env python
import csv
import os
from utils import unzip, clean_dir, zip_files_to_gtfs

class BaseGtfsValidator(object):
    """
        BaseClass for processes GTFS files
        - Read GTFS File
        - Validate (implement in derived class)
        - Rewrite (implement in derived class)
        - Overwrite GTFS File
    """
    source_filename = None
    gtfs_files = {
        'fare_rules': None,
        'agency': None,
        'feed_info': None,
        'stops': None,
        'stop_times': None,
        'shapes': None,
        'calendar_dates': None,
        'routes': None,
        'trips': None,
        'fare_attributes': None
    }

    def __init__(self, source_filename):
        self.source_filename = source_filename

        self.__extract()
        self.__setup_gtfs_files()

    def __call__(self):
        # TODO: Make sure clean() is always called
        self.validate()
        self.rewrite()
        self.__compress()
        self.__clean()

    def validate(self):
        print("implement me!")

    def rewrite(self):
        print("implement me!")

    def gtfs_csv_reader(self, name):
        return self.__gtfs_csv_reader_writer(name, "rb")

    def gtfs_csv_writer(self, name):
        return self.__gtfs_csv_reader_writer(name, "wb")


    """
        Private methods
    """

    def __gtfs_csv_reader_writer(self, name, type):
        if name is None or self.gtfs_files[name] is None:
            return None
        file = open(self.gtfs_files[name], type)
        if type == "rb":
            return csv.reader(file)
        elif type == "wb":
            return csv.writer(file)

    @property
    def _tmp_destination(self):
        """
        # TODO: make less fragile
        :return:
        """
        return self.source_filename.split('/')[0] + '/tmp'

    def __extract(self):
        unzip(self.source_filename, self._tmp_destination)

    def __setup_gtfs_files(self):
        for filename in os.listdir(self._tmp_destination):
            if filename.endswith(".txt") or filename.endswith(".csv"):
                path = os.path.join(self._tmp_destination, filename)
                filename = os.path.splitext(filename)[0]
                self.gtfs_files[filename] = path
                continue
            else:
                continue
        return self.gtfs_files

    def __compress(self):
        files = [file for file in self.gtfs_files.values() if file is not None]
        zip_files_to_gtfs(self.source_filename, files)

    def __clean(self):
        clean_dir(self._tmp_destination)