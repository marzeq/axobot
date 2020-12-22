admin_command_descriptions = \
    {
        "admin_help": {
            "args": {
                "command": {
                    "required": False
                }
            },
            "desc": "Shows all admin commands and their respective arguments, aliases and its description. If a command name is passed, it will show help about the specified admin command",
            "aliases": ["adminhelp", "admhelp"]
        },
        "load": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Loads all cogs avalible. If an extension (cog) is provided, it will load only the specified cog.",
            "aliases": ["l"]
        },
        "unload": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Unoads all cogs avalible. If an extension (cog) is provided, it will unload only the specified cog.",
            "aliases": ["ul"]
        },
        "reload": {
            "args": {
                "extension": {
                    "required": False
                }
            },
            "desc": "Reoads all cogs avalible. If an extension (cog) is provided, it will reload only the specified cog.",
            "aliases": ["rl"]
        },
        "update": {
            "args": {},
            "desc": "Pulls from the Github repo and reruns the program",
            "aliases": ["up"]
        },
        "hardreload": {
            "args": {},
            "desc": "Reruns the program",
            "aliases": ["hr"]
        },
        "pull_reload": {
            "args": {},
            "desc": "Pulls from the Github repo and reloads all extensions",
            "aliases": ["prl"]
        },
        "up_discordpy": {
            "args": {},
            "desc": "Pulls from the Github repo for discord.py and updates it.",
            "aliases": ["udpy"]
        },
        "presence": {
            "args": {
                "type": {"required": True},
                "presence": {"required": True}
            },
            "desc": "Changes the bot presence. Set type 0 for watching, 1 for listening, 2 for playing and 3 to reset.",
            "aliases": []
        }
    }
