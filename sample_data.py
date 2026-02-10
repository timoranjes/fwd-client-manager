"""
Sample Data Generator for FWD Client Management System
Run this to add sample clients and activities
"""

from app import app, get_db, init_db
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Generate sample clients for demo purposes"""
    
    sample_clients = [
        {
            "name": "Chan Tai Man",
            "email": "chan.taiman@email.com",
            "phone": "+852 9876 5432",
            "wechat": "ctm_hk",
            "policy_type": "Life Insurance",
            "coverage_amount": 5000000,
            "policy_start_date": "2024-01-15",
            "policy_end_date": "2025-01-15",
            "status": "Active"
        },
        {
            "name": "Lam Wai Lin",
            "email": "lam.wailin@email.com",
            "phone": "+852 9123 4567",
            "wechat": "lwl_2019",
            "policy_type": "Health Insurance",
            "coverage_amount": 3000000,
            "policy_start_date": "2024-06-01",
            "policy_end_date": "2025-06-01",
            "status": "Active"
        },
        {
            "name": "Wong Siu Ming",
            "email": "wong.siuming@email.com",
            "phone": "+852 9456 7890",
            "wechat": "wsm_finance",
            "policy_type": "Critical Illness",
            "coverage_amount": 2000000,
            "policy_start_date": "2024-03-20",
            "policy_end_date": "2025-03-20",
            "status": "Active"
        },
        {
            "name": "Cheung Ka Yi",
            "email": "cheung.kayi@email.com",
            "phone": "+852 9678 1234",
            "wechat": "cky_design",
            "policy_type": "Investment Linked",
            "coverage_amount": 1000000,
            "policy_start_date": "2024-09-01",
            "policy_end_date": "2025-02-10",
            "status": "Active"
        },
        {
            "name": "Ng Man Chun",
            "email": "ng.manchun@email.com",
            "phone": "+852 9234 5678",
            "wechat": "nmc_sports",
            "policy_type": "Accident Insurance",
            "coverage_amount": 500000,
            "policy_start_date": "2023-12-01",
            "policy_end_date": "2024-12-01",
            "status": "Expired"
        },
        {
            "name": "Liu Xiao Ming",
            "email": "liu.xiaoming@email.com",
            "phone": "+852 9345 6789",
            "wechat": "lxm_business",
            "policy_type": "General Insurance",
            "coverage_amount": 800000,
            "policy_start_date": "2024-08-15",
            "policy_end_date": "2025-08-15",
            "status": "Active"
        },
        {
            "name": "Leung Hoi Yan",
            "email": "leung.hoiyan@email.com",
            "phone": "+852 9567 8901",
            "wechat": "lhy_teacher",
            "policy_type": "Travel Insurance",
            "coverage_amount": 1000000,
            "policy_start_date": "2025-01-10",
            "policy_end_date": "2025-02-10",
            "status": "Active"
        },
        {
            "name": "Ho Chun Kit",
            "email": "ho.chunkit@email.com",
            "phone": "+852 9789 0123",
            "wechat": "hck_tech",
            "policy_type": "Life Insurance",
            "coverage_amount": 6000000,
            "policy_start_date": "2024-11-01",
            "policy_end_date": "2025-05-01",
            "status": "Active"
        }
    ]
    
    activity_types = [
        ("Call", "Follow-up call about policy details"),
        ("WeChat", "Sent WeChat message about renewal"),
        ("Email", "Sent email with policy proposal"),
        ("Meeting", "In-person meeting to discuss coverage"),
        ("Follow-up", "Scheduled follow-up for next week"),
        ("Renewal", "Discussed renewal options"),
        ("Claim", "Explained claim process"),
        ("Other", "General inquiry received")
    ]
    
    with app.app_context():
        conn = get_db()
        c = conn.cursor()
        
        # Check if clients already exist
        c.execute("SELECT COUNT(*) FROM clients")
        if c.fetchone()[0] > 0:
            print(f"⚠️  Database already has {c.fetchone()[0]} clients.")
            choice = input("Overwrite with sample data? (y/n): ")
            if choice.lower() != 'y':
                print("Cancelled.")
                conn.close()
                return
        
        # Clear existing data
        c.execute("DELETE FROM activity_log")
        c.execute("DELETE FROM clients")
        
        # Insert sample clients
        client_ids = []
        for client in sample_clients:
            c.execute('''
                INSERT INTO clients (name, email, phone, wechat, policy_type, 
                                   coverage_amount, policy_start_date, policy_end_date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                client['name'], client['email'], client['phone'],
                client['wechat'], client['policy_type'], client['coverage_amount'],
                client['policy_start_date'], client['policy_end_date'], client['status']
            ))
            client_ids.append(c.lastrowid)
            
            # Add random activities for each client
            num_activities = random.randint(1, 4)
            for _ in range(num_activities):
                activity_type, description = random.choice(activity_types)
                days_ago = random.randint(1, 90)
                created_at = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
                c.execute('''
                    INSERT INTO activity_log (client_id, activity_type, description, created_at)
                    VALUES (?, ?, ?, ?)
                ''', (c.lastrowid, activity_type, description, created_at))
        
        conn.commit()
        
        print(f"✅ Added {len(sample_clients)} sample clients!")
        print(f"✅ Added activities for each client")
        print(f"✅ Total clients: {len(client_ids)}")
        
        conn.close()

if __name__ == "__main__":
    generate_sample_data()
