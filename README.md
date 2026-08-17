# Home Credit Default Risk Dashboard

An interactive Streamlit dashboard for analyzing customer credit risk, loan default patterns, financial behavior, demographics, and portfolio-level risk using the Home Credit application dataset.

The project contains 20 analytical dashboard pages covering customer characteristics, financial indicators, external credit scores, regional patterns, occupation, combined risk segmentation, and portfolio-level insights.

---

## 1. Project Overview

The objective of this project is to understand the factors associated with loan default and provide an interactive dashboard for exploring credit-risk patterns.

The dashboard analyzes:

- Customer demographics
- Age and gender
- Income
- Credit amount
- Annuity burden
- Education
- Employment
- Family structure
- Housing
- Asset ownership
- Contract type
- External credit scores
- Regional characteristics
- Occupation and organization
- Combined customer risk
- Portfolio-level risk

---

## 2. Business Objectives

The dashboard is designed to answer questions such as:

- What is the overall loan default rate?
- Which customer segments have higher default rates?
- Does income level relate to default risk?
- How does credit burden relate to default?
- Does employment duration affect repayment behavior?
- How does education level relate to default?
- Are certain housing types associated with higher default rates?
- Does car or realty ownership relate to repayment behavior?
- How do cash loans compare with revolving loans?
- How do external credit scores relate to default?
- Which regional ratings have higher default rates?
- Which occupations and organization types show higher observed default rates?
- What proportion of customers fall into High or Very High Risk categories?
- How is credit exposure distributed across contract types?

---

## 3. Dashboard Pages

The application contains 20 analytical pages.

### 1. Executive Overview

Provides a high-level overview of the portfolio, including applications, defaults, default rate, income, and credit metrics.

### 2. Default Analysis

Analyzes default and non-default customer populations and overall repayment behavior.

### 3. Demographic Analysis

Explores customer demographic characteristics and their relationship with default risk.

### 4. Age Analysis

Analyzes customer age distribution and default rates across age groups.

### 5. Gender Analysis

Compares customer populations and observed default rates across gender segments.

### 6. Income Analysis

Analyzes income distribution, income groups, and observed default rates.

### 7. Credit Analysis

Examines credit amounts and credit-related risk patterns.

### 8. Annuity Analysis

Analyzes loan annuity values and repayment-related characteristics.

### 9. Income vs Credit

Examines the relationship between customer income and requested credit.

### 10. Annuity Burden

Analyzes the relationship between loan annuity and customer income.

### 11. Education Analysis

Examines education levels, financial characteristics, and observed default rates.

### 12. Employment Analysis

Analyzes employment duration, employment groups, occupations, and repayment behavior.

### 13. Family Analysis

Analyzes family status, number of children, family size, and observed default risk.

### 14. Housing and Assets

Analyzes housing type, car ownership, realty ownership, car age, and asset combinations.

### 15. Contract Analysis

Compares Cash Loans and Revolving Loans across customer volume, default rates, and financial metrics.

### 16. External Credit Score

Analyzes:

- EXT_SOURCE_1
- EXT_SOURCE_2
- EXT_SOURCE_3

and their relationship with default behavior.

### 17. Regional Analysis

Analyzes regional client ratings, regional ratings by city, population density, financial characteristics, and default rates.

### 18. Occupation and Organization

Analyzes occupation types, organization types, income groups, and observed default rates.

### 19. Combined Risk

Creates an analytical risk segmentation using multiple customer-level indicators, including:

- External credit scores
- Credit burden
- Annuity burden
- Regional rating

Customers are classified into:

- Low Risk
- Moderate Risk
- High Risk
- Very High Risk

### 20. Portfolio Risk Summary

Provides an executive-level portfolio view combining:

- Portfolio size
- Default rate
- Credit exposure
- Contract mix
- Income profile
- Risk distribution
- High-risk customer population

---

## 4. Key Analytical Findings

The following figures were observed during validation using a 10,000-customer sample from the dataset.

### Overall Portfolio

| Metric | Value |
|---|---:|
| Customers | 10,000 |
| Defaults | 775 |
| Default Rate | 7.75% |
| Average Income | 167,448.90 |
| Average Credit | 600,753.07 |
| Average Annuity | 27,088.01 |

### Combined Risk Segmentation

| Risk Category | Customers | Portfolio Share | Default Rate |
|---|---:|---:|---:|
| Low Risk | 563 | 5.63% | 2.49% |
| Moderate Risk | 4,611 | 46.11% | 5.94% |
| High Risk | 4,005 | 40.05% | 9.69% |
| Very High Risk | 821 | 8.21% | 12.06% |

The observed default rate increases progressively from Low Risk to Very High Risk.

### High and Very High Risk Population

| Metric | Value |
|---|---:|
| Customers | 4,826 |
| Portfolio Share | 48.26% |
| Defaults | 487 |
| Default Rate | 10.09% |

### Contract Type

| Contract Type | Customers | Portfolio Share | Default Rate |
|---|---:|---:|---:|
| Cash Loans | 9,005 | 90.05% | 8.08% |
| Revolving Loans | 995 | 9.95% | 4.72% |

Cash loans represent the majority of the customer portfolio and credit exposure in the validation sample.

### External Credit Score

Lower external credit scores showed higher observed default rates.

For example, in the validation sample:

- EXT_SOURCE_2 score 0.0-0.2: 21.32% default rate
- EXT_SOURCE_2 score 0.6-0.8: 4.25% default rate

Similarly, lower EXT_SOURCE_3 score groups showed higher observed default rates.

---

## 5. Risk Segmentation Methodology

The combined risk framework is an analytical segmentation created from multiple customer attributes.

### External Credit Score

The combined external score is calculated from the available values of:

```text
EXT_SOURCE_1
EXT_SOURCE_2
EXT_SOURCE_3