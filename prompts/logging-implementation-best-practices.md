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

**Configuration**:
- **Dev**: 50-100MB files, 3-7 days local
- **Prod**: 100-500MB files, 7-30 days local, gzip/zstd, 1-7 years archive
- **Audit**: 100-200MB files, 30-90 days local, 7-10 years archive

**Strategy**: Size-based (100-500MB) + daily rotation, compress after rotation, keep 24-48h uncompressed

**Tools**: logrotate (Linux), Docker logging driver (`max-size: 100m`, `max-file: 7`), app-level libraries (winston-daily-rotate-file, python-logrotate)

### 📦 **Long-Term Archive & Lifecycle**

**Tiered storage**: Hot tier (7-30d) for indexed logs in Elasticsearch/Loki/CloudWatch, warm tier (30-90d) with reduced replicas, cold tier/archive (90d→7+yrs) in object storage (S3/GCS) with lifecycle rules (transition to Glacier after 365d)

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

---

## **Deliverables**

1. **Logging library config**: Structured logging setup, JSON formatter, correlation middleware, PII redaction
2. **Rotation config**: logrotate config, Docker logging driver, compression/retention settings
3. **Archive automation**: S3/GCS lifecycle policy, log export script, GitHub Actions workflow
4. **Ingestion pipeline**: Fluent Bit/Vector config, aggregation architecture, schema validation
5. **Monitoring**: Prometheus metrics, alert rules, Grafana dashboard, SLO definitions
6. **Documentation**: Policy doc (retention, PII, compliance), developer guide, runbook, schema docs

**Update `/docs/`**: OPERATIONS.md (architecture, levels, schema, retention), ARCHITECTURE.md (observability, pipeline), SECURITY_AND_PRIVACY.md (PII handling, access control, audit)

---

## **Success Criteria**

- [ ] Structured JSON logging with required fields (ts, level, service, env, message) and correlation IDs
- [ ] PII redaction working (verified with tests)
- [ ] Log rotation configured and tested (files <500MB, compressed, 7-30d retention)
- [ ] Archive pipeline operational (exported to S3/GCS daily, lifecycle policies applied, Glacier transition after 365d)
- [ ] Log aggregation operational (ingestion lag <60s, alerts for error rates)
- [ ] Documentation complete (developer guide, runbook, restore tested)

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

**Phase 1 (Week 1)**: Implement structured logging library, add required fields/JSON formatting, configure log levels, add correlation ID middleware, implement PII redaction

**Phase 2 (Week 1-2)**: Configure log rotation (logrotate/app-level), set file size/retention/compression, test rotation

**Phase 3 (Week 2-3)**: Deploy log shipping agents, configure ingestion pipeline, set up storage (Elasticsearch/Loki), create dashboards, implement correlation with traces/metrics

**Phase 4 (Week 3-4)**: Set up object storage (S3/GCS), create export automation, schedule daily archive jobs, apply lifecycle policies, test restore, document retention policy

**Phase 5 (Week 4)**: Configure pipeline health metrics, set up alerting, test failure scenarios, document runbooks, train team

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

---

File: `operations/logging-implementation-best-practices.md`
