import pandas as pd
import requests

def fetch_college_data_for_year(api_key, state, year):
    base_url = 'https://api.data.gov/ed/collegescorecard/v1/schools'
    fields = f'id,school.name,school.state,school.ownership,school.degrees_awarded.predominant,school.carnegie_size_setting,{year}.admissions.admission_rate.overall,{year}.admissions.sat_scores.average.overall,{year}.admissions.act_scores.midpoint.cumulative,{year}.student.size,{year}.completion.completion_rate_4yr_150nt,{year}.student.retention_rate.four_year.full_time,{year}.aid.median_debt.completers.overall,{year}.aid.federal_loan_rate,{year}.aid.pell_grant_rate,{year}.cost.avg_net_price.public,{year}.cost.avg_net_price.private,{year}.earnings.10_yrs_after_entry.median,{year}.earnings.6_yrs_after_entry.median'

    all_data = []
    page_num = 0
    while True:
        params = {
            'api_key': api_key,
            'school.state': state,
            'fields': fields,
            'per_page': 100,
            'page': page_num,
        }
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json().get('results', [])
            if not data:
                break
            all_data.extend(data)
            page_num += 1
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}, Message: {response.text}")
            return None

    df = pd.DataFrame(all_data)
    df['year'] = year
    return df

if __name__ == "__main__":
    api_key = "MWAHo6aJF76npZt2CJS824esSyDnkQzUfvPOPkHi"
    state = "CA"
    years = ["2019", "2020", "2021", "2022", "2023"]
    all_dataframes = [fetch_college_data_for_year(api_key, state, year) for year in years]
    combined_df = pd.concat(all_dataframes)
    combined_df.to_csv('california_colleges_data_combined.csv', index=False)
