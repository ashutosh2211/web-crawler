import argparse

import pytest

from web_crawler.validators.input_validator import SeedsAction, AllowedDomainsAction


class TestSeedAction:

    def test_seed_action_with_invalid_seeds(self):
        seeds = "abc|def"

        parser = argparse.ArgumentParser()
        parser.add_argument('--seeds', dest='seeds', action=SeedsAction, required=True)

        with pytest.raises(argparse.ArgumentTypeError) as exc:
            parser.parse_args(["--seeds", seeds])

        assert "Seeds should be valid urls" == str(exc.value)

    def test_seed_action_with_valid_seeds(self):
        seeds = "https://abc.com|https://def.com"

        parser = argparse.ArgumentParser()
        parser.add_argument('--seeds', dest='seeds', action=SeedsAction, required=True)

        args = parser.parse_args(["--seeds", seeds])

        assert args.seeds == seeds.split("|")

    def test_seed_action_with_empty_seeds(self):
        seeds = ""

        parser = argparse.ArgumentParser()
        parser.add_argument('--seeds', dest='seeds', action=SeedsAction, required=True)

        with pytest.raises(argparse.ArgumentTypeError) as exc:
            parser.parse_args(["--seeds", seeds])

        assert "Seeds should be valid urls" == str(exc.value)


class TestAllowedDomainsAction:

    def test_allowed_domains_action_with_invalid_domains(self):
        allowed_domains = "abc.c|def"

        parser = argparse.ArgumentParser()
        parser.add_argument('--allowed_domains', dest='allowed_domains', action=AllowedDomainsAction)

        with pytest.raises(argparse.ArgumentTypeError) as exc:
            parser.parse_args(["--allowed_domains", allowed_domains])

        assert "Allowed domains should be valid urls" == str(exc.value)

    def test_allowed_domains_action_with_valid_domains(self):
        allowed_domains = "abc.com|def.com"

        parser = argparse.ArgumentParser()
        parser.add_argument('--allowed_domains', dest='allowed_domains', action=AllowedDomainsAction)

        args = parser.parse_args(["--allowed_domains", allowed_domains])

        assert args.allowed_domains == allowed_domains.split("|")

    def test_allowed_domains_action_with_empty_domains(self):
        allowed_domains = ""

        parser = argparse.ArgumentParser()
        parser.add_argument('--allowed_domains', dest='allowed_domains', action=AllowedDomainsAction)

        with pytest.raises(argparse.ArgumentTypeError) as exc:
            parser.parse_args(["--allowed_domains", allowed_domains])

        assert "Allowed domains cannot be empty" == str(exc.value)
