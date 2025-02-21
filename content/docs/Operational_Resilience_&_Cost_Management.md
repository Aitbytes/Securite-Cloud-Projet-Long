# **Operational Resilience & Cost Management**

### **FinOps & Cost Optimization**

#### Addressing budget overruns through FinOps.

#### Tools for monitoring and optimizing cloud spend.

### **Disaster Recovery Strategies**

#### Building redundancy in multi-cloud architectures (e.g., Netflix migration to AWS).

### 

## High level security considerations.

Cloud infrastructures present unique security challenges. The increased
exposure associated with cloud services can lead to a higher risk of
cyberattacks and human error. The multitude of interactions within cloud
environments heightens the potential for insider threats and operational
mistakes, necessitating robust security measures and constant
monitoring; Furthermore, while many cloud platforms tout advanced
security features, organizations must ensure these are properly
implemented to protect sensitive data effectively

.

.

## Container registries

### Comprehensive Analysis: Security Risks of Exposed Container Registries and Compromised Docker Hub Accounts

[[trendmicro.com]{.underline}](https://www.trendmicro.com/en_us/research/21/k/compromised-docker-hub-accounts-abused-for-cryptomining-linked-t.html?utm_source=chatgpt.com)

The integration of container technologies into modern development
workflows has streamlined application deployment and scalability.
However, as highlighted by Trend Micro, misconfigurations and inadequate
security measures in container environments can introduce significant
vulnerabilities.

**Risks Associated with Exposed Container Registries**

Container registries function as centralized repositories for storing
and distributing container images. When these registries are publicly
accessible without proper authentication, they become susceptible to
unauthorized access. Trend Micro emphasizes that such exposure can lead
to:

-   **Unauthorized Data Access**: Attackers can download proprietary
    > software or sensitive data embedded within container images. This
    > unauthorized access can result in data breaches and intellectual
    > property theft.

-   **Malware Distribution**: Malicious actors gaining access to exposed
    > registries can upload compromised images. These images, once
    > deployed, can disseminate malware across systems, posing
    > significant security threats.

**Case Study: Compromised Docker Hub Accounts and Cryptomining**

In October 2021, Trend Micro observed a campaign targeting misconfigured
servers with exposed Docker REST APIs. Threat actors exploited these
vulnerabilities by deploying containers from images designed to execute
malicious scripts. These scripts facilitated unauthorized cryptocurrency
mining, consuming substantial system resources and potentially leading
to operational disruptions.

The group identified in this campaign, known as TeamTNT, has a history
of abusing cloud environments for cryptomining activities. Their tactics
include compromising Docker Hub accounts to distribute malicious images,
further emphasizing the necessity for stringent security practices in
container ecosystems.

**Mitigation Strategies**

To safeguard container environments from such threats, Trend Micro
recommends the following measures:

-   **Implement Robust Authentication and Access Controls**: Ensure that
    > access to container registries and APIs is restricted to
    > authorized personnel only. This prevents unauthorized interactions
    > with container resources.

-   **Regular Monitoring and Logging**: Continuously monitor container
    > activities and maintain logs to detect and respond to suspicious
    > behaviors promptly. Proactive monitoring aids in early threat
    > detection and mitigation.

-   **Network Segmentation**: Isolate container environments from other
    > network segments to minimize potential attack surfaces. Proper
    > segmentation restricts lateral movement of threats within the
    > network.

-   **Regular Vulnerability Scanning**: Conduct periodic scans of
    > container images and registries to identify and remediate
    > vulnerabilities. Regular assessments help maintain the integrity
    > and security of containerized applications.

## Virtualization

### Analysis of various virtual machine attacks in cloud computing

### Co-Resident Attack and its impact on Virtual Environment

In order to implement Resource pooling and multi-tenancy, cloud
companies started using virtualization, allowing them to run multiple OS
on the same computer. This technology is also the target of several
attacks

-   **DoS Attacks :** A hacker can use a cloud provider to perform a
    > DDoS attack on the cloud provider itself or one of its clients.

-   **Co-Residential Attacks :** Using side channels, a hacker can steal
    > private information from virtual machines who share the same
    > server as a malicious VM. But first, the hacker needs to co-locate
    > one of his VMs with the target VM.

-   **Cache-Based Side Channel Attacks :** Possible for two VMs on the
    > same computer using bare-metal hypervisor sharing highest
    > level-cache

-   **Hypervisor compromission :** The hypervisor is the software
    > responsible for virtualization. A compromised hypervisor may lead
    > to the compromission of all hosted virtual machines.

-   **VM Escape :** A hacker tries to exploit a fault in isolation
    > features to gain access to the host machine.

-   **VM Cloning :** A hacker copies the program files of a VM from the
    > host OS and then makes a clone to access sensitive data.

-   **VM Memory Dump :** A hacker dumps the memory assigned to the
    > target VM to search for information.

.**Countermeasures**

To mitigate the risk of co-resident attacks, researchers proposed
various approaches

-   **Preventing Side Channel Attacks :** Most SCA work with high
    > resolution internal clocks, eliminating references to internal
    > clocks will protect software from several SCA. This solution
    > however is hardware-based and costly

-   **Periodic Migration :** Regular migration following a VCG mechanism
    > will hinders the capacity of an attackers to perform
    > co-residential attacks
