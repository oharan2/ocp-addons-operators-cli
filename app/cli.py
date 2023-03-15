import sys

import click
from addon_cmds import commands as addon
from operator_cmds import commands as operator


@click.group()
def entry_point():
    # Entrypoint for all click groups (Addons and Operators)
    pass


if __name__ == "__main__":
    entry_point.add_command(addon.addon)
    entry_point.add_command(operator.operator)
    print(f"Click Version: {click.__version__}")
    print(f"Python Version: {sys.version}")
    _commands = {
        "addon-install": addon.addon_install,
        "addon-uninstall": addon.addon_uninstall,
        "operator-install": operator.operator_install,
        "operator-uninstall": operator.operator_uninstall,
    }
    user_help_command = [ar.strip() for ar in sys.argv[-2:]]
    sub_command = _commands.get(user_help_command[0])
    if user_help_command[-1] == "--help" and sub_command:
        with click.Context(sub_command) as ctx:
            click.echo(sub_command.get_help(ctx))

    else:
        entry_point(obj={})
