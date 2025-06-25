from twilio.rest import Client
import pandas as pd
import time
from datetime import datetime

# Configuration
TWILIO_ACCOUNT_SID = 'AC29b05318e33dcd3931506affa258d272'
TWILIO_AUTH_TOKEN = '8c8e2e1e5f8e1e81d8c01557a8ffac4c'
TWILIO_PHONE ='YourTwilioSender'
SALES_TEAM_CONTACT_NUMBERS = ['+91932808769', '+919328087695', '+919106879660']

# Scoring criteria
SCORE_CRITERIA = {
    'job_title': {
        'CEO': 25,
        'Director': 15,
        'Manager': 10,
        'Sales Executive': 5,
        'Sales Associate': 2,
        'Intern': 1,
    },
    'experience': {
        '10+ years': 25,
        '5-10 years': 15,
        '3-5 years': 10,
        '1-3 years': 5,
        '0-1 years': 2,
    },
    'education': {
        'MBA': 20,
        'BBA': 15,
        'BCA': 10,
    },
    'company_size': {
        '1000 employees': 25,
        '500 employees': 15,
        '300 employees': 10,
        '15 employees': 5,
    },
    'location': {
        'Mumbai': 25,
        'Delhi': 15,
        'Bangalore': 10,
    },
    'industry': {
        'IT': 25,
        'Finance': 15,
        'Healthcare': 10,
    },
    'salary': {
        'high': 2500,
        'medium': 1500,
        'low': 1000,
    }
}

class LeadScoring:
    def __init__(self):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def calculate_score(self, lead):
        """Calculate score for a lead based on the scoring criteria"""
        score = 0

        # Job title scoring
        score += SCORE_CRITERIA['job_title'].get(lead['job_title'], 0)
        score += SCORE_CRITERIA['experience'].get(lead['experience'], 0)
        score += SCORE_CRITERIA['education'].get(lead['education'], 0)
        score += SCORE_CRITERIA['company_size'].get(lead['company_size'], 0)
        score += SCORE_CRITERIA['location'].get(lead['location'], 0)
        score += SCORE_CRITERIA['industry'].get(lead['industry'], 0)

        # Salary scoring
        if lead['salary'] >= SCORE_CRITERIA['salary']['high']:
            score += SCORE_CRITERIA['salary']['high']
        elif lead['salary'] >= SCORE_CRITERIA['salary']['medium']:
            score += SCORE_CRITERIA['salary']['medium']
        else:
            score += SCORE_CRITERIA['salary']['low']

        # Experience scoring
        if lead['experience'] >= 10:
            score += SCORE_CRITERIA['experience']['10+ years']
        elif lead['experience'] >= 5:
            score += SCORE_CRITERIA['experience']['5-10 years']

        else:
            score += SCORE_CRITERIA['experience']['0-1 years']

        return score

    def send_sms(self, to_number, message):
        """Send SMS to sales team"""
        try:
            self.client.messages.create(
                to=to_number, from_=TWILIO_PHONE, body=message
            )
            print(f"SMS sent to {to_number} with message: {message}")
            return True
        except Exception as e:
            print(f"Error sending SMS to {to_number}: {str(e)}")
            return False

    def send_alert(self, lead):
        message = f"New lead detected: {lead['name']} with score: {lead['score']}"
        for number in SALES_TEAM_CONTACT_NUMBERS:
            self.send_sms(number, message)

    def process_leads(self, leads):
        """Process leads and notify sales team of high priority leads"""
        # Calculate scores for all leads
        for lead in leads:
            lead['score'] = self.calculate_score(lead)

        # Sort by score (descending)
        sorted_leads = sorted(leads, key=lambda x: x['score'], reverse=True)

        # Notify sales team about high priority leads (score > 50)
        for lead in sorted_leads:
            if lead['score'] > 50:
                print(f" High priority lead: {lead['name']} (Score: {lead['score']})")
                self.send_alert(lead)
                
          
            elif lead['score'] > 30:
                print(f" medium priority lead: {lead['name']} (Score: {lead['score']})")
                self.send_alert(lead)
             
            else: 
                print(f" low priority lead: {lead['name']} (Score: {lead['score']})")
                self.send_alert(lead)
            
                time.sleep(1)  # Avoid API rate limits

        return sorted_leads

