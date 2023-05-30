# Dumb UPS Auto Shutdown (D.U.A.S.)

> **Note** check [BlackoutDefender](https://github.com/sujaldev/Blackout-Defender) for a simpler approach.

As the name suggests, this is a script that can be used to auto shutdown a server if using a dumb UPS in case of a power
outage. This is achieved by simply pinging a host on your network which does not have power backup and will immediately
shut down in case of a power outage.

## Config File

You can either compile the binary along with the config file or you can compile with an empty config file and then
specify it through the --config flag to the binary. I haven't written documentation for the config file but, you can
read the schema.json in the meantime. Here's an example:

```json5
{
  // define a node and give it any name you like, it's name will be used in the logs.
  "raspberry_pi": {
    // this is a required parameter for every host declared, it can be one of ipv4/ipv6/hostname/idna-hostname
    // if a node has errors in config, it'll be disabled and the other nodes will be used 
    "location": "10.0.3.14",
    // This host will be checked via ping
    "ping": {
      "retry_limit": 10
    },
    // Check methods are executed in the order you define them, this also applies to nodes.
    "https": {
      // this will check if the string "It works!" is present in the response body.
      "response_data": "It works!"
    }
  }
}
```

## Usage

```bash
usage: duas [-h] [-c CONFIG] [-l LOG_FILE] [--log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [-f LOG_FORMAT] [-d DATE_FORMAT] [-i INTERVAL] [--dry-run]

Signals an auto shutdown for a device connected to a dumb UPS by checking other network devices that shut down in case of a power outage

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Path to the config file
  -l LOG_FILE, --log-file LOG_FILE
                        Path to the log file
  --log-level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Recommend level is INFO
  -f LOG_FORMAT, --log-format LOG_FORMAT
                        See python's logging module docs for help
  -d DATE_FORMAT, --date-format DATE_FORMAT
                        The date format in logs, see python's logging module docs for help
  -i INTERVAL, --interval INTERVAL
                        Amount of time to wait after a successful healthcheck.
  --dry-run             Testing mode, will not shutdown server but will create a log
```

## Installation

Run the following commands on any machine, not necessarily on the machine you wish to run the script on.

```bash
git clone https://github.com/sujaldev/duas/
cd duas
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt pyinstaller
```

### Build

Before you build the binary you can define a duas.conf.json in the `src/` directory

```bash
cd src
pyinstaller --onefile --name duas --add-data=duas.conf.json:. --add-data=schema.json:. main.py
```

A binary file will be created: `src/dist/duas`

### Systemd

Once you have built the file, copy it to the machine you intend to shut down during a power outage. Then you can copy
the `src/sample.service` file to any systemd location such as `/etc/systemd/system/duas.service`
or `~/.config/systemd/user` depending on what user you want to run the service under. Update the value of `ExecStart` to
match the actual path of the binary and pass any extra parameters if you wish (run /path/to/binary --help).

Reload systemd by running:

```bash
systemctl daemon-reload
```

Start the service and enable it:

```bash
sudo systemctl enable --now duas.service

# or if you placed the service file under ~/.config
systemctl --user enable --now duas.service
```
