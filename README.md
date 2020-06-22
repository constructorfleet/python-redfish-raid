# python-redfish-raid
Redfish for RAID

## Running the Application

## Configuring the Application

### Configuration File

#### Structure:

`$COMMAND`: Command you wish to run  
  `prefix`: Starting API Endpoint for the command  
  `property`: Optional value that will pull the `Link.property` from the root API response  
  `recurse`: Use `False` to disable API recursion, `True` to enable full API recursion or an integer to specify the maximum recursion depth  
  `json_queries`: List of resource endpoints and JSON Query strings to make the output less cluttered  
    `endpoint`: Regular expression to match resource endpoint
    `queries`: List of JSON Query and Select statements to display
