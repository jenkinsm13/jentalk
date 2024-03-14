from setuptools import setup, find_packages

setup(
    name='JentalkIDE',
    version='0.1.7',
    author='Mike Jenkins',
    author_email='mike@chrotonics.com',
    packages=find_packages(),
    install_requires=[
        'graphviz',
    ],
    entry_points={
           'console_scripts': [
               'jentalk-ide = JentalkIDE.jentalk_ide:main',
           ],
       },
    url='http://pypi.python.org/pypi/JentalkIDE/',
    license='LICENSE',
    description='An Integrated Development Environment for Jentalk language',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
