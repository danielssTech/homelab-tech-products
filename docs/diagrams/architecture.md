# System Architecture Diagram

This document illustrates the overall architecture of the **Tech Products Web Application** project.  
The design follows a layered and secure structure separating external and internal services.

```mermaid
flowchart LR
    subgraph DMZ["DMZ / Services Network"]
        NGINX["Nginx\n(Reverse Proxy + Static Files)\n:80 / :443"]
    end
    subgraph LAN["Internal Network / Backend"]
        APP["App - Tech Products API\n(e.g., :8080)"]
        DB[("PostgreSQL\n:5432 (internal only)")]
    end

    CLIENT[("Client / Browser")] -- HTTPS :443 (recommended) 🔒\nHTTP :80 (redirect to 443) --> NGINX
    NGINX -- Internal HTTP :8080 --> APP
    APP -- Internal connection :5432\nLeast-privileged user --> DB
    NGINX --- NOTE1[/"External traffic only reaches Nginx.\nThe App and Database never expose public ports."/]
    DB --- NOTE2[/"Backup and restore successfully tested.\nSecrets stored outside the repository."/]
