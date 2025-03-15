"""
Command-line interface for the APIKI package.

This module provides a command-line interface for interacting with APIs
using the APIKI package's agent-based approach or direct client.
"""
import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from apiki.agent import AgentResponse, APIAgent, APIAgentConfig
from apiki.client import APIClient, APIClientConfig, APIResponse


def setup_argparse() -> argparse.ArgumentParser:
    """Set up the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="APIKI - API Knowledge Integration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--openapi",
        default="http://localhost:7272/openapi.json",
        help="URL to the OpenAPI specification (default: %(default)s)",
    )

    parser.add_argument(
        "--base-url",
        default="http://localhost:7272",
        help="Base URL for the API (default: %(default)s)",
    )

    parser.add_argument(
        "--api-key",
        help="OpenAI API key (can also be set via OPENAI_API_KEY env var)",
    )

    parser.add_argument(
        "--model",
        default="gpt-3.5-turbo",
        help="OpenAI model to use (default: %(default)s)",
    )

    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Temperature for the model (default: %(default)s)",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="Timeout for API requests in seconds (default: %(default)s)",
    )

    parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )

    # Create subparsers for different modes
    subparsers = parser.add_subparsers(dest="mode", help="Mode of operation")

    # Agent mode
    agent_parser = subparsers.add_parser(
        "agent", help="Use the API agent to interact with the API"
    )
    agent_parser.add_argument(
        "query", help="Natural language query to send to the agent"
    )

    # Client mode with subcommands for HTTP methods
    client_parser = subparsers.add_parser(
        "client", help="Use the API client to interact with the API directly"
    )
    client_subparsers = client_parser.add_subparsers(
        dest="method", help="HTTP method to use", required=True
    )

    # GET method
    get_parser = client_subparsers.add_parser("get", help="Make a GET request")
    get_parser.add_argument("path", help="Path to request")
    get_parser.add_argument("--params", help="Query parameters as JSON string")

    # POST method
    post_parser = client_subparsers.add_parser(
        "post", help="Make a POST request"
    )
    post_parser.add_argument("path", help="Path to request")
    post_parser.add_argument("--data", help="Request body as JSON string")
    post_parser.add_argument(
        "--params", help="Query parameters as JSON string"
    )

    # PUT method
    put_parser = client_subparsers.add_parser("put", help="Make a PUT request")
    put_parser.add_argument("path", help="Path to request")
    put_parser.add_argument("--data", help="Request body as JSON string")
    put_parser.add_argument("--params", help="Query parameters as JSON string")

    # DELETE method
    delete_parser = client_subparsers.add_parser(
        "delete", help="Make a DELETE request"
    )
    delete_parser.add_argument("path", help="Path to request")
    delete_parser.add_argument(
        "--params", help="Query parameters as JSON string"
    )

    # PATCH method
    patch_parser = client_subparsers.add_parser(
        "patch", help="Make a PATCH request"
    )
    patch_parser.add_argument("path", help="Path to request")
    patch_parser.add_argument("--data", help="Request body as JSON string")
    patch_parser.add_argument(
        "--params", help="Query parameters as JSON string"
    )

    # Endpoints info
    client_subparsers.add_parser(
        "endpoints", help="Get information about available endpoints"
    )

    return parser


def parse_json_arg(arg: Optional[str]) -> Optional[Dict[str, Any]]:
    """
    Parse a JSON string argument.

    Args:
        arg: JSON string argument

    Returns:
        Parsed JSON object or None
    """
    if not arg:
        return None

    try:
        return json.loads(arg)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)


def format_response(response: Any) -> None:
    """
    Format and print a response.

    Args:
        response: Response to format and print
    """
    if isinstance(response, dict):
        print(json.dumps(response, indent=2))
    elif isinstance(response, (APIResponse, AgentResponse)):
        if hasattr(response, "status_code"):
            print(f"Status Code: {response.status_code}")

        if hasattr(response, "success"):
            print(f"Success: {response.success}")

        if hasattr(response, "output") and response.output:
            print(f"\nOutput:\n{response.output}")

        if hasattr(response, "data") and response.data:
            print("\nData:")
            print(json.dumps(response.data, indent=2))

        if hasattr(response, "error") and response.error:
            print(f"\nError: {response.error}")
    else:
        print(response)


def run_agent_mode(args: argparse.Namespace) -> None:
    """
    Run in agent mode.

    Args:
        args: Command-line arguments
    """
    config = APIAgentConfig(
        openapi_url=args.openapi,
        api_base_url=args.base_url,
        api_key=args.api_key,
        model_name=args.model,
        temperature=args.temperature,
        timeout=args.timeout,
        verbose=args.verbose,
    )

    agent = APIAgent(config)
    response = agent.run(args.query)
    format_response(response)


def run_client_mode(args: argparse.Namespace) -> None:
    """
    Run in client mode.

    Args:
        args: Command-line arguments
    """
    config = APIClientConfig(
        openapi_url=args.openapi,
        api_base_url=args.base_url,
        timeout=args.timeout,
        verbose=args.verbose,
    )

    client = APIClient(config)

    if args.method == "endpoints":
        endpoints = client.get_available_endpoints()
        format_response(endpoints)
        return

    params = parse_json_arg(getattr(args, "params", None))
    data = parse_json_arg(getattr(args, "data", None))

    if args.method == "get":
        response = client.get(args.path, params=params)
    elif args.method == "post":
        response = client.post(args.path, data=data, params=params)
    elif args.method == "put":
        response = client.put(args.path, data=data, params=params)
    elif args.method == "delete":
        response = client.delete(args.path, params=params)
    elif args.method == "patch":
        response = client.patch(args.path, data=data, params=params)
    else:
        print(f"Unknown method: {args.method}")
        sys.exit(1)

    format_response(response)


def main() -> None:
    """Main entry point for the CLI."""
    load_dotenv()  # Load environment variables from .env file

    parser = setup_argparse()
    args = parser.parse_args()

    # If no mode is specified, print help
    if not args.mode:
        parser.print_help()
        sys.exit(1)

    # Use environment variable for API key if not provided in args
    if not args.api_key and os.environ.get("OPENAI_API_KEY"):
        args.api_key = os.environ.get("OPENAI_API_KEY")

    # Run in the appropriate mode
    if args.mode == "agent":
        if not args.api_key:
            print("Error: OpenAI API key is required for agent mode")
            print("       Set it with --api-key or OPENAI_API_KEY env var")
            sys.exit(1)
        run_agent_mode(args)
    elif args.mode == "client":
        run_client_mode(args)


if __name__ == "__main__":
    main()
