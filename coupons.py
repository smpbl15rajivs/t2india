from datetime import datetime, timedelta
import uuid
import json
import random
import string

coupons_bp = Blueprint('coupons', __name__)

# Sample coupon storage (in production, use proper database)
ACTIVE_COUPONS = {
    'WELCOME10': {
        'code': 'WELCOME10',
        'type': 'percentage',
        'value': 10,
        'description': 'Welcome discount for new customers',
        'min_amount': 5000,
        'max_discount': 2000,
        'valid_from': '2024-01-01',
        'valid_until': '2024-12-31',
        'usage_limit': 1000,
        'used_count': 156,
        'applicable_categories': ['all'],
        'status': 'active',
        'created_by': 'admin',
        'created_at': '2024-01-01T00:00:00'
    },
    'SUMMER25': {
        'code': 'SUMMER25',
        'type': 'percentage',
        'value': 25,
        'description': 'Summer special discount',
        'min_amount': 15000,
        'max_discount': 5000,
        'valid_from': '2024-04-01',
        'valid_until': '2024-09-30',
        'usage_limit': 500,
        'used_count': 89,
        'applicable_categories': ['Heritage & Culture', 'Scenic & Nature'],
        'status': 'active',
        'created_by': 'marketing',
        'created_at': '2024-03-25T10:30:00'
    },
    'FAMILY500': {
        'code': 'FAMILY500',
        'type': 'fixed',
        'value': 500,
        'description': 'Fixed discount for family bookings',
        'min_amount': 8000,
        'max_discount': 500,