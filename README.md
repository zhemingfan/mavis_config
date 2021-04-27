# MAVIS Config

[![build](https://github.com/bcgsc/mavis_config/actions/workflows/build.yml/badge.svg?branch=master)](https://github.com/bcgsc/mavis_config/actions/workflows/build.yml) [![codecov](https://codecov.io/gh/bcgsc/mavis_config/branch/master/graph/badge.svg)](https://codecov.io/gh/bcgsc/mavis_config) ![PyPi](https://img.shields.io/pypi/v/mavis_config.svg)

Workflow configuration validation for [MAVIS](https://github.com/bcgsc/mavis) via snakemake.

This is a separate package from [MAVIS](https://github.com/bcgsc/mavis)
itself to allow for [MAVIS](https://github.com/bcgsc/mavis) uses running snakemake with the
docker container to install this to check their snakemake config JSON without requiring all
of the other [MAVIS](https://github.com/bcgsc/mavis) dependencies since they will be encapsulated
in the docker image
