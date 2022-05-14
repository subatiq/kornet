from distutils.core import setup
setup(
  name = 'chieftane',
  packages = ['chieftane'],
  version = 'pre-0.0.0',
  license='MIT',
  description = 'A library for mass execution of ssh commands on remote machines fleet.',
  author = 'Vladimir Semenov',
  author_email = 'subatiq@gmail.com',
  url = 'https://github.com/subatiq/chieftane',
  download_url = 'https://github.com/subatiq/chieftane/archive/refs/tags/pre-0.0.0.tar.gz',    # I explain this later on
  keywords = ['SSH', 'AUTOMATION', 'ORCHESTRATION'],
  install_requires=[
        'paramiko',
        'pydantic',
        'pyyaml',
        'loguru',
        'typer',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Automation',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.8',
  ],
)