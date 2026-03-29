# email_sender.py - Milestone 4 (SMTP Simulation)
def send_summary_email(receiver_email, total, pos, neg, neu):
    """
    Simulates the SMTP email sending process for Milestone 4.
    This bypasses Google's security blocks while proving the logic works.
    """
    print("\n" + "="*50)
    print("📧 --- OUTGOING EMAIL REPORT (SIMULATED) ---")
    print("="*50)
    print(f"TO:      {receiver_email}")
    print(f"SUBJECT: 📊 Final Sentiment Analysis Report")
    print(f"BODY:")
    print(f"   - Total Processed: {total}")
    print(f"   - Positive: {pos}")
    print(f"   - Negative: {neg}")
    print(f"   - Neutral:  {neu}")
    print("-" * 50)
    print("✅ Success: Email Report Sent via SMTP Simulator!")
    print("="*50 + "\n")
    
    return True