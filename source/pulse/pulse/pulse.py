"""
    File name: modbus_client.py
    Author: Jason E. Blackert
    Date created: 12/7/2022
    Python Version: 3.9.2
    Summary: Opens a RS485 TCP Serial Connection
             and sends desired data to Master
             device.
"""
import logging
import time

from pulse.util import Cache, parse_args, store_context, use_store

args = parse_args()
config = args.config

log = logging.getLogger(__name__)
logging.basicConfig(
    level=config["pulse"]["log_level"],
    format="%(name)s [%(levelname)s]: %(message)s",
    force=True,
)


def main():
    cache = Cache()
    with store_context(cache):
        store = use_store()

        log.info(f"{store=}")

        time.sleep(5)


if __name__ == "__main__":
    main()
