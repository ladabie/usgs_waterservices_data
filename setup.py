from setuptools import setup

setup(name="usgs_waterservices_data",
      version='0.0.0.dev1',
      description="Wrapper to handle pulling data from USGS Water Services API",
      url="https://github.com/ladabie/usgs_waterservices_data.git",
      author="Lauren Adabie",
      author_email="lauren.adabie@gmail.com",
      license='MIT',
      packages=['usgs_waterservices_data'],
      install_requires=['pandas','requests'],
      python_requires='>=3',
      zip_safe=False)
