# Log Management Prompt & Best Practices

Purpose: A concise, actionable prompt and guide to manage application and infrastructure logs, including long-term retention, security, indexing, archival, and operational practices.

---

## Prompt (use this to ask an AI or to standardize internal requests)

"You are a senior SRE/observability engineer. Produce a comprehensive, actionable Log Management Policy and implementation plan for a production service running on Docker + Kubernetes with Node.js backends and batch workers. Cover:

- Structured logging format and fields (JSON schema) with examples
- Logging levels, sampling, and rate-limiting strategies
- Redaction and PII handling rules
- Correlation IDs and enriched context (request, trace IDs)
- Local buffering, shipping, and backpressure handling
- Ingestion pipelines (Fluentd/Fluent Bit/Vector) and schema enforcement
- Indexing strategy (Elasticsearch/Opensearch, Loki, or BigQuery) and retention tiers
- Short-term hot storage and long-term cold archive strategies (S3/GCS/Archive) with lifecycle rules and cost estimates
- Compression, chunking and format choices for long-term storage (NDJSON, Parquet)
- Retention policy examples by log type (access, audit, error, debug)
- Backup and restore verification procedures for long-term logs
- Access control, encryption at-rest/in-transit, and audit trails
- Monitoring, alerts, and SLOs for log pipeline health
- Automation: example GitHub Actions steps to export and archive logs on schedule
- Compliance/legal considerations (GDPR, CCPA), legal holds, and deletions

Output a reusable policy document, sample config snippets (Fluent Bit, Vector, logrotate), S3 lifecycle rules, and an actionable migration plan to retain logs for 1, 3, and 7+ years. Include sample retention durations with trade-offs and cost/benefit notes."

---

## Executive Summary

Good logging is essential for debugging, security audits, compliance, and analytics. This document describes practical practices to collect, process, store, secure, and retain logs long-term while controlling cost and ensuring compliance.

Key principles:
- Emit structured logs (JSON) with consistent fields
- Keep production default log level to `info`; send `debug` to ephemeral stores or on-demand sampling
- Redact secrets/PII at source
- Use correlation IDs for traceability
- Keep hot indexes for 7–30 days, warm indexes for 30–90 days, and cold archives for years
- Archive to object storage (S3/GCS) in compressed NDJSON/Parquet for long-term retention
- Automate lifecycle and retention policies and validate restore regularly

---

## Structured Logging Schema (recommended)

Use JSON with stable keys. Example:

```json
{
  "ts": "2025-12-23T12:34:56.789Z",
  "level": "info",
  "service": "auth-service",
  "env": "production",
  "instance_id": "i-0123456789abcd",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "span_id": "00f067aa0ba902b7",
  "request_id": "req-12345",
  "user_id": "user-987",
  "path": "/api/login",
  "method": "POST",
  "status": 200,
  "latency_ms": 52,
  "message": "User logged in",
  "meta": { "client": "web" }
}
```

Required fields: `ts`, `level`, `service`, `env`, `trace_id`/`request_id` (where applicable), `message`.

Sensitive fields (PII, tokens) must never be logged in raw form — redact or hash.

---

## Levels, Sampling & Rate Limiting

- Levels: `fatal`/`error` -> critical; `warn` -> actionable; `info` -> routine; `debug`/`trace` -> verbose
- Default production level: `info`. Turn on `debug` via runtime flags or dynamic sampling.
- Sampling: sample 1-5% of `debug` logs cluster-wide; always log errors.
- Rate limit noisy sources (per-host/per-service) to avoid spike-induced costs and pipeline overload.

---

## Correlation & Context

- Generate a `request_id` at ingress and pass it to downstream services.
- Include `trace_id` from distributed tracing (W3C TraceContext) for cross-correlation.
- Ensure logs and traces share IDs to reconstruct request flows.

---

## Redaction & PII Handling

- Apply redaction at the log generation point where possible.
- Use allow-lists for fields permitted to be stored; block-list sensitive paths.
- For PII needed for audits, store hashed identifiers and store mapping in a secured vault if necessary.

---

## Local Buffering and Backpressure

- Use local file buffers (Fluent Bit/Vector) with size limits and retry policies.
- Configure backpressure: when remote ingestion is unavailable, buffer to disk and apply backoff.
- Enforce max buffer retention (e.g., 48–72 hours) to avoid disk exhaustion.

---

## Ingestion Pipelines

Recommended stack choices (pick one):
- Fluent Bit → Kafka → Vector/Fluentd → Elasticsearch/Opensearch
- Fluent Bit → Loki (for logs-as-metrics) for app logs + Prometheus for metrics
- Vector → ClickHouse/BigQuery for analytics-heavy workloads

Schema enforcement can be done with a validation stage (Vector transforms or ingest pipelines) to convert and reject invalid entries.

---

## Indexing & Short-term Storage

- Hot tier (Elasticsearch/OpenSearch): hold detailed logs for 7–30 days (fast queries)
- Warm tier: aggregated indexes for 30–90 days (less replicas, more compression)
- Cold tier: move to object storage-backed indices or snapshot archives for 90+ days

Use ILM (Index Lifecycle Management) to automatically rollover and shrink indices.

---

## Long-term Retention (1, 3, 7+ years)

Strategy: Tiered storage + periodic archiving.

1) Short-term (hot): 7–30 days — full indexed logs for fast search and alerting.
2) Medium-term (warm): 30–90 days — keep reduced replicas, compressed indices.
3) Long-term archive: 90 days → 7+ years — move to object storage (S3/GCS/Azure Blob) in compressed, queryable format.

Formats & trade-offs:
- NDJSON (newline-delimited JSON): simple, appendable, easy to restore, best for archival logs
- Parquet/ORC: columnar, much smaller, better for analytics (BigQuery/Presto), requires ETL

Compression: use gzip/zst for NDJSON, or Parquet's native compression (snappy/zstd).

Example retention timeline:
- Access logs: hot 14d → warm 60d → cold 3y archive
- Error/alert logs: hot 30d → warm 180d → cold 7y archive
- Audit logs (compliance): hot 90d → cold 7–10y (immutable, legal hold support)

Cost considerations:
- Hot indexes are expensive; keep only needed retention.
- Cold object storage with lifecycle (S3 Glacier/Archive) reduces cost at restore latency cost.

---

## Archival & Lifecycle Automation

- Export index snapshots or stream bulk logs to S3 using ingest jobs nightly/weekly.
- Store compressed NDJSON or Parquet with partitioning: `s3://company-logs/service/year=2025/month=12/day=23/part-0001.ndjson.gz`
- Apply S3 lifecycle rules to transition to Glacier/Archive after N days and set expiration for deletion.

S3 Lifecycle example (JSON):

```json
{
  "Rules": [
    {
      "ID": "MoveToGlacier",
      "Filter": {"Prefix": "service/"},
      "Status": "Enabled",
      "Transitions": [
        {"Days": 90, "StorageClass": "STANDARD_IA"},
        {"Days": 365, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 3650}
    }
  ]
}
```

---

## Storage Format & Queryability

- NDJSON: easy to restore and reindex; good general-purpose archival
- Parquet: efficient for analytics and cheaper to query in data warehouses
- Keep metadata (service, env, date, partition) in object path for quick discovery

For occasional ad-hoc queries on archives, consider storing a lightweight index/manifest (small JSON/CSV) listing partitions and example keys.

---

## Security, Encryption & Access Control

- Encrypt in transit (TLS) and at rest (server-side KMS or customer-managed keys)
- Restrict S3/GCS bucket access to dedicated roles; enable logging + MFA delete for sensitive buckets
- Use IAM roles for ingestion agents, not long-lived tokens
- Audit access with logs and monitor unusual access patterns

---

## Backup & Restore Verification

- Regularly test restores from cold archive (quarterly/annually depending on retention tier)
- Automate a small restore job that fetches a sample partition and re-indexes to a test cluster
- Validate checksums and integrity after archive

---

## Monitoring, Alerts & SLOs

- Monitor pipeline lag (time between log generation and index availability)
- Alert on buffer fill levels, shipping errors, and ingestion failures
- SLO examples:
  - Ingest latency < 60s (P99)
  - Archive job success rate > 99.9%

---

## Compliance & Legal Holds

- Implement legal hold procedures: mark partitions as non-deletable when under hold
- Provide deletion/erasure workflows for GDPR requests while preserving audit trail
- Keep immutable, tamper-evident archives for regulated data

---

## Practical Config Snippets

### Fluent Bit output to S3 (pseudo)

```ini
[OUTPUT]
    Name  s3
    Match *
    bucket  company-logs
    total_file_size  50M
    use_put_object On
    store_dir /var/log/fluent/s3
    s3_key_format /$TAG/%Y/%m/%d/%H/%M/%S-${UUID}.ndjson.gz
```

### Vector transform example (extract fields)

```toml
[sinks.my_elastic]
  type = "elasticsearch"
  inputs = ["app_logs"]
  endpoint = "https://es.internal:9200"
  index = "app-%Y.%m.%d"

[transforms.add_fields]
  type = "remap"
  inputs = ["app_logs"]
  source = "{ service = .service, env = .env }"
```

### Export to S3 via GitHub Actions (nightly)

```yaml
name: Archive Logs
on:
  schedule:
    - cron: '0 2 * * *' # daily 02:00 UTC
jobs:
  archive:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run export job
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Example: run a script that pulls logs from Elasticsearch and writes compressed NDJSON to S3
          ./scripts/export-logs-to-s3.sh --from-yesterday
```

---

## Retention Policy Examples (recommended)

- Audit logs: retain 7–10 years (compliance), immutable, archived to Glacier
- Error logs: 3–7 years (analytics + root cause analysis) — archived after 90 days
- Access logs: 1–3 years depending on business needs
- Debug logs: 14–30 days, or sampled

---

## Cost Optimization Tips

- Reduce index replicas and refresh rates in warm tier
- Aggregate non-critical logs before indexing
- Use partitioned archives to fetch small datasets
- Consider queryable cold storage (e.g., Athena/BigQuery) to avoid rehydrating archives frequently

---

## Testing & Validation

- Add CI checks to ensure logs are emitted in JSON schema
- Add pipeline e2e smoke tests simulating backpressure and verifying buffer recovery
- Validate archive restore monthly/quarterly with automation

---

## Actionable Migration Plan (short)

1. Implement structured logging library and enforce schema in PR checks
2. Deploy ingestion agents with local buffering
3. Configure hot/warm ILM policies for short-term indexes
4. Implement nightly archive job to write compressed NDJSON/Parquet to S3
5. Add S3 lifecycle rules to transition/archive and expire
6. Add restore tests and monitoring

---

## Appendix: Quick S3 Archive Commands

Export (example using `es2json` or `curator`):

```bash
# Export daily index to ndjson and upload to S3
es2json --index "app-2025.12.23" > app-2025-12-23.ndjson
gzip app-2025-12-23.ndjson
aws s3 cp app-2025-12-23.ndjson.gz s3://company-logs/app/2025/12/23/
```

Set lifecycle via AWS CLI:

```bash
aws s3api put-bucket-lifecycle-configuration --bucket company-logs --lifecycle-configuration file://lifecycle.json
```

---

## Sample Prompt for Policy Generation (copy/paste)

```
Create a Log Management Policy for service X:
- Include structured schema (JSON) with mandatory fields
- Define retention tiers: hot 14d, warm 90d, cold 3y
- Provide Fluent Bit and Vector examples for ingestion and transforms
- Provide S3 lifecycle rules and a sample GitHub Actions archive job
- Provide access control and encryption recommendations
- Provide a restore-testing checklist and schedule
- Output the policy in markdown with examples and a short migration timeline
```

---

## Next Steps & Verification

- Add `log-management.md` to the repo docs and link from `/docs/`
- Implement schema validation in CI (PR checks)
- Create an `export-logs-to-s3.sh` script and schedule a daily job
- Run a restore test and record the result

---

File: `operations/logging/log-management.md`
