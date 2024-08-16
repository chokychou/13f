fileCacheFn = lambda filing_year, filing_quarter: os.path.join(
                                  "tmp",
                                  "sec_daily_index_files",
                                  str(filing_year),
                                  f"QTR{filing_quarter}",
                                  "cache.txt"
                                )

def run_once(current_year):
  year_list = list(range(2008,current_year))
  quarter_list = list(range(1,5))

  for year in year_list:
    for quarter in quarter_list:
      download_and_save_sec_filings(year, quarter)
      forms = organize_forms_by_types(year, quarter, THIRTEEN_F_FORM_TYPES)
      filename = fileCacheFn(year, quarter)
      os.makedirs(os.path.dirname(filename), exist_ok=True)
      j = json.dumps(forms, indent=4)
      with open(filename, 'a') as f:
        f.write(j)