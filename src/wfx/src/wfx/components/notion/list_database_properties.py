import requests
from langchain.tools import StructuredTool
from pydantic import BaseModel, Field
from wfx.base.langchain_utilities.model import LCToolComponent
from wfx.field_typing import Tool
from wfx.inputs.inputs import SecretStrInput, StrInput
from wfx.log.logger import logger
from wfx.schema.data import Data


class notionDatabaseProperties(LCToolComponent):
    display_name: str = "List Database Properties "
    description: str = "Retrieve properties of a notion database."
    documentation: str = "https://docs.agent.khulnasoft.com/bundles-notion"
    icon = "notionDirectoryLoader"

    inputs = [
        StrInput(
            name="database_id",
            display_name="Database ID",
            info="The ID of the notion database.",
        ),
        SecretStrInput(
            name="notion_secret",
            display_name="notion Secret",
            info="The notion integration token.",
            required=True,
        ),
    ]

    class notionDatabasePropertiesSchema(BaseModel):
        database_id: str = Field(..., description="The ID of the notion database.")

    def run_model(self) -> Data:
        result = self._fetch_database_properties(self.database_id)
        if isinstance(result, str):
            # An error occurred, return it as text
            return Data(text=result)
        # Success, return the properties
        return Data(text=str(result), data=result)

    def build_tool(self) -> Tool:
        return StructuredTool.from_function(
            name="notion_database_properties",
            description="Retrieve properties of a notion database. Input should include the database ID.",
            func=self._fetch_database_properties,
            args_schema=self.notionDatabasePropertiesSchema,
        )

    def _fetch_database_properties(self, database_id: str) -> dict | str:
        url = f"https://api.notion.com/v1/databases/{database_id}"
        headers = {
            "Authorization": f"Bearer {self.notion_secret}",
            "notion-Version": "2022-06-28",  # Use the latest supported version
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("properties", {})
        except requests.exceptions.RequestException as e:
            return f"Error fetching notion database properties: {e}"
        except ValueError as e:
            return f"Error parsing notion API response: {e}"
        except Exception as e:  # noqa: BLE001
            logger.debug("Error fetching notion database properties", exc_info=True)
            return f"An unexpected error occurred: {e}"
