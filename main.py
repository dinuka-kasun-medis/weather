from logging_config import configure_logging
from tools.weather_tools import mcp
import logging


def main() -> None:

    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Weather MCP Server")
    mcp.run(
        transport="stdio"
    )


if __name__ == "__main__":
    main()