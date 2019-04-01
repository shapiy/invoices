# Invoices

Generate DOCX Invoice based on Toggl report and Google Docs template.

## Getting started
1) Enable Google Drive API as described 
[in Drive API Python Quickstart](https://developers.google.com/drive/api/v3/quickstart/python).
1) Save `credentials.json` to the working directory.
1) Create Invoice template in Google Docs.
1) In the working directory, create `invoices.toml` file with Toggl settings:
    ```toml
    [toggl]
    token = '<Toggle API token>'
    user_agent = '<User email>'
    workspace_id = '3058838'
    ```
1) Define hourly rate in the `invoice` section of the settings file: 
    ```toml
    [invoice]
    rate = 20,5
    ```
1) Add the following tags to the template. Use the Jinja 2 format `{{ tag }}`: 
  * `invoice_no`: 4,
  * `date_en`': Date in English
  * `date_uk`': Date in Ukrainian
  * `hours`: Number of hours
  * `rate`: Hourly rate in US dollars  
  * `amount`: Compensation in US dollars  

## Development
Running tests and static code checks.
```bash
tox
``` 

### Updating tox dependencies
```bash
pipenv lock --requirements > requirements.txt
pipenv lock --requirements --dev | grep -v '^\-e .$' > requirements-dev.txt
```  
