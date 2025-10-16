
# Project: HealthCore — Enterprise-grade hospital platform with domain-driven modular monolith, microservices readiness, AKS deployment, full observability, and FHIR alignment. [web:38][web:40]

## STATUS.md Policy

- Always update on start and completion: what changed, measurable SLO deltas, links to PRs, OpenAPI changelog, k6 reports, dashboards; list blockers and the next step with Definition of Done. [web:38]

## Guiding Objectives

- Build a hospital platform covering patient management, scheduling, beds/ICU/CCU, results and imaging, 24x7 staffing, specialties, and secure result access, with a modular monolith first and a deliberate path to microservices on AKS with strong observability and security. [web:38]
- Enforce industry-aligned interoperability using HL7/FHIR for patients, appointments, observations, diagnostic reports, and imaging workflows. [web:40]
- Automate quality gates (lint, SAST, tests, contract checks, performance, container scanning) and enforce API versioning and backward compatibility. [web:55]

## Architecture Strategy

- Start as a modular monolith with strict bounded contexts and clean layers (API, Application/Services, Domain, Infrastructure); extract services via the Strangler pattern once domain boundaries stabilize. [web:38]
- One datastore per future service boundary (no cross-schema joins), enabling later migration to isolated databases on AKS/Azure managed stores without coupling. [web:38]
- Security by design: RBAC, tenant-aware authorization, encryption in transit/at rest, audit logs, principle of least privilege; secrets in Key Vault; gateway/service mesh ready. [web:38]

## Bounded Contexts

- Patients
- Practitioners (medical and nursing staff)
- Scheduling (appointments/exams)
- Admissions & Beds (ward/ICU/CCU)
- Results & Imaging (reports, observations, DICOM metadata)
- Shifts & Availability (24x7 operations)
- Departments/Specialties (oncology, cardiology, pediatrics, OB/GYN, imaging)
- Orders & Referrals (ServiceRequest/encounters)
- Notifications (candidate for first extraction)
- Billing/Authorizations (optional future)
- Admin/Identity & Access

## Roadmap (Phased)

### Phase 0 — Repository, Tooling, Conventions & Governance

- Mandatory Status Discipline: first action for any task is to update STATUS.md to “In Progress” with owner and branch; upon completion, update with results and evidence. [web:38]
- Git Workflow and Commit Policy:
  - Branching Strategy: trunk-based; work only on short-lived branches from main. [web:38]
  - Branch Naming: type/scope/short-description (e.g., feature/patients/implement-fhir-patient-model). [web:55]
  - Commit Messages: Conventional Commits; all code, comments, and docs in English. [web:55]
- Architecture Decision Records (ADRs): log all significant decisions in adr/ with context, options, and consequences. [web:38]
- Module Scaffolding Template: apps/_template with services, repositories, domain events, DTOs, validators, OpenAPI stub, tests, health/metrics/tracing, Helm values, and CI fragments. [web:38]
- Contributor Rules: English-only; no cross-domain DB joins; update OpenAPI, tests, and STATUS.md in every PR; add OpenAPI changelog and deprecation notices when applicable. [web:55]
- Dev Container: Docker, buildx, kubectl, helm, k9s, azure-cli, make, tilt/skaffold, OpenAPI tools, k6, OpenTelemetry CLI; ruff/black/mypy/pytest preinstalled. [web:38]
- API Versioning: URI-based /api/v1 with optional Accept header versioning; add Deprecation and Sunset headers; CI check blocks breaking changes without a new version. [web:55]
- Contract-first APIs: OpenAPI per module; generate SDKs and run consumer-driven contract tests in CI. [web:55]
- Multi-tenancy policy: tenant resolution from JWT claim/header; strict tenant scoping on queries and caches; data partitioning strategy documented. [web:38]

### Phase 1 — Core Domain Modeling (Patients, Practitioners)

- Implement Patients and Practitioners with FHIR-aligned fields and strong auditing; one schema per domain; repository interfaces; seed data. [web:40]
- Add authentication, RBAC, tenant claim resolution, and audit logging; correlation-id middleware; rate limits on auth-sensitive endpoints. [web:38]
- Expose initial v1 endpoints and run E2E locally via devcontainer/compose; include OpenAPI and contract tests as gates. [web:55]

### Phase 2 — Scheduling and Admissions/Beds

- Scheduling: appointments, slots, exam prep rules, conflicts/rescheduling, waitlist; business rules per specialty. [web:55]
- Admissions & Beds: occupancy, ward/ICU/CCU tracking, patient stay time (LOS), transfers, discharge; constraints for isolation and equipment. [web:38]
- Domain events: AppointmentCreated, BedAssigned, AdmissionStarted published to an internal event bus abstraction ready for Kafka/Service Bus. [web:38]

### Phase 3 — Results & Imaging

- Diagnostic Reports and Observations with FHIR mapping; ingest text and imaging metadata; secure retrieval and fine-grained authorization. [web:40]
- Retention policies and access controls with immutable audit trails; support for report attachments and references to ImagingStudy. [web:40]

### Phase 4 — 24x7 Shifts & Specialties

- Shifts & Availability with staffing constraints; integration into scheduling; department-level calendars. [web:38]
- Departments/Specialties as feature-flagged subdomains, exposing rules through APIs/events with compatibility guarantees. [web:55]

### Phase 5 — Observability, APM, Performance

- Prometheus metrics, structured logs, and distributed tracing via OpenTelemetry; exporters to DataDog/New Relic; standard labels for tenant and endpoint. [web:38]
- SLIs/SLOs per endpoint (P50/P95/P99, error rate) with alerting; k6 load/stress/soak test suites with CI thresholds and automatic regression gating. [web:38]

### Phase 6 — Resilience, Caching, Events

- Timeouts, retries (exponential backoff + jitter), circuit breakers, bulkheads; idempotency keys for all mutating POST operations. [web:38]
- Redis caching: cache-aside/read-through; ETag/If-None-Match for GET; event-driven invalidation wired to domain events. [web:38]
- Event sourcing selectively for Admissions & Beds to preserve full temporal history; other domains rely on event-carried state and audit logs. [web:38]

### Phase 7 — Kubernetes/AKS Delivery

- Helm charts per module with Deployment, Service, HPA, PDB, NetworkPolicy, Ingress, probes, resource limits/requests, tolerations/affinity; Key Vault CSI for secrets. [web:38]
- AKS advanced patterns: Entra Workload ID, restricted egress, Azure Monitor/OTel for logs/metrics/traces, multi-AZ and multi-region guidance, cost- and SLO-aware autoscaling policies. [web:38]
- Prefer managed data services (Azure SQL/Cosmos) or PVs via Azure Disk/Files for state when justified; avoid node-local persistence for critical data. [web:38]

### Phase 8 — CI/CD and Compliance

- CI: build/test/lint/typecheck/contract tests/SAST/image scan/SBOM; ephemeral namespaces for integration tests; performance gates with k6; artifact signing and image provenance. [web:55]
- CD: staged releases, canary on AKS, automated rollback; policy checks: non-root images, resource quotas, egress policies, NetworkPolicy coverage, API deprecation headers. [web:38]
- Compliance: immutable audit logs and secure retention; regular key rotations; API catalog with lifecycle policies and deprecation timelines. [web:38]

### Phase 9 — Extraction to Microservices

- Strangler pattern: extract Notifications first, then Scheduling or Results; maintain stable contracts and per-service data; observe parity metrics before cutting traffic. [web:38]
- Introduce API gateway and/or service mesh (MTLS, retries, timeouts, tracing propagation) as extractions proceed. [web:38]

## Discipline & Policies

### Status Discipline (STATUS.md)

- Before starting: set item to In Progress with owner and branch; include planned SLOs and acceptance criteria. [web:55]
- After completing: document shipped changes (PR links, OpenAPI diffs), evidence (dashboards, k6, coverage), and Next Step with DoD and owners. [web:38]

## API Endpoints (v1, sample paths)

### Patients

- POST /api/v1/patients — create patient; returns FHIR-aligned identifier; audit trail entry. [web:40]
- GET /api/v1/patients?name=&dob=&identifier= — search with filters and pagination; tenant-scoped. [web:55]
- GET /api/v1/patients/{id} — retrieve patient with consents and allergies summary; ETag support. [web:40]
- PATCH /api/v1/patients/{id} — partial update with audit reason; optimistic concurrency. [web:55]
- GET /api/v1/patients/{id}/history — audit and event stream slice for the patient. [web:38]

### Practitioners

- POST /api/v1/practitioners — create practitioner (role, specialties, credentials). [web:55]
- GET /api/v1/practitioners?specialty=&status= — filterable listing; availability flag. [web:55]
- GET /api/v1/practitioners/{id} — profile with active privileges and department associations. [web:55]
- PATCH /api/v1/practitioners/{id} — update scoped by RBAC. [web:38]

### Scheduling

- POST /api/v1/appointments — book appointment/exam with slot validation and prep instructions. [web:55]
- GET /api/v1/appointments?patientId=&practitionerId=&dateFrom=&dateTo= — list/filter. [web:55]
- GET /api/v1/appointments/{id} — appointment details, status transitions. [web:55]
- POST /api/v1/appointments/{id}/reschedule — safe conflict resolution and audit. [web:55]
- POST /api/v1/appointments/{id}/cancel — business rules and waitlist promotion. [web:55]
- GET /api/v1/slots?department=&modality=&date= — discover availability by department/modality. [web:55]

### Admissions & Beds

- POST /api/v1/admissions — start admission; link patient and initial ward. [web:38]
- POST /api/v1/admissions/{id}/transfer — move between wards/ICU/CCU; record timestamps. [web:38]
- POST /api/v1/admissions/{id}/discharge — close admission and compute LOS. [web:38]
- GET /api/v1/beds?ward=&icu=true — current bed inventory, occupancy, isolation flags. [web:38]
- POST /api/v1/beds/{id}/assign — assign patient to bed with constraints and idempotency key. [web:38]

### Results & Imaging

- POST /api/v1/results — create DiagnosticReport (links to Observations and optional document attachments). [web:40]
- GET /api/v1/results?patientId=&type=&dateFrom=&dateTo= — filtered listing with RBAC. [web:55]
- GET /api/v1/results/{id} — retrieve DiagnosticReport with references to Observations. [web:40]
- GET /api/v1/observations/{id} — retrieve Observation (lab values, imaging findings). [web:40]
- POST /api/v1/imaging/studies — register ImagingStudy metadata (DICOM-aligned references). [web:43]
- GET /api/v1/imaging/studies?patientId=&modality= — list studies with series/instance counts. [web:43]

### Shifts & Availability

- POST /api/v1/shifts — create staffing shift; constraints and overlap validation. [web:38]
- GET /api/v1/shifts?department=&date= — list shifts for scheduling views. [web:38]
- GET /api/v1/practitioners/{id}/availability?date= — compute availability across shifts/scheduling. [web:55]

### Departments/Specialties

- GET /api/v1/departments — list departments with capabilities. [web:55]
- GET /api/v1/departments/{id}/rules — fetch domain rules/flags (feature-flag aware). [web:55]

### Orders & Referrals

- POST /api/v1/orders — create ServiceRequest/referral linking patient, practitioner, and department. [web:55]
- GET /api/v1/orders?patientId=&status= — list and track fulfillment lifecycle. [web:55]

### Notifications (candidate microservice)

- POST /api/v1/notifications — enqueue notification (email/SMS/push). [web:55]
- GET /api/v1/notifications/{id}/status — delivery status. [web:55]

### Admin/Identity

- POST /api/v1/tenants — create tenant (optional multi-tenancy). [web:38]
- GET /api/v1/me — current principal, roles, tenant, permissions. [web:38]

### Observability/Health

- GET /health/live — liveness probe. [web:38]
- GET /health/ready — readiness probe (downstream checks). [web:38]
- GET /metrics — Prometheus metrics. [web:38]
- Trace context on all requests (correlation-id, baggage); propagate via OTel. [web:38]

## Data Model Skeleton (models blueprint, not code)

### Patients

- Patient: id (UUID), identifiers (MRN, national id), name (given, family), birthDate, sex, contact info, address, weight, height, BMI (derived), allergies (list), conditions (pre-existing), pastSurgeries (list), medications (current), consents (scoped), emergencyContacts, primaryPractitionerId, preferredLanguage, communicationPreferences, tenantId, createdAt, updatedAt, version. [web:40]
- Allergy: substance, reaction, severity, recordedDate. [web:40]
- Condition: code, onsetDate, status, notes. [web:40]
- Consent: scope, policyRef, grantedAt, revokedAt. [web:40]

### Practitioners

- Practitioner: id, name, role (physician, nurse, tech), specialties (list), licenseNumbers, credentials, departments (refs), availabilityDefaults, privileges, active, tenantId, createdAt, updatedAt, version. [web:55]
- DepartmentMembership: practitionerId, departmentId, privileges, effectiveFrom, effectiveTo. [web:55]

### Scheduling

- Appointment: id, patientId, practitionerId, departmentId, type (consultation, exam), modality (imaging), location, startTime, endTime, status (booked, rescheduled, cancelled, completed), prepInstructions, notes, waitlistRank, tenantId, createdAt, updatedAt, version. [web:55]
- Slot: id, departmentId, modality, startTime, endTime, capacity, reserved, tenantId. [web:55]
- RescheduleHistory: appointmentId, fromTime, toTime, reason, actorId, at. [web:55]

### Admissions & Beds

- Admission: id, patientId, status (active, transferred, discharged), startedAt, endedAt, currentWardId, currentBedId, acuityLevel, isolationRequired, notes, tenantId, version. [web:38]
- Transfer: id, admissionId, fromWardId, toWardId, fromBedId, toBedId, at, reason. [web:38]
- Bed: id, wardId, type (standard, ICU, CCU, isolation), status (free, reserved, occupied, cleaning), features (ventilator, negativePressure), tenantId, version. [web:38]
- Ward: id, name, departmentId, capacity, features, tenantId. [web:38]

### Results & Imaging

- DiagnosticReport: id, patientId, status, category (lab, imaging), code, issuedAt, performerIds, conclusionText, conclusionCodes, mediaRefs, observationIds, documentUri/hash, imagingStudyRefs, tenantId, version. [web:40]
- Observation: id, patientId, code, value[x] (quantity, codeableConcept, text), unit, referenceRange, effectiveAt, performerId, interpretation, relatedReportId, tenantId, version. [web:40]
- ImagingStudy: id, patientId, modality, startedAt, numberOfSeries, numberOfInstances, dicomStudyUid, seriesMetadata, authorizationTrace, tenantId, version. [web:43]

### Shifts & Availability

- Shift: id, departmentId, role, startTime, endTime, requiredCount, assignedPractitionerIds, constraints, tenantId, version. [web:38]
- PractitionerAvailability: practitionerId, date, availableWindows, notes, tenantId. [web:38]

### Departments/Specialties

- Department: id, name, type, capabilities (flags), contact, tenantId. [web:55]
- SpecialtyRule: id, departmentId, ruleKey, ruleValue (JSON), effectiveFrom, effectiveTo. [web:55]

### Orders & Referrals

- Order (ServiceRequest): id, patientId, requesterPractitionerId, departmentId, reasonCode, priority, status, scheduledFor, linkedAppointmentId, tenantId, version. [web:40]

### Notifications

- Notification: id, recipient (patient/practitioner/contact), channel (email/SMS/push), templateKey, payload (JSON), status, attempts, lastError, tenantId, version. [web:55]

### Admin/Identity

- Tenant: id, name, slug, settings (JSON), status, createdAt, updatedAt. [web:38]
- Role: id, name, permissions (list), tenantId. [web:38]
- UserPrincipal: id, externalId, displayName, roles, tenantId. [web:38]

### Cross-cutting

- AuditLog: id, actorId, action, resourceType, resourceId, before (JSON), after (JSON), at, tenantId. [web:38]
- OutboxEvent: id, aggregateType, aggregateId, eventType, payload (JSON), occurredAt, publishedAt, retries. [web:38]

## Interoperability (FHIR)

- Map Patient ↔ FHIR Patient; Appointment ↔ FHIR Appointment; Observation ↔ FHIR Observation; DiagnosticReport ↔ FHIR DiagnosticReport; ImagingStudy ↔ FHIR ImagingStudy; ensure references and workflow semantics are coherent. [web:40]
- Imaging workflows: DiagnosticReport should reference Observations and ImagingStudy; follow IHE radiology guidance for structured report composition when applicable. [web:34]

## Observability and APM

- Expose /metrics including HTTP, DB, cache, and queue metrics; label by tenant and endpoint; use OTel for distributed traces; export to DataDog/New Relic; centralize logs in Azure Monitor/Log Analytics. [web:38]
- Define SLIs/SLOs and alerts (e.g., P95 latency and error rate per endpoint); run k6 suites (smoke, ramp-up, stress, soak) with CI thresholds. [web:38]

## Resilience and Performance

- Defaults: timeouts, retries with exponential backoff + jitter, circuit-breakers, bulkheads; idempotency keys on all mutating POST operations. [web:38]
- Pagination, ETag/If-None-Match, gzip/br compression; defensive validation and rate limiting on hot endpoints. [web:55]

## Caching Strategy

- Redis cache-aside for read-heavy resources; read-through for reference data; write-through only by exception; cache keys include tenant; invalidation on domain events. [web:38]

## Kubernetes/AKS Manifests

- Helm per module/service: Deployment, Service, HPA, PDB, NetworkPolicy, Ingress, probes, resource limits/requests, tolerations/affinity; Key Vault CSI for secrets; optional OTel sidecar/agent. [web:38]
- Use managed data services (Azure SQL/Cosmos) or PVs via Azure Disk/Files for state; avoid node-local persistence for critical data. [web:38]

## CI/CD and Governance

- CI stages: lint/typecheck/tests/coverage, contract tests (OpenAPI diff), SAST, image build+scan, SBOM; integration tests in ephemeral namespaces; k6 gates; artifact signing and provenance. [web:55]
- CD: canary releases on AKS with automated rollback; enforce non-root images, resource quotas, NetworkPolicy coverage, egress restrictions; publish API deprecations. [web:38]

## Microservices Extraction Criteria

- Candidate service has isolated data, stable contracts, clear team ownership; extract Notifications first, then Scheduling or Results; measure parity and cut traffic gradually. [web:38]

## MCP and Best Practices Automation

- Provide a Scaffolding CLI to generate modules/services with standard layers, OpenAPI stubs, health/metrics/tracing, tests, Helm chart, and CI fragments; enforce ADR creation and checklists. [web:55]

## Contributor Rules

- English only; domain-driven naming; no shared cross-domain DB joins; every PR updates OpenAPI, tests, and STATUS.md; breaking changes require a new API version and deprecation headers. [web:55]


```

This version adds Orders/Referrals, multi-tenancy enforcement, explicit SLO practices, imaging authorization trace, and operational rigor on AKS and API design while strengthening FHIR alignment and contract governance for an enterprise-grade delivery path.[4][2][3]
