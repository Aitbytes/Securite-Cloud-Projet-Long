# Practical application

## Objective

Our goal is to create a standard cloud infrastructure, and leverage our
understanding to highlight and exploit the vulnerabilities we would have
left behind.

Throughout the labs, we will be leveraging IaC with terraform and
ansible extensively, as it self-documents every step, while also making
our configurations easily repeatable.

## Setting up authorisations

We start by creating a google cloud project :

![](../media/image3.png)

We proceed to the IAM section to create a service account for managing
the IAM policies.

| ![](../media/image2.png) | ![](../media/image1.png) |
|------------------------------------|------------------------------------|

Once the service account is created we can export its credentials file,
which will be the key to automating all the remaining configuration
using IaC.

All the configuration is referenced under in this repo :
[[https://github.com/Aitbytes/Projet-Long-Infra/]](https://github.com/Aitbytes/Projet-Long-Infra/)

The first step consists in creating a separate service account, then
providing it with the necessary roles for further deployments tasks. The
script used for that end is referenced under :
[[https://github.com/Aitbytes/Projet-Long-Infra/tree/main/PrepareAccounts]](https://github.com/Aitbytes/Projet-Long-Infra/tree/main/PrepareAccounts)

Simultaneously it provides each team mate with the identical rôles.

The roles granted to both the service account and the teammates are :

-   **Compute.admin**

-   **Container.admin**

-   **Storage.admin**

-   **Run.admin**

-   **Run.invoker**

-   **Compute.instanceAdmin**

-   **Artifactregistry.reader**

-   **iam.serviceAccountUser**

-   **logging.viewer**

-   **monitoring.viewer**

## Explanation of the authorisations

The **compute.admin** role grants full control over Compute Engine
resources, allowing users to create, modify, and delete virtual
machines, networks, and other related resources. Complementing this, the
**container.admin** role provides administrative access to Google
Kubernetes Engine (GKE) resources, enabling users to manage clusters,
nodes, and workloads within the container environment. Meanwhile, the
**storage.admin** role allows users to administer Cloud Storage
resources by creating and deleting buckets, uploading and downloading
objects, and setting access controls. For serverless applications, the
**run.admin** role grants comprehensive access to Cloud Run services,
permitting users to deploy, update, and delete applications. On the
other hand, the **run.invoker** role enables users to invoke Cloud Run
services, allowing the triggering of serverless applications without
administrative privileges.

Furthermore, the **compute.instanceAdmin.v1** role provides permissions
to manage Compute Engine instances, including operations like starting,
stopping, and modifying virtual machines. To facilitate access to
containerized applications, the **artifactregistry.reader** role allows
users to view and list container images stored in Artifact Registry. The
**iam.serviceAccountUser** role empowers users to act as a service
account, permitting them to execute operations on behalf of the service
account. In terms of observability, the **logging.viewer** role grants
read-only access to view logs in Cloud Logging, while the
**monitoring.viewer** role provides read-only access to Cloud Monitoring
data, enabling users to monitor system performance and health by viewing
metrics, dashboards, and alerts.

## Running a k3s cluster on GCP compute engine

The goal for this first lab is two folds. Learn how to build and break a
kubernetes cluster.

## Building the cluster

### Provisioning the VMs

The first step of building

### Creating the cluster using k3s

The following repo :
[[https://github.com/techno-tim/k3s-ansible]](https://github.com/techno-tim/k3s-ansible)
contains a multitude of scripts for provisioning a k3s cluster on
Proxmox. After much investigating, an hours of trial and error. We
managed
