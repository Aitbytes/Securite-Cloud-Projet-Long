# Practical application

## Objective

Our goal is to create a standard cloud infrastructure, and leverage our
understanding to highlight and exploit the vulnerabilities we would have
left behind.

## Setting up authorisations

We start by creating a google cloud project :

![](../media/image1.png)

We proceed to the IAM section to create a service account for managing
the IAM policies.

| ![](../media/image2.png) | ![](../media/image3.png) |
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

-   **Cloud Run Admin**

-   **Cloud Run Invoker**

-   **Compute Admin**

-   **Kubernetes Engine Admin**

-   **Storage Admin.**

1\. \*\*roles/compute.admin\*\*: This role grants full control over
Compute Engine resources, allowing users to create, modify, and delete
virtual machines, networks, and other related resources.

2\. \*\*roles/container.admin\*\*: This role provides administrative
access to Google Kubernetes Engine (GKE) resources, enabling users to
manage clusters, nodes, and workloads within the container environment.

3\. \*\*roles/storage.admin\*\*: This role allows users to manage Cloud
Storage resources, including creating and deleting buckets, uploading
and downloading objects, and setting access controls.

4\. \*\*roles/run.admin\*\*: This role grants full access to Cloud Run
services, allowing users to deploy, update, and delete serverless
applications.

5\. \*\*roles/run.invoker\*\*: This role permits users to invoke Cloud
Run services, enabling them to trigger serverless applications without
having administrative access.

6\. \*\*roles/compute.instanceAdmin.v1\*\*: This role provides
permissions to manage Compute Engine instances, including starting,
stopping, and modifying virtual machines.

7\. \*\*roles/artifactregistry.reader\*\*: This role allows users to
view and list container images stored in Artifact Registry, facilitating
access to containerized applications.

8\. \*\*roles/iam.serviceAccountUser\*\*: This role enables users to act
as a service account, allowing them to execute operations on behalf of
the service account.

9\. \*\*roles/logging.viewer\*\*: This role grants read-only access to
view logs in Cloud Logging, enabling users to monitor and analyze
application and system logs.

10\. \*\*roles/monitoring.viewer\*\*: This role provides read-only
access to Cloud Monitoring data, allowing users to view metrics,
dashboards, and alerts to monitor system performance and health.
