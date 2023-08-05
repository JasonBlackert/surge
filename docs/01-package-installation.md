# 02.0 Package Installation

## 02.1 Update and Upgrade OS Packages

`sudo apt update && sudo apt full-upgrade -y && sudo dist-upgrade`

### 02.2 Document Device Serial Number - One Time

`cat /sys/firmware/devicetree/base/serial-number`

### 02.3 Install Mosquitto Broker and Client

`sudo apt install -y mosquitto mosquitto-clients`
`sudo systemctl enable mosquitto.service`

### 02.4 Miscellaneous tools: Install QMI library tools, udhcpc, and tmux

`sudo apt install tmux -y`
