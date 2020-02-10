from setuptools import setup

setup(name="usgs_waterservices_data",
      version='0.1',
      description="Wrapper to handle pulling data from USGS Water Services API",
      url="https://github.com/ladabie/usgs_waterservices_data.git",
      author="Lauren Adabie",
      author_email="lauren.adabie@gmail.com",
      license='MIT',
      packages=['usgs_waterservices_data'],
      install_requires=['pandas','requests','re'],
      zip_safe=False)
