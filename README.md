# python-redfish-raid
Redfish for RAID


## Running the Application

`python3 -m main.py [args]`

Commandline arguments/flags:

`--api`: Specifies which API client to use (currently only standard Redfish Api Client is implemented)  
`--host`: The DNS or IP of the hose you wish to connect to  
`--account`: The username for authentication with the API  
`--password`: The password associated with username for authentication  
`--system`: Which system configuration to load - you can ignore the extension of the configuration file  
`--prefix`: Override the starting endpoint for the API 

`--showallinfo`: Show all data (except that filtered using the Json Queries below)  
`--showprinfo`: Show the Patrol Read status information [NOT IMPLEMENTED]  
`--showccinfo`: Show the consistency check information [NOT IMPLEMENTED]  
`--showbbuinfo`: Show the backup battery information [NOT IMPLEMENTED]  
`--showencinfo`: Show information related to the RAID enclosure
`--showdisks`: Show the physical disk information for the array
`--showlogical`: Show the information related to the logical volumes in the array
`--nagios`: Perform a nagios status check on the array [NOT IMPLEMENTED]

## Configuring the Application

### Configuration File

Configuration files are YAML based and can be specified at run time using the `--system` to specify which system configuration file you wish you use.

#### Structure:

```yaml
$COMMAND: Command you wish to run  
  prefix: Starting API Endpoint for the command    
  recurse: Use False to disable API recursion, True to enable full API recursion or an integer to specify the maximum recursion depth  
  json_filters: List of JMESPath strings to filter the JSON output  
    key: Resulting JSON key  
    jq: JMESPath Query string (See http://jmespath.org/ for syntax and information)
    format: Resulting text output format for JMESPath queries
    sub_formats: Resulting output format for specific JMESPath JSON key (i.e. physical drives which are members of a logial drive)
  report: Report with placeholders for the formatted result data (Replacers are of the format `{key_name)`
```
##### Example YAML configuration
```yaml
show_logical:
  prefix: /redfish/v1/Systems/System.Embedded.1/Storage/RAID.Integrated.1-1/Volumes
  recurse: 4

  json_filters:

    - key: allvolumes
      jq: >
        Members[*].{
        Name: Oem.Dell.DellVirtualDisk.Id,
        VirtualDiskTargetID: Oem.Dell.DellVirtualDisk.VirtualDiskTargetID,
        DiskCachePolicy: Oem.Dell.DellVirtualDisk.DiskCachePolicy,
        ReadCachePolicy: Oem.Dell.DellVirtualDisk.ReadCachePolicy,
        WriteCachePolicy: Oem.Dell.DellVirtualDisk.WriteCachePolicy,
        SpanDepth: Oem.Dell.DellVirtualDisk.SpanDepth,
        SpanLength: Oem.Dell.DellVirtualDisk.SpanLength,
        Status: Status.Health
        MemberDisks: "@Redfish.Settings".SettingsObject.Links.Drives[*].{ BlockSizeBytes: BlockSizeBytes, Revision: Revision, CapableSpeedGbs: CapableSpeedGbs, Manufacturer: Manufacturer, SerialNumber: SerialNumber, CapacityBytes: naturalsize(CapacityBytes), Model: Model, Name: Name }
        }

      format: |
        [{Name}]
          Virtual Drive: {VirtualDiskTargetID}
          Cache Policy: {DiskCachePolicy}
          Span Depth: {SpanDepth}
          Span Length: {SpanLength}

          Status: {Status}
          Members:
        {MemberDisks}

      sub_formats:
        MemberDisks: |
          \t\t[{Name}] {CapacityBytes} {Manufacturer} {Model} {SerialNumber}

  report: |
    {allvolumes}
```

##### Command output from above example
```bash
#> python3 __main__.py --host 'https://10.253.20.221' --account 'root' --password <password> --showlogical --system dell

[Disk.Virtual.0:RAID.Integrated.1-1]
  Virtual Drive: 0
  Cache Policy: Default
  Span Depth: 1
  Span Length: 2

  Status: OK
  Members:
    [Solid State Disk 0:1:0] 119.5 GB INTEL SSDSC2BB120G7R PHDV721600AY150MGN
    [Solid State Disk 0:1:1] 119.5 GB INTEL SSDSC2BB120G7R PHDV7215088V150MGN


[Disk.Virtual.1:RAID.Integrated.1-1]
  Virtual Drive: 1
  Cache Policy: Enabled
  Span Depth: 1
  Span Length: 1

  Status: OK
  Members:
    [Solid State Disk 0:1:6] 959.7 GB TOSHIBA PX05SVB096Y 67L0A184TEZE

```

## Application Environment Setup (python virtual environment)
```shell script
❯ cd python-redfish-raid_customerfiles
❯ python3 -m venv venv
❯ source venv/bin/activate
❯ pip install -r requirements.txt
❯ cd python-redfish-raid
❯ python __main__.py --host 'https://10.253.20.221' --account 'root' --password <password> --showd --system dell

Total Drives: 3

[Solid State Disk 0:1:0]  PFail: False  PLife: 100%  Capacity: 119.5 GB INTEL SSDSC2BB120G7R SN: PHDV721600AY150MGN Rev: N201DL42  Online
[Solid State Disk 0:1:1]  PFail: False  PLife: 100%  Capacity: 119.5 GB INTEL SSDSC2BB120G7R SN: PHDV7215088V150MGN Rev: N201DL42  Online
[Solid State Disk 0:1:6]  PFail: False  PLife: 100%  Capacity: 959.7 GB TOSHIBA PX05SVB096Y SN: 67L0A184TEZE Rev: AS03  Online


  3 Healthy Drives:
    OK: Solid State Disk 0:1:0
    OK: Solid State Disk 0:1:1
    OK: Solid State Disk 0:1:6


  0 Unhealthy Drives:
```

## Custom API clients

For extensibility, custom api clients can be added as needed. To add a new API client, create a client in `python-redfish-raid/srrc/data/client` following the existing `RedfishClient.py` client implementation.  
An API client must implement the following methods:

`connect(self, **kwargs)`  
This method specifies how the client will connect the the remote API

`get(self, path)`  
This method performs an HTTP GET request for the specified path

`disconnect(self, **kwargs)`  
This method disconnects the client to make sure sessions are closed responsibly.

### Extending the API interface

If, For example, your client needs to perform `POST` or `PUT` - you should add the appropriate methods to `python-redfish-raid/framework/client/Client.py` base API client class, and then implement the appropriate method in your custom API client. You may need to add the invocation of these methods to the InvokeApiUseCase as needed.

