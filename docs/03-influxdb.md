# InfluxDB

## Installation

Install the InfluxDB daemon and CLI by running

```bash
sudo apt install influxdb influxdb-client
```

## Configuration

Start the InfluxDB shell by running the `influx` command. You should be prompted
with a connection string and version identifier:

```<open influx terminal>
$ influx
Connected to http://localhost:8086 version 1.6.7~rc0
InfluxDB shell version: 1.6.7~rc0
>
```

Create the `telemetry` database with a 30 day retention policy by running

Verify the settings by running

```<influx terminal>
> show retention policies on telemetry
name    duration shardGroupDuration replicaN default
----    -------- ------------------ -------- -------
autogen 720h0m0s 168h0m0s           1        true
```

Create the `inventory` database by running

```<influx terminal>
> create database inventory
```

Note that the `inventory` database has an infinite retention policy by design,
since it is intended to be used as an audit trail.

## Helpful Queries

Windows GUI: <https://timeseriesadmin.github.io/>

Query all the data from the telemetry database within the last day.
`SELECT * FROM "telemetry" WHERE time >= now() - 1d AND time < now()`

Query all the data from the telemetry database within the last thirty minutes.
`SELECT * FROM "telemetry" WHERE time >= now() - 30m AND time < now()`

Query all the data from the telemetry database within the last day for a specific MAC address.
`SELECT * FROM "telemetry" WHERE "mac_address" = <MAC_ADDRESS> AND time >= now() - 1d AND time < now()`

Query all the MAC addresses that have reported within the last 10 minutes.
`SELECT DISTINCT "mac_address" FROM "telemetry" WHERE time >= now() - 10m`
