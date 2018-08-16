from setuptools import setup

setup(
    name='django-exacttarget',
    version='0.1',
    description='Django wrapper for Exact Target',
    author='Mike Lewis',
    author_email='mlewis@sandow.com',
    license='MIT',
    url='https://github.com/snadow-digital/django-exacttarget',
    packages=['django_exacttarget'],
    install_requires=[
        'Salesforce-FuelSDK',
    ]
)
