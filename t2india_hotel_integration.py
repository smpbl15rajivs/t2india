"""
T2India Hotel Contract Processing Integration
Seamlessly integrates hotel rate management with T2India routing system
"""

import os
import sys
import json
import sqlite3
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import uuid

class T2IndiaHotelIntegration:
    def __init__(self):
        self.hotel_db_path = '/home/ubuntu/hotel-rate-upload/src/costing_data.db'
        self.t2india_db_path = '/home/ubuntu/t2india-integrated-api/src/database/app.db'
        
    def get_hotel_rates_for_destination(self, destination, check_in, check_out, pax_count=2):
        """
        Get available hotel rates for a destination from the hotel contract system
        """
        try:
            conn = sqlite3.connect(self.hotel_db_path)
            cursor = conn.cursor()
            
            # Query hotels in the destination
            cursor.execute('''
                SELECT DISTINCT h.hotel_id, h.hotel_name, h.location, h.category,
                       pr.room_type, pr.meal_plan, pr.occupancy, pr.selling_price,
                       pr.special_conditions
                FROM hotel_uploads h
                JOIN processed_rates pr ON h.hotel_id = pr.hotel_id
                WHERE LOWER(h.location) LIKE LOWER(?) 
                AND h.processing_status = 'completed'
                AND pr.occupancy = ?
                ORDER BY pr.selling_price ASC
            ''', (f'%{destination}%', 'double' if pax_count == 2 else 'single'))
            
            hotels = cursor.fetchall()
            conn.close()
            
            # Process and format hotel data
            hotel_options = []
            for hotel in hotels:
                # Calculate total cost for stay duration
                check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
                check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
                nights = (check_out_date - check_in_date).days
                
                total_cost = hotel[7] * nights  # selling_price * nights
                
                hotel_option = {
                    'hotel_id': hotel[0],
                    'hotel_name': hotel[1],
                    'location': hotel[2],
                    'category': hotel[3],
                    'room_type': hotel[4],
                    'meal_plan': hotel[5],
                    'occupancy': hotel[6],
                    'rate_per_night': hotel[7],
                    'total_cost': total_cost,
                    'nights': nights,
                    'special_conditions': hotel[8],
                    'check_in': check_in,
                    'check_out': check_out
                }
                hotel_options.append(hotel_option)
            
            return {
                'success': True,
                'destination': destination,
                'hotels_found': len(hotel_options),
                'hotels': hotel_options[:10]  # Limit to top 10 options
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'destination': destination
            }
    
    def get_itinerary_hotel_costs(self, itinerary_data):
        """
        Calculate hotel costs for complete itinerary
        """
        try:
            total_hotel_cost = 0
            itinerary_hotels = []
            
            destinations = itinerary_data.get('destinations', [])
            
            for dest in destinations:
                destination_name = dest.get('name')
                check_in = dest.get('check_in')
                check_out = dest.get('check_out')
                pax_count = itinerary_data.get('pax_count', 2)
                
                # Get hotel options for this destination
                hotel_result = self.get_hotel_rates_for_destination(
                    destination_name, check_in, check_out, pax_count
                )
                
                if hotel_result['success'] and hotel_result['hotels']:
                    # Select best hotel based on category preference
                    preferred_category = itinerary_data.get('hotel_category', '4-star')
                    
                    # Find hotel matching preferred category
                    selected_hotel = None
                    for hotel in hotel_result['hotels']:
                        if preferred_category.lower() in hotel['category'].lower():
                            selected_hotel = hotel
                            break
                    
                    # If no preferred category found, select first available
                    if not selected_hotel:
                        selected_hotel = hotel_result['hotels'][0]
                    
                    total_hotel_cost += selected_hotel['total_cost']
                    itinerary_hotels.append({
                        'destination': destination_name,
                        'hotel': selected_hotel,
                        'selected_reason': f"Best {preferred_category} option available"
                    })
                else:
                    # Add estimated cost if no hotel data available
                    estimated_cost = self._estimate_hotel_cost(destination_name, check_in, check_out, pax_count)
                    total_hotel_cost += estimated_cost
                    itinerary_hotels.append({
                        'destination': destination_name,
                        'hotel': {
                            'hotel_name': f'Estimated {preferred_category} Hotel',
                            'category': preferred_category,
                            'total_cost': estimated_cost,
                            'rate_per_night': estimated_cost / ((datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days),
                            'estimated': True
                        },
                        'selected_reason': 'Estimated cost - no contract data available'
                    })
            
            return {
                'success': True,
                'total_hotel_cost': total_hotel_cost,
                'hotels_selected': itinerary_hotels,
                'cost_breakdown': {
                    'accommodation': total_hotel_cost,
                    'currency': 'INR'
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _estimate_hotel_cost(self, destination, check_in, check_out, pax_count):
        """
        Estimate hotel cost when no contract data available
        """
        # Base rates by destination type
        destination_rates = {
            'delhi': 8000, 'mumbai': 10000, 'bangalore': 7000, 'chennai': 6000,
            'kolkata': 5500, 'hyderabad': 6500, 'pune': 6000, 'ahmedabad': 5000,
            'jaipur': 6000, 'agra': 5500, 'goa': 12000, 'kerala': 8000,
            'cochin': 8000, 'munnar': 9000, 'alleppey': 10000,
            'kashmir': 9000, 'rajasthan': 6000, 'himachal': 7000, 'uttarakhand': 7000
        }
        
        # Find matching rate
        base_rate = 6000  # Default rate
        for location, rate in destination_rates.items():
            if location.lower() in destination.lower():
                base_rate = rate
                break
        
        # Calculate nights
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        nights = (check_out_date - check_in_date).days
        
        # Adjust for occupancy
        if pax_count == 1:
            base_rate *= 0.8
        elif pax_count >= 3:
            base_rate *= 1.3
        
        return base_rate * nights
    
    def integrate_with_routing_system(self, routing_result):
        """
        Integrate hotel costs with T2India routing system results
        """
        try:
            # Extract itinerary data from routing result
            itinerary_data = {
                'destinations': [],
                'pax_count': routing_result.get('pax_count', 2),
                'hotel_category': routing_result.get('hotel_preference', '4-star')
            }
            
            # Process each destination in the route
            route_destinations = routing_result.get('optimized_route', [])
            for i, dest in enumerate(route_destinations):
                if i < len(route_destinations) - 1:  # Not the last destination
                    destination_data = {
                        'name': dest['name'],
                        'check_in': dest.get('arrival_date', '2025-02-01'),
                        'check_out': route_destinations[i+1].get('arrival_date', '2025-02-03')
                    }
                    itinerary_data['destinations'].append(destination_data)
            
            # Get hotel costs
            hotel_result = self.get_itinerary_hotel_costs(itinerary_data)
            
            # Integrate with routing result
            if hotel_result['success']:
                routing_result['hotel_costs'] = hotel_result
                routing_result['total_accommodation_cost'] = hotel_result['total_hotel_cost']
                
                # Add hotel details to each destination
                for dest in routing_result.get('destinations', []):
                    dest_name = dest.get('name')
                    for hotel_info in hotel_result['hotels_selected']:
                        if hotel_info['destination'].lower() == dest_name.lower():
                            dest['recommended_hotel'] = hotel_info['hotel']
                            dest['hotel_cost'] = hotel_info['hotel']['total_cost']
                            break
            
            return routing_result
            
        except Exception as e:
            routing_result['hotel_integration_error'] = str(e)
            return routing_result

# Flask app for hotel integration API
app = Flask(__name__)
CORS(app)

hotel_integration = T2IndiaHotelIntegration()

@app.route('/api/hotels/destination/<destination>')
def get_destination_hotels(destination):
    """API endpoint to get hotels for a destination"""
    check_in = request.args.get('check_in', '2025-02-01')
    check_out = request.args.get('check_out', '2025-02-03')
    pax_count = int(request.args.get('pax_count', 2))
    
    result = hotel_integration.get_hotel_rates_for_destination(
        destination, check_in, check_out, pax_count
    )
    return jsonify(result)

@app.route('/api/hotels/itinerary-cost', methods=['POST'])
def calculate_itinerary_hotel_cost():
    """API endpoint to calculate hotel costs for complete itinerary"""
    itinerary_data = request.json
    result = hotel_integration.get_itinerary_hotel_costs(itinerary_data)
    return jsonify(result)

@app.route('/api/routing/with-hotels', methods=['POST'])
def routing_with_hotels():
    """API endpoint for routing with integrated hotel costs"""
    routing_data = request.json
    
    # This would integrate with the existing T2India routing system
    # For now, we'll simulate the integration
    routing_result = {
        'optimized_route': routing_data.get('destinations', []),
        'pax_count': routing_data.get('pax_count', 2),
        'hotel_preference': routing_data.get('hotel_category', '4-star'),
        'destinations': routing_data.get('destinations', [])
    }
    
    # Integrate hotel costs
    integrated_result = hotel_integration.integrate_with_routing_system(routing_result)
    return jsonify(integrated_result)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {
        'status': 'healthy',
        'service': 'T2India Hotel Integration',
        'version': '1.0.0',
        'hotel_db_status': 'connected' if os.path.exists(hotel_integration.hotel_db_path) else 'not_found'
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)

