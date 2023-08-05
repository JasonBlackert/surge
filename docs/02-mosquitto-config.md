# 03.0 Configure Mosquitto (MQTT) Broker for Use

## 03.1 Create Mosquitto Configuration File

`sudo nano /etc/mosquitto/conf.d/standard.conf`

```<new file contents>
listener 1883
protocol mqtt
allow_anonymous true
```

## 03.3 Make Mosquitto Wait Until Network is Online

`sudo systemctl edit mosquitto.service`

```<mosquitto.service>
[Unit]
After=
After=network-online.target
Wants=
Wants=network-online.target
```

`sudo systemctl restart mosquitto`
