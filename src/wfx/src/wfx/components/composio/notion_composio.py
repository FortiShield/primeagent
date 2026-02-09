from wfx.base.composio.composio_base import ComposioBaseComponent


class ComposionotionAPIComponent(ComposioBaseComponent):
    display_name: str = "notion"
    icon = "notion"
    documentation: str = "https://docs.composio.dev"
    app_name = "notion"

    def set_default_tools(self):
        """Set the default tools for notion component."""
