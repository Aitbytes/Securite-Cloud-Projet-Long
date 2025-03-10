# Core Security Challenges in Cloud Environments

### Case studies

#### Capital One (2019)

On July 17, 2019, Capital One\'s security team was alerted to a data
leak by an email sent to their responsible disclosure box. A user
reported that a GitHub repository contained suspicious commands to
exfiltrate data from an AWS S3 storage belonging to the bank.
Examination of these commands revealed a critical flaw: in just a few
lines executed via the AWS CLI interface, an attacker could retrieve the
authentication information of an IAM role, list all associated S3
buckets and massively download their contents. Log analysis showed that
these commands had been executed several months earlier, potentially
compromising the sensitive data of millions of customers.

Further investigation revealed the attack chain exploited. The attacker
had exploited a Server-Side Request Forgery (SSRF) flaw on an exposed
web server, a reverse proxy using ModSecurity, hosted on an AWS EC2
instance. By bypassing filtering rules, the attacker was able to query
the EC2 instance\'s metadata service, an internal service that provides
sensitive information, including the temporary credentials of IAM roles
attached to the instance. Using these credentials, he was able to
execute commands as this role and gain free access to the associated AWS
resources.

The final link in the flaw lay in the misconfiguration of IAM
permissions. By bypassing the filtering rules, the attacker was able to
query the EC2 instance\'s metadata service, an internal service that
provides sensitive information, including the temporary credentials of
the IAM roles attached to the instance. Using these credentials, he was
able to execute commands as this role and gain free access to the
associated AWS resources.

The final link in the flaw lay in the misconfiguration of IAM
permissions. The compromised role had excessive rights, including read
access to all S3 buckets and the ability to decrypt protected data. This
error enabled the attacker to exfiltrate around 30 GB of data, including
millions of credit card applications, social security numbers and bank
details. Once the breach was identified, Capital One and AWS took
immediate action: revoking the compromised credentials, shutting down
the vulnerable instance and notifying the authorities, notably the FBI.
This incident underlined the importance of strict access controls and
reinforced protection against SSRF attacks, which are now better
controlled in cloud environments.

#### iCloud (2014), 

On August 31, 2014, a massive leak of private celebrity photos flooded
Reddit. These intimate images, stolen from some of the most high-profile
actresses, models, singers, and athletes, quickly spread across the
internet. Despite efforts to contain the spread, copies of the photos
appeared on underground forums and other websites, dominating headlines
for weeks.

Investigations into the hack led to a secretive group within 4chan
forums called *Stol*, consisting of several men across the United
States. These individuals engaged in hacking and trading stolen private
images, primarily targeting celebrities. Their methods involved phishing
attacks, tricking victims into revealing their Apple iCloud credentials,
granting them access to personal photo libraries.

The primary vulnerability exploited was a security flaw in Apple\'s
\"Find My iPhone\" service, which lacked a mechanism to limit the number
of incorrect password attempts. This absence allowed attackers to
perform brute-force attacks---systematically attempting numerous
password combinations until the correct one was found---without
triggering account lockouts or alerts.

#### CloudBleed (2017)

On February 18, 2017, at 4:11 PM PST, a security researcher from
Google\'s Project Zero discovered a critical vulnerability in
Cloudflare\'s infrastructure. The issue was severe enough that he
immediately reached out to Cloudflare, and by 4:32 PM, the company was
made aware of a possible widespread data leak.

Cloudflare, a major Content Delivery Network (CDN) provider, had been
unknowingly exposing sensitive customer data, including cookies,
passwords, HTTPS requests, and private keys. This data leakage occurred
due to a bug in how Cloudflare\'s edge servers processed HTML content.
Worse, search engines like Google had already cached some of the leaked
data, making it publicly accessible.

**Initial Investigation & Mitigation Efforts**

Upon discovery, Cloudflare engineers quickly convened and correlated the
bug with the **email obfuscation** feature, which had recently undergone
a partial migration to a new HTML parser. They disabled this feature
globally, but the bug persisted. Further investigation identified **two
more problematic features**:

1.  **Automatic HTTP rewrites**

2.  **Server-side excludes**

Each of these features also processed HTML content dynamically on the
edge servers. While the first two features had global kill switches and
were disabled immediately, **server-side excludes** was an older feature
that lacked such a mechanism. Engineers had to develop and deploy a
patch to disable it.

Despite these measures, the **root cause remained unclear**, and there
was a lingering risk of reoccurrence.

**Root Cause Analysis**

The engineers determined that all three affected features used
Cloudflare's **new HTML parser (cf-html)**, which replaced an older
parser generated with **Ragel**, a finite state machine-based parser.
However, the **bug actually originated in the old Ragel-based parser**,
which had been in use for years without causing issues.

The bug was triggered by an **edge case involving unclosed HTML
attributes at the end of a data buffer**. In such cases:

-   The parser would attempt to reprocess an attribute but fail to check
    > for buffer boundaries correctly.

-   A pre-increment operation caused the parser's pointer (p) to **skip
    > over** the check that should have stopped it from reading past
    > valid memory.

-   As a result, **heap memory beyond the allocated buffer was
    > accessed**, leading to unintended data exposure.

The **new parser's migration process inadvertently triggered this
pre-existing bug** by handling buffers differently, exposing memory that
the old system never accessed.

### Takeaways

These case studies highlight the diversity of attack vectors in cloud
environments. While low-level memory safety issues remain a key concern,
as they do in any software, adequate identity and access management
becomes increasingly crucial in cloud environments.

In on-premises environment, data access is often based on a defined
network perimeter with more static controls, which limits opportunistic
attacks more common in cloud environments characterized by broad network
access.

Meanwhile, faster deployments increase the risk of rapid exploitation
but also enable quicker responses to threats. This is further supported
by managed logging and monitoring.

#### 

### Threats to Service Reliability

#### Impact of high-profile outages (e.g., AWS 2012 downtime).

Cloud service providers have experienced several significant outages
over the years, impacting various services and users worldwide. Notable
incidents include:

**Amazon Web Services (AWS):**

April 20, 2011: An outage in the Northern Virginia data center affected
services like Foursquare and Reddit.
[[Wikipédia]](https://en.wikipedia.org/wiki/Amazon_Web_Services)

June 29, 2012: A severe storm in Northern Virginia led to outages for
several websites relying on AWS.

[[Wikipédia]](https://en.wikipedia.org/wiki/Amazon_Web_Services)

February 28, 2017: A human error during debugging caused a massive
outage of S3 services in the Northern Virginia region, affecting
numerous websites.

[[Wikipédia]](https://en.wikipedia.org/wiki/Amazon_Web_Services)

**Microsoft Azure:**

February 29, 2012: An incorrect code for calculating leap day dates led
to a significant outage.
[[Wikipédia]](https://en.wikipedia.org/wiki/Microsoft_Azure?utm_source=chatgpt.com)

September 4, 2018: A lightning strike caused a cooling system failure,
resulting in a major outage in the North Europe region.
[[Wikipédia]](https://en.wikipedia.org/wiki/Microsoft_Azure?utm_source=chatgpt.com)

September 12, 2024: A change within a third-party internet service
provider\'s environment led to a global outage affecting services like
Word, Excel, and Teams.

[[reuters.com]](https://www.reuters.com/technology/microsoft-365-down-thousands-users-downdetector-shows-2024-09-12/?utm_source=chatgpt.com)

**Google Cloud:**

June 2, 2019: Google Cloud experienced a significant outage due to
network congestion, affecting services like YouTube and Gmail.

[[datacenterknowledge.com]](http://datacenterknowledge.com)

**Fastly**:

June 8, 2021: A misconfiguration caused a global outage, taking down
several major news websites and retailers.

[[pingdom.com]](https://www.pingdom.com/outages/internet-outages-the-12-most-impactful/)

**OVHcloud:**

March 10, 2021: A fire in the Strasbourg data center destroyed one
center and partially affected another, causing widespread disruptions.

fr.wikipedia.org

These incidents highlight the vulnerabilities in cloud infrastructures
and the widespread impact such outages can have on global services.

#### Mitigating risks of third-party dependencies.

## 
