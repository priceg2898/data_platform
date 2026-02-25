poetry -C docker/container__scripts run -- black ../../scripts
poetry -C docker/container__scripts run -- ruff check ../../scripts --fix