"""
A basic data storage object, must be instantiated on a plugins __init__ method with the name
"""


class PluginConfiguration:

    def __init__(self,
                 plugin_name="My sql-fusion Plugin",
                 plugin_version="0.1.0",
                 plugin_short_description="My very cool sql-fusion plugin!"):
        self.plugin_name = plugin_name
        self.plugin_version = plugin_version
        self.plugin_short_description = plugin_short_description

