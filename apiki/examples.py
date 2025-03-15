"""
Examples of using the APIKI package.

This module provides examples of how to use the APIKI package
for interacting with APIs using LangChain agents.
"""
import os
import sys
from typing import Dict

from dotenv import load_dotenv

from apiki.client import APIClient, APIClientConfig


def agent_example() -> None:
    """Example of using the API agent."""
    print("\n" + "=" * 80)
    print("  API AGENT EXAMPLE")
    print("-" * 80)

    # Load environment variables from .env file
    load_dotenv()

    # Get OpenAI API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set it in a .env file or in your environment.")
        sys.exit(1)

    # Example OpenAPI specification URL
    openapi_url = "http://localhost:7272/openapi.json"
    base_url = "http://localhost:7272"

    # Create agent configuration
    # Note: We're not using the agent due to compatibility issues
    print(
        "Note: Using API client directly instead of agent "
        "due to compatibility issues"
    )
    client_config = APIClientConfig(
        openapi_url=openapi_url, api_base_url=base_url, verbose=True
    )
    client = APIClient(client_config)

    try:
        # Get available endpoints
        endpoints = client.get_available_endpoints()
        print("\nAvailable endpoints:")
        for path, methods in endpoints.items():
            for method, details in methods.items():
                summary = details.get("summary", "")
                print(f"  {method} {path} - {summary}")

        # Example: Get health status
        print("\nExample: Get health status")
        response = client.get("/v3/health")
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"Health data: {response.data}")
        else:
            print(f"Error: {response.error}")

        # Example: Get system status
        print("\nExample: Get system status")
        response = client.get("/v3/system/status")
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"System status: {response.data}")
        else:
            print(f"Error: {response.error}")

    except Exception as e:
        print(f"Error: {e}")


def client_example() -> None:
    """Example of using the API client directly."""
    print("\n" + "=" * 80)
    print("  API CLIENT EXAMPLE")
    print("-" * 80)

    # Example OpenAPI specification URL
    openapi_url = "http://localhost:7272/openapi.json"
    base_url = "http://localhost:7272"

    # Create client configuration
    config = APIClientConfig(
        openapi_url=openapi_url, api_base_url=base_url, verbose=True
    )

    # Create the client
    try:
        client = APIClient(config)

        # Get available endpoints
        endpoints = client.get_available_endpoints()
        print("\nAvailable endpoints:")
        for path, methods in endpoints.items():
            for method, details in methods.items():
                summary = details.get("summary", "")
                print(f"  {method} {path} - {summary}")

        # Example: Get health status
        print("\nExample: Get health status")
        response = client.get("/v3/health")
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"Health data: {response.data}")
        else:
            print(f"Error: {response.error}")

        # Example: Get system status
        print("\nExample: Get system status")
        response = client.get("/v3/system/status")
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"System status: {response.data}")
        else:
            print(f"Error: {response.error}")

        # Example: List available prompts
        print("\nExample: List available prompts")
        response = client.get("/v3/prompts")
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"Prompts: {response.data}")
        else:
            print(f"Error: {response.error}")

        # Example: Search for documents
        print("\nExample: Search for documents")
        search_data: Dict = {"query": "example search", "search_mode": "basic"}
        response = client.post("/v3/retrieval/search", data=search_data)
        print(f"Status: {response.status_code}")
        print(f"Success: {response.success}")
        if response.success:
            print(f"Search results: {response.data}")
        else:
            print(f"Error: {response.error}")

    except Exception as e:
        print(f"Error: {e}")


def main() -> None:
    """Run all examples."""
    agent_example()
    client_example()


if __name__ == "__main__":
    main()
