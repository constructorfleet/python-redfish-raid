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

```
$COMMAND: Command you wish to run  
  prefix: Starting API Endpoint for the command    
  recurse: Use False to disable API recursion, True to enable full API recursion or an integer to specify the maximum recursion depth  
  json_queries: List of JMESPath strings to filter the JSON output  
    key: Resulting JSON key  
    jq: JMESPath Query string (See http://jmespath.org/ for syntax and information)
  reportv: Report with placeholders for the result data (Replacers are of the format `{key_name)`
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
