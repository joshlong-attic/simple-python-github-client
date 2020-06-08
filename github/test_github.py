import unittest

from github import *
import os

# https://realpython.com/python-testing/

github = SimpleGithubClient(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'].strip())
users = github.users()
repos = github.repos()
actions = github.actions()


class ActionsTest(unittest.TestCase):

    def test_list_workflow_runs(self):
        owner = 'joshlong'
        project = 'jwt-spring-boot-starter'
        failures = actions.list_workflow_runs(owner, project, 'build.yml', status='failure')['total_count']
        all = actions.list_workflow_runs(owner, project, 'build.yml')['total_count']
        self.assertTrue(all > failures)  # I hope!


class ReposTest(unittest.TestCase):

    def test_create_repository_dispatch_event(self):
        owner = 'joshlong'
        project = 'jwt-spring-boot-starter'
        print(repos.create_repository_dispatch_event(owner, project, 'update-event'))


class UsersTest(unittest.TestCase):

    def test_get_events_for_authenticated_user(self):
        events = users.get_events_for_authenticated_user('joshlong')
        self.assertTrue(len(events) > 0, 'there must be more than one event in the github repository')


if __name__ == '__main__':
    unittest.main()
