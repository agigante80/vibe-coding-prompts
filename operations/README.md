# Operations Prompts

Prompts for establishing and maintaining operational excellence: logging, monitoring, incident response, and infrastructure management.

## 🎯 Purpose

Operations prompts help you build reliable, observable, and maintainable systems by establishing industry best practices for logging, monitoring, alerting, and operational procedures.

## 📋 Available Prompts

### [Logging Implementation & Best Practices](./logging-implementation-best-practices.md)
**Word Count**: ~2850 words | **Platform**: ChatGPT, Claude, Gemini (Copilot Chat)

**What it does**: Comprehensive logging implementation generator that:
- Auto-detects project language and existing logging setup
- Generates structured JSON logging configuration
- Creates log rotation and retention policies
- Establishes long-term archival strategies (S3/GCS)
- Implements PII redaction and security controls
- Sets up log aggregation pipelines (Fluent Bit/Vector)
- Integrates with observability platforms (ELK, Loki, CloudWatch)
- Generates monitoring and alerting for log pipelines

**When to use**:
- ✅ New projects needing logging standards
- ✅ Migrating from unstructured to structured logging
- ✅ Implementing compliance requirements (HIPAA, PCI-DSS, GDPR)
- ✅ Setting up centralized logging infrastructure
- ✅ Establishing log rotation and long-term retention
- ✅ Quarterly logging practice reviews

**Outputs**:
- Language-specific structured logging configuration
- Log rotation configs (logrotate, Docker, application-level)
- Archive automation (S3/GCS lifecycle policies, export scripts)
- Ingestion pipeline setup (Fluent Bit/Vector/Fluentd)
- Monitoring dashboards and alert rules
- Comprehensive documentation and runbooks

---

## 🔄 Usage Patterns

### For New Projects
1. Run [Logging Implementation](./logging-implementation-best-practices.md) during initial setup (Week 1-2)
2. Establish structured logging before writing business logic
3. Configure rotation and retention early to avoid disk issues
4. Set up basic monitoring and alerting from day one

### For Existing Projects
1. Run during project reassessment or quarterly reviews
2. Migrate incrementally from unstructured to structured logs
3. Add rotation/compression to prevent disk exhaustion
4. Establish archive pipeline for compliance requirements

### Maintenance Schedule
- **Weekly**: Review log volume and costs
- **Monthly**: Check rotation is working, validate PII redaction
- **Quarterly**: Test archive restore, review retention policies
- **Annually**: Full logging infrastructure audit

---

## 🚀 Quick Start

1. **Choose your scenario**:
   - New project → Full implementation from scratch
   - Existing project → Assessment and incremental migration
   - Compliance need → Focus on retention and archive sections

2. **Copy the prompt** to your AI assistant (ChatGPT, Claude, Copilot Chat)

3. **Let AI detect context**:
   - Project language and framework
   - Existing logging libraries
   - Deployment environment
   - Compliance requirements

4. **Review generated outputs**:
   - Logging configuration files
   - Rotation and retention policies
   - Archive automation scripts
   - Monitoring and alerting rules

5. **Implement in phases**:
   - Phase 1: Structured logging (Week 1)
   - Phase 2: Rotation and local retention (Week 1-2)
   - Phase 3: Aggregation and observability (Week 2-3)
   - Phase 4: Archive and compliance (Week 3-4)
   - Phase 5: Monitoring and hardening (Week 4)

---

## 💡 Best Practices

### Structured Logging
- Always use JSON format with consistent schema
- Include required fields: `ts`, `level`, `service`, `env`, `message`
- Add correlation IDs: `trace_id`, `request_id` for distributed tracing
- Never log PII, passwords, tokens, or sensitive data

### Log Rotation
- Rotate by size (100-500 MB) AND time (daily minimum)
- Compress immediately after rotation (gzip or zstd)
- Keep 7-30 days locally, archive the rest
- Test rotation doesn't lose log entries

### Long-Term Retention
- Use tiered storage: hot (7-30d), warm (30-90d), cold (90d+)
- Archive to object storage (S3/GCS) with lifecycle rules
- Compress archives (NDJSON.gz or Parquet)
- Test restore quarterly from archive

### Observability
- Integrate logs with traces and metrics
- Use consistent correlation IDs across systems
- Set up dashboards for log volume and error rates
- Alert on pipeline failures and high error rates

### Security
- Implement PII redaction at log emission
- Encrypt logs in transit (TLS) and at rest (KMS)
- Restrict log access with IAM/RBAC
- Support legal holds for compliance

---

## 📚 Related Resources

- [Log Management Policy & Templates](./log-management.md) - Policy document and prompt templates
- [Documentation Standardization](../documentation/documentation-standardization.md) - For documenting logging practices
- [Security Audit Generator](../security/security-audit-generator.md) - For security review of logging practices

---

## 🤝 Contributing

See [Prompt Creation Guide](../PROMPT_CREATION_GUIDE.md) for guidelines on creating new operations prompts.

Planned operations prompts:
- [ ] Performance Optimization & Profiling
- [ ] Error Tracking Integration (Sentry, Datadog)
- [ ] Incident Response Runbook Generator
- [ ] SRE Best Practices Implementation
- [ ] Capacity Planning & Resource Optimization

---

*Operational excellence through automation and best practices.* 🔧✨
