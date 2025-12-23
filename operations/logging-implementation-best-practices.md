# Logging Implementation & Best Practices Generator

## **Objective**

Assess current logging practices and generate a comprehensive, production-ready logging implementation plan that establishes structured logging, log rotation, retention policies, security controls, and observability integration for any project.

---

## **Assessment Phase**

### 1. **Project Analysis**

Auto-detect and analyze:

* **Technology Stack**:
  - Detect project type and language (Python, Node.js, Java, Go, Rust, PHP, etc.)
  - Identify existing logging libraries (Winston, Pino, Log4j, Logback, slog, etc.)
  - Analyze application architecture (monolith, microservices, serverless)
  - Detect deployment environment (Docker, Kubernetes, bare metal, cloud)

* **Current Logging State**:
  - Review existing log statements and formats
  - Identify log levels in use (debug, info, warn, error)
  - Check for structured vs. unstructured logging
  - Assess log file locations and naming conventions
  - Review existing rotation/retention configurations

* **Infrastructure Context**:
  - Detect log aggregation tools (ELK, Loki, Splunk, CloudWatch, etc.)
  - Identify container runtime log drivers
  - Check for centralized logging infrastructure
  - Review existing monitoring/alerting on logs

### 2. **Compliance & Operational Requirements**

Analyze requirements based on:

* **Industry/Domain**:
  - Healthcare (HIPAA) → 7+ year retention, audit trails
  - Finance (PCI-DSS, SOX) → 7-10 year retention, immutable logs
  - E-commerce → 1-3 years, PCI compliance for payment logs
  - SaaS/General → 30-90 days hot, 1-3 years archive

* **Operational Needs**:
  - Development vs. Production environments
  - Debug requirements and sampling strategies
  - Performance constraints (high-volume services)
  - Storage budget and costs

---

## **Logging Standards to Implement**

### 🗂️ **Structured Logging Schema**

**What to implement**:
- JSON-formatted log entries with consistent schema
- Required fields: `ts` (ISO 8601), `level`, `service`, `env`, `message`
- Correlation fields: `trace_id`, `request_id`, `span_id` (for distributed tracing)
- Contextual fields: `user_id`, `path`, `method`, `status`, `latency_ms`
- Metadata field: `meta` object for additional context

**Example schema** (language-agnostic):

```json
{
  "ts": "2025-12-23T12:34:56.789Z",
  "level": "info",
  "service": "auth-service",
  "env": "production",
  "instance_id": "i-0123456789abcd",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "request_id": "req-12345",
  "user_id": "user-987",
  "path": "/api/login",
  "method": "POST",
  "status": 200,
  "latency_ms": 52,
  "message": "User logged in successfully",
  "meta": { "client": "web", "ip": "192.168.1.1" }
}
```

**Language-specific implementation**:

| Language | Recommended Library | Configuration |
|----------|-------------------|---------------|
| **Node.js** | Pino, Winston | JSON formatter, correlation middleware |
| **Python** | structlog, python-json-logger | JSON renderer, context binding |
| **Java** | Logback + logstash-logback-encoder | JSON layout, MDC for context |
| **Go** | slog (stdlib), zap, zerolog | JSON handler, structured fields |
| **Rust** | tracing, slog | JSON subscriber, span context |
| **PHP** | Monolog | JSON formatter, processors |

### 📊 **Log Levels & Sampling Strategy**

**Default levels** (production):
- `fatal`/`error` → Always emit, immediate alerting
- `warn` → Always emit, review regularly
- `info` → Default production level, key business events
- `debug` → Sample 1-5%, or on-demand via feature flags
- `trace` → Disabled in production, or <1% sample

**Sampling implementation**:
- Use probabilistic sampling for debug/trace logs
- Sample by trace ID for distributed request sampling
- Allow runtime log level adjustment (no restart required)
- Implement rate limiting per service/host to prevent log storms

**Code example patterns**:

```javascript
// Node.js with Pino - sampling
const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  formatters: { level: (label) => ({ level: label }) },
  // Sample debug logs at 5%
  hooks: {
    logMethod(args, method) {
      if (this.level === 'debug' && Math.random() > 0.05) return;
      method.apply(this, args);
    }
  }
});
```

```python
# Python with structlog - sampling
import structlog
import random

def sample_debug(logger, method_name, event_dict):
    if event_dict.get('level') == 'debug' and random.random() > 0.05:
        raise structlog.DropEvent
    return event_dict

structlog.configure(processors=[sample_debug, structlog.processors.JSONRenderer()])
```

### 🔐 **Security & PII Handling**

**Redaction rules** (implement at log emission):
- Never log: passwords, tokens, API keys, credit cards, SSNs
- Hash/mask: email addresses, phone numbers, IP addresses (if PII)
- Truncate: long request/response bodies (first 200 chars)
- Allow-list: only log known-safe fields

**Implementation checklist**:
- [ ] Configure automatic PII redaction in logging library
- [ ] Use field-level allow-lists instead of block-lists
- [ ] Store hashed identifiers for audit requirements
- [ ] Implement log sanitization processors/middleware
- [ ] Add unit tests for redaction logic
- [ ] Document PII handling policy

**Example redaction config**:

```yaml
# Logstash/Fluentd filter example
<filter app.**>
  @type record_modifier
  <replace>
    key password
    expression /.+/
    replace [REDACTED]
  </replace>
  <replace>
    key credit_card
    expression /.+/
    replace [REDACTED]
  </replace>
</filter>
```

### 🔄 **Log Rotation & Retention**

**Industry-standard configuration**:

| Environment | File Size | Local Retention | Compression | Archive Retention |
|------------|-----------|----------------|-------------|------------------|
| **Development** | 50-100 MB | 3-7 days | Optional | None |
| **Production** | 100-500 MB | 7-30 days | gzip/zstd | 1-7 years |
| **Audit Logs** | 100-200 MB | 30-90 days | Required | 7-10 years |

**Rotation strategy**:
- Primary trigger: Size-based (100-500 MB per file)
- Secondary trigger: Daily rotation at minimum
- Compress immediately after rotation (gzip or zstd)
- Keep last 24-48h uncompressed for quick access

**logrotate configuration** (Linux):

```bash
/var/log/myapp/*.log {
    daily
    rotate 14
    maxsize 100M
    compress
    delaycompress
    missingok
    notifempty
    create 0640 appuser appgroup
    sharedscripts
    postrotate
        systemctl reload myapp || true
    endscript
}
```

**Docker/container configuration**:

```yaml
# docker-compose.yml
services:
  app:
    logging:
      driver: "json-file"
      options:
        max-size: "100m"
        max-file: "7"
        compress: "true"
```

**Application-level rotation** (Node.js example):

```javascript
const winston = require('winston');
require('winston-daily-rotate-file');

const transport = new winston.transports.DailyRotateFile({
  filename: 'app-%DATE%.log',
  datePattern: 'YYYY-MM-DD',
  maxSize: '100m',
  maxFiles: '14d',
  compress: true,
  zippedArchive: true
});
```

### 📦 **Long-Term Archive & Lifecycle**

**Archival strategy** (tiered storage):

1. **Hot tier** (7-30 days):
   - Full indexed logs in Elasticsearch/Loki/CloudWatch
   - Fast queries, dashboards, real-time alerting
   - High cost per GB

2. **Warm tier** (30-90 days):
   - Reduced replicas, higher compression
   - Slower queries acceptable
   - Medium cost

3. **Cold tier/Archive** (90 days → 7+ years):
   - Object storage (S3/GCS/Azure Blob)
   - Compressed NDJSON or Parquet format
   - Lifecycle rules: transition to Glacier after 365 days
   - Low cost, restore latency acceptable

**S3 lifecycle policy example**:

```json
{
  "Rules": [
    {
      "ID": "LogArchival",
      "Filter": {"Prefix": "logs/"},
      "Status": "Enabled",
      "Transitions": [
        {"Days": 90, "StorageClass": "STANDARD_IA"},
        {"Days": 365, "StorageClass": "GLACIER"}
      ],
      "Expiration": {"Days": 2555}
    }
  ]
}
```

**Archive export automation** (GitHub Actions):

```yaml
name: Archive Logs
on:
  schedule:
    - cron: '0 2 * * *'
jobs:
  archive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Export logs to S3
        run: ./scripts/export-logs-to-s3.sh --from-yesterday
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### 🔍 **Observability Integration**

**Correlation with other signals**:
- Share `trace_id` between logs and distributed traces (Jaeger, Zipkin)
- Link logs to metrics using common labels (service, env, instance)
- Include `request_id` in HTTP responses for user support debugging

**Log aggregation pipeline**:

```
Application → Local Buffer → Agent (Fluent Bit/Vector) 
  → Kafka (optional) → Processing (Logstash/Vector) 
  → Storage (Elasticsearch/Loki) → Visualization (Grafana/Kibana)
```

**Fluent Bit output example**:

```ini
[OUTPUT]
    Name  elasticsearch
    Match *
    Host  elasticsearch.internal
    Port  9200
    Index app-logs
    Type  _doc
    Retry_Limit 5

[OUTPUT]
    Name  s3
    Match *
    bucket  company-logs
    total_file_size  50M
    s3_key_format /app-logs/%Y/%m/%d/%H/%M/%S-${UUID}.json.gz
```

### 📈 **Monitoring & Alerting**

**Key metrics to monitor**:
- Log ingestion rate (logs/second)
- Log pipeline lag (time from emission to indexing)
- Error log rate (errors/minute)
- Buffer fill levels (disk usage %)
- Failed log shipments

**Alert examples**:
- Error log rate > 10/min for 5 minutes → Page on-call
- Log pipeline lag > 5 minutes → Warning
- Buffer fill > 80% → Critical
- Failed log exports → Warning

**SLO examples**:
- Log ingestion latency < 60s (P99)
- Log delivery success rate > 99.9%
- Log query response time < 2s (P95)

---

## **Deliverables**

Generate the following outputs based on project context:

1. **Logging Library Configuration**
   - Language-specific structured logging setup
   - JSON formatter with required fields
   - Correlation ID middleware/context binding
   - PII redaction configuration

2. **Log Rotation Configuration**
   - `logrotate` config for Linux systems
   - Docker logging driver configuration
   - Application-level rotation (if applicable)
   - Compression and retention settings

3. **Archive & Lifecycle Automation**
   - S3/GCS lifecycle policy (JSON)
   - Log export script (`scripts/export-logs-to-s3.sh`)
   - Scheduled GitHub Actions workflow for archival
   - Restore verification script

4. **Ingestion Pipeline Setup**
   - Fluent Bit/Vector/Fluentd configuration
   - Log aggregation pipeline architecture
   - Schema validation rules
   - Backpressure and retry configuration

5. **Monitoring & Alerting**
   - Prometheus metrics for log pipeline health
   - Alert rules for error rates and failures
   - Grafana dashboard for log observability
   - SLO definitions

6. **Documentation**
   - Logging policy document (retention, PII, compliance)
   - Developer guide for adding structured logs
   - Runbook for log pipeline troubleshooting
   - Schema documentation and examples

### **Documentation Updates**

Update the following files in `/docs/`:

- **`/docs/OPERATIONS.md`** (or create if missing):
  - Add logging architecture and pipeline diagram
  - Document log levels and when to use each
  - Include log schema and required fields
  - Add retention policy and compliance notes

- **`/docs/ARCHITECTURE.md`**:
  - Add observability section with logging component
  - Document log aggregation pipeline
  - Include correlation ID flow diagram

- **`/docs/README.md`**:
  - Add link to logging documentation
  - Include quick reference for viewing logs

- **`/docs/SECURITY_AND_PRIVACY.md`**:
  - Document PII handling and redaction rules
  - Add log access control policies
  - Include audit log requirements

---

## **Success Criteria**

- [ ] Structured JSON logging implemented across all services
- [ ] Required fields (`ts`, `level`, `service`, `env`, `message`) present in all logs
- [ ] Correlation IDs (`trace_id`, `request_id`) flow through distributed systems
- [ ] PII redaction working correctly (verified with unit tests)
- [ ] Log rotation configured and tested (no log file >500MB)
- [ ] Logs compressed after rotation (gzip or zstd)
- [ ] Local retention policy enforced (7-30 days hot)
- [ ] Archive pipeline operational (logs exported to S3/GCS daily)
- [ ] Lifecycle policies applied (transition to Glacier after 365 days)
- [ ] Log aggregation pipeline operational (ingestion lag <60s)
- [ ] Monitoring alerts configured for error rates and pipeline health
- [ ] Documentation complete and developer guide available
- [ ] Restore tested successfully from archive

---

## **Best Practices**

### **General Logging**
* Log meaningful events, not every function call
* Use appropriate log levels consistently
* Include context (user, request, session) in structured fields
* Never log sensitive data (passwords, tokens, keys)
* Write log messages for humans first (clear, actionable)

### **Performance**
* Use asynchronous logging to avoid blocking application
* Implement sampling for high-volume debug logs
* Buffer logs locally before shipping to aggregation
* Monitor and limit log volume to prevent cost overruns
* Use log levels to reduce production verbosity

### **Reliability**
* Implement local buffering with disk backoff
* Configure retry logic with exponential backoff
* Alert on log pipeline failures
* Test log rotation doesn't lose entries
* Verify archive restore quarterly

### **Security**
* Encrypt logs in transit (TLS) and at rest (KMS)
* Restrict log access with IAM/RBAC
* Audit who accesses archived logs
* Implement legal hold capabilities for compliance
* Use short-lived credentials for log shipping

### **Cost Optimization**
* Keep hot retention minimal (7-30 days)
* Use sampling for debug/trace logs
* Compress logs immediately after rotation
- Archive to object storage early (90 days)
* Query cold archives directly (Athena/BigQuery) instead of rehydrating

---

## **Implementation Phases**

### **Phase 1: Foundation (Week 1)**
1. Implement structured logging library in all services
2. Add required fields and JSON formatting
3. Configure log levels appropriately
4. Add correlation ID middleware
5. Implement basic PII redaction

### **Phase 2: Rotation & Local Retention (Week 1-2)**
1. Configure log rotation (logrotate or app-level)
2. Set file size limits and retention periods
3. Enable compression
4. Test rotation doesn't lose logs
5. Monitor disk usage

### **Phase 3: Aggregation & Observability (Week 2-3)**
1. Deploy log shipping agents (Fluent Bit/Vector)
2. Configure ingestion pipeline
3. Set up log storage (Elasticsearch/Loki)
4. Create dashboards (Grafana/Kibana)
5. Implement correlation with traces/metrics

### **Phase 4: Archive & Compliance (Week 3-4)**
1. Set up object storage (S3/GCS)
2. Create export automation script
3. Schedule daily archive jobs
4. Apply lifecycle policies
5. Test restore from archive
6. Document retention policy

### **Phase 5: Monitoring & Hardening (Week 4)**
1. Configure pipeline health metrics
2. Set up alerting rules
3. Test failure scenarios
4. Document runbooks
5. Train team on log access and troubleshooting

---

## **Usage Instructions**

Run this prompt when:

* Starting a new project and establishing logging standards
* Migrating from unstructured to structured logging
* Implementing compliance requirements (HIPAA, PCI-DSS, GDPR)
* Setting up centralized logging infrastructure
* Preparing for production deployment
* Addressing log management technical debt
* Establishing observability practices
* Quarterly review of logging practices

---

## **Multi-Language Quick Reference**

| Language | Structured Logging | Rotation | Redaction | Correlation |
|----------|------------------|----------|-----------|-------------|
| **Node.js** | Pino, Winston | winston-daily-rotate | pino-noir | cls-hooked |
| **Python** | structlog | logging.handlers.RotatingFileHandler | Custom processor | contextvars |
| **Java** | Logback + Logstash encoder | RollingFileAppender | Logback filters | MDC |
| **Go** | slog, zap | lumberjack | Custom middleware | context.Context |
| **Rust** | tracing | tracing-appender | Custom layer | span context |
| **PHP** | Monolog | RotatingFileHandler | Monolog processors | Request context |

---

File: `operations/logging-implementation-best-practices.md`
