from setuptools import setup, find_packages

setup(
    name='JentalkIDE',
    version='0.1.0',
    author='Mike Jenkins',
    author_email='mike@chrotonics.com',
    packages=find_packages(),
    install_requires=[
        'tkinter',  # Assuming tkinter is a dependency; replace with actual dependencies
    ],
    url='http://pypi.python.org/pypi/JentalkIDE/',
    license='LICENSE',
    description='An Integrated Development Environment for Jentalk language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
