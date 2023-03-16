import os

import click
from ocm_python_wrapper.cluster import TIMEOUT_30MIN, ClusterAddOn
from ocm_python_wrapper.ocm_client import OCMPythonClient


@click.group()
@click.option("-a", "--addon", help="Addon name to install", required=True)
@click.option(
    "--timeout",
    help="Timeout in seconds to wait for addon to be installed/uninstalled",
    default=TIMEOUT_30MIN,
    show_default=True,
)
@click.option(
    "-e",
    "--endpoint",
    help="SSO endpoint url",
    default="https://sso.redhat.com/auth/realms/redhat-external/protocol/openid-connect/token",
    show_default=True,
)
@click.option(
    "-t",
    "--token",
    help="OCM token (Taken from oc environment OCM_TOKEN if not passed)",
    required=True,
    default=os.environ.get("OCM_TOKEN"),
)
@click.option("-c", "--cluster", help="Cluster name", required=True)
@click.option("--debug", help="Enable debug logs", is_flag=True)
@click.option(
    "--api-host",
    help="API host",
    default="production",
    type=click.Choice(["stage", "production"]),
    show_default=True,
)
@click.pass_context
def addon(ctx, addon, token, api_host, cluster, endpoint, timeout, debug):
    """
    Command line to Install/Uninstall Addon on OCM managed cluster.
    """
    ctx.ensure_object(dict)
    ctx.obj["timeout"] = timeout
    if debug:
        os.environ["OCM_PYTHON_WRAPPER_LOG_LEVEL"] = "DEBUG"
        os.environ["OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL"] = "DEBUG"

    _client = OCMPythonClient(
        token=token,
        endpoint=endpoint,
        api_host=api_host,
        discard_unknown_keys=True,
    ).client
    ctx.obj["cluster_addon"] = ClusterAddOn(
        client=_client, cluster_name=cluster, addon_name=addon
    )


@addon.command()
@click.option(
    "-p",
    "--parameters",
    multiple=True,
    help="Addon parameters for installation. each parameter pass as id=value. multiple parameters are allowed",
)
@click.pass_context
def install(ctx, parameters):
    """Install cluster Addon."""
    timeout = ctx.obj["timeout"]
    cluster_addon = ctx.obj["cluster_addon"]
    _parameters = []
    for parameter in parameters:
        if "=" not in parameter:
            click.echo(f"parameters should be id=value, got {parameter}\n")
            raise click.Abort()

        _id, _value = parameter.split("=")
        _parameters.append({"id": _id, "value": _value})

    cluster_addon.install_addon(parameters=_parameters, wait_timeout=timeout)


@addon.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall cluster Addon."""
    timeout = ctx.obj["timeout"]
    cluster_addon = ctx.obj["cluster_addon"]
    cluster_addon.uninstall_addon(wait_timeout=timeout)
