import typing

import requests
import json


# This uses the Github v3 API
# * https://developer.github.com/v3/#current-version
# * all dates are in ISO 8601 format
# * uses requests Python package: https://www.edureka.co/blog/python-requests-tutorial/#z3
# * for more on pagination and client errors: https://developer.github.com/v3/#pagination

class ActionsClient(object):
    '''
    This client supports the endpoints described in
    https://developer.github.com/v3/actions/workflow-runs
    '''

    def __init__(self, parent: 'SimpleGithubClient') -> None:
        self.parent = parent

    def list_workflow_runs(self,
                           owner: str,
                           repo: str,
                           workflow_file_name_or_id: str,
                           actor: str = None,
                           branch: str = None,
                           event: str = None,
                           status: str = None) -> typing.Dict:
        params = {}
        if actor is not None:
            params['actor'] = actor

        if branch is not None:
            params['branch'] = branch

        if event is not None:
            params['event'] = event

        if status is not None:
            params['status'] = status

        reply = requests.get(
            f'{SimpleGithubClient.GH_ROOT}/repos/{owner}/{repo}/actions/workflows/{workflow_file_name_or_id}/runs',
            params=params, headers=self.parent.build_headers())
        return reply.json()


class ReposClient(object):

    def __init__(self, parent: 'SimpleGithubClient'):
        self.parent = parent

    def create_repository_dispatch_event(self, owner: str, repo: str, event_type: str,
                                         client_payload: str = '{"test":"true"}'):
        '''
        https://goobar.io/2019/12/07/manually-trigger-a-github-actions-workflow/
        :param owner:
        :param repo:
        :param event_type:
        :param client_payload:
        :return:
        '''
        data = {'event_type': event_type, 'client_payload': client_payload}
        # json_data = json.dumps(data)
        json_data = '''
            {
                "event_type": "%s",
                "client_payload": {
                    "unit": false,
                    "integration": true
                }
            }
        ''' % event_type
        response = requests.post(f'{SimpleGithubClient.GH_ROOT}/repos/{owner}/{repo}/dispatches',
                                 params=data,
                                 data=json_data,
                                 # json=json_data,
                                 headers=self.parent.build_headers(
                                     {'Accept': 'application/vnd.github.everest-preview+json'}))
        return response.content


class UsersClient(object):

    def __init__(self, parent: 'SimpleGithubClient'):
        self.parent = parent

    def get_events_for_authenticated_user(self, username: str) -> typing.List[typing.Dict]:
        r = requests.get(f'{SimpleGithubClient.GH_ROOT}/users/{username}/events '.strip(),
                         headers=self.parent.build_headers())
        return r.json()


class SimpleGithubClient(object):
    GH_ROOT = ' https://api.github.com  '.strip()

    def repos(self) -> ReposClient:
        return ReposClient(self)

    def actions(self) -> ActionsClient:
        return ActionsClient(self)

    def users(self) -> UsersClient:
        return UsersClient(self)

    def __init__(self, personal_access_token: str):
        self.personal_access_token = personal_access_token
        self.default_headers = {'Authorization': f'token {self.personal_access_token}'}

    def build_headers(self, custom_headers: typing.Dict = {}) -> typing.Dict:
        n_dict = {}
        for k, v in self.default_headers.items():
            n_dict[k] = self.default_headers[k]
        for k, v in custom_headers.items():
            n_dict[k] = custom_headers[k]
        return n_dict
