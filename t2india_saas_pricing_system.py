"""
T2India SaaS Pricing Model Integration
Subscription-based pricing system for travel agencies and businesses
"""

import os
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid
import hashlib

class T2IndiaSaaSPricing:
    def __init__(self):
        self.db_path = '/home/ubuntu/t2india_saas.db'
        self.init_database()
        
        # SaaS pricing tiers
        self.pricing_tiers = {
            'starter': {
                'name': 'Starter',
                'monthly_price': 2999,  # INR
                'annual_price': 29990,  # INR (2 months free)
                'features': {
                    'itinerary_generation': 50,
                    'destinations_access': 25,
                    'handicraft_experiences': 10,
                    'hotel_rate_access': True,
                    'basic_support': True,
                    'api_calls': 1000,
                    'users': 2,
                    'custom_branding': False,
                    'advanced_analytics': False,
                    'priority_support': False
                },
                'target': 'Small travel agencies, freelance agents'
            },
            'professional': {
                'name': 'Professional',
                'monthly_price': 7999,  # INR
                'annual_price': 79990,  # INR
                'features': {
                    'itinerary_generation': 200,
                    'destinations_access': 100,
                    'handicraft_experiences': 50,
                    'hotel_rate_access': True,
                    'omneky_integration': True,
                    'advanced_routing': True,
                    'api_calls': 5000,
                    'users': 10,
                    'custom_branding': True,
                    'advanced_analytics': True,
                    'priority_support': True,
                    'white_label_option': False
                },
                'target': 'Medium travel agencies, tour operators'
            },
            'enterprise': {
                'name': 'Enterprise',
                'monthly_price': 19999,  # INR
                'annual_price': 199990,  # INR
                'features': {
                    'itinerary_generation': 'unlimited',
                    'destinations_access': 'unlimited',
                    'handicraft_experiences': 'unlimited',
                    'hotel_rate_access': True,
                    'omneky_integration': True,
                    'advanced_routing': True,
                    'api_calls': 'unlimited',
                    'users': 'unlimited',
                    'custom_branding': True,
                    'advanced_analytics': True,
                    'priority_support': True,
                    'white_label_option': True,
                    'dedicated_account_manager': True,
                    'custom_integrations': True,
                    'sla_guarantee': '99.9%'
                },
                'target': 'Large travel companies, OTAs, enterprise clients'
            }
        }
    
    def init_database(self):
        """Initialize SaaS subscription database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Subscriptions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                contact_email TEXT NOT NULL,
                contact_phone TEXT,
                plan_type TEXT NOT NULL,
                billing_cycle TEXT NOT NULL,
                subscription_status TEXT DEFAULT 'active',
                start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                end_date TIMESTAMP,
                monthly_price REAL,
                annual_price REAL,
                payment_status TEXT DEFAULT 'pending',
                last_payment_date TIMESTAMP,
                next_billing_date TIMESTAMP,
                usage_limits TEXT,
                current_usage TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_tracking (
                id TEXT PRIMARY KEY,
                subscription_id TEXT,
                feature_type TEXT,
                usage_count INTEGER DEFAULT 0,
                usage_date DATE DEFAULT CURRENT_DATE,
                api_endpoint TEXT,
                FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
            )
        ''')
        
        # Payment history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payment_history (
                id TEXT PRIMARY KEY,
                subscription_id TEXT,
                amount REAL,
                currency TEXT DEFAULT 'INR',
                payment_method TEXT,
                payment_status TEXT,
                transaction_id TEXT,
                payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                billing_period_start DATE,
                billing_period_end DATE,
                FOREIGN KEY (subscription_id) REFERENCES subscriptions (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_subscription(self, subscription_data):
        """Create new SaaS subscription"""
        try:
            plan_type = subscription_data.get('plan_type', 'starter')
            billing_cycle = subscription_data.get('billing_cycle', 'monthly')
            
            if plan_type not in self.pricing_tiers:
                return {'success': False, 'error': 'Invalid plan type'}
            
            plan_info = self.pricing_tiers[plan_type]
            subscription_id = str(uuid.uuid4())
            
            # Calculate pricing and dates
            if billing_cycle == 'annual':
                price = plan_info['annual_price']
                end_date = datetime.now() + timedelta(days=365)
            else:
                price = plan_info['monthly_price']
                end_date = datetime.now() + timedelta(days=30)
            
            next_billing = end_date
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO subscriptions 
                (id, company_name, contact_email, contact_phone, plan_type, billing_cycle,
                 end_date, monthly_price, annual_price, next_billing_date, usage_limits)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                subscription_id,
                subscription_data.get('company_name'),
                subscription_data.get('contact_email'),
                subscription_data.get('contact_phone'),
                plan_type,
                billing_cycle,
                end_date.isoformat(),
                plan_info['monthly_price'],
                plan_info['annual_price'],
                next_billing.isoformat(),
                json.dumps(plan_info['features'])
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'subscription_id': subscription_id,
                'plan': plan_info['name'],
                'price': price,
                'billing_cycle': billing_cycle,
                'features': plan_info['features'],
                'next_billing_date': next_billing.strftime('%Y-%m-%d'),
                'api_key': self._generate_api_key(subscription_id)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_usage_limits(self, subscription_id, feature_type):
        """Check if subscription has reached usage limits"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get subscription details
            cursor.execute('SELECT plan_type, usage_limits FROM subscriptions WHERE id = ?', (subscription_id,))
            result = cursor.fetchone()
            
            if not result:
                return {'allowed': False, 'error': 'Subscription not found'}
            
            plan_type, usage_limits_json = result
            usage_limits = json.loads(usage_limits_json)
            
            # Check feature limit
            feature_limit = usage_limits.get(feature_type)
            if feature_limit == 'unlimited':
                return {'allowed': True, 'remaining': 'unlimited'}
            
            if not isinstance(feature_limit, int):
                return {'allowed': True, 'remaining': 'unlimited'}
            
            # Get current month usage
            current_month = datetime.now().strftime('%Y-%m')
            cursor.execute('''
                SELECT SUM(usage_count) FROM usage_tracking 
                WHERE subscription_id = ? AND feature_type = ? 
                AND strftime('%Y-%m', usage_date) = ?
            ''', (subscription_id, feature_type, current_month))
            
            current_usage = cursor.fetchone()[0] or 0
            remaining = max(0, feature_limit - current_usage)
            
            conn.close()
            
            return {
                'allowed': remaining > 0,
                'remaining': remaining,
                'limit': feature_limit,
                'used': current_usage
            }
            
        except Exception as e:
            return {'allowed': False, 'error': str(e)}
    
    def track_usage(self, subscription_id, feature_type, usage_count=1, api_endpoint=None):
        """Track feature usage for billing and limits"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            usage_id = str(uuid.uuid4())
            cursor.execute('''
                INSERT INTO usage_tracking 
                (id, subscription_id, feature_type, usage_count, api_endpoint)
                VALUES (?, ?, ?, ?, ?)
            ''', (usage_id, subscription_id, feature_type, usage_count, api_endpoint))
            
            conn.commit()
            conn.close()
            
            return {'success': True, 'usage_tracked': usage_count}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_subscription_analytics(self, subscription_id):
        """Get usage analytics for subscription"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get subscription info
            cursor.execute('''
                SELECT company_name, plan_type, subscription_status, start_date, usage_limits
                FROM subscriptions WHERE id = ?
            ''', (subscription_id,))
            
            sub_info = cursor.fetchone()
            if not sub_info:
                return {'success': False, 'error': 'Subscription not found'}
            
            # Get current month usage
            current_month = datetime.now().strftime('%Y-%m')
            cursor.execute('''
                SELECT feature_type, SUM(usage_count) as total_usage
                FROM usage_tracking 
                WHERE subscription_id = ? AND strftime('%Y-%m', usage_date) = ?
                GROUP BY feature_type
            ''', (subscription_id, current_month))
            
            usage_data = dict(cursor.fetchall())
            
            # Get usage limits
            usage_limits = json.loads(sub_info[4])
            
            # Calculate usage percentages
            usage_analytics = {}
            for feature, limit in usage_limits.items():
                if isinstance(limit, int):
                    used = usage_data.get(feature, 0)
                    percentage = (used / limit * 100) if limit > 0 else 0
                    usage_analytics[feature] = {
                        'used': used,
                        'limit': limit,
                        'percentage': round(percentage, 2),
                        'remaining': max(0, limit - used)
                    }
                else:
                    usage_analytics[feature] = {
                        'used': usage_data.get(feature, 0),
                        'limit': 'unlimited',
                        'percentage': 0,
                        'remaining': 'unlimited'
                    }
            
            conn.close()
            
            return {
                'success': True,
                'subscription_info': {
                    'company_name': sub_info[0],
                    'plan_type': sub_info[1],
                    'status': sub_info[2],
                    'start_date': sub_info[3]
                },
                'current_month_usage': usage_analytics,
                'billing_period': current_month
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upgrade_subscription(self, subscription_id, new_plan_type):
        """Upgrade subscription to higher tier"""
        try:
            if new_plan_type not in self.pricing_tiers:
                return {'success': False, 'error': 'Invalid plan type'}
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get current subscription
            cursor.execute('SELECT plan_type, billing_cycle FROM subscriptions WHERE id = ?', (subscription_id,))
            current_info = cursor.fetchone()
            
            if not current_info:
                return {'success': False, 'error': 'Subscription not found'}
            
            current_plan, billing_cycle = current_info
            new_plan_info = self.pricing_tiers[new_plan_type]
            
            # Calculate prorated pricing
            if billing_cycle == 'annual':
                new_price = new_plan_info['annual_price']
            else:
                new_price = new_plan_info['monthly_price']
            
            # Update subscription
            cursor.execute('''
                UPDATE subscriptions 
                SET plan_type = ?, usage_limits = ?, monthly_price = ?, annual_price = ?
                WHERE id = ?
            ''', (
                new_plan_type,
                json.dumps(new_plan_info['features']),
                new_plan_info['monthly_price'],
                new_plan_info['annual_price'],
                subscription_id
            ))
            
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'upgraded_from': current_plan,
                'upgraded_to': new_plan_type,
                'new_price': new_price,
                'new_features': new_plan_info['features']
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _generate_api_key(self, subscription_id):
        """Generate API key for subscription"""
        key_data = f"t2india_{subscription_id}_{datetime.now().isoformat()}"
        return hashlib.sha256(key_data.encode()).hexdigest()[:32]
    
    def get_pricing_comparison(self):
        """Get pricing comparison for all tiers"""
        comparison = {}
        
        for tier_id, tier_info in self.pricing_tiers.items():
            comparison[tier_id] = {
                'name': tier_info['name'],
                'monthly_price': tier_info['monthly_price'],
                'annual_price': tier_info['annual_price'],
                'annual_savings': tier_info['monthly_price'] * 12 - tier_info['annual_price'],
                'key_features': [
                    f"Up to {tier_info['features']['itinerary_generation']} itineraries/month",
                    f"{tier_info['features']['destinations_access']} destinations access",
                    f"{tier_info['features']['handicraft_experiences']} handicraft experiences",
                    f"{tier_info['features']['users']} team members",
                    "Hotel rate access" if tier_info['features']['hotel_rate_access'] else "No hotel rates",
                    "Custom branding" if tier_info['features'].get('custom_branding') else "Standard branding",
                    "Priority support" if tier_info['features'].get('priority_support') else "Basic support"
                ],
                'target_audience': tier_info['target']
            }
        
        return comparison

# Flask app for SaaS pricing API
app = Flask(__name__)
CORS(app)

saas_pricing = T2IndiaSaaSPricing()

@app.route('/api/saas/pricing')
def get_pricing():
    """Get all pricing tiers"""
    return jsonify(saas_pricing.get_pricing_comparison())

@app.route('/api/saas/subscribe', methods=['POST'])
def create_subscription():
    """Create new subscription"""
    subscription_data = request.json
    result = saas_pricing.create_subscription(subscription_data)
    return jsonify(result)

@app.route('/api/saas/usage-check/<subscription_id>/<feature_type>')
def check_usage(subscription_id, feature_type):
    """Check usage limits for feature"""
    result = saas_pricing.check_usage_limits(subscription_id, feature_type)
    return jsonify(result)

@app.route('/api/saas/track-usage', methods=['POST'])
def track_usage():
    """Track feature usage"""
    usage_data = request.json
    result = saas_pricing.track_usage(
        usage_data.get('subscription_id'),
        usage_data.get('feature_type'),
        usage_data.get('usage_count', 1),
        usage_data.get('api_endpoint')
    )
    return jsonify(result)

@app.route('/api/saas/analytics/<subscription_id>')
def get_analytics(subscription_id):
    """Get subscription analytics"""
    result = saas_pricing.get_subscription_analytics(subscription_id)
    return jsonify(result)

@app.route('/api/saas/upgrade', methods=['POST'])
def upgrade_subscription():
    """Upgrade subscription"""
    upgrade_data = request.json
    result = saas_pricing.upgrade_subscription(
        upgrade_data.get('subscription_id'),
        upgrade_data.get('new_plan_type')
    )
    return jsonify(result)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'T2India SaaS Pricing System',
        'version': '1.0.0',
        'available_plans': list(saas_pricing.pricing_tiers.keys())
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=False)

