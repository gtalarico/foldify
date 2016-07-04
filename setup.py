from distutils.core import setup
setup(
  name = 'foldify',
  packages = ['foldify'], # this must be the same as the name above
  scripts=['foldify/foldify'],
  version = '0.3.3',
  description = 'Python CLI tools to help manage directory trees and templates',
  author = 'Gui Talarico',
  author_email = 'gtalarico@gmail.com',
  url = 'https://github.com/gtalarico/foldify', # use the URL to the github repo
  license = 'MIT',
  download_url = 'https://github.com/gtalarico/foldify/archive/0.3.3.tar.gz', # I'll explain this in a second
  keywords = ['folders', 'directories'], # arbitrary keywords
  classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        # 'Programming Language :: Python :: 2.6',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
