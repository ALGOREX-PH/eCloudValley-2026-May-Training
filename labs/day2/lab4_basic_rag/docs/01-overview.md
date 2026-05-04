# CloudKaiju — Product Overview

CloudKaiju is a cloud-native observability platform built for engineering teams running modern microservice architectures across AWS, GCP, and Azure. It unifies metrics, logs, and distributed traces into a single workspace and adds AI-powered anomaly detection on top.

## What CloudKaiju does

- **Metrics** — Time-series ingestion at up to 5 million data points per second per workspace, with 13-month retention by default on the Pro tier.
- **Logs** — Structured and unstructured log ingest, full-text + structured search, hot retention up to 90 days, cold retention up to 7 years on Enterprise.
- **Traces** — OpenTelemetry-native distributed tracing with automatic service maps and head-based sampling.
- **AI anomaly detection** — Built-in models flag unusual patterns in any time series and propose root-cause candidates.

## Architecture

CloudKaiju is delivered as a managed multi-tenant SaaS, with optional single-tenant Enterprise deployments in the customer's own VPC (AWS PrivateLink or Azure Private Link). The data plane uses ClickHouse for metrics and logs, and a custom columnar store for traces.

## Supported integrations

CloudKaiju ships first-class integrations for: AWS CloudWatch, AWS X-Ray, GCP Cloud Monitoring, Kubernetes (kube-state-metrics + node-exporter), PostgreSQL, MySQL, Redis, Kafka, Snowflake, Datadog migration, and the OpenTelemetry Collector.

For everything else, the **CloudKaiju Agent** runs as a sidecar or daemonset and exposes a Prometheus-compatible scrape endpoint.

## Workspaces and roles

Every customer gets one or more **workspaces**. Each workspace has:

- **Owners** — full admin, including billing
- **Editors** — can create/edit dashboards, alerts, integrations
- **Viewers** — read-only access
- **Service accounts** — non-human identities used by API integrations

Role assignments are workspace-scoped; there is no global cross-workspace role.

## Data residency

CloudKaiju supports the following regions for the SaaS data plane: us-east-1 (Virginia), us-west-2 (Oregon), eu-west-1 (Ireland), eu-central-1 (Frankfurt), ap-southeast-1 (Singapore), ap-northeast-1 (Tokyo). Workspaces can choose their region at creation; data does not leave that region.
