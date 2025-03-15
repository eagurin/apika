"""
LangChain agent for API interaction.

This module provides a LangChain agent that can interact with any API
using its OpenAPI specification.
"""
import json
import logging
from typing import Any, Dict, List, Optional

import requests
from langchain_community.agent_toolkits.openapi.base import (
    create_openapi_agent,
)
from langchain_community.agent_toolkits.openapi.toolkit import OpenAPIToolkit
from langchain_community.tools.json.tool import JsonSpec
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI, OpenAI
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class APIAgentConfig(BaseModel):
    """Configuration for the API Agent."""

    openapi_url: str = Field(
        default="http://localhost:7272/openapi.json",
        description="The URL of the OpenAPI specification",
    )
    api_base_url: str = Field(
        default="http://localhost:7272", description="The base URL of the API"
    )
    model_name: str = Field(
        default="gpt-3.5-turbo",
        description="The name of the OpenAI model to use",
    )
    temperature: float = Field(
        default=0.0,
        description="The temperature for the model, 0.0 means deterministic",
    )
    api_key: Optional[str] = Field(
        default=None,
        description="OpenAI API key (if None, will use environment variable)",
    )
    headers: Dict[str, str] = Field(
        default_factory=dict, description="Headers to include in API requests"
    )
    allow_dangerous_requests: bool = Field(
        default=True,
        description="Whether to allow potentially dangerous API requests",
    )
    use_chat_model: bool = Field(
        default=True, description="Whether to use ChatOpenAI instead of OpenAI"
    )
    timeout: int = Field(
        default=30, description="Timeout for API requests in seconds"
    )
    max_token_limit: int = Field(
        default=4000,
        description="Maximum number of tokens to use in the JsonSpec",
    )
    verbose: bool = Field(
        default=True, description="Whether to enable verbose logging"
    )


class AgentResponse(BaseModel):
    """Response from the API agent."""

    output: str = Field(description="The output text from the agent")
    intermediate_steps: Optional[List[Any]] = Field(
        default=None, description="The intermediate steps taken by the agent"
    )
    raw_response: Optional[Dict[str, Any]] = Field(
        default=None, description="The raw response from the agent"
    )


class APIAgent:
    """Agent for interacting with an API using its OpenAPI specification."""

    def __init__(self, config: APIAgentConfig):
        """
        Initialize the API agent.

        Args:
            config: Configuration for the API agent
        """
        self.config = config
        self._setup_logging()

        # Initialize the language model
        if config.use_chat_model:
            self.llm = ChatOpenAI(
                model_name=config.model_name,
                temperature=config.temperature,
                api_key=config.api_key,
                verbose=config.verbose,
            )
        else:
            self.llm = OpenAI(
                model_name=config.model_name,
                temperature=config.temperature,
                api_key=config.api_key,
                verbose=config.verbose,
            )

        # Setup agent components
        self.spec_dict = self._fetch_openapi_spec()
        self.json_spec = JsonSpec(
            dict_=self.spec_dict, max_value_length=config.max_token_limit
        )
        self.requests_wrapper = self._create_requests_wrapper()

        # For older versions of langchain, we need to use a different approach
        try:
            # Try the newer approach first
            self.toolkit = OpenAPIToolkit.from_llm(
                self.llm,
                self.json_spec,
                self.requests_wrapper,
                verbose=config.verbose,
            )
            self.agent_executor = create_openapi_agent(
                llm=self.llm,
                toolkit=self.toolkit,
                allow_dangerous_requests=config.allow_dangerous_requests,
                verbose=config.verbose,
            )
        except (TypeError, ValueError) as e:
            logger.warning(f"Using fallback agent creation method due to: {e}")
            # Fallback to direct toolkit creation for compatibility
            from langchain.agents import AgentExecutor
            from langchain.agents.agent_toolkits.openapi import (
                base as openapi_base,
            )

            self.toolkit = OpenAPIToolkit(
                spec=self.json_spec, requests_wrapper=self.requests_wrapper
            )
            self.agent_executor = AgentExecutor.from_agent_and_tools(
                agent=openapi_base.create_openapi_agent(
                    llm=self.llm, toolkit=self.toolkit, verbose=config.verbose
                ),
                tools=self.toolkit.get_tools(),
                verbose=config.verbose,
            )

    def _setup_logging(self) -> None:
        """Configure logging for the agent."""
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
                self.config.openapi_url, timeout=self.config.timeout
            )
            response.raise_for_status()
            spec = response.json()
            logger.info(
                f"Successfully fetched OpenAPI spec with {len(spec)} keys"
            )
            return spec
        except Exception as e:
            error_msg = f"Failed to fetch OpenAPI spec: {e}"
            logger.error(error_msg)
            raise ValueError(error_msg)

    def _create_requests_wrapper(self) -> Dict[str, Any]:
        """
        Create a requests wrapper for the API.

        Returns:
            A dictionary with functions for interacting with the API
        """
        headers = {"Content-Type": "application/json"}
        headers.update(self.config.headers)

        # Use base URL from spec if available, otherwise use the configured one
        base_url = self.config.api_base_url
        if "servers" in self.spec_dict and self.spec_dict["servers"]:
            if "url" in self.spec_dict["servers"][0]:
                base_url = self.spec_dict["servers"][0]["url"]

        logger.info(f"Using base URL: {base_url}")

        def _get(path: str, **kwargs):
            """Make a GET request to the API."""
            full_url = f"{base_url}{path}"
            logger.info(f"Making GET request to {full_url}")
            return requests.get(
                full_url,
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )

        def _post(path: str, **kwargs):
            """Make a POST request to the API."""
            full_url = f"{base_url}{path}"
            logger.info(f"Making POST request to {full_url}")
            if "json" in kwargs and isinstance(kwargs["json"], str):
                try:
                    kwargs["json"] = json.loads(kwargs["json"])
                except json.JSONDecodeError:
                    pass
            return requests.post(
                full_url,
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )

        def _put(path: str, **kwargs):
            """Make a PUT request to the API."""
            full_url = f"{base_url}{path}"
            logger.info(f"Making PUT request to {full_url}")
            if "json" in kwargs and isinstance(kwargs["json"], str):
                try:
                    kwargs["json"] = json.loads(kwargs["json"])
                except json.JSONDecodeError:
                    pass
            return requests.put(
                full_url,
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )

        def _delete(path: str, **kwargs):
            """Make a DELETE request to the API."""
            full_url = f"{base_url}{path}"
            logger.info(f"Making DELETE request to {full_url}")
            return requests.delete(
                full_url,
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )

        def _patch(path: str, **kwargs):
            """Make a PATCH request to the API."""
            full_url = f"{base_url}{path}"
            logger.info(f"Making PATCH request to {full_url}")
            if "json" in kwargs and isinstance(kwargs["json"], str):
                try:
                    kwargs["json"] = json.loads(kwargs["json"])
                except json.JSONDecodeError:
                    pass
            return requests.patch(
                full_url,
                headers=headers,
                timeout=self.config.timeout,
                **kwargs,
            )

        return {
            "get": _get,
            "post": _post,
            "put": _put,
            "delete": _delete,
            "patch": _patch,
        }

    def run(self, query: str, **kwargs) -> AgentResponse:
        """
        Run the agent with the given query.

        Args:
            query: The task for the agent to perform
            **kwargs: Additional arguments to pass to the agent

        Returns:
            The result of running the agent
        """
        logger.info(f"Running agent with query: {query}")
        config = RunnableConfig(callbacks=kwargs.pop("callbacks", None))

        try:
            result = self.agent_executor.invoke(
                {"input": query}, config=config
            )
            logger.info("Agent run completed successfully")

            return AgentResponse(
                output=result.get("output", ""),
                intermediate_steps=result.get("intermediate_steps"),
                raw_response=result,
            )
        except Exception as e:
            error_msg = f"Error running agent: {e}"
            logger.error(error_msg)
            return AgentResponse(
                output=f"Error: {str(e)}",
                intermediate_steps=None,
                raw_response={"error": str(e)},
            )

    def get_available_endpoints(self) -> Dict[str, Any]:
        """
        Get a list of available endpoints from the API specification.

        Returns:
            A dictionary of available endpoints grouped by HTTP method
        """
        endpoints = {}

        if "paths" not in self.spec_dict:
            return {}

        for path, methods in self.spec_dict["paths"].items():
            for method, details in methods.items():
                if method.lower() not in [
                    "get",
                    "post",
                    "put",
                    "delete",
                    "patch",
                ]:
                    continue

                if method.upper() not in endpoints:
                    endpoints[method.upper()] = []

                endpoint_info = {
                    "path": path,
                    "summary": details.get("summary", ""),
                    "description": details.get("description", ""),
                    "parameters": details.get("parameters", []),
                    "requestBody": details.get("requestBody", {}),
                }

                endpoints[method.upper()].append(endpoint_info)

        return endpoints
