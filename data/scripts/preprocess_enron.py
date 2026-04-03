"""
Simulated Enron Email Preprocessing.

Since the real Enron dataset is ~1.7GB, this script generates a small
mock 'cleaned' dataset that mirrors the structure we'd expect after
parsing and cleaning the raw Enron emails.
"""

import pandas as pd
import os
import random

# Ensure output directory exists
os.makedirs("data/processed", exist_ok=True)


def generate_mock_enron_data(num_samples=100) -> pd.DataFrame:
    """Generate a small mock dataframe that looks like cleaned Enron data."""
    subjects = [
        "Project Update",
        "Meeting Rescheduled",
        "Q3 Earnings Report",
        "Action Required: Compliance Training",
        "Lunch today?",
        "Contract Review",
        "Welcome to the team",
        "Weekly Sync",
        "Follow up on our call",
        "Important: Office Policy Changes",
    ]

    bodies = [
        "Hi team, just a quick update on the project. We are on track for next week's release. Regards, John",
        "Apologies, but I need to reschedule our meeting to tomorrow at 2 PM. Let me know if that works.",
        "Please find attached the Q3 earnings report for your review before the board meeting.",
        "Reminder: All employees must complete the annual compliance training by Friday. Thank you.",
        "Anyone up for grabbing lunch at the new deli downstairs around noon?",
        "I've reviewed the latest draft of the vendor contract. I added a few comments, let's discuss.",
        "Please join me in welcoming Sarah to our engineering team starting today!",
        "Our weekly sync is starting in 5 minutes. See you in conference room A.",
        "Great speaking with you earlier. As discussed, I will send over the proposal by EOD.",
        "Please read the updated office policy regarding remote work, effective next month.",
    ]

    senders = [
        "john.doe@enron.com",
        "jane.smith@enron.com",
        "admin@enron.com",
        "hr@enron.com",
    ]
    receivers = ["team@enron.com", "all-employees@enron.com", "sarah.connor@enron.com"]

    data = []
    for _ in range(num_samples):
        data.append(
            {
                "subject": random.choice(subjects),
                "body": random.choice(bodies),
                "sender": random.choice(senders),
                "receiver": random.choice(receivers),
                "word_count": random.randint(15, 60),
            }
        )

    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Pre-processing 'Enron' data...")
    df = generate_mock_enron_data(num_samples=200)
    output_path = "data/processed/enron_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} cleaned emails to {output_path}")
