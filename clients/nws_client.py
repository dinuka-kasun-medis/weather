import logging
from typing import Any

import httpx

from config import settings

logger = logging.getLogger(__name__)


class NWSClient:
    def __init__(self) -> None:
        self._headers = {
            "User-Agent": settings.user_agent,
            "Accept": "application/geo+json",
        }

    async def get_json(
        self,
        url: str,
    ) -> dict[str, Any] | None:

        try:
            async with httpx.AsyncClient(
                timeout=settings.timeout_seconds
            ) as client:

                response = await client.get(
                    url,
                    headers=self._headers,
                )

                response.raise_for_status()

                logger.info(
                    "NWS request successful: %s",
                    url,
                )

                return response.json()

        except httpx.TimeoutException:
            logger.warning(
                "NWS timeout: %s",
                url,
            )

        except httpx.HTTPStatusError as ex:
            logger.error(
                "NWS returned %s for %s",
                ex.response.status_code,
                url,
            )

        except httpx.HTTPError as ex:
            logger.exception(
                "HTTP error calling NWS: %s",
                ex,
            )

        return None