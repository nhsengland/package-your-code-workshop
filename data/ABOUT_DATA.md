# Data Information

## Source

The data in this directory is publicly available from the NHS Digital publication:

### Appointments in General Practice - July 2025

**Publication Page:** [NHS Digital - Appointments in General Practice](https://digital.nhs.uk/data-and-information/publications/statistical/appointments-in-general-practice/july-2025)

**Direct Download Link:** [Practice_Level_Crosstab_Jul_25.zip](https://files.digital.nhs.uk/81/BA7A8F/Practice_Level_Crosstab_Jul_25.zip)

## Data Structure

- `raw/` - Contains the original data files from the NHS Digital publication
- `lookup/` - Contains mapping files for data interpretation
- `processed/` - For any processed or transformed versions of the data

## Files Included

From the original zip file:

- Practice level crosstab data for May, June, and July 2025
- Mapping file for data interpretation (moved to lookup folder)

## Important Note for Production Projects

**Data in Git Repositories**: In production projects, you should typically add the `data/` folder to your `.gitignore` file to prevent data files from being committed to your git history. This helps to:

- Keep repository sizes manageable
- Avoid accidentally publishing sensitive data
- Prevent data versioning conflicts
- Follow data governance best practices

The data is only included in this workshop repository to make the setup and follow-along process simpler for participants. In your own projects, consider downloading data programmatically or storing it separately from your code repository.

## License and Usage

This data is published by NHS Digital and is available under the terms specified in their publication. Please refer to the original publication page for full terms and conditions.
