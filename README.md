# ScraPy-McScrapeface
### Deed Data Pipeline Tool V-0.2

This tool, "Scrapy-McScrapeface", is a series of scripts designed for, owned, and licensed by PropLogix. 
The scripts and code included form the components of a data pipeline from acquisition to anaylsis. 

The pipeline can be summarized by the following steps:

1. Scraping of Deed records from public county clerk websites. Each county clerk website is a unique snowflake, and must have a custom scraper.
2. Optical Character Recognition (OCR) of the Deed PDFs, to produce editable text.
3. Extraction of desired data fields from OCRed text.
4. Analysis and visualization of final extracted data.


## Instructions

1. run GUI_pdf_grab.py to select multiple counties at once, or run any of the individual scrapers independently. This will download a mass of PDFs for the date range you specify.
2. Perform OCR of your choice. Our current pipeline utilizes ABBYYFINE corporate Hotfolder to perform scheduled OCR. It consolidates all the OCR text into a single .csv, with a seperate OCR job and .csv for each county.
3. run data_extract.py to get the tidy data of the relevant fields extracted from the .csv files. This will produce a final_data file.
4. proplogix_jobs_report.Rmd is an R markdown file that contains munging, cleaning, analysis, and visualization for a variety of proplogix records and data, as well as the same for the final data.


## Notes, bugs, and considerations

- The OCR step can be performed by any OCR software. There are plans to change the OCR step from the ABBYYFINE corporate hotfolder software to the open-source tesseract 4.0 package maintained by google. Additionally, plans include running tesseract from a AWS Lambda instance for speed and cost savings.
- Sarasota and Pinellas scrapers require a headed browser driver to navigate past captcha/pages. As such, their performance is somewhat slow and obtrusive compared to the headless scrapers. Plans are to alter these scrapers to a use a headless driver in the future. 
- Sarasota scraper currently skips pages occasionally, fixing this behavior is a high priority.
- Network visualization produces some minimally interesting results for proplogix data, and not much of use from the scraped data.
