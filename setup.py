from setuptools import setup

setup(
    name='simple-python-github-client',
    version='0.2',
    description="You probably don't want to use this",
    long_description=open('README.md').read(),
    url='http://github.com/joshlong/simple-python-github-client',
    author='Josh Long',
    author_email='josh@joshlong.com',
    license='MIT',
    setup_requires=['wheel'],
    install_requires=['requests'],
    packages=['github'],
    ## TODO
    ## figure out why the deployed artifact has no Python code!
    ## TODO
    zip_safe=False
)
