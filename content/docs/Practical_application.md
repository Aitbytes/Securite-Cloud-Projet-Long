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

![](../media/image2.png)

We proceed to the IAM section to create a service account for managing
the IAM policies.

| ![](../media/image1.png) | ![](../media/image3.png) |
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

By default, managing permissions and roles in Google Cloud can be
complex, particularly when dealing with multiple users and service
accounts. However, using Terraform scripts simplifies this process by
providing an infrastructure as code approach. In this article, we will
explore how to construct a Terraform script to assign roles and manage
IAM permissions efficiently in a Google Cloud project.

Step 1: Define Variables

To begin, we declare variables in Terraform to capture the list of user
emails and the project ID for which we will be managing permissions.
This is done using the \`variable\` block and allows flexibility in
specifying user details and project settings outside the script itself.

\`\`\`hcl

variable \"user_emails\" {

description = \"List of email addresses of the users\"

type = list(string)

}

variable \"project_id\" {

description = \"ID of the project\"

type = string

}

\`\`\`

Step 2: Configure the Google Provider

Next, we configure the Google Cloud provider with the necessary
credentials, project ID, and default region. This provider block is
crucial for authenticating and interacting with Google Cloud resources.

\`\`\`hcl

provider \"google\" {

credentials = file(\"./secrets/credentials.json\")

project = var.project_id

region = \"europe-west1\"

}

\`\`\`

Step 3: Create a Service Account

We create a Google Cloud service account using the \`resource\` block.
This account will be used to manage resources within the project.

\`\`\`hcl

resource \"google_service_account\" \"resrc_mgr_service_account\" {

account_id = \"resrc-mgr-service-account\"

display_name = \"Ressource Manager Service Account\"

}

\`\`\`

Step 4: Define IAM Roles

The \`locals\` block is used to define a list of roles that we intend to
assign to both users and the service account. It allows for an organized
way to manage and update roles centrally.

\`\`\`hcl

locals {

roles = \[

\"roles/compute.admin\",

\"roles/container.admin\",

\"roles/storage.admin\",

\...

\]

}

\`\`\`

Step 5: Assign Roles to Users

Using the \`google_project_iam_member\` resource, we loop through each
combination of user email and roles to create the necessary IAM
bindings. This ensures that each user is granted the appropriate
permissions within the project.

\`\`\`hcl

resource \"google_project_iam_member\" \"role_binding\" {

for_each = {

for pair in setproduct(var.user_emails, local.roles) :

\"\${pair\[0\]}\_\${pair\[1\]}\" =\> {

email = pair\[0\]

role = pair\[1\]

}

}

project = var.project_id

role = each.value.role

member = \"user:\${each.value.email}\"

}

\`\`\`

Step 6: Assign Roles to the Service Account

Similarly, roles are assigned to the service account itself, ensuring it
has the required permissions to perform its intended functions within
the infrastructure.

\`\`\`hcl

resource \"google_project_iam_member\" \"service_account_role_binding\"
{

for_each = toset(local.roles)

project = var.project_id

role = each.value

member =
\"serviceAccount:\${google_service_account.resrc_mgr_service_account.email}\"

}

\`\`\`

Step 7: Grant Additional Permissions

Finally, specific roles such as \`Service Account User\` and \`Service
Account Admin\` are granted to user accounts to further manage and
interact with the service account. This is vital for delegating service
account management tasks.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th><p>resource "google_service_account_iam_member"
"service_account_user_permission" {</p>
<p>for_each = toset(var.user_emails)</p>
<p>service_account_id =
google_service_account.resrc_mgr_service_account.name</p>
<p>role = "roles/iam.serviceAccountUser"</p>
<p>member = "user:${each.value}"</p>
<p>}</p>
<p>resource "google_service_account_iam_member"
"service_account_admin_permission" {</p>
<p>for_each = toset(var.user_emails)</p>
<p>service_account_id =
google_service_account.resrc_mgr_service_account.name</p>
<p>role = "roles/iam.serviceAccountAdmin"</p>
<p>member = "user:${each.value}"</p>
<p>}</p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

\`\`\`hcl

\`\`\`

In conclusion, this Terraform script efficiently manages Google Cloud
IAM roles and permissions by automating the assignment process for users
and service accounts, providing both flexibility and security in
large-scale cloud operations.

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
