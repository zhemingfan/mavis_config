# MAVIS Config

[![build](https://github.com/bcgsc/mavis_config/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/bcgsc/mavis_config/actions/workflows/build.yml) [![codecov](https://codecov.io/gh/bcgsc/mavis_config/branch/master/graph/badge.svg)](https://codecov.io/gh/bcgsc/mavis_config) ![PyPi](https://img.shields.io/pypi/v/mavis_config.svg)

Workflow configuration validation for [MAVIS](https://github.com/bcgsc/mavis) via snakemake. This package should not be used without [MAVIS](https://github.com/bcgsc/mavis). If you are a [MAVIS](https://github.com/bcgsc/mavis) user, please see [MAVIS](https://github.com/bcgsc/mavis) instead.

## For Developers

This is a separate package from [MAVIS](https://github.com/bcgsc/mavis)
itself so that [MAVIS](https://github.com/bcgsc/mavis) users running snakemake with the
docker container do not need to install [MAVIS](https://github.com/bcgsc/mavis) to check their snakemake config JSON.
This is to ensure that all the hard-to-install [MAVIS](https://github.com/bcgsc/mavis) dependencies are not required to run 
snakemake with docker.
