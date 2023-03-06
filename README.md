# Dumb UPS Auto Shutdown (D.U.A.S.)

As the name suggests, this is a script that can be used to auto shutdown a server if using a dumb UPS in case of a power
outage. This is achieved by simply pinging a host on your network which does not have power backup and will immediately
shut down in case of a power outage.

## Config File

The config file is a simple text file like this:

```
10.195.15.2
10.195.15.13
```

The above script implies that it will only check the second host `10.195.15.13` if and only if the first host
`10.195.15.2` is offline. If it finds that all hosts listed here are offline, it will shut down the system on which the
script in running. You can list as many hosts as you like here.