\# Raw data sources



All files gitignored. Download to reproduce.



## 1. ONS — Private rental market in London, April 2025 to March 2026

File: londonrentalstatsaccessibleq12026.xlsx

URL: https://www.ons.gov.uk/economy/inflationandpriceindices/adhocs/

&#x20;    3389privaterentalmarketinlondonapril2025tomarch2026

Licence: Open Government Licence v3.0

Content: Sheet 3 = 329 postcode districts x 6 bedroom categories = 1,974 rows

Known issue: 927 medians suppressed (47%); Room 76%, Studio 66%

Downloaded: 08-10-2026



## 2. ONS — Price Index of Private Rents, UK

File: priceindexofprivaterentsukmonthlypricestatistics.xlsx

URL: https://www.ons.gov.uk/economy/inflationandpriceindices/datasets/

&#x20;    priceindexofprivaterentsukmonthlypricestatistics

Licence: Open Government Licence v3.0

VERSION OF RECORD: release of 16 September 2026 (49,980 rows, to Aug 2026)

Note: superseded by release of 21 October 2026 (50,337 rows, to Sep 2026).

&#x20;     September release frozen for reproducibility, per supervisory guidance.

Downloaded: 08-10-2026



## 3. Kaggle — London property rental

File: rent\_ads\_rightmove\_extended.csv

URL: https://www.kaggle.com/datasets/psgpyc/london-property-rental

Content: 3,478 listings scraped from Rightmove, c.2024

Known issues: Council Tax 99% missing, SIZE 73.5% missing,

&#x20;             nearest\_station\_count has no variance

Usable after cleaning: 2,167 rows, 227 districts

Downloaded: 08-10-2026



## 4. DWP — Local Housing Allowance rates, April 2026 to March 2027

Files: 2026-27\_LHA\_TABLES.xlsx ; england-rates-2026-to-2027.csv

URL: https://www.gov.uk/government/publications/

&#x20;    local-housing-allowance-lha-rates-applicable-from-april-2026-to-march-2027

Licence: Open Government Licence

Content: 152 BRMAs, CAT A-E (shared, 1-4 bed), weekly rates

&#x20; Table 1 = LHA April 2024

&#x20; Table 2 = 30th percentile of market rents

&#x20; Table 3 = maximum LHA caps

&#x20; Table 4 = LHA April 2026 (identical to Table 1 - rates frozen since 2024)

CSV variant gives monthly Universal Credit conversions

Encoding: CSV is latin-1, not UTF-8

Downloaded: 09-11-2026



## 5. Urban Big Data Centre — Postcode to BRMA lookup v2.2

File: pcode\_brma\_lookup\_v2.2.csv (127 MB)

URL: https://data.ubdc.ac.uk/datasets?q=%22postcode+to+Broad+Rental+Market+Area%22

Licence: Open Government Licence

Content: 2,936,738 unit postcodes; 2,247,615 England

Derivation: ONS postcode centroids + BRMA boundaries obtained by FoI

&#x20;           (Boswarva, Datadaptive)

Note: v2.2 corrects omission of West Dunbartonshire BRMA in earlier release

Downloaded: 09-11-2026



## 6. London Datastore / VOA — Average Private Rents by Borough

File: voa-average-rent-borough.xls

URL: https://data.london.gov.uk/dataset/average-private-rents-borough-29j80

Licence: Open Government Licence v2.0

Coverage: 2011 Q2 to 2019. ARCHIVE ONLY, not used for modelling.

Downloaded: 08-10-2026



## 7. ONS Postcode Directory

URL: https://geoportal.statistics.gov.uk (search ONSPD)

Licence: Open Government Licence v3.0

Use: spatial feature engineering

Downloaded: 08-10-2026



## 8. ONS Postcode Directory for London
File: london_postcodes-ons-postcodes-directory-feb22.csv
URL: https://data.london.gov.uk/dataset/postcode-directory-for-london-exp5p
Licence: Open Government Licence v3.0
Release: February 2022 (latest London-specific release available; the full UK
         directory is issued quarterly and is current to August 2026)
Content: 326,214 London postcodes, 50 columns
Columns used: pcds, oseast1m, osnrth1m, oslaua
Use: district centroids and distance from central London for spatial features;
     Local Authority District codes for the council tax join
Note: contains Royal Mail, Gridlink, Ordnance Survey and ONS Intellectual
      Property Rights
Downloaded: 19 November 2026

## 9. DWP Local Housing Allowance rates, April 2026 to March 2027
File: 2026-27_LHA_TABLES.xlsx ; england-rates-2026-to-2027.csv
URL: https://www.gov.uk/government/publications/
     local-housing-allowance-lha-rates-applicable-from-april-2026-to-march-2027
Licence: Open Government Licence
Content: 152 Broad Rental Market Areas, categories A to E (shared, 1-4 bed)
  Table 1 = LHA rates April 2024
  Table 2 = 30th percentile of market rents
  Table 3 = maximum LHA caps
  Table 4 = LHA rates April 2026 (identical to Table 1; rates frozen since 2024)
Rates are weekly; the CSV variant gives monthly Universal Credit conversions
Encoding: the CSV is latin-1, not UTF-8
Downloaded: 9 November 2026



---

## Derived files

These are produced from the sources above and committed to the repository, since
they are small and the agents depend on them at runtime.

| File | Produced by | Content |
|---|---|---|
| data/processed/district_brma.csv | notebooks/03_brma_lookup.ipynb | 2,322 districts mapped to BRMAs by modal assignment, with modal share |
| data/processed/district_spatial.csv | notebooks/04_spatial_features.ipynb | 329 London districts with centroid, distance from Charing Cross, and LAD code |
| data/processed/listings_clean.csv | notebooks/02_data_cleaning.ipynb | 2,400 cleaned London listings |