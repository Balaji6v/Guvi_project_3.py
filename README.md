#  PAT Capstone Project – Selenium Automation using PyTest

##  Project Structure

- **Framework**: Python + Selenium + PyTest
- **Design Pattern**: Page Object Model (POM)
- **Features**:
  - Data Driven Testing (DDT) via CSV
  - HTML Reports using `pytest-html`
  - Explicit waits for synchronization
  - Proper comments and Pylint compliant

##  Folder Overview

## Test Data

Test data is maintained using `YAML` format inside the `/data` directory for easy scalability and Keyword Driven Testing.

Example snippet from `login_test_data.yaml`:
```yaml
- username: "standard_user"
  password: "secret_sauce"
  expected_result: "success"

