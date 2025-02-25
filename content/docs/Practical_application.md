# Practical application

## Objective

Our goal is to create a standard cloud infrastructure, and leverage our
understanding to highlight and exploit the vulnerabilities we would have
left behind.

## Setting up authorisations

We start by creating a google cloud project :

![](../media/image3.png)

We proceed to the IAM section to create a service account for managing
the IAM policies.

| ![](../media/image1.png) | ![](../media/image2.png) |
|------------------------------------|------------------------------------|

Once the service account is created we can export its credentials file,
which will be the key to automating all the remaining configuration with
IaC.

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
