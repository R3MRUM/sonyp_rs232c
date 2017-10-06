from setuptools import setup
from distutils.core import setup

with open('README') as file:
    long_description = file.read()

setup(name='sonyp_rs232c',
      version='0.1',
      description='A Python3 class used for controlling a Sony VPL-HWXXES projector via serial connection.',
      keywords = "sony projector VPL-HW35ES VPL-HW40ES VPL-HW50ES VPL-HW55ES VPL-HW58ES HW35ES HW40ES HW50ES HW55ES HW58ES",
      url='https://github.com/R3MRUM/sonyp_rs232c',
      author='R3MRUM',
      author_email='robpantazopoulos@gmail.com',
      license='GPLv3+',
      packages=['sonyp_rs232c'],
      classifiers=[
      	"Development Status :: 4 - Beta",
      	"Topic :: Home Automation",
      	"License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)"],
     long_description=long_description)