# Virtualization

### Analysis of various virtual machine attacks in cloud computing

### Co-Resident Attack and its impact on Virtual Environment

### An approach with two-stage mode to detect cache-based side channel attacks

### Using Virtual Machine Allocation Policies to Defend against Co-Resident Attacks in Cloud Computing

In order to implement Resource pooling and multi-tenancy, cloud
companies started using virtualization, allowing them to run multiple OS
on the same computer. This technology is also the target of several
attacks

-   **DoS Attacks :** A hacker can use a cloud provider to perform a
    DDoS attack on the cloud provider itself or one of its clients.

-   **Co-Residential Attacks :** Using side channels, a hacker can steal
    private information from virtual machines who share the same server
    as a malicious VM. But first, the hacker needs to co-locate one of
    his VMs with the target VM.

-   **Cache-Based Side Channel Attacks :** Possible for two VMs on the
    same computer using bare-metal hypervisor sharing highest
    level-cache

-   **Hypervisor compromission :** The hypervisor is the software
    responsible for virtualization. A compromised hypervisor may lead to
    the compromission of all hosted virtual machines.

-   **VM Escape :** A hacker tries to exploit a fault in isolation
    features to gain access to the host machine.

-   **VM Cloning :** A hacker copies the program files of a VM from the
    host OS and then makes a clone to access sensitive data.

-   **VM Memory Dump :** A hacker dumps the memory assigned to the
    target VM to search for information.

.**Countermeasures**

To mitigate the risk of co-resident attacks, researchers proposed
various approaches

-   **Preventing Side Channel Attacks :** Most SCA work with high
    resolution internal clocks. Eliminating references to internal
    clocks will protect software from several SCA. This solution however
    is hardware-based and costly

-   **Periodic Migration :** Regular migration following a VCG mechanism
    will hinder the capacity of an attacker to perform co-residential
    attacks. Drawbacks of this method include performance degradation
    and power consumption.

-   **Preventing Co-Residency Verification :** To verify co-residency,
    attackers check if their VMs and the target VM share the same Dom0
    IP address. If the Dom0 IP address is confined, a malicious user
    will have to resort to difficult techniques if he wants to confirm
    co-residency.

-   **Detecting Co-location attacks :** Various features can be observed
    for anomalies in order to detect Cache-Based Side Channel Attacks,
    including CPU usage, RAM usage and cache miss.

-   **Allocation Policy :** An allocation policy is the policy employed
    by a cloud provider to allocate VMs to a physical resource. Some
    policies can increase the number of attempts an attacker needs to
    achieve a co-residency. For example, CLR (Co-location Resistance
    Algorithm) opens a fixed number of servers and randomly allocates a
    VM, or PSSF (Previously-selected-server-first) will try to allocate
    a user's VM to a server already used by the user.
