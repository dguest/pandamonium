import logging
import argparse

from ..version import __version__

logging.basicConfig()
log = logging.getLogger(__name__)


def pandamonium():
    parser = argparse.ArgumentParser(
        description="library CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="pandamonium, version {version}".format(version=__version__),
    )

    return parser.parse_args()
