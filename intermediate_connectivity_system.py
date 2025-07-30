"""
T2India Intermediate Connectivity System
A → C → B routing where C is the intermediate hub
"""

class IntermediateConnectivitySystem:
    def __init__(self):
        # Define intermediate hubs (C locations) for various destinations
        self.intermediate_hubs = {
            # Airport hubs for flight connections
            "Hampi": {
                "nearest_airports": {
                    "Hubli": {"distance": "160km", "travel_time": "3h", "transport": "cab"},
                    "Bangalore": {"distance": "350km", "travel_time": "6h", "transport": "cab"},
                    "Belgaum": {"distance": "190km", "travel_time": "4h", "transport": "cab"}
                },
                "primary_hub": "Hubli"
            },
            "Darjeeling": {
                "nearest_airports": {
                    "Bagdogra": {"distance": "95km", "travel_time": "3h", "transport": "cab"},
                    "Siliguri": {"distance": "78km", "travel_time": "2.5h", "transport": "cab"}
                },
                "primary_hub": "Bagdogra"
            },
            "Rishikesh": {
                "nearest_airports": {
                    "Dehradun": {"distance": "35km", "travel_time": "1h", "transport": "cab"},
                    "Delhi": {"distance": "240km", "travel_time": "6h", "transport": "road"}
                },
                "primary_hub": "Dehradun"
            },
            "Haridwar": {
                "nearest_airports": {
                    "Dehradun": {"distance": "55km", "travel_time": "1.5h", "transport": "cab"},
                    "Delhi": {"distance": "220km", "travel_time": "5.5h", "transport": "road"}
                },
                "primary_hub": "Dehradun"
            },
            "Puri": {
                "nearest_airports": {
                    "Bhubaneswar": {"distance": "65km", "travel_time": "1.5h", "transport": "cab"}
                },
                "primary_hub": "Bhubaneswar"
            },
            "Alleppey": {
                "nearest_airports": {
                    "Cochin": {"distance": "85km", "travel_time": "2h", "transport": "cab"}
                },
                "primary_hub": "Cochin"
            },
            "Kumarakom": {
                "nearest_airports": {
                    "Cochin": {"distance": "95km", "travel_time": "2.5h", "transport": "cab"}
                },
                "primary_hub": "Cochin"
            },
            "Manali": {
                "nearest_airports": {
                    "Bhuntar": {"distance": "50km", "travel_time": "2h", "transport": "cab"},
                    "Chandigarh": {"distance": "310km", "travel_time": "8h", "transport": "road"}
                },
                "primary_hub": "Bhuntar"
            },
            "Shimla": {
                "nearest_airports": {
                    "Chandigarh": {"distance": "120km", "travel_time": "3.5h", "transport": "cab"},
                    "Delhi": {"distance": "350km", "travel_time": "8h", "transport": "road"}
                },
                "primary_hub": "Chandigarh"
            }
        }
        
        # Major connectivity hubs with flight connections
        self.major_hubs = {
            "Delhi": {
                "type": "major_airport",
                "connections": "International + Domestic",
                "serves_regions": ["North India", "Golden Triangle", "Hill Stations"]
            },
            "Mumbai": {
                "type": "major_airport", 
                "connections": "International + Domestic",
                "serves_regions": ["West India", "Goa", "Rajasthan"]
            },
            "Bangalore": {
                "type": "major_airport",
                "connections": "International + Domestic", 
                "serves_regions": ["South India", "Karnataka", "Tech Cities"]
            },
            "Kolkata": {
                "type": "major_airport",
                "connections": "International + Domestic",
                "serves_regions": ["East India", "West Bengal", "Northeast"]
            },
            "Chennai": {
                "type": "major_airport",
                "connections": "International + Domestic",
                "serves_regions": ["Tamil Nadu", "South India Coast"]
            },
            "Cochin": {
                "type": "major_airport",
                "connections": "International + Domestic",
                "serves_regions": ["Kerala", "Backwaters", "Spice Coast"]
            },
            "Hubli": {
                "type": "regional_airport",
                "connections": "Domestic only",
                "serves_regions": ["North Karnataka", "Hampi region"]
            },
            "Bagdogra": {
                "type": "regional_airport", 
                "connections": "Domestic only",
                "serves_regions": ["North Bengal", "Darjeeling", "Sikkim"]
            },
            "Bhubaneswar": {
                "type": "regional_airport",
                "connections": "Domestic only", 
                "serves_regions": ["Odisha", "Temple circuits"]
            }
        }
        
        # Railway junction hubs
        self.railway_hubs = {
            "New Jalpaiguri": {
                "serves": ["Darjeeling", "Sikkim", "Northeast"],
                "major_trains": ["Rajdhani Express", "Darjeeling Mail"]
            },
            "Hospet Junction": {
                "serves": ["Hampi"],
                "major_trains": ["Hampi Express", "Karnataka Express"]
            },
            "Haridwar Junction": {
                "serves": ["Rishikesh", "Char Dham"],
                "major_trains": ["Shatabdi Express", "Jan Shatabdi"]
            }
        }

    def find_intermediate_hub(self, origin, destination):
        """Find intermediate hub C for A→C→B routing"""
        
        # Check if origin needs intermediate hub
        if origin in self.intermediate_hubs:
            hub_info = self.intermediate_hubs[origin]
            primary_hub = hub_info["primary_hub"]
            hub_details = hub_info["nearest_airports"][primary_hub]
            
            return {
                "origin": origin,
                "intermediate_hub": primary_hub,
                "destination": destination,
                "route_type": "A→C→B",
                "leg1": {
                    "from": origin,
                    "to": primary_hub,
                    "distance": hub_details["distance"],
                    "time": hub_details["travel_time"],
                    "transport": hub_details["transport"]
                },
                "leg2": {
                    "from": primary_hub,
                    "to": destination,
                    "transport": "flight",
                    "note": "Flight connection from hub"
                },
                "total_complexity": "2-leg journey"
            }
        
        # Check if destination needs intermediate hub (reverse routing)
        if destination in self.intermediate_hubs:
            hub_info = self.intermediate_hubs[destination]
            primary_hub = hub_info["primary_hub"]
            hub_details = hub_info["nearest_airports"][primary_hub]
            
            return {
                "origin": origin,
                "intermediate_hub": primary_hub,
                "destination": destination,
                "route_type": "A→C→B",
                "leg1": {
                    "from": origin,
                    "to": primary_hub,
                    "transport": "flight",
                    "note": "Flight to nearest hub"
                },
                "leg2": {
                    "from": primary_hub,
                    "to": destination,
                    "distance": hub_details["distance"],
                    "time": hub_details["travel_time"],
                    "transport": hub_details["transport"]
                },
                "total_complexity": "2-leg journey"
            }
        
        # Direct connection available
        return {
            "origin": origin,
            "destination": destination,
            "route_type": "A→B",
            "direct_connection": True,
            "note": "No intermediate hub required"
        }

    def get_all_possible_routes(self, origin, destination):
        """Get all possible routing options including intermediate hubs"""
        
        routes = []
        
        # Primary route via intermediate hub
        primary_route = self.find_intermediate_hub(origin, destination)
        routes.append(primary_route)
        
        # Alternative routes if origin has multiple hub options
        if origin in self.intermediate_hubs:
            hub_info = self.intermediate_hubs[origin]
            for hub_name, hub_details in hub_info["nearest_airports"].items():
                if hub_name != hub_info["primary_hub"]:
                    alternative_route = {
                        "origin": origin,
                        "intermediate_hub": hub_name,
                        "destination": destination,
                        "route_type": "A→C→B (Alternative)",
                        "leg1": {
                            "from": origin,
                            "to": hub_name,
                            "distance": hub_details["distance"],
                            "time": hub_details["travel_time"],
                            "transport": hub_details["transport"]
                        },
                        "leg2": {
                            "from": hub_name,
                            "to": destination,
                            "transport": "flight",
                            "note": "Alternative hub connection"
                        },
                        "priority": "secondary"
                    }
                    routes.append(alternative_route)
        
        return routes

    def calculate_total_journey_time(self, route):
        """Calculate total journey time for multi-leg routes"""
        
        if route.get("direct_connection"):
            return {"total_time": "Direct connection", "complexity": "Simple"}
        
        leg1_time = 0
        leg2_time = 0
        
        # Parse leg 1 time
        if "leg1" in route and "time" in route["leg1"]:
            time_str = route["leg1"]["time"]
            if "h" in time_str:
                leg1_time = float(time_str.replace("h", ""))
        
        # Estimate leg 2 time (flight time based on distance categories)
        if "leg2" in route:
            # Rough flight time estimates
            flight_estimates = {
                "short": 1.5,  # < 500km
                "medium": 2.5,  # 500-1000km  
                "long": 3.5    # > 1000km
            }
            leg2_time = flight_estimates["medium"]  # Default estimate
        
        total_time = leg1_time + leg2_time + 2  # +2 hours for connections/transfers
        
        return {
            "leg1_time": f"{leg1_time}h",
            "leg2_time": f"{leg2_time}h", 
            "connection_time": "2h",
            "total_time": f"{total_time}h",
            "complexity": "Multi-leg journey"
        }

    def format_route_output(self, routes):
        """Format route information for client presentation"""
        
        output = "=== INTERMEDIATE CONNECTIVITY ANALYSIS ===\n\n"
        
        for i, route in enumerate(routes, 1):
            route_priority = "PRIMARY" if i == 1 else "ALTERNATIVE"
            output += f"{route_priority} ROUTE {i}:\n"
            output += f"Route Type: {route['route_type']}\n"
            
            if route.get("direct_connection"):
                output += f"{route['origin']} → {route['destination']} (Direct)\n"
                output += "No intermediate hub required\n"
            else:
                output += f"{route['origin']} → {route['intermediate_hub']} → {route['destination']}\n"
                
                # Leg 1 details
                leg1 = route['leg1']
                output += f"\nLeg 1: {leg1['from']} → {leg1['to']}\n"
                if 'distance' in leg1:
                    output += f"  Distance: {leg1['distance']}\n"
                if 'time' in leg1:
                    output += f"  Time: {leg1['time']}\n"
                output += f"  Transport: {leg1['transport'].title()}\n"
                
                # Leg 2 details  
                leg2 = route['leg2']
                output += f"\nLeg 2: {leg2['from']} → {leg2['to']}\n"
                output += f"  Transport: {leg2['transport'].title()}\n"
                if 'note' in leg2:
                    output += f"  Note: {leg2['note']}\n"
                
                # Journey time calculation
                time_analysis = self.calculate_total_journey_time(route)
                output += f"\nJourney Time Analysis:\n"
                output += f"  Leg 1: {time_analysis['leg1_time']}\n"
                output += f"  Leg 2: {time_analysis['leg2_time']}\n" 
                output += f"  Connections: {time_analysis['connection_time']}\n"
                output += f"  Total: {time_analysis['total_time']}\n"
                output += f"  Complexity: {time_analysis['complexity']}\n"
            
            output += "\n" + "-"*50 + "\n\n"
        
        return output

def test_intermediate_connectivity():
    """Test the intermediate connectivity system"""
    
    system = IntermediateConnectivitySystem()
    
    test_routes = [
        ("Hampi", "Delhi"),
        ("Darjeeling", "Mumbai"), 
        ("Delhi", "Darjeeling"),
        ("Goa", "Hampi"),
        ("Rishikesh", "Kolkata"),
        ("Puri", "Delhi"),
        ("Cochin", "Darjeeling"),
        ("Delhi", "Goa")  # Direct connection test
    ]
    
    print("=" * 80)
    print("T2INDIA INTERMEDIATE CONNECTIVITY SYSTEM - TESTING")
    print("=" * 80)
    
    for origin, destination in test_routes:
        print(f"\n{'='*20} ROUTE: {origin} → {destination} {'='*20}")
        
        routes = system.get_all_possible_routes(origin, destination)
        formatted_output = system.format_route_output(routes)
        print(formatted_output)
    
    print("=" * 80)
    print("INTERMEDIATE CONNECTIVITY TESTING COMPLETED")
    print("=" * 80)

if __name__ == "__main__":
    test_intermediate_connectivity()

