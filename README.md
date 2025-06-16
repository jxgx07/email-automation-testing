# Jenkins Webhook + Payload Aggregator

## Project Structure

- Jenkinsfile — Full CI/CD pipeline
- aggregate_payloads.py — Aggregation logic (Python 3)
- payloads/ — Folder where webhook JSON files are stored

## Jenkins Configuration

- The pipeline accepts webhook payload as a string parameter `payload`.
- Every webhook hit stores the payload as timestamped JSON.
- Payload files older than 48h are auto-deleted.
- After each webhook or scheduled run, aggregation happens:
  - Collects all payloads from last 24 hours
  - Converts into Excel format
  - Splits into `slave1_TIMESTAMP.xlsx` & `slave2_TIMESTAMP.xlsx`

## Python Dependencies

```bash
pip install pandas openpyxl
