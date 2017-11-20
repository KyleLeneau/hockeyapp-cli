HockeyApp CLI
========

A CLI providing Access to the HockeyApp API. Serves as a wrapper
making HTTP requests to the [HockeyApp API](https://support.hockeyapp.net/kb/api).

## Quickstart

```
git clone https://github.com/KyleLeNeau/hockeyapp-cli
cd hockeyapp-cli
virtualenv env
source env/bin/activate
pip install --editable .
hockeyapp
```

## Configuration

Most of the HockeyApp API calls needs a Token present. Instead of having to pass on every call the environment variable of `HOCKEYAPP_TOKEN` can be set to aide easier calls.

## Documentation

The best way to get the most current documentation is via the CLI itself:
`hockeyapp --help`
