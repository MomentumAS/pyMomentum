from setuptools import setup

setup(name='pyMomentum',
      packages=['pyMomentum','pyMomentum.sms','pyMomentum.sms.providers'],
      version='0.1.2',
      description='Python libraries developed by Momentum',
      url='https://github.com/MomentumAS/pyMomentum',
      keywords=['momentum', 'library', 'sms'],
      author='Momentum Teknoloji AS',
      author_email='info@mtas.com.tr',
      license='MIT',
      install_requires=[
          'requests',
      ],
      zip_safe=False
      )
