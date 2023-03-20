import os

import click
from constants import TIMEOUT_30MIN
from ocp_resources.cluster_service_version import ClusterServiceVersion
from ocp_resources.namespace import Namespace
from ocp_resources.operator import Operator
from ocp_resources.operator_group import OperatorGroup
from ocp_resources.subscription import Subscription
from ocp_utilities.infra import get_client
from ocp_utilities.operators import wait_for_operator_install


def _client(ctx):
    return get_client(config_file=ctx.obj["kubeconfig"])


@click.group()
@click.option("--debug", help="Enable debug logs", is_flag=True)
@click.option(
    "--kubeconfig",
    help="Path to kubeconfig file",
    required=True,
    default=os.environ.get("KUBECONFIG"),
    type=click.Path(exists=True),
    show_default=True,
)
@click.option("-n", "--name", help="Operator name to install/uninstall", required=True)
@click.pass_context
def operator(ctx, kubeconfig, name, debug):
    """
    Command line to Install/Uninstall Operator on OCP cluster.
    """
    ctx.ensure_object(dict)
    ctx.obj["name"] = name
    ctx.obj["kubeconfig"] = kubeconfig
    if debug:
        os.environ["OCM_PYTHON_WRAPPER_LOG_LEVEL"] = "DEBUG"
        os.environ["OPENSHIFT_PYTHON_WRAPPER_LOG_LEVEL"] = "DEBUG"


@operator.command()
@click.option(
    "-c",
    "--channel",
    help="Operator channel to install from",
    default="stable",
    show_default=True,
)
@click.option(
    "-s",
    "--source",
    help="Catalog source name install from",
    default="redhat-operators",
    show_default=True,
)
@click.option(
    "--target-namespaces",
    help="target namespaces for the operator. comma separated string",
)
@click.pass_context
def install(ctx, channel, source, target_namespaces):
    """Install cluster Operator."""
    client = _client(ctx=ctx)
    name = ctx.obj["name"]
    _target_namespaces = None

    if target_namespaces:
        _target_namespaces = target_namespaces.split(",")
        for namespace in _target_namespaces:
            ns = Namespace(client=client, name=namespace)
            if ns.exists:
                continue

            ns.deploy(wait=True)

    else:
        ns = Namespace(client=client, name=name)
        if not ns.exists:
            ns.deploy(wait=True)

    OperatorGroup(
        client=client,
        name=name,
        namespace=name,
        target_namespaces=_target_namespaces,
    ).deploy(wait=True)

    subscription = Subscription(
        client=client,
        name=name,
        namespace=name,
        channel=channel,
        source=source,
        source_namespace="openshift-marketplace",
        install_plan_approval="Automatic",
    )
    subscription.deploy(wait=True)
    wait_for_operator_install(
        admin_client=client, subscription=subscription, timeout=TIMEOUT_30MIN
    )


@operator.command()
@click.pass_context
def uninstall(ctx):
    """Uninstall cluster Operator."""
    name = ctx.obj["name"]
    client = _client(ctx=ctx)
    csv_name = None

    subscription = Subscription(
        client=client,
        name=name,
        namespace=name,
    )
    if subscription.exists:
        csv_name = subscription.instance.status.installedCSV
        subscription.clean_up()

    OperatorGroup(
        client=client,
        name=name,
        namespace=name,
    ).clean_up()

    for _operator in Operator.get(dyn_client=client):
        if _operator.name.startswith(name):
            # operator name convention is <name>.<namespace>
            namespace = name.split(".")[-1]
            ns = Namespace(client=client, name=namespace)
            if ns.exists:
                ns.clean_up()

    if csv_name:
        csv = ClusterServiceVersion(
            client=client,
            namespace=subscription.namespace,
            name=csv_name,
        )

        csv.wait_deleted(timeout=60 * 10)
