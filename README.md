[comment]: # "Auto-generated SOAR connector documentation"
# Statuspage

Publisher: Splunk  
Connector Version: 1\.0\.1  
Product Vendor: Atlassian  
Product Name: Statuspage  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.2\.0  

This app is an Atlassian product that is used to help monitor and communicate status issues for various products

# Splunk> Phantom

Welcome to the open-source repository for Splunk> Phantom's statuspage App.

Please have a look at our [Contributing Guide](https://github.com/Splunk-SOAR-Apps/.github/blob/main/.github/CONTRIBUTING.md) if you are interested in contributing, raising issues, or learning more about open-source Phantom apps.

## Legal and License

This Phantom App is licensed under the Apache 2.0 license. Please see our [Contributing Guide](https://github.com/Splunk-SOAR-Apps/.github/blob/main/.github/CONTRIBUTING.md#legal-notice) for further details.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a Statuspage asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**base\_url** |  required  | string | Base URL to Statuspage service
**api\_key** |  required  | password | API Key
**page\_id** |  required  | string | Page Identifier
**timeout** |  required  | numeric | Timeout \(seconds\)

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using the supplied credentials  
[list incidents](#action-list-incidents) - Get a list of incidents  
[get incident](#action-get-incident) - Get an incident's details  
[create incident subscriber](#action-create-incident-subscriber) - Create an incident subscriber  
[create incident](#action-create-incident) - Create an incident  
[update incident](#action-update-incident) - Update an incident  
[list incident subscribers](#action-list-incident-subscribers) - Get a list of incident subscribers  

## action: 'test connectivity'
Validate the asset configuration for connectivity using the supplied credentials

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'list incidents'
Get a list of incidents

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**query** |  optional  | Provide text to search in the incident name, status, postmortem body and incident\_updates fields | string | 
**limit** |  optional  | The maximum number of rows to return per page \(default and max\: 100\) | numeric | 
**page\_offset** |  optional  | Page offset to fetch | numeric | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.limit | numeric | 
action\_result\.parameter\.page\_offset | numeric | 
action\_result\.parameter\.query | string | 
action\_result\.data\.\*\.components\.\*\.created\_at | string | 
action\_result\.data\.\*\.components\.\*\.description | string | 
action\_result\.data\.\*\.components\.\*\.group\_id | string | 
action\_result\.data\.\*\.components\.\*\.id | string | 
action\_result\.data\.\*\.components\.\*\.name | string | 
action\_result\.data\.\*\.components\.\*\.page\_id | string | 
action\_result\.data\.\*\.components\.\*\.position | numeric | 
action\_result\.data\.\*\.components\.\*\.showcase | boolean | 
action\_result\.data\.\*\.components\.\*\.start\_date | string | 
action\_result\.data\.\*\.components\.\*\.status | string | 
action\_result\.data\.\*\.components\.\*\.updated\_at | string | 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.id | string |  `incident id` 
action\_result\.data\.\*\.name | string |  `incident name` 
action\_result\.data\.\*\.status | string |  `incident status` 
action\_result\.data\.\*\.impact | string |  `incident impact` 
action\_result\.data\.\*\.impact\_override | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.code | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.name | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.new\_status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.old\_status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.body | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.created\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.custom\_tweet | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.deliver\_notifications | boolean | 
action\_result\.data\.\*\.incident\_updates\.\*\.display\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.incident\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.tweet\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.twitter\_updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.wants\_twitter\_update | boolean | 
action\_result\.data\.\*\.monitoring\_at | string | 
action\_result\.data\.\*\.page\_id | string | 
action\_result\.data\.\*\.postmortem\_body | string | 
action\_result\.data\.\*\.postmortem\_body\_last\_updated\_at | string | 
action\_result\.data\.\*\.postmortem\_ignored | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_subscribers | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_twitter | boolean | 
action\_result\.data\.\*\.postmortem\_published\_at | string | 
action\_result\.data\.\*\.resolved\_at | string | 
action\_result\.data\.\*\.scheduled\_auto\_completed | boolean | 
action\_result\.data\.\*\.scheduled\_auto\_in\_progress | boolean | 
action\_result\.data\.\*\.scheduled\_for | string | 
action\_result\.data\.\*\.scheduled\_remind\_prior | boolean | 
action\_result\.data\.\*\.scheduled\_reminded\_at | string | 
action\_result\.data\.\*\.scheduled\_until | string | 
action\_result\.data\.\*\.shortlink | string | 
action\_result\.data\.\*\.started\_at | string | 
action\_result\.data\.\*\.updated\_at | string | 
action\_result\.summary\.num\_incident | numeric | 
action\_result\.summary\.num\_incidents | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'get incident'
Get an incident's details

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**incident\_id** |  required  | Incident Identifier | string |  `incident id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.incident\_id | string |  `incident id` 
action\_result\.data\.\*\.components\.\*\.automation\_email | string | 
action\_result\.data\.\*\.components\.\*\.created\_at | string | 
action\_result\.data\.\*\.components\.\*\.description | string | 
action\_result\.data\.\*\.components\.\*\.group | boolean | 
action\_result\.data\.\*\.components\.\*\.group\_id | string | 
action\_result\.data\.\*\.components\.\*\.id | string | 
action\_result\.data\.\*\.components\.\*\.name | string | 
action\_result\.data\.\*\.components\.\*\.only\_show\_if\_degraded | boolean | 
action\_result\.data\.\*\.components\.\*\.page\_id | string | 
action\_result\.data\.\*\.components\.\*\.position | numeric | 
action\_result\.data\.\*\.components\.\*\.showcase | boolean | 
action\_result\.data\.\*\.components\.\*\.start\_date | string | 
action\_result\.data\.\*\.components\.\*\.status | string | 
action\_result\.data\.\*\.components\.\*\.updated\_at | string | 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.id | string |  `incident id` 
action\_result\.data\.\*\.name | string |  `incident name` 
action\_result\.data\.\*\.status | string |  `incident status` 
action\_result\.data\.\*\.impact | string |  `incident impact` 
action\_result\.data\.\*\.impact\_override | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.code | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.name | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.new\_status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components\.\*\.old\_status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.body | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.created\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.custom\_tweet | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.deliver\_notifications | boolean | 
action\_result\.data\.\*\.incident\_updates\.\*\.display\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.incident\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.tweet\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.twitter\_updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.wants\_twitter\_update | boolean | 
action\_result\.data\.\*\.monitoring\_at | string | 
action\_result\.data\.\*\.page\_id | string | 
action\_result\.data\.\*\.postmortem\_body | string | 
action\_result\.data\.\*\.postmortem\_body\_last\_updated\_at | string | 
action\_result\.data\.\*\.postmortem\_ignored | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_subscribers | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_twitter | boolean | 
action\_result\.data\.\*\.postmortem\_published\_at | string | 
action\_result\.data\.\*\.resolved\_at | string | 
action\_result\.data\.\*\.scheduled\_auto\_completed | boolean | 
action\_result\.data\.\*\.scheduled\_auto\_in\_progress | boolean | 
action\_result\.data\.\*\.scheduled\_for | string | 
action\_result\.data\.\*\.scheduled\_remind\_prior | boolean | 
action\_result\.data\.\*\.scheduled\_reminded\_at | string | 
action\_result\.data\.\*\.scheduled\_until | string | 
action\_result\.data\.\*\.shortlink | string | 
action\_result\.data\.\*\.updated\_at | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create incident subscriber'
Create an incident subscriber

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**incident\_id** |  required  | Incident Identifier | string |  `incident id` 
**email** |  required  | Email address for creating email subscriber | string |  `email id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.parameter\.email | string |  `email id` 
action\_result\.parameter\.incident\_id | string |  `incident id` 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.id | string |  `subscriber id` 
action\_result\.data\.\*\.email | string |  `email id` 
action\_result\.status | string | 
action\_result\.data\.\*\.mode | string | 
action\_result\.data\.\*\.purge\_at | string | 
action\_result\.data\.\*\.quarantined\_at | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'create incident'
Create an incident

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**name** |  required  | Incident Name | string |  `incident name` 
**status** |  optional  | Incident status\. Default is investigating | string |  `incident status` 
**impact\_override** |  optional  | Select value to override calculated impact value | string |  `incident impact value` 
**body** |  optional  | Write a initial message, created as the first incident update | string |  `incident body` 
**component\_ids** |  optional  | Specify component's id affected by this incident\. Separate multiple ids with commas | string | 
**components** |  optional  | A JSON object of 'component affected' and 'status' | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string |  `incident id` 
action\_result\.parameter\.name | string |  `incident name` 
action\_result\.status | string | 
action\_result\.parameter\.body | string |  `incident body` 
action\_result\.parameter\.component\_ids | string | 
action\_result\.parameter\.components | string | 
action\_result\.parameter\.impact\_override | string |  `incident impact value` 
action\_result\.parameter\.status | string |  `incident status` 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.impact | string | 
action\_result\.data\.\*\.impact\_override | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.body | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.created\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.custom\_tweet | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.deliver\_notifications | boolean | 
action\_result\.data\.\*\.incident\_updates\.\*\.display\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.incident\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.tweet\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.twitter\_updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.wants\_twitter\_update | boolean | 
action\_result\.data\.\*\.monitoring\_at | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.page\_id | string | 
action\_result\.data\.\*\.postmortem\_body | string | 
action\_result\.data\.\*\.postmortem\_body\_last\_updated\_at | string | 
action\_result\.data\.\*\.postmortem\_ignored | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_subscribers | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_twitter | boolean | 
action\_result\.data\.\*\.postmortem\_published\_at | string | 
action\_result\.data\.\*\.resolved\_at | string | 
action\_result\.data\.\*\.scheduled\_auto\_completed | boolean | 
action\_result\.data\.\*\.scheduled\_auto\_in\_progress | boolean | 
action\_result\.data\.\*\.scheduled\_for | string | 
action\_result\.data\.\*\.scheduled\_remind\_prior | boolean | 
action\_result\.data\.\*\.scheduled\_reminded\_at | string | 
action\_result\.data\.\*\.scheduled\_until | string | 
action\_result\.data\.\*\.shortlink | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.updated\_at | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'update incident'
Update an incident

Type: **generic**  
Read only: **False**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**incident\_id** |  required  | Incident Identifier | string |  `incident id` 
**name** |  optional  | Update Incident Name | string |  `incident name` 
**status** |  optional  | Update Incident status | string |  `incident status` 
**impact\_override** |  optional  | Select value to override impact value | string |  `incident impact value` 
**body** |  optional  | Update initial message, created as the first incident update | string |  `incident body` 
**component\_ids** |  optional  | Specify component's id affected by this incident\. Separate multiple ids with commas | string | 
**components** |  optional  | A JSON object of 'component affected' and 'status' | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.data\.\*\.id | string |  `incident id` 
action\_result\.data\.\*\.name | string |  `incident name` 
action\_result\.status | string | 
action\_result\.parameter\.body | string |  `incident body` 
action\_result\.parameter\.component\_ids | string | 
action\_result\.parameter\.components | string | 
action\_result\.parameter\.impact\_override | string |  `incident impact value` 
action\_result\.parameter\.incident\_id | string |  `incident id` 
action\_result\.parameter\.name | string |  `incident name` 
action\_result\.parameter\.status | string |  `incident status` 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.impact | string | 
action\_result\.data\.\*\.impact\_override | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.affected\_components | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.body | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.created\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.custom\_tweet | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.deliver\_notifications | boolean | 
action\_result\.data\.\*\.incident\_updates\.\*\.display\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.incident\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.status | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.tweet\_id | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.twitter\_updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.updated\_at | string | 
action\_result\.data\.\*\.incident\_updates\.\*\.wants\_twitter\_update | boolean | 
action\_result\.data\.\*\.monitoring\_at | string | 
action\_result\.data\.\*\.page\_id | string | 
action\_result\.data\.\*\.postmortem\_body | string | 
action\_result\.data\.\*\.postmortem\_body\_last\_updated\_at | string | 
action\_result\.data\.\*\.postmortem\_ignored | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_subscribers | boolean | 
action\_result\.data\.\*\.postmortem\_notified\_twitter | boolean | 
action\_result\.data\.\*\.postmortem\_published\_at | string | 
action\_result\.data\.\*\.resolved\_at | string | 
action\_result\.data\.\*\.scheduled\_auto\_completed | boolean | 
action\_result\.data\.\*\.scheduled\_auto\_in\_progress | boolean | 
action\_result\.data\.\*\.scheduled\_for | string | 
action\_result\.data\.\*\.scheduled\_remind\_prior | boolean | 
action\_result\.data\.\*\.scheduled\_reminded\_at | string | 
action\_result\.data\.\*\.scheduled\_until | string | 
action\_result\.data\.\*\.shortlink | string | 
action\_result\.data\.\*\.status | string | 
action\_result\.data\.\*\.updated\_at | string | 
action\_result\.summary | string | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list incident subscribers'
Get a list of incident subscribers

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**incident\_id** |  required  | Incident Identifier | string |  `incident id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.incident\_id | string |  `incident id` 
action\_result\.data\.\*\.created\_at | string | 
action\_result\.data\.\*\.id | string |  `subscriber id` 
action\_result\.data\.\*\.email | string |  `email id` 
action\_result\.data\.\*\.mode | string | 
action\_result\.data\.\*\.purge\_at | string | 
action\_result\.data\.\*\.quarantined\_at | string | 
action\_result\.summary\.num\_of\_subscribers | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 