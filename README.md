## ocp-addons-operators-cli
CLI to install/uninstall Addons/operators on Openshift clusters.



### Container
image locate at [ocp-addons-operators-cli](https://quay.io/repository/<place holder>/ocp-addons-operators-cli)  
To pull the image: `podman pull quay.io/<place holder>/ocp-addons-operators-cli`

### Usages

```
podman run quay.io/<place holder>/ocp-addons-operators-cli --help
podman run quay.io/<place holder>/ocp-addons-operators-cli addon addon-install --help
podman run quay.io/<place holder>/ocp-addons-operators-cli addon addon-uninstall --help
podman run quay.io/<place holder>/ocp-addons-operators-cli operator operator-install --help
podman run quay.io/<place holder>/ocp-addons-operators-cli operator operator-uninstall --help
```

### Addons
#### Install Addon

```
podman run quay.io/<place holder>/ocp-addons-operators-cli \
    addon \
    -t $OCM_TOKEN \
    -a ocm-addon-test-operator \
    -c cluster-name \
    addon-install \
    -p has-external-resources=false \
    -p aws-cluster-test-param=false
```

#### Uninstall Addon

```
podman run quay.io/<place holder>/ocp-addons-operators-cli \
    addon \
    -t $OCM_TOKEN \
    -a ocm-addon-test-operator \
    -c cluster-name \
    addon-uninstall
```
