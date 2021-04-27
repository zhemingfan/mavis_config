from setuptools import find_packages, setup

TEST_REQS = [
    'coverage>=4.2',
    'pycodestyle>=2.3.1',
    'pytest',
    'pytest-cov',
]


DOC_REQS = [
    'mkdocs==1.1.2',
    'markdown_refdocs',
    'mkdocs-material==5.4.0',
    'markdown-include',
    'mkdocs-simple-hooks==0.1.2',
]


DEPLOY_REQS = ['twine', 'm2r', 'wheel']

VERSION = '1.0.0'

setup(
    name='mavis_config',
    version='{}'.format(VERSION),
    url='https://github.com/bcgsc/mavis_config.git',
    download_url='https://github.com/bcgsc/mavis_config/archive/v{}.tar.gz'.format(VERSION),
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    description='Config validation for running MAVIS via Snakemake',
    install_requires=['snakemake>=6.1.1, <7', 'braceexpand'],
    extras_require={
        'docs': DOC_REQS,
        'test': TEST_REQS,
        'dev': ['black==20.8b1', 'flake8'] + DOC_REQS + TEST_REQS + DEPLOY_REQS,
        'deploy': DEPLOY_REQS,
    },
    tests_require=TEST_REQS,
    setup_requires=['pip>=9.0.0', 'setuptools>=36.0.0'],
    python_requires='>=3.6',
    author='Caralyn Reisle',
    author_email='creisle@bcgsc.ca',
    test_suite='tests',
    include_package_data=True,
    data_files=[
        ('mavis_config', ['src/mavis_config/config.json', 'src/mavis_config/overlay.json'])
    ],
    project_urls={'mavis_config': 'http://mavis.bcgsc.ca'},
)