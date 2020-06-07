import unittest

from main import *

github = SimpleGithubClient(os.environ['GITHUB_TOKEN'].strip())
users = github.users()
actions = github.actions()


class ActionsTest(unittest.TestCase):
    def test_list_workflow_runs(self):
        owner = 'joshlong'
        project = 'jwt-spring-boot-starter'
        failures = actions.list_workflow_runs(owner, project, 'build.yml', status='failure')['total_count']
        all = actions.list_workflow_runs(owner, project, 'build.yml')['total_count']
        self.assertTrue(all > failures) # I hope!


class UsersTest(unittest.TestCase):

    def test_get_events_for_authenticated_user(self):
        events = users.get_events_for_authenticated_user('joshlong')
        self.assertTrue(len(events) > 0, 'there must be more than one event in the github repository')


if __name__ == '__main__':
    unittest.main()
