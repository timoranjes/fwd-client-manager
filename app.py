"""
FWD Client Management System
A lightweight Flask web application for insurance agents
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import sqlite3
import os
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)
app.secret_key = 'fwd-client-manager-secret-key'
DATABASE = os.path.join(os.path.dirname(__file__), 'database.db')

# ============== DATABASE HELPERS ==============

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with all tables"""
    conn = get_db()
    c = conn.cursor()
    
    # Clients table
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            wechat TEXT,
            policy_type TEXT,
            coverage_amount REAL,
            policy_start_date TEXT,
            policy_end_date TEXT,
            status TEXT DEFAULT 'Active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Activity log table
    c.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            activity_type TEXT,
            description TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    # Settings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# ============== ROUTES ==============

@app.route('/')
def dashboard():
    """Dashboard overview"""
    conn = get_db()
    c = conn.cursor()
    
    # Get stats
    c.execute('SELECT COUNT(*) FROM clients')
    total_clients = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM clients WHERE status = ?', ('Active',))
    active_policies = c.fetchone()[0]
    
    # Get upcoming renewals (30 days)
    today = datetime.now().strftime('%Y-%m-%d')
    thirty_days = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    c.execute('''
        SELECT COUNT(*) FROM clients 
        WHERE policy_end_date BETWEEN ? AND ?
    ''', (today, thirty_days))
    upcoming_renewals = c.fetchone()[0]
    
    # Get expired policies
    c.execute('SELECT COUNT(*) FROM clients WHERE status = ?', ('Expired',))
    expired_policies = c.fetchone()[0]
    
    # Get recent clients
    c.execute('SELECT * FROM clients ORDER BY created_at DESC LIMIT 5')
    recent_clients = c.fetchall()
    
    # Get recent activities
    c.execute('''
        SELECT al.*, c.name as client_name 
        FROM activity_log al 
        LEFT JOIN clients c ON al.client_id = c.id 
        ORDER BY al.created_at DESC LIMIT 10
    ''')
    recent_activities = c.fetchall()
    
    conn.close()
    
    return render_template('dashboard.html',
                         total_clients=total_clients,
                         active_policies=active_policies,
                         upcoming_renewals=upcoming_renewals,
                         expired_policies=expired_policies,
                         recent_clients=recent_clients,
                         recent_activities=recent_activities)

@app.route('/clients')
def clients():
    """List all clients"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clients ORDER BY name')
    clients = c.fetchall()
    conn.close()
    return render_template('clients.html', clients=clients)

@app.route('/client/add', methods=['GET', 'POST'])
def add_client():
    """Add new client"""
    if request.method == 'POST':
        conn = get_db()
        c = conn.cursor()
        c.execute('''
            INSERT INTO clients (name, email, phone, wechat, policy_type, 
                               coverage_amount, policy_start_date, policy_end_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            request.form['name'],
            request.form.get('email'),
            request.form.get('phone'),
            request.form.get('wechat'),
            request.form.get('policy_type'),
            request.form.get('coverage_amount'),
            request.form.get('policy_start_date'),
            request.form.get('policy_end_date'),
            request.form.get('status', 'Active')
        ))
        client_id = c.lastrowid
        
        # Log activity
        c.execute('''
            INSERT INTO activity_log (client_id, activity_type, description)
            VALUES (?, 'Created', 'Client added to system')
        ''', (client_id,))
        
        conn.commit()
        conn.close()
        flash('Client added successfully!', 'success')
        return redirect(url_for('clients'))
    
    return render_template('client_form.html', client=None, action='Add')

@app.route('/client/<int:client_id>')
def client_detail(client_id):
    """View client details"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client = c.fetchone()
    
    if client:
        c.execute('''
            SELECT * FROM activity_log 
            WHERE client_id = ? 
            ORDER BY created_at DESC
        ''', (client_id,))
        activities = c.fetchall()
        conn.close()
        return render_template('client_detail.html', client=client, activities=activities)
    else:
        conn.close()
        flash('Client not found!', 'error')
        return redirect(url_for('clients'))

@app.route('/client/<int:client_id>/edit', methods=['GET', 'POST'])
def edit_client(client_id):
    """Edit client"""
    conn = get_db()
    c = conn.cursor()
    
    if request.method == 'POST':
        c.execute('''
            UPDATE clients SET 
                name = ?, email = ?, phone = ?, wechat = ?, 
                policy_type = ?, coverage_amount = ?, 
                policy_start_date = ?, policy_end_date = ?, status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (
            request.form['name'],
            request.form.get('email'),
            request.form.get('phone'),
            request.form.get('wechat'),
            request.form.get('policy_type'),
            request.form.get('coverage_amount'),
            request.form.get('policy_start_date'),
            request.form.get('policy_end_date'),
            request.form.get('status'),
            client_id
        ))
        
        # Log activity
        c.execute('''
            INSERT INTO activity_log (client_id, activity_type, description)
            VALUES (?, 'Updated', 'Client information updated')
        ''', (client_id,))
        
        conn.commit()
        conn.close()
        flash('Client updated successfully!', 'success')
        return redirect(url_for('client_detail', client_id=client_id))
    
    c.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client = c.fetchone()
    conn.close()
    
    if client:
        return render_template('client_form.html', client=client, action='Edit')
    else:
        flash('Client not found!', 'error')
        return redirect(url_for('clients'))

@app.route('/client/<int:client_id>/delete')
def delete_client(client_id):
    """Delete client"""
    conn = get_db()
    c = conn.cursor()
    c.execute('DELETE FROM activity_log WHERE client_id = ?', (client_id,))
    c.execute('DELETE FROM clients WHERE id = ?', (client_id,))
    conn.commit()
    conn.close()
    flash('Client deleted successfully!', 'success')
    return redirect(url_for('clients'))

@app.route('/client/<int:client_id>/add_note', methods=['POST'])
def add_note(client_id):
    """Add activity note"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO activity_log (client_id, activity_type, description)
        VALUES (?, ?, ?)
    ''', (client_id, request.form['activity_type'], request.form['description']))
    conn.commit()
    conn.close()
    flash('Note added successfully!', 'success')
    return redirect(url_for('client_detail', client_id=client_id))

@app.route('/renewals')
def renewals():
    """View upcoming renewals"""
    conn = get_db()
    c = conn.cursor()
    
    # Get filter parameter
    filter_type = request.args.get('filter', 'all')
    today = datetime.now().strftime('%Y-%m-%d')
    
    if filter_type == 'expired':
        c.execute('''
            SELECT * FROM clients 
            WHERE status = 'Expired' OR policy_end_date < ?
            ORDER BY policy_end_date ASC
        ''', (today,))
    elif filter_type == '30':
        thirty_days = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        c.execute('''
            SELECT * FROM clients 
            WHERE policy_end_date BETWEEN ? AND ?
            ORDER BY policy_end_date ASC
        ''', (today, thirty_days))
    elif filter_type == '60':
        sixty_days = (datetime.now() + timedelta(days=60)).strftime('%Y-%m-%d')
        c.execute('''
            SELECT * FROM clients 
            WHERE policy_end_date BETWEEN ? AND ?
            ORDER BY policy_end_date ASC
        ''', (today, sixty_days))
    elif filter_type == '90':
        ninety_days = (datetime.now() + timedelta(days=90)).strftime('%Y-%m-%d')
        c.execute('''
            SELECT * FROM clients 
            WHERE policy_end_date BETWEEN ? AND ?
            ORDER BY policy_end_date ASC
        ''', (today, ninety_days))
    else:
        c.execute('''
            SELECT * FROM clients 
            WHERE policy_end_date >= ?
            ORDER BY policy_end_date ASC
        ''', (today,))
    
    renewals = c.fetchall()
    conn.close()
    return render_template('renewals.html', renewals=renewals, filter_type=filter_type)

@app.route('/calendar')
def calendar():
    """View renewal calendar"""
    return render_template('calendar.html')

@app.route('/api/calendar_events')
def calendar_events():
    """API for calendar events"""
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT id, name, policy_end_date as date, policy_type, status
        FROM clients
        WHERE policy_end_date IS NOT NULL
    ''')
    events = c.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in events])

@app.route('/search')
def search():
    """Search clients"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('clients'))
    
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        SELECT * FROM clients 
        WHERE name LIKE ? OR email LIKE ? OR phone LIKE ? OR wechat LIKE ?
        ORDER BY name
    ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
    results = c.fetchall()
    conn.close()
    return render_template('clients.html', clients=results, search_query=query)

@app.route('/export')
def export():
    """Export clients data"""
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM clients ORDER BY name')
    clients = c.fetchall()
    conn.close()
    
    # Generate CSV
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['ID', 'Name', 'Email', 'Phone', 'WeChat', 'Policy Type', 
                    'Coverage', 'Start Date', 'End Date', 'Status', 'Created'])
    
    # Data
    for client in clients:
        writer.writerow([client['id'], client['name'], client['email'], 
                        client['phone'], client['wechat'], client['policy_type'],
                        client['coverage_amount'], client['policy_start_date'],
                        client['policy_end_date'], client['status'], client['created_at']])
    
    response = app.response_class(
        response=output.getvalue(),
        status=200,
        mimetype='text/csv'
    )
    response.headers.set('Content-Disposition', 'attachment', filename='clients_export.csv')
    return response

@app.route('/reports')
def reports():
    """Reports and analytics"""
    conn = get_db()
    c = conn.cursor()
    
    # Policy type breakdown
    c.execute('''
        SELECT policy_type, COUNT(*) as count, SUM(coverage_amount) as total
        FROM clients
        WHERE policy_type IS NOT NULL AND policy_type != ''
        GROUP BY policy_type
    ''')
    policy_breakdown = c.fetchall()
    
    # Status breakdown
    c.execute('''
        SELECT status, COUNT(*) as count
        FROM clients
        GROUP BY status
    ''')
    status_breakdown = c.fetchall()
    
    # Monthly new clients (last 6 months)
    c.execute('''
        SELECT strftime('%Y-%m', created_at) as month, COUNT(*) as count
        FROM clients
        WHERE created_at >= date('now', '-6 months')
        GROUP BY month
        ORDER BY month DESC
    ''')
    monthly_new = c.fetchall()
    
    conn.close()
    
    return render_template('reports.html',
                         policy_breakdown=policy_breakdown,
                         status_breakdown=status_breakdown,
                         monthly_new=monthly_new)

# ============== MAIN ==============

if __name__ == '__main__':
    # Initialize database
    if not os.path.exists(DATABASE):
        init_db()
        print("Database initialized!")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
