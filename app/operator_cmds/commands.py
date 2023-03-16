import click


@click.group()
@click.pass_context
def operator(ctx):
    """
    Command line to Install/Uninstall Operator on OCP cluster.
    """
    ctx.ensure_object(dict)
    raise NotImplementedError


@operator.command()
@click.pass_context
def install(ctx):
    """Install cluster Operator."""
    raise NotImplementedError


@operator.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall cluster Operator."""
    raise NotImplementedError
