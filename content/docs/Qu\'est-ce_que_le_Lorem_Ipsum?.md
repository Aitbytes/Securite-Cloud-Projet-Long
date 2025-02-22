# Qu\'est-ce que le Lorem Ipsum?

Le **Lorem Ipsum** est simplement du faux texte employé dans la
composition et la mise en page avant impression. Le Lorem Ipsum est le
faux texte standard de l\'imprimerie depuis les années 1500, quand un
imprimeur anonyme assembla ensemble des morceaux de texte pour réaliser
un livre spécimen de polices de texte. Il n\'a pas fait que survivre
cinq siècles, mais s\'est aussi adapté à la bureautique informatique,
sans que son contenu n\'en soit modifié. Il a été popularisé dans les
années 1960 grâce à la vente de feuilles Letraset contenant des passages
du Lorem Ipsum, et, plus récemment, par son inclusion dans des
applications de mise en page de texte, comme Aldus PageMaker.

## 

## **Core Security Challenges in Cloud Environments**

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
internet. The leak, dubbed *The Fappening*, gained immediate traction,
with a subreddit dedicated to the images amassing over 100,000 followers
in just 24 hours. Despite efforts to contain the spread, copies of the
photos appeared on underground forums and other websites, dominating
headlines for weeks.

Investigations into the hack revealed that private photos had initially
surfaced on the imageboard *4chan* and the obscure forum *Anon-IB*, both
known for anonymously sharing explicit content. On August 26, 2014, an
Anon-IB user claimed that members of a private group had accessed and
obtained nude photos of Jennifer Lawrence, among other celebrities.
Initially, the stolen photos were traded or sold in underground
communities, with collectors amassing images in hopes of profiting.
However, on August 31, someone decided to release the entire collection
publicly on *4chan*, igniting the scandal.

Further digging led to a secretive group within Anon-IB called *Stol*,
consisting of several men across the United States. These individuals,
ranging from a teacher to a bank teller, engaged in hacking and trading
stolen private images, primarily targeting celebrities. Their methods
involved phishing attacks, tricking victims into revealing their Apple
iCloud credentials, granting them access to personal photo libraries.

The hack exposed major vulnerabilities in cloud security, prompting
Apple to strengthen iCloud protections. Multiple individuals were
eventually identified and prosecuted for their roles in the breach,
though the damage had already been done. The scandal remains one of the
most infamous digital privacy breaches in history.

CloudBleed (2017)

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

By 4:40 PM, Cloudflare\'s incident response team mobilized, including
engineers from both San Francisco and London. Initial investigation
suggested the bug was linked to Cloudflare's email obfuscation feature,
which had recently undergone modifications. Engineers swiftly disabled
this feature via a global kill switch at 5:22 PM PST, but the issue
persisted.

Further debugging identified two additional problematic features:
automatic HTTP rewrites and server-side excludes. While automatic HTTP
rewrites could be turned off immediately, server-side excludes lacked a
kill switch, requiring a patch. By 11:22 PM PST, after hours of effort,
a fix was finally deployed, preventing further data leakage.

### Vulnerabilities

#### Risks of misconfigured cloud settings and unauthorized access.

### Threats to Service Reliability

#### Impact of high-profile outages (e.g., AWS 2012 downtime).

#### Mitigating risks of third-party dependencies.

## 

## **Infrastructure & Architectural Security**

### Shared Responsibility Models

#### Évolution of IaaS (EC2, S3), PaaS (Google App Engine), and SaaS (Salesforce).

#### Security gaps in provider vs. user obligations.

### Hybrid & Multi-Cloud Complexity

#### Balancing control and flexibility in hybrid architectures (e.g., Azure, IBM SmartCloud).

#### Risks of vendor lock-in and interoperability challenges.
