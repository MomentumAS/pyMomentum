from setuptools import setup

setup(name='pyMomentum',
      version='0.1',
      description='Python libraries developed by Momentum',
      url='https://github.com/MomentumAS/pyMomentum',
      author='Momentum Teknoloji AS',
      author_email='info@mtas.com.tr',
      license='MIT',
      packages=['pyMomentum'],
      install_requires=[
          'requests',
      ],
      zip_safe=False
      )
