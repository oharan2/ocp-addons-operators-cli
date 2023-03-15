import click


@click.group()
@click.pass_context
def operator(ctx):
    """
    Command line to Install/Uninstall Operator on OCP cluster.
    """
    ctx.ensure_object(dict)


@operator.command()
@click.pass_context
def install(ctx):
    """Install cluster Operator."""
    print(ctx)


@operator.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall cluster Operator."""
    print(ctx)
