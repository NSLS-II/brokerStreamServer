__author__ = 'arkilic'

from distutils.core import setup

setup(
    name='brokerStreamServer',
    version='0.0.x',
    author='Arman Arkilic',
    packages=["brokerStreamServer",
              "brokerStreamServer.server",
              "brokerStreamServer.client",
              "brokerStreamServer.commands",
              "brokerStreamServer.startup"
              ],
    )
