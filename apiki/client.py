"""
API client for directly interacting with APIs.

This module provides a client for interacting with APIs
using the OpenAPI specification without needing the LangChain agent.
"""
import json
import logging
from typing import Any, Dict, Optional

import requests
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class APIClientConfig(BaseModel):
    """Configuration for the API Client."""

    openapi_url: str = Field(
        default="http://localhost:7272/openapi.json",
        description="The URL of the OpenAPI specification",
    )
    api_base_url: str = Field(
        default="http://localhost:7272", description="The base URL of the API"
    )
    headers: Dict[str, str] = Field(
        default_factory=dict, description="Headers to include in API requests"
    )
    timeout: int = Field(
        default=30, description="Timeout for API requests in seconds"
    )
    verify_ssl: bool = Field(
        default=True, description="Whether to verify SSL certificates"
    )
    verbose: bool = Field(
        default=True, description="Whether to enable verbose logging"
    )


class APIResponse(BaseModel):
    """Response from an API call."""

    status_code: int = Field(description="HTTP status code")
    success: bool = Field(description="Whether the request was successful")
    data: Optional[Any] = Field(
        default=None, description="Response data if successful"
    )
    error: Optional[str] = Field(
        default=None, description="Error message if unsuccessful"
    )
    headers: Dict[str, str] = Field(
        default_factory=dict, description="Response headers"
    )
    request_info: Dict[str, Any] = Field(
        default_factory=dict,
        description="Information about the request that was made",
    )


class APIClient:
    """Client for interacting with an API using its OpenAPI specification."""

    def __init__(self, config: APIClientConfig):
        """
        Initialize the API client.

        Args:
            config: Configuration for the API client
        """
        self.config = config
        self._setup_logging()
        self.spec_dict = self._fetch_openapi_spec()
        self.endpoints = self._parse_endpoints()

    def _setup_logging(self) -> None:
        """Configure logging for the client."""
        if self.config.verbose:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            )
        else:
            logging.basicConfig(level=logging.WARNING)

    def _fetch_openapi_spec(self) -> Dict[str, Any]:
        """
        Fetch the OpenAPI specification from the configured URL.

        Returns:
            The OpenAPI specification as a dictionary

        Raises:
            ValueError: If the OpenAPI specification could not be fetched
        """
        try:
            logger.info(
                f"Fetching OpenAPI spec from {self.config.openapi_url}"
            )
            response = requests.get(
                self.config.openapi_url,
                timeout=self.config.timeout,
                verify=self.config.verify_ssl,
            )
            response.raise_for_status()
            spec = response.json()
            logger.info("Successfully fetched OpenAPI spec")
            return spec
        except Exception as e:
            error_msg = f"Failed to fetch OpenAPI spec: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _parse_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """
        Parse all endpoints from the OpenAPI specification.

        Returns:
            A dictionary mapping endpoint paths to their details
        """
        endpoints = {}

        if "paths" not in self.spec_dict:
            return {}

        for path, methods in self.spec_dict["paths"].items():
            endpoints[path] = {}
            for method, details in methods.items():
                if method.lower() not in [
                    "get",
                    "post",
                    "put",
                    "delete",
                    "patch",
                ]:
                    continue

                endpoints[path][method.upper()] = {
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "parameters": details.get("parameters", []),
                    "requestBody": details.get("requestBody", {}),
                    "responses": details.get("responses", {}),
                }

        return endpoints

    def _get_base_url(self) -> str:
        """
        Get the base URL from the OpenAPI spec or config.

        Returns:
            The base URL for API requests
        """
        base_url = self.config.api_base_url
        if "servers" in self.spec_dict and self.spec_dict["servers"]:
            if "url" in self.spec_dict["servers"][0]:
                base_url = self.spec_dict["servers"][0]["url"]

        # Ensure the base URL doesn't end with a slash
        if base_url.endswith("/"):
            base_url = base_url[:-1]

        # Make sure the URL has a scheme
        if not base_url.startswith(("http://", "https://")):
            base_url = "https://" + base_url

        return base_url

    def _prepare_request_kwargs(
        self,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Prepare kwargs for requests.

        Args:
            params: Query parameters
            data: Request body data

        Returns:
            Dictionary of kwargs for requests
        """
        kwargs = {
            "timeout": self.config.timeout,
            "verify": self.config.verify_ssl,
            "headers": {"Content-Type": "application/json"},
        }

        kwargs["headers"].update(self.config.headers)

        if params:
            kwargs["params"] = params

        if data:
            kwargs["json"] = data

        return kwargs

    def _process_response(
        self, response: requests.Response, request_info: Dict[str, Any]
    ) -> APIResponse:
        """
        Process a response from the API.

        Args:
            response: Response from requests
            request_info: Information about the request

        Returns:
            Processed API response
        """
        try:
            data = response.json() if response.content else None
        except json.JSONDecodeError:
            data = response.text if response.content else None

        headers = {k: v for k, v in response.headers.items()}

        return APIResponse(
            status_code=response.status_code,
            success=response.status_code < 400,
            data=data,
            error=None if response.status_code < 400 else str(data),
            headers=headers,
            request_info=request_info,
        )

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make a GET request to the API.

        Args:
            path: Path to request
            params: Query parameters

        Returns:
            API response
        """
        base_url = self._get_base_url()

        # Ensure path starts with a slash
        if not path.startswith("/"):
            path = "/" + path

        # Construct the full URL - avoid duplicate path parts
        url = base_url + path

        request_info = {"method": "GET", "url": url, "params": params}

        logger.info(f"Making GET request to {url}")

        try:
            kwargs = self._prepare_request_kwargs(params=params)
            response = requests.get(url, **kwargs)
            return self._process_response(response, request_info)
        except Exception as e:
            logger.error(f"Error making GET request: {e}")
            return APIResponse(
                status_code=500,
                success=False,
                error=str(e),
                request_info=request_info,
            )

    def post(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> APIResponse:
        """
        Make a POST request to the API.

        Args:
            path: Path to request
            data: Request body data
            params: Query parameters

        Returns:
            API response
        """
        base_url = self._get_base_url()

        # Ensure path starts with a slash
        if not path.startswith("/"):
            path = "/" + path

        # Construct the full URL - avoid duplicate path parts
        url = base_url + path

        request_info = {
            "method": "POST",
            "url": url,
            "params": params,
            "data": data,
        }

        logger.info(f"Making POST request to {url}")

        try:
            kwargs = self._prepare_request_kwargs(params=params, data=data)
            response = requests.post(url, **kwargs)
            return self._process_response(response, request_info)
        except Exception as e:
            logger.error(f"Error making POST request: {e}")
            return APIResponse(
                status_code=500,
                success=False,
                error=str(e),
                request_info=request_info,
            )

    def put(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> APIResponse:
        """
        Make a PUT request to the API.

        Args:
            path: Path to request
            data: Request body data
            params: Query parameters

        Returns:
            API response
        """
        base_url = self._get_base_url()

        # Ensure path starts with a slash
        if not path.startswith("/"):
            path = "/" + path

        # Construct the full URL - avoid duplicate path parts
        url = base_url + path

        request_info = {
            "method": "PUT",
            "url": url,
            "params": params,
            "data": data,
        }

        logger.info(f"Making PUT request to {url}")

        try:
            kwargs = self._prepare_request_kwargs(params=params, data=data)
            response = requests.put(url, **kwargs)
            return self._process_response(response, request_info)
        except Exception as e:
            logger.error(f"Error making PUT request: {e}")
            return APIResponse(
                status_code=500,
                success=False,
                error=str(e),
                request_info=request_info,
            )

    def delete(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> APIResponse:
        """
        Make a DELETE request to the API.

        Args:
            path: Path to request
            params: Query parameters

        Returns:
            API response
        """
        base_url = self._get_base_url()

        # Ensure path starts with a slash
        if not path.startswith("/"):
            path = "/" + path

        # Construct the full URL - avoid duplicate path parts
        url = base_url + path

        request_info = {"method": "DELETE", "url": url, "params": params}

        logger.info(f"Making DELETE request to {url}")

        try:
            kwargs = self._prepare_request_kwargs(params=params)
            response = requests.delete(url, **kwargs)
            return self._process_response(response, request_info)
        except Exception as e:
            logger.error(f"Error making DELETE request: {e}")
            return APIResponse(
                status_code=500,
                success=False,
                error=str(e),
                request_info=request_info,
            )

    def patch(
        self,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> APIResponse:
        """
        Make a PATCH request to the API.

        Args:
            path: Path to request
            data: Request body data
            params: Query parameters

        Returns:
            API response
        """
        base_url = self._get_base_url()

        # Ensure path starts with a slash
        if not path.startswith("/"):
            path = "/" + path

        # Construct the full URL - avoid duplicate path parts
        url = base_url + path

        request_info = {
            "method": "PATCH",
            "url": url,
            "params": params,
            "data": data,
        }

        logger.info(f"Making PATCH request to {url}")

        try:
            kwargs = self._prepare_request_kwargs(params=params, data=data)
            response = requests.patch(url, **kwargs)
            return self._process_response(response, request_info)
        except Exception as e:
            logger.error(f"Error making PATCH request: {e}")
            return APIResponse(
                status_code=500,
                success=False,
                error=str(e),
                request_info=request_info,
            )

    def get_available_endpoints(self) -> Dict[str, Dict[str, Any]]:
        """
        Get a dictionary of all available endpoints.

        Returns:
            Dictionary of all endpoints
        """
        return self.endpoints

    def get_endpoint_details(self, path: str, method: str) -> Dict[str, Any]:
        """
        Get details about a specific endpoint.

        Args:
            path: Endpoint path
            method: HTTP method (GET, POST, etc.)

        Returns:
            Endpoint details

        Raises:
            ValueError: If the endpoint doesn't exist
        """
        method = method.upper()

        if path not in self.endpoints:
            raise ValueError(f"Path '{path}' not found in API specification")

        if method not in self.endpoints[path]:
            error_msg = (
                f"Method '{method}' not found for path '{path}' "
                f"in API specification"
            )
            raise ValueError(error_msg)

        return self.endpoints[path][method]
