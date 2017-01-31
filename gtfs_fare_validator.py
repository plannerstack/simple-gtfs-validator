#!/usr/bin/env python
import argparse
from base_gtfs_validator import BaseGtfsValidator

class GtfsFareValidator(BaseGtfsValidator):
    """
        removes fare_rules that have an unknown route_id
        overwrites given gtfs-file
    """
    valid_fare_rows_list = None
    valid_fare_attr_rows_list = None

    def validate(self):
        existing_route_ids = self.__get_existing_route_ids()
        self.valid_fare_rows_list = self.__create_filter_fare_rules_rows(existing_route_ids)
        self.valid_fare_attr_rows_list = self.__create_filter_fare_attributes_rows()

    def rewrite(self):
        fares_writer = self.gtfs_csv_writer('fare_rules')
        fares_writer.writerows(self.valid_fare_rows_list)
        fares_attr_writer = self.gtfs_csv_writer('fare_attributes')
        fares_attr_writer.writerows(self.valid_fare_attr_rows_list)

    """
        Private
    """
    def __create_filter_fare_attributes_rows(self,):
        print('check fare_attributes')
        fare_ids = set()
        valid_fare_rows_list = []
        print('check fare_attributes')
        fares_reader = self.gtfs_csv_reader('fare_attributes')
        fare_id_index = None
        for row in fares_reader:
            if fare_id_index is None:
                fare_id_index = row.index("fare_id")
                valid_fare_rows_list.append(row)
                continue
            if row[fare_id_index] not in fare_ids:
                fare_ids.add(row[fare_id_index])
                valid_fare_rows_list.append(row)
            else:
                print('duplicate fare id')

        return valid_fare_rows_list

    def __create_filter_fare_rules_rows(self, existing_route_ids):
        valid_fare_rows_list = []

        print('check fare_rules')
        fares_reader = self.gtfs_csv_reader('fare_rules')
        route_id_index = None
        for row in fares_reader:
            if route_id_index is None:
                route_id_index = row.index("route_id")
                valid_fare_rows_list.append(row)
                continue

            if row[route_id_index] in existing_route_ids:
                valid_fare_rows_list.append(row)
            else:
                print("unknown route::", row)
        return valid_fare_rows_list


    def __get_existing_route_ids(self):
        known_route_ids = []
        routes_reader = self.gtfs_csv_reader('routes')
        route_id_index = None
        for row in routes_reader:
            if route_id_index is None:
                route_id_index = row.index("route_id")
                continue
            known_route_ids.append(row[route_id_index])
        return known_route_ids


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='this will validate and rewrite a gtfs zip on order to have valid fare_rules')
    parser.add_argument('--source', required=True, help="e.q. : test/test.zip")

    g = GtfsFareValidator(parser.parse_args().source)
    g()
