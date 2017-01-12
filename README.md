# Simple GTFS Validator


## Requirements

This gtfs validator has no dependecies except for python. (tested on 2.7)

## Usage

Currently the only `BaseGtfsValidator` implemented is `GtfsFareValidator`:

- it reads and unzips a GTFS file
- removes rows in `fare_rules` that don't have an appropriate `route_id` in routes
- zips it back in to the same locations


```
python gtfs_fare_validator.py --source test/gtfs_with_all_fares.zip
```

## Extending

The `BaseGtfsValidator` takes care of reading, unzipping, zipping and cleaning itself.

Extending on it and implementing the `validate` and `rewrite` function is all that's needed to create another simple validator.

```
class ExampleFareValidator(BaseGtfsValidator):
    def validate(self):
        pass

    def rewrite(self):
        pass
```

Take note of the different gtfs files that can be accessed after instantiating it:

```
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
```


```
# As the
GTFS_URL1="http://gtfs.ovapi.nl/new/gtfs-nl.zip"
wget ${GTFS_URL1} -O gtfs1.zip --tries=5 --timeout=600 -q
zip -j gtfs1.zip fare_attributes.txt
zip -j gtfs1.zip fare_rules.txt
```