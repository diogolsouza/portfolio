# 🔁 Orchestration & CI/CD — FAA Lakehouse Pipelines

## Objective

The Orchestration & CI/CD layer defines **how data pipelines are coordinated, executed, and deployed** across the Azure Lakehouse architecture.

This layer ensures that ingestion, transformation, and serving processes run:
- In the correct order
- With clear dependencies
- In a repeatable and controlled manner

It also documents the **deployment and promotion mindset** used for this project.

---

## Scope

This layer focuses on:
- Pipeline orchestration and scheduling
- Dependency management across layers
- Parameterization and environment awareness
- CI/CD concepts applied to data engineering assets

It does **not** contain business logic or data transformations.

---

## Orchestration Strategy

### Primary Orchestrator: Azure Data Factory (ADF)

Azure Data Factory is used as the **control plane** for pipeline execution.

ADF is responsible for:
- Triggering ingestion pipelines
- Coordinating Bronze → Silver → Gold execution
- Managing dependencies and retries
- Passing runtime parameters
- Centralizing execution monitoring

Databricks is used as the **execution engine**, not the orchestrator.

---

## Pipeline Dependency Flow

```
ADF Trigger
   │
   ▼
Bronze Ingestion
   │
   ▼
Silver Transformation
   │
   ▼
Gold Serving
   │
   ▼
Synapse Warehouse Load
```

Each stage executes **only after successful completion** of the upstream dependency.

---

## Parameterization Strategy

Pipelines are designed to be **parameter-driven**, enabling reuse and flexibility.

Typical parameters include:
- Processing date / period (year, month)
- Source dataset identifiers
- Environment (dev / test / prod)
- Reprocessing flags

This allows:
- Backfills and reprocessing
- Environment isolation
- Reduced duplication of pipeline definitions

---

## Failure Handling & Retries

Orchestration logic includes:
- Retry policies for transient failures
- Clear failure propagation between stages
- Stop-the-line behavior for critical failures

Pipelines fail fast when:
- Data quality thresholds are breached
- Upstream dependencies fail
- Required inputs are missing

---

## CI/CD Mindset

This project applies **CI/CD principles** adapted for data engineering.

### Version Control
- All pipeline definitions, notebooks, and SQL scripts are versioned in Git
- Changes are reviewed before being merged

---

### Deployment Strategy (Conceptual)

While this portfolio does not deploy live infrastructure, it documents a realistic approach:

- Separate environments (dev / test / prod)
- Promotion via Git branches
- Parameterized deployments
- Infrastructure as Code readiness

Examples may include:
- Azure DevOps or GitHub Actions pipelines
- ARM / Bicep / Terraform templates (skeletons)

---

## Environment Awareness

Pipelines are designed with environment separation in mind:

- Environment-specific configuration
- Isolated storage locations
- Non-shared compute resources

This mirrors real enterprise deployments.

---

## Observability Integration

Orchestration integrates with observability by:
- Emitting execution metadata
- Tracking pipeline start/end times
- Recording execution outcomes

This information feeds the **Observability layer** for monitoring and alerting.

---

## What Is Explicitly Out of Scope

The following are **not responsibilities** of this layer:

- Data transformation logic
- Data quality rule definitions
- Analytics or metric calculations

These belong to downstream processing layers.

---

## Technologies Used

- Azure Data Factory
- Azure Databricks (as execution engine)
- GitHub / Git
- CI/CD pipelines (conceptual)
- Infrastructure as Code (conceptual)

---

## Outcome

This layer provides **reliable, repeatable, and maintainable pipeline execution**, ensuring that the FAA Lakehouse operates as a cohesive system rather than a collection of disconnected jobs.

By separating orchestration concerns from transformation logic, the architecture improves **clarity, debuggability, and scalability**.

---

## Disclaimer

This orchestration setup is documented for **educational and portfolio purposes**, reflecting enterprise best practices without deploying live production infrastructure.
