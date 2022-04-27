# File: statuspage_connector.py
#
# Copyright (c) 2022 Splunk Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.
#
#
import json
import sys

import phantom.app as phantom
import requests
from bs4 import BeautifulSoup
from phantom.action_result import ActionResult
from phantom.base_connector import BaseConnector

from statuspage_consts import *


class RetVal(tuple):
    def __new__(cls, val1, val2):
        return tuple.__new__(RetVal, (val1, val2))


class StatuspageConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(StatuspageConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

        self._api_key = None

    def _get_error_message_from_exception(self, e):
        """
        Get appropriate error message from the exception.

        :param e: Exception object
        :return: error message
        """
        error_code = None
        error_msg = ERR_MSG_UNAVAILABLE

        try:
            if hasattr(e, "args"):
                if len(e.args) > 1:
                    error_code = e.args[0]
                    error_msg = e.args[1]
                elif len(e.args) == 1:
                    error_msg = e.args[0]
        except:
            pass

        if not error_code:
            error_text = "Error Message: {}".format(error_msg)
        else:
            error_text = "Error Code: {}. Error Message: {}".format(error_code, error_msg)

        return error_text

    def _process_empty_reponse(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(
            phantom.APP_ERROR,
            "Status Code: {}. Empty response and no information in the header.".format(response.status_code)
        ), None)

    def _process_html_response(self, response, action_result):

        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            # Remove the script, style, footer and navigation part from the HTML message
            for element in soup(["script", "style", "footer", "nav"]):
                element.extract()
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code,
                error_text)

        message = message.replace('{', '{{').replace('}', '}}')

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):

        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        try:
            if resp_json.get('type') and resp_json.get('message'):
                message = "Error from server. Status Code: {0} Data from server: Error Type: {1}. Error Message: {2}".format(
                    r.status_code, resp_json.get('type'), resp_json.get('message'))
            if resp_json.get('errors', [])[0][0].get('message'):
                message = "Error from server. Status Code: {0} Data from server: {1}".format(
                    r.status_code, resp_json.get('errors', [])[0][0].get('message'))
        except:
            pass
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML resonse, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between SOAR and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_reponse(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, headers=None, params=None, data=None, json=None, method="get", files=None):

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)), resp_json)

        # Create a URL to connect to
        url = "{}{}".format(self._base_url, endpoint)

        try:
            r = request_func(
                        url,
                        data=data,
                        json=json,
                        headers=headers,
                        verify=config.get('verify_server_cert', False),
                        params=params)
        except requests.exceptions.InvalidURL as e:
            self.debug_print(self._get_error_message_from_exception(e))
            return RetVal(action_result.set_status(phantom.APP_ERROR, STATUSPAGE_ERR_INVALID_URL.format(url=url)), resp_json)
        except requests.exceptions.ConnectionError as e:
            self.debug_print(self._get_error_message_from_exception(e))
            return RetVal(action_result.set_status(phantom.APP_ERROR, STATUSPAGE_ERR_CONNECTION_REFUSED.format(url=url)), resp_json)
        except requests.exceptions.InvalidSchema as e:
            self.debug_print(self._get_error_message_from_exception(e))
            return RetVal(action_result.set_status(phantom.APP_ERROR, STATUSPAGE_ERR_INVALID_SCHEMA.format(url=url)), resp_json)
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            self.debug_print(self._get_error_message_from_exception(error_msg))
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR,
                    STATUSPAGE_ERR_CONNECTING_TO_SERVER.format(error=error_msg),
                ),
                resp_json
            )

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        self.save_progress("Starting connectivity test")
        # make rest call
        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Authorization': api_key}

        endpoint = 'pages/{}/incidents'.format(self._page_id)  # pragma: allowlist secret

        ret_val, _ = self._make_rest_call(endpoint, action_result, headers=headers)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_get_incident(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Authorization': api_key}

        incident_id = param.get('incident_id')

        endpoint = 'pages/{0}/incidents/{1}'.format(self._page_id, incident_id)  # pragma: allowlist secret

        ret_val, response = self._make_rest_call(endpoint, action_result, headers=headers)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully fetched incident")

    def _handle_list_incidents(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Authorization': api_key}

        parameters = dict()
        query = param.get('query')
        limit = param.get('limit')
        page = param.get('page_offset')

        if query:
            parameters['q'] = query
        if limit:
            parameters['limit'] = limit
        if page:
            parameters['page'] = page

        endpoint = 'pages/{}/incidents'.format(self._page_id)  # pragma: allowlist secret
        endpoint += '?{}'.format(parameters)

        ret_val, response = self._make_rest_call(endpoint, action_result, headers=headers, params=parameters)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        for incident in response:
            action_result.add_data(incident)

        summary = action_result.set_summary({})
        summary['num_incidents'] = len(response)

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_create_incident(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Content-Type': 'application/json', 'Authorization': api_key}

        data = dict()

        components = dict()
        ret_val, components = self._get_fields(param, action_result)

        data["incident"] = {
            "name": param.get('name'),
            "status": param.get('status'),
            "impact_override": param.get('impact_override'),
            "body": param.get('body'),
            "component_ids": param.get('component_ids'),
            "components": components
        }

        endpoint = 'pages/{}/incidents'.format(self._page_id)  # pragma: allowlist secret
        ret_val, response = self._make_rest_call(endpoint, action_result, json=data, headers=headers, method="post")

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created incident")

    def _handle_update_incident(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Content-Type': 'application/json', 'Authorization': api_key}

        data = dict()
        components = dict()
        ret_val, components = self._get_fields(param, action_result)

        incident_id = param.get('incident_id')

        name = param.get('name')
        status = param.get('status')
        impact_override = param.get('impact_override')
        body = param.get('body')
        component_ids = param.get('component_ids')

        if name:
            data['incident'] = {
                'name': name
            }
        if status:
            data['incident'] = {
                'status': status
            }
        if impact_override:
            data['incident'] = {
                'impact_override': impact_override
            }
        if body:
            data['incident'] = {
                'body': body
            }
        if component_ids:
            data['incident'] = {
                'component_ids': component_ids
            }
        if components:
            data['incident'] = {
                'components': components
            }

        endpoint = 'pages/{0}/incidents/{1}'.format(self._page_id, incident_id)  # pragma: allowlist secret
        ret_val, response = self._make_rest_call(endpoint, action_result, headers=headers, json=data, method="patch")

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully updated incident")

    def _get_fields(self, param, action_result):

        components = param.get('components')

        # fields is an optional field
        if not components:
            return RetVal(phantom.APP_SUCCESS, None)

        # we take in as a dictionary string, first try to load it as is
        try:
            components = json.loads(components)
        except Exception as e:
            error_msg = self._get_error_message_from_exception(e)
            return RetVal(action_result.set_status(phantom.APP_ERROR, STATUSPAGE_ERR_FIELDS_JSON_PARSE.format(error=error_msg)), None)

        return RetVal(phantom.APP_SUCCESS, components)

    def _handle_create_incident_subscriber(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Content-Type': 'application/json', 'Authorization': api_key}

        incident_id = param.get('incident_id')

        data = dict()
        data['subscriber'] = {
            'email': param.get('email'),
            'phone_country': param.get('phone_country'),
            'phone_number': param.get('phone_number'),
            'skip_confirmation_notification': param.get('skip_confirmation_notification')
        }

        endpoint = 'pages/{0}/incidents/{1}/subscribers'.format(self._page_id, incident_id)  # pragma: allowlist secret
        ret_val, response = self._make_rest_call(endpoint, action_result, headers=headers, json=data, method='post')

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        action_result.add_data(response)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully created incident subscriber")

    def _handle_list_incident_subscribers(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        api_key = "API Key {}".format(self._api_key)  # pragma: allowlist secret
        headers = {'Authorization': api_key}

        incident_id = param.get('incident_id')
        endpoint = 'pages/{0}/incidents/{1}/subscribers'.format(self._page_id, incident_id)  # pragma: allowlist secret

        ret_val, response = self._make_rest_call(endpoint, action_result, headers=headers)

        if phantom.is_fail(ret_val):
            return action_result.get_status()

        for incident in response:
            action_result.add_data(incident)

        summary = action_result.set_summary({})
        summary['num of subscribers'] = len(response)

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id: {}".format(self.get_action_identifier()))

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)
        elif action_id == 'list_incidents':
            ret_val = self._handle_list_incidents(param)
        elif action_id == 'create_incident':
            ret_val = self._handle_create_incident(param)
        elif action_id == 'get_incident':
            ret_val = self._handle_get_incident(param)
        elif action_id == 'update_incident':
            ret_val = self._handle_update_incident(param)
        elif action_id == 'create_incident_subscriber':
            ret_val = self._handle_create_incident_subscriber(param)
        elif action_id == 'list_incident_subscribers':
            ret_val = self._handle_list_incident_subscribers(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()
        if not isinstance(self._state, dict):
            self.debug_print("Resetting the state file with the default format")
            self._state = {
                "app_version": self.get_app_json().get('app_version')
            }
            return self.set_status(phantom.APP_ERROR, STATUSPAGE_STATE_FILE_CORRUPT_ERR)

        config = self.get_config()
        self._base_url = config['base_url']
        if not self._base_url.endswith('/'):
            self._base_url = "{}/".format(self._base_url)

        self._api_key = config['api_key']
        self._page_id = config['page_id']

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved accross actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import argparse

    import pudb

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            login_url = StatuspageConnector._get_phantom_base_url() + '/login'
            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            sys.exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = StatuspageConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    sys.exit(0)
