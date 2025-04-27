from os import getenv
from typing import List

from fastmcp import Client

from src.client.llm_integration import sampling_handler
from src.models.vehicle_model import VehicleModel
from src.server.mcp_server import mcp as mcp_server
from src.server.process_request import execute_raw_sql


OLLAMA_MODEL = getenv("OLLAMA_MODEL")


class MCPOpenAIClient:
    def __init__(self, model: str = OLLAMA_MODEL):
        """Initialize the OpenAI MCP client.

        Args:
            model: The OpenAI model to use.
        """
        self.client = None
        self.model = model

    async def start_session(self):
        self.client = await self.client_session()
        return self

    @classmethod
    async def client_session(cls) -> Client:
        """Create and return a client session."""
        client = await Client(
            mcp_server, sampling_handler=sampling_handler
        ).__aenter__()
        return client

    async def close(self):
        """Close the client session."""
        if self.client:
            await self.client.__aexit__(None, None, None)
            self.client = None

    async def process_query(self, query: str) -> List[VehicleModel]:
        """Process a query using Ollama and available MCP tools.

        Args:
            query: The user query.

        Returns:
            List of vehicle models.
        """

        # Generate a Json with keys is a filter to search car
        json_car_filters = await self.client.call_tool(
            "generate_json", {"user_input": f"{query}"}
        )

        # Generate a SELECT query based on json_car_filters
        raw_query = await self.client.call_tool(
            "generate_sql_select", {"json_car_filters": f"{json_car_filters[0].text}"}
        )

        response = execute_raw_sql(raw_query[0].text)

        return response
