# Business Glossary

## Document Information

| Attribute            | Value                                |
| -------------------- | ------------------------------------ |
| **Document Name**    | Business Glossary                    |
| **Project**          | Insurance Risk Intelligence Platform |
| **Document Version** | 1.0                                  |
| **Status**           | Approved                             |
| **Owner**            | Saurabh Singh                        |
| **Prepared By**      | Data Engineering Team                |
| **Last Updated**     | 2026-06-27                           |

---

# 1. Purpose

The Business Glossary establishes a standardized business vocabulary for the **Insurance Risk Intelligence Platform**.

Its primary objective is to ensure that business users, data engineers, data analysts, solution architects, and AI-powered applications use consistent terminology across the entire platform.

This glossary serves as the **Single Source of Truth (SSOT)** for all business terminology used throughout the project.

---

# 2. Scope

This glossary covers terminology related to:

* Customer Management
* Insurance Policies
* Coverage
* Claims
* Financial Metrics
* Product Management
* Distribution Channels
* Time Dimension
* Socioeconomic Enrichment
* Environmental Enrichment
* Data Warehousing
* Artificial Intelligence
* Metadata & Governance

---

# 3. Customer Domain

| Business Term     | Definition                                                                               | Business Importance            | Related Entity | Related KPI           |
| ----------------- | ---------------------------------------------------------------------------------------- | ------------------------------ | -------------- | --------------------- |
| Customer          | Individual receiving insurance coverage.                                                 | Core business entity.          | Customer       | Customer Count        |
| Insured           | Person whose health risk is covered under a policy.                                      | Risk assessment.               | Customer       | Claim Frequency       |
| Policyholder      | Individual responsible for purchasing and maintaining the insurance policy.              | Revenue generation.            | Policy         | Retention Rate        |
| Customer Age      | Age of the insured at the beginning of the policy year.                                  | Primary underwriting variable. | Customer       | Risk Profile          |
| Gender            | Gender of the insured individual.                                                        | Demographic analysis.          | Customer       | Customer Segmentation |
| Geographic Region | Customer location determined from postal code.                                           | Regional portfolio analysis.   | Customer       | Regional Loss Ratio   |
| Postal Code       | Customer residential ZIP/Postal code.                                                    | Geographic enrichment.         | Customer       | Regional Analytics    |
| Customer Segment  | Business classification of customers based on demographic or behavioral characteristics. | Marketing & Risk Analysis.     | Customer       | Segment Performance   |

---

# 4. Policy Domain

| Business Term     | Definition                                                               | Business Importance        | Related Entity | Related KPI        |
| ----------------- | ------------------------------------------------------------------------ | -------------------------- | -------------- | ------------------ |
| Policy            | Legal agreement between insurer and insured defining insurance coverage. | Core business entity.      | Policy         | Active Policies    |
| Policy Number     | Unique identifier assigned to a policy.                                  | Business Key.              | Policy         | All KPIs           |
| Policy Year       | Calendar year associated with policy information.                        | Defines reporting period.  | Time           | Annual KPIs        |
| Policy Start Date | Effective date of policy coverage.                                       | Coverage tracking.         | Policy         | Active Policies    |
| Policy End Date   | Expiry date of policy.                                                   | Renewal monitoring.        | Policy         | Renewal Rate       |
| Active Policy     | Policy currently providing insurance coverage.                           | Portfolio size.            | Policy         | Active Policies    |
| Renewal           | Continuation of policy after expiry.                                     | Customer retention.        | Policy         | Retention Rate     |
| Policy Lapse      | Failure to renew policy after expiry.                                    | Customer churn.            | Policy         | Lapse Rate         |
| New Business      | Newly issued policy within reporting period.                             | Business growth indicator. | Policy         | New Business Ratio |

---

# 5. Coverage Domain

| Business Term   | Definition                                                              | Business Importance          | Related Entity | Related KPI       |
| --------------- | ----------------------------------------------------------------------- | ---------------------------- | -------------- | ----------------- |
| Coverage        | Insurance protection provided by a policy.                              | Determines insured benefits. | Coverage       | Coverage Mix      |
| Coverage Period | Duration during which insurance benefits remain active.                 | Coverage analysis.           | Coverage       | Active Policies   |
| Exposure        | Portion of time the policy remained active during the reporting period. | Actuarial calculations.      | Coverage       | Claim Frequency   |
| Exposure Unit   | Standard unit representing one insured policy-year.                     | Risk measurement.            | Coverage       | Exposure Analysis |
| Coverage Type   | Type of insurance benefits included in the policy.                      | Product analysis.            | Coverage       | Product Mix       |

---

# 6. Claims Domain

| Business Term     | Definition                                                       | Business Importance           | Related Entity | Related KPI         |
| ----------------- | ---------------------------------------------------------------- | ----------------------------- | -------------- | ------------------- |
| Claim             | Request submitted for reimbursement of covered medical expenses. | Core insurance event.         | Claims         | Claim Count         |
| Claim Cost        | Total amount paid by insurer for claims.                         | Major business expense.       | Claims         | Loss Ratio          |
| Medical Service   | Healthcare service utilized by the insured.                      | Represents claim utilization. | Claims         | Service Utilization |
| Claim Frequency   | Number of claims relative to exposure.                           | Risk measurement.             | Claims         | Claim Frequency     |
| Claim Severity    | Average cost per claim.                                          | Cost analysis.                | Claims         | Severity Index      |
| High Cost Claim   | Claim exceeding predefined cost threshold.                       | Fraud & Risk Monitoring.      | Claims         | High Cost Claims    |
| Claim Utilization | Frequency of healthcare service usage.                           | Customer behavior analysis.   | Claims         | Utilization Rate    |

---

# 7. Financial Domain

| Business Term     | Definition                                                   | Business Importance         | Related Entity | Related KPI    |
| ----------------- | ------------------------------------------------------------ | --------------------------- | -------------- | -------------- |
| Premium           | Amount paid by customer for insurance coverage.              | Primary revenue source.     | Financial      | Premium Growth |
| Annual Premium    | Total premium charged for one policy year.                   | Revenue analysis.           | Financial      | Annual Premium |
| Earned Premium    | Portion of premium corresponding to elapsed coverage period. | Profitability calculations. | Financial      | Loss Ratio     |
| Total Claim Cost  | Aggregate claim payments during reporting period.            | Expense analysis.           | Financial      | Total Claims   |
| Profitability     | Difference between premium earned and claim cost.            | Business objective.         | Financial      | Profit Margin  |
| Loss Ratio        | Claim Cost ÷ Earned Premium.                                 | Primary profitability KPI.  | Financial      | Loss Ratio     |
| Cost Per Customer | Average claims cost incurred per insured individual.         | Cost optimization.          | Financial      | Cost Analysis  |

---

# 8. Product Domain

| Business Term       | Definition                                               | Business Importance   | Related Entity | Related KPI           |
| ------------------- | -------------------------------------------------------- | --------------------- | -------------- | --------------------- |
| Insurance Product   | Commercial insurance plan offered to customers.          | Product portfolio.    | Product        | Product Performance   |
| Product Category    | Classification of insurance products.                    | Portfolio management. | Product        | Product Mix           |
| Product Performance | Evaluation of profitability and utilization of products. | Product optimization. | Product        | Product Profitability |

---

# 9. Sales & Distribution Domain

| Business Term        | Definition                                           | Business Importance   | Related Entity | Related KPI         |
| -------------------- | ---------------------------------------------------- | --------------------- | -------------- | ------------------- |
| Distribution Channel | Channel through which insurance policy was sold.     | Sales analysis.       | Sales          | Channel Performance |
| Direct Sales         | Policies sold directly by insurer.                   | Sales monitoring.     | Sales          | Direct Sales Ratio  |
| Broker               | Third-party intermediary selling insurance products. | Distribution partner. | Sales          | Broker Performance  |
| Agency               | Authorized insurance sales organization.             | Sales network.        | Sales          | Agency Performance  |

---

# 10. Socioeconomic Domain

| Business Term         | Definition                                                 | Business Importance       | Related Entity | Related KPI           |
| --------------------- | ---------------------------------------------------------- | ------------------------- | -------------- | --------------------- |
| Income Percentile     | Relative household income ranking within population.       | External risk factor.     | Socioeconomic  | Customer Segmentation |
| Education Level       | Average educational attainment in customer's locality.     | Socioeconomic enrichment. | Socioeconomic  | Risk Profiling        |
| Employment Rate       | Employment characteristics of customer's region.           | Risk assessment.          | Socioeconomic  | Portfolio Risk        |
| Household Composition | Demographic structure of customer locality.                | Customer profiling.       | Socioeconomic  | Customer Insights     |
| Socioeconomic Index   | Composite indicator representing socioeconomic conditions. | Risk segmentation.        | Socioeconomic  | Risk Score            |

---

# 11. Environmental Domain

| Business Term          | Definition                                                              | Business Importance               | Related Entity | Related KPI            |
| ---------------------- | ----------------------------------------------------------------------- | --------------------------------- | -------------- | ---------------------- |
| Environmental Variable | Geographic or environmental characteristic linked to customer location. | Risk enrichment.                  | Environment    | Regional Risk          |
| Climate Variable       | Weather-related attribute influencing healthcare utilization.           | Risk modeling.                    | Environment    | Environmental Risk     |
| Population Density     | Number of residents within a geographical area.                         | Portfolio concentration analysis. | Environment    | Regional Exposure      |
| Urbanization Level     | Classification of region as urban, suburban, or rural.                  | Regional analytics.               | Environment    | Portfolio Distribution |

---

# 12. Time Domain

| Business Term    | Definition                                 | Business Importance   | Related Entity | Related KPI       |
| ---------------- | ------------------------------------------ | --------------------- | -------------- | ----------------- |
| Calendar Year    | Reporting year of policy information.      | Reporting period.     | Time           | Annual Reports    |
| Reporting Period | Time interval used for KPI calculation.    | Performance tracking. | Time           | All KPIs          |
| Financial Year   | Accounting period for financial reporting. | Business reporting.   | Time           | Financial Reports |

---

# 13. Data Warehouse Domain

| Business Term                   | Definition                                                            | Business Importance |
| ------------------------------- | --------------------------------------------------------------------- | ------------------- |
| Bronze Layer                    | Raw ingested data stored without business transformations.            | Data ingestion      |
| Silver Layer                    | Cleansed, standardized, and validated business data.                  | Data integration    |
| Gold Layer                      | Business-ready dimensional model optimized for analytics.             | Reporting           |
| Fact Table                      | Table storing measurable business events.                             | Analytics           |
| Dimension Table                 | Table storing descriptive business attributes.                        | Reporting           |
| Surrogate Key                   | System-generated unique identifier used in dimensional modeling.      | Warehouse Design    |
| Business Key                    | Natural identifier originating from source systems.                   | Data Integration    |
| Slowly Changing Dimension (SCD) | Technique used to manage historical changes in dimension data.        | Historical Analysis |
| Metadata                        | Information describing data assets and ETL processes.                 | Governance          |
| Data Lineage                    | Complete traceability of data movement from source to consumption.    | Governance          |
| Data Quality                    | Measure of accuracy, completeness, consistency, and validity of data. | Governance          |

---

# 14. AI & Analytics Domain

| Business Term                        | Definition                                                                | Business Importance    |
| ------------------------------------ | ------------------------------------------------------------------------- | ---------------------- |
| Artificial Intelligence (AI)         | Technology enabling automated reasoning and intelligent decision support. | AI Layer               |
| Large Language Model (LLM)           | AI model capable of understanding and generating human language.          | AI Analytics           |
| Retrieval-Augmented Generation (RAG) | AI architecture combining document retrieval with LLM reasoning.          | AI Assistant           |
| Vector Database                      | Database storing vector embeddings for semantic search.                   | AI Search              |
| Embedding                            | Numerical representation of textual information.                          | Semantic Search        |
| Semantic Search                      | Search based on contextual meaning instead of keywords.                   | AI Retrieval           |
| Prompt Engineering                   | Process of designing prompts for LLM interactions.                        | AI Development         |
| NL2SQL                               | Translation of natural language into executable SQL queries.              | Self-Service Analytics |

---

# 15. Metadata & Governance Domain

| Business Term   | Definition                                                            | Business Importance   |
| --------------- | --------------------------------------------------------------------- | --------------------- |
| Data Governance | Framework ensuring data quality, security, ownership, and compliance. | Enterprise Governance |
| Data Steward    | Individual responsible for maintaining data quality and definitions.  | Governance            |
| Data Owner      | Business owner responsible for a data domain.                         | Governance            |
| ETL             | Extract, Transform, Load process used to populate the data warehouse. | Data Engineering      |
| Data Pipeline   | Sequence of automated processes moving data across layers.            | ETL                   |
| Audit Trail     | Historical record of ETL execution and data modifications.            | Governance            |
| Data Validation | Process of verifying data quality against business rules.             | Data Quality          |
| Data Profiling  | Analysis of source data to understand its characteristics.            | Data Quality          |

---

# 16. References

1. Source Research Dataset Documentation
2. Insurance Risk Intelligence Platform Architecture v1.0
3. Business Rules Document
4. KPI Catalogue
5. Data Dictionary

---

# 17. Version Information

| Attribute      | Value                                                       |
| -------------- | ----------------------------------------------------------- |
| Version        | 1.0                                                         |
| Status         | **Frozen**                                                  |
| Review Status  | Approved                                                    |
| Next Review    | After Business Rules completion                             |
| Change Control | Changes permitted only through approved Change Request (CR) |
