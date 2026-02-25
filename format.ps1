$SCRIPT_PATH = "../../scripts"

poetry -C docker/container__scripts run -- black $SCRIPT_PATH

poetry -C docker/container__scripts run -- ruff check $SCRIPT_PATH --fix