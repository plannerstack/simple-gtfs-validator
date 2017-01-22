# Simple GTFS Validator

An extremely simple dependency-free Python GTFS validator. So simple it's stupid.

- Allows to easily explore and write fixes for invalid GTFS
- For a less stupid feed validation: https://github.com/google/transitfeed

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
