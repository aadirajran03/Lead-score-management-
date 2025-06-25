from pandas import pandas
from score import LeadScoring
import time
from datetime import datetime
import pandas as pd
sample_leads = [
    {
        'name': 'Seem Rapine',
        'phone': '+919106879660',
        'company': 'Tech Solutions',
        'job_title': 'Director',
        'company_size': 'Large',
        'experience': 10,
        'education': 'MBA',
        'location': 'Mumbai',
        'industry': 'IT',
        'salary': 800000,  # High salary
        'requested_demo': True,
        'activities': ['visited pricing page', 'downloaded whitepaper'],
        'last_activity': datetime(2023, 6, 24)
    },
    {
        'name': 'Agita Rapine',
        'phone': '+919328087695',
        'company': 'Innovate Corp',
        'job_title': 'Manager',
        'company_size': 'Large',
        'experience': 5,
        'education': 'BBA',
        'location': 'Delhi',
        'industry': 'Finance',
        'salary': 500000,  # Medium salary
        'requested_demo': False,
        'activities': ['viewed case studies'],
        'last_activity': datetime(2023, 6, 24)
    },
    {
        'name': 'Audra',
        'phone': '+919328087694',
        'company': 'Complot Corp',
        'job_title': 'Manager',
        'company_size': 'Large',
        'experience': 2,
        'education': 'BCA',
        'location': 'Bangalore',
        'industry': 'Healthcare',
        'salary': 200000,  # Low salary
        'requested_demo': False,
        'activities': ['viewed case result'],
        'last_activity': datetime(2023, 6, 24)
    }
]

if __name__ == "__main__":
    scorer = LeadScoring()
    scored_leads = scorer.process_leads(sample_leads)
    filtered_leads = [lead for lead in scored_leads if lead.get('score', 0) < 100]

    # Display all scored leads
    print("\nAll Leads (Sorted by Score):")
    df = pd.DataFrame(scored_leads)
    print(df[['name', 'experience', 'job_title', 'salary', 'score']].to_markdown())
