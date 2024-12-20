# selfhostwatch

For details about developing selfhostwatch, see [HACKING](HACKING.md).

Self-hosting is a valuable tool to keep the Internet useful to the people, and not to private for-profit companies.

Many good software is available to self-host.
However, self-hosting this software often requires Linux administration tasks.
(For example, installing the software, creating a database, and configuing backups.)

Projects such as [YunoHost](https://yunohost.org/) automate the deployment of self-hosted software.
These projects provide a step-by-step installation process for a base system, and then offer a web interface to install completely functional instances of packages.

(Although Linux distributions often package the same software, generally administrators must do significant configuration.)

When self-hosting software, especially if exposing such software to the Internet, keeping the software up to date is essential to prevent malicious actors from disrupting your self-hosted systems.

(Remember that automated malicious actors scan the Internet for outdated exploitable software.)

selfhostwatch scrapes self-hosting systems (currently, only YunoHost) and displays a timeline of upstream and downstream updates.
With these timelines, people who want to self-host software can evaluate whether a self-hosting system provides good-enough updates.

You can view the current timelines at <https://alexpdp7.github.io/selfhostwatch/>.
