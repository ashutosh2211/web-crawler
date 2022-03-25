import argparse

import validators


def uri_validator(uri):
    if validators.url(uri):
        return True

    return False


def domain_validator(domain):
    if validators.domain(domain):
        return True

    return False


class SeedsAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        list_data = values.split("|")
        filtered_values = list(filter(uri_validator, list_data))
        if not filtered_values:
            raise argparse.ArgumentTypeError("Seeds should be valid urls")
        setattr(namespace, self.dest, filtered_values)


class AllowedDomainsAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        if not values:
            raise argparse.ArgumentTypeError("Allowed domains cannot be empty")
        list_data = values.split("|")
        filtered_values = list(filter(domain_validator, list_data))
        if not filtered_values:
            raise argparse.ArgumentTypeError("Allowed domains should be valid urls")
        setattr(namespace, self.dest, filtered_values)
