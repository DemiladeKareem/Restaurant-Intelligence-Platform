# Restaurant Intelligence Platform

## Business Requirements Document (BRD)

### 1. Project Background

The Restaurant Intelligence Platform is a business intelligence solution developed for a simulated Nigerian quick-service restaurant group operating five outlets and one central production kitchen in Lagos.

As restaurant operations expand, management must coordinate sales, menu performance, ingredient purchasing, kitchen production, inventory, and operating expenses across multiple locations.

When these activities are reported separately, obtaining a consolidated view of business performance becomes difficult.

This project explores how an integrated analytical platform can support better financial and operational visibility.

**Project classification:** Portfolio case study using synthetic data. The business scenario is fictional and does not represent a commissioned implementation for Yum-Yum Café or another real restaurant.

### 2. Business Problem

The simulated restaurant group requires a centralized reporting solution to address five key challenges:

1. Limited consolidated visibility into sales performance across branches.
2. Difficulty evaluating revenue alongside estimated profitability and operating expenses.
3. Limited insight into menu-product and category-level profitability.
4. Inadequate visibility into kitchen production, waste, and ingredient consumption.
5. Fragmented procurement and inventory activity reporting.

### 3. Business Objectives

The project prioritizes three business areas.

**Priority 1 — Sales & Revenue Intelligence**

Provide consolidated visibility into revenue, order volume, branch performance, menu categories, products, and sales channels.

**Priority 2 — Food Costs & Inventory**

Monitor ingredient consumption, procurement activity, production volumes, waste, and inventory movements.

**Priority 3 — Financial Performance**

Evaluate estimated gross profit, operating expenses, estimated operating profit, and branch-level financial performance.

### 4. Business Scope

The simulated business includes:

| Component          | Scope                                                        |
| ------------------ | ------------------------------------------------------------ |
| Restaurant outlets | Five Lagos branches                                          |
| Central kitchen    | One production facility                                      |
| Menu               | 73 modeled products across multiple categories               |
| Ingredients        | 61 modeled ingredients                                       |
| Suppliers          | Six modeled suppliers                                        |
| Sales              | Customer orders, order items, and payment records            |
| Operations         | Production, ingredient consumption, inventory, and transfers |
| Finance            | Estimated product costs and operating expenses               |

The restaurant branches are Abule Egba, Egbeda, Ipaja, Ikorodu, and Surulere.

### 5. Stakeholders and Reporting Needs

The following roles represent potential users of the proposed solution.

| Stakeholder                           | Information required                                        |
| ------------------------------------- | ----------------------------------------------------------- |
| Business Owner / Executive Management | Consolidated revenue, profitability, and branch comparisons |
| Branch Manager                        | Branch sales and operating performance                      |
| Kitchen / Operations Manager          | Production volumes, waste rates, and facility activity      |
| Procurement Manager                   | Purchase-order values and ingredient purchasing patterns    |
| Finance Manager                       | Revenue, estimated profitability, and operating expenses    |

These are illustrative stakeholder roles, not individuals interviewed during the project.

### 6. Functional Requirements

| ID    | Requirement                                                                                  | Priority | Delivery             |
| ----- | -------------------------------------------------------------------------------------------- | -------- | -------------------- |
| BR-01 | Display consolidated revenue and order volume                                                | High     | Executive Overview   |
| BR-02 | Compare financial performance across branches                                                | High     | Executive Overview   |
| BR-03 | Analyze monthly revenue and operating expenses                                               | High     | Executive Overview   |
| BR-04 | Analyze revenue by menu category and product                                                 | High     | Menu & Sales         |
| BR-05 | Compare sales-channel contributions                                                          | Medium   | Menu & Sales         |
| BR-06 | Evaluate estimated product gross profitability                                               | High     | Menu & Sales         |
| BR-07 | Monitor kitchen production and waste rates                                                   | High     | Kitchen & Operations |
| BR-08 | Compare production across facilities                                                         | High     | Kitchen & Operations |
| BR-09 | Identify major ingredient consumption costs                                                  | High     | Kitchen & Operations |
| BR-10 | Monitor procurement order value                                                              | Medium   | Kitchen & Operations |
| BR-11 | Analyze inventory movement activity                                                          | Medium   | Kitchen & Operations |
| BR-12 | Support interactive date, branch, category, channel, and facility filtering where applicable | High     | Power BI             |
| BR-13 | Provide consistent navigation across report pages                                            | Medium   | Power BI             |

### 7. Key Performance Indicators

**Executive Overview**

- Total Revenue
- Total Orders
- Estimated Gross Profit
- Estimated Operating Profit
- Estimated Operating Margin

**Menu & Sales**

- Total Units Sold
- Average Order Value
- Estimated Gross Margin
- Distinct Products Sold
- Product Revenue and Gross Profit

**Kitchen & Operations**

- Total Produced Portions
- Total Waste Portions
- Production Waste Rate
- Procurement Order Value
- Estimated Ingredient Consumption Cost
- Inventory Movement Count

### 8. Non-Functional Requirements

The proposed solution should:

- Use a structured and maintainable analytical data model.
- Apply consistent business definitions across reporting pages.
- Support appropriate filtering without misleading aggregations.
- Present readable and consistent dashboard visuals.
- Distinguish estimated financial values from actual financial results.
- Maintain traceability from reporting measures to underlying data sources.
- Provide documentation sufficient for technical review and reproduction.

### 9. Analytical Constraints

Several constraints must be respected.

**Financial granularity:** Operating expenses are not allocated to individual products or sales channels. Consequently, operating profitability should not be presented at those levels without an appropriate allocation method.

**Central kitchen:** Central-kitchen operations must be distinguished from individual branch activity.

**Procurement:** Purchase-order values must not automatically be treated as confirmed cash payments.

**Inventory:** Quantities using incompatible units of measurement must not be aggregated without conversion.

**Synthetic data:** Results demonstrate analytical capabilities rather than actual business performance.

### 10. Out of Scope

The current project does not include:

- Live POS or accounting-system integrations.
- Real customer-level behavior analysis.
- Production-ready automated data refresh.
- Demand forecasting or predictive optimization.
- Audited financial reporting.
- A deployed inventory replenishment system.
- Measured financial improvements from real-world interventions.

These may be considered future enhancements.

### 11. Acceptance Criteria

The project will be considered complete when:

- [ ] Generated datasets pass the required integrity and quality checks.
- [ ] SQL staging, transformation, and analytical objects are available.
- [ ] Power BI relationships and business measures are validated.
- [ ] All three dashboard pages present the intended analytical information.
- [ ] Relevant slicers, navigation, and reset controls function correctly.
- [ ] Business findings are supported by actual simulated-data results.
- [ ] Technical documentation accurately describes the implemented solution.
- [ ] The final repository contains the necessary scripts, report, documentation, and setup instructions.

These checkboxes should be marked complete only after the corresponding evidence has been verified.

### 12. Expected Deliverables

1. Python scripts and synthetic operational datasets.
2. SQL Server database creation, loading, transformation, and analytical scripts.
3. Dimensional and fact-based analytical model.
4. Three-page interactive Power BI report.
5. Business and technical documentation.
6. Evidence-based analytical findings and recommendations.
7. GitHub repository with a project README and dashboard screenshots.

### 13. Expected Business Value

A comparable solution using validated real-world restaurant data could support:

- Faster preparation of management reports.
- More transparent branch performance comparisons.
- Better visibility into menu profitability.
- Earlier investigation of production waste patterns.
- Improved monitoring of procurement and ingredient costs.
- More informed operational and financial decisions.

These benefits are potential applications, not measured outcomes achieved by this portfolio project.

### 14. Conclusion

The Restaurant Intelligence Platform is designed to demonstrate how a growing restaurant business can move from disconnected operational reporting toward integrated business intelligence.

The project's central objective is to connect sales, financial, and kitchen operations data into a coherent analytical solution that supports meaningful management questions.

The implementation is evaluated through data integrity, model correctness, reporting functionality, and the quality of the analytical findings.
