import logging
from typing import Any

from influxdb import InfluxDBClient

from pulse.util.store import Store

log = logging.getLogger(__name__)


class Database(Store):
    def __init__(self) -> None:
        self.client = InfluxDBClient(database="telemetry")

    def list_macs(self) -> list[str]:
        result = self.client.query(
            'SELECT DISTINCT "mac_address" FROM "telemetry" WHERE time >= now() - 2m'
        )

        return [item["distinct"] for item in result["telemetry"]]  # type: ignore

    def select_telemetry(self, measure: str) -> dict[str, Any]:
        result = self.client.query(
            f'SELECT {measure}, mac_address FROM "telemetry" WHERE time > now() - 2m GROUP BY "mac_address" LIMIT 1'  # noqa: E501
        )

        return {item["mac_address"]: item[measure] for item in result["telemetry"]}  # type: ignore  # noqa: E501

    def populate_cache(self) -> dict[str, Any]:
        result = self.client.query(
            """
            SELECT last(sl_status) AS sl_status,
                P_PV,
                BMS_SOC,
                BMS_Min_Cell_V,
                timestamp,
                mac_address
            FROM telemetry
            WHERE time > now() - 2m
            GROUP BY mac_address
            """
        )

        return {item["solarleaf_id"]: item for item in result["telemetry"]}  # type: ignore  # noqa: E501
