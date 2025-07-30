"""
Intelligent Itinerary Builder for T2India
Helps clients build complete travel plans from minimal input
"""

class ItinerarySuggestionEngine:
    def __init__(self):
        # Popular travel circuits in India
        self.travel_circuits = {
            "golden_triangle": {
                "destinations": ["Delhi", "Agra", "Jaipur"],
                "optimal_route": ["Delhi", "Agra", "Jaipur", "Delhi"],
                "recommended_duration": {"min": 5, "max": 7, "optimal": 6},
                "entry_exit": "Delhi",
                "travel_times": {
                    "Delhi-Agra": {"hours": 3.5, "km": 230},
                    "Agra-Jaipur": {"hours": 4.5, "km": 240},
                    "Jaipur-Delhi": {"hours": 5, "km": 280}
                },
                "highlights": [
                    "Red Fort & India Gate (Delhi)",
                    "Taj Mahal & Agra Fort (Agra)", 
                    "Amber Fort & City Palace (Jaipur)"
                ]
            },
            "rajasthan_royal": {
                "destinations": ["Jaipur", "Jodhpur", "Udaipur"],
                "optimal_route": ["Jaipur", "Jodhpur", "Udaipur", "Jaipur"],
                "recommended_duration": {"min": 7, "max": 10, "optimal": 8},
                "entry_exit": "Jaipur",
                "travel_times": {
                    "Jaipur-Jodhpur": {"hours": 5.5, "km": 340},
                    "Jodhpur-Udaipur": {"hours": 4.5, "km": 250},
                    "Udaipur-Jaipur": {"hours": 6, "km": 390}
                },
                "highlights": [
                    "Pink City & Amber Fort (Jaipur)",
                    "Blue City & Mehrangarh Fort (Jodhpur)",
                    "City of Lakes & Lake Palace (Udaipur)"
                ]
            },
            "kerala_backwaters": {
                "destinations": ["Kochi", "Munnar", "Alleppey"],
                "optimal_route": ["Kochi", "Munnar", "Alleppey", "Kochi"],
                "recommended_duration": {"min": 5, "max": 8, "optimal": 6},
                "entry_exit": "Kochi",
                "travel_times": {
                    "Kochi-Munnar": {"hours": 4, "km": 130},
                    "Munnar-Alleppey": {"hours": 4.5, "km": 170},
                    "Alleppey-Kochi": {"hours": 1.5, "km": 60}
                },
                "highlights": [
                    "Chinese Fishing Nets & Spice Markets (Kochi)",
                    "Tea Plantations & Hill Stations (Munnar)",
                    "Houseboat & Backwater Cruise (Alleppey)"
                ]
            }
        }
        
        # Distance and travel time matrix for major Indian cities
        self.city_matrix = {
            "Delhi": {
                "Agra": {"hours": 3.5, "km": 230},
                "Jaipur": {"hours": 5, "km": 280},
                "Mumbai": {"hours": 17, "km": 1400, "flight": 2},
                "Goa": {"hours": 20, "km": 1900, "flight": 2.5},
                "Kolkata": {"hours": 17, "km": 1500, "flight": 2.5}
            },
            "Mumbai": {
                "Goa": {"hours": 8, "km": 600},
                "Pune": {"hours": 3, "km": 150},
                "Delhi": {"hours": 17, "km": 1400, "flight": 2}
            },
            "Goa": {
                "Mumbai": {"hours": 8, "km": 600},
                "Bangalore": {"hours": 8, "km": 560},
                "Hampi": {
                    "hours": 5, "km": 350,
                    "public_transport": {"bus": "₹350-500"},
                    "private_transport": {"car": "₹3000-4500", "taxi": "₹4000-6000"}
                },
                "Delhi": {"hours": 20, "km": 1900, "flight": 2.5}
            },
            "Kolkata": {
                "Delhi": {"hours": 17, "km": 1500, "flight": 2.5},
                "Darjeeling": {
                    "hours": 12, "km": 650,
                    "public_transport": {"bus": "₹550-1400", "train": "₹3000-11000"},
                    "private_transport": {"car": "₹8000-12000", "taxi": "₹10000-15000"}
                },
                "Sikkim": {
                    "hours": 14, "km": 720,
                    "public_transport": {"bus": "₹800-1500"},
                    "private_transport": {"car": "₹10000-15000", "taxi": "₹12000-18000"}
                },
                "Puri": {
                    "hours": 6, "km": 500,
                    "public_transport": {"bus": "₹500-800", "train": "₹800-2000"},
                    "private_transport": {"car": "₹4000-6000", "taxi": "₹5000-8000"}
                }
            },
            "Hampi": {
                "Goa": {"hours": 5, "km": 350},
                "Bangalore": {"hours": 6, "km": 350}
            },
            "Darjeeling": {
                "Kolkata": {"hours": 12, "km": 650},
                "Sikkim": {"hours": 4, "km": 100}
            },
            "Puri": {
                "Kolkata": {"hours": 6, "km": 500},
                "Bhubaneswar": {"hours": 1, "km": 60}
            }
        }

        # Regional extensions - suggest nearby destinations
        self.regional_extensions = {
            "Kolkata": {
                "hill_stations": {
                    "destinations": ["Darjeeling", "Sikkim"],
                    "theme": "Mountain & Tea Gardens",
                    "description": "Explore hill stations, tea plantations, and mountain monasteries",
                    "additional_days": 3
                },
                "religious": {
                    "destinations": ["Puri"],
                    "theme": "Religious & Spiritual",
                    "description": "Visit the sacred Jagannath Temple and spiritual sites",
                    "additional_days": 2
                }
            },
            "Goa": {
                "heritage": {
                    "destinations": ["Hampi"],
                    "theme": "UNESCO Heritage",
                    "description": "Explore ancient Vijayanagara Empire ruins and temples",
                    "additional_days": 2
                },
                "cultural": {
                    "destinations": ["Bangalore"],
                    "theme": "Modern Culture",
                    "description": "Experience India's Silicon Valley and modern culture",
                    "additional_days": 2
                }
            },
            "Jaipur": {
                "desert": {
                    "destinations": ["Jodhpur", "Jaisalmer"],
                    "theme": "Desert & Forts",
                    "description": "Explore the Thar Desert and magnificent forts",
                    "additional_days": 4
                }
            },
            "Delhi": {
                "golden_triangle": {
                    "destinations": ["Agra", "Jaipur"],
                    "theme": "Golden Triangle - Essential India",
                    "description": "Complete the iconic Golden Triangle with Taj Mahal and royal palaces",
                    "additional_days": 3,
                    "priority": 1
                },
                "spiritual": {
                    "destinations": ["Rishikesh", "Haridwar"],
                    "theme": "Yoga & Spirituality", 
                    "description": "Experience yoga capital and spiritual Ganges",
                    "additional_days": 3,
                    "priority": 2
                }
            }
        }

    def identify_circuit(self, destinations):
        """Identify if destinations match a known travel circuit"""
        dest_set = set([d.lower().replace(" ", "_") for d in destinations])
        
        for circuit_name, circuit_data in self.travel_circuits.items():
            circuit_destinations = set([d.lower().replace(" ", "_") for d in circuit_data["destinations"]])
            if dest_set.issubset(circuit_destinations) or circuit_destinations.issubset(dest_set):
                return circuit_name, circuit_data
        
        return None, None

    def suggest_itinerary(self, user_input):
        """Generate intelligent itinerary suggestions from minimal user input"""
        
        # Parse user input
        destinations = self.extract_destinations(user_input)
        
        if not destinations:
            return {"error": "Could not identify destinations from input"}
        
        # Check if it matches a known circuit
        circuit_name, circuit_data = self.identify_circuit(destinations)
        
        if circuit_data:
            return self.build_circuit_suggestion(circuit_name, circuit_data, user_input)
        else:
            return self.build_custom_suggestion(destinations, user_input)

    def extract_destinations(self, user_input):
        """Extract destination names from user input"""
        input_lower = user_input.lower()
        
        # Known destination mappings
        destination_keywords = {
            "golden triangle": ["Delhi", "Agra", "Jaipur"],
            "delhi": ["Delhi"],
            "agra": ["Agra"], 
            "jaipur": ["Jaipur"],
            "rajasthan": ["Jaipur", "Jodhpur", "Udaipur"],
            "kerala": ["Kochi", "Munnar", "Alleppey"],
            "goa": ["Goa"],
            "mumbai": ["Mumbai"],
            "kolkata": ["Kolkata"],
            "darjeeling": ["Darjeeling"],
            "sikkim": ["Sikkim"],
            "puri": ["Puri"],
            "hampi": ["Hampi"],
            "bangalore": ["Bangalore"],
            "jodhpur": ["Jodhpur"],
            "udaipur": ["Udaipur"],
            "jaisalmer": ["Jaisalmer"]
        }
        
        destinations = []
        for keyword, places in destination_keywords.items():
            if keyword in input_lower:
                destinations.extend(places)
        
        return list(set(destinations))  # Remove duplicates

    def build_circuit_suggestion(self, circuit_name, circuit_data, user_input):
        """Build suggestion for known travel circuits"""
        
        # Determine entry point from user input
        entry_point = self.determine_entry_point(user_input, circuit_data)
        
        # Optimize route based on entry point
        optimized_route = self.optimize_route(circuit_data["optimal_route"], entry_point)
        
        return {
            "type": "circuit",
            "circuit_name": circuit_name.replace("_", " ").title(),
            "destinations": circuit_data["destinations"],
            "suggested_route": optimized_route,
            "duration_options": [
                {
                    "days": circuit_data["recommended_duration"]["min"],
                    "type": "Quick Tour",
                    "description": f"Fast-paced {circuit_data['recommended_duration']['min']}-day journey covering highlights"
                },
                {
                    "days": circuit_data["recommended_duration"]["optimal"], 
                    "type": "Recommended",
                    "description": f"Balanced {circuit_data['recommended_duration']['optimal']}-day itinerary with comfortable pace"
                },
                {
                    "days": circuit_data["recommended_duration"]["max"],
                    "type": "Leisurely",
                    "description": f"Relaxed {circuit_data['recommended_duration']['max']}-day tour with extra time for exploration"
                }
            ],
            "entry_exit_suggestions": {
                "recommended": entry_point,
                "alternatives": circuit_data["destinations"]
            },
            "travel_logistics": circuit_data["travel_times"],
            "highlights": circuit_data["highlights"],
            "total_distance": self.calculate_total_distance(optimized_route, circuit_data["travel_times"]),
            "regional_extensions": self.get_regional_extensions(circuit_data["destinations"])
        }

    def determine_entry_point(self, user_input, circuit_data):
        """Determine best entry point from user input"""
        input_lower = user_input.lower()
        
        # Check if user specified "from [city]"
        for dest in circuit_data["destinations"]:
            if f"from {dest.lower()}" in input_lower:
                return dest
        
        # Default to circuit's recommended entry point
        return circuit_data["entry_exit"]

    def optimize_route(self, default_route, entry_point):
        """Optimize route based on entry point"""
        if entry_point not in default_route:
            return default_route
        
        # Rotate route to start from entry point
        start_index = default_route.index(entry_point)
        optimized = default_route[start_index:] + default_route[:start_index]
        
        # Ensure we return to starting point
        if optimized[-1] != entry_point:
            optimized.append(entry_point)
            
        return optimized

    def calculate_total_distance(self, route, travel_times):
        """Calculate total distance for the route"""
        total_km = 0
        total_hours = 0
        
        for i in range(len(route) - 1):
            leg = f"{route[i]}-{route[i+1]}"
            if leg in travel_times:
                total_km += travel_times[leg]["km"]
                total_hours += travel_times[leg]["hours"]
        
        return {"total_km": total_km, "total_hours": total_hours}

    def build_custom_suggestion(self, destinations, user_input):
        """Build suggestion for custom destination combinations"""
        
        # For custom routes, suggest logical ordering
        optimized_route = self.suggest_route_order(destinations)
        
        # Estimate duration based on number of destinations
        estimated_days = len(destinations) * 2 + 1  # 2 days per destination + 1 travel day
        
        return {
            "type": "custom",
            "destinations": destinations,
            "suggested_route": optimized_route,
            "duration_options": [
                {
                    "days": estimated_days - 1,
                    "type": "Quick Tour",
                    "description": f"Fast-paced {estimated_days - 1}-day journey"
                },
                {
                    "days": estimated_days,
                    "type": "Recommended", 
                    "description": f"Balanced {estimated_days}-day itinerary"
                },
                {
                    "days": estimated_days + 2,
                    "type": "Leisurely",
                    "description": f"Relaxed {estimated_days + 2}-day tour"
                }
            ],
            "entry_exit_suggestions": {
                "recommended": destinations[0],
                "alternatives": destinations
            },
            "travel_logistics": self.get_travel_logistics(optimized_route),
            "recommendations": [
                "Consider grouping nearby destinations together",
                "Allow extra time for long-distance travel",
                "Book flights for distances over 1000km"
            ]
        }

    def suggest_route_order(self, destinations):
        """Suggest optimal order for visiting destinations"""
        # Simple heuristic: start with northernmost, move south
        # In real implementation, use geographical optimization
        
        region_order = {
            "Delhi": 1, "Agra": 2, "Jaipur": 3,
            "Mumbai": 4, "Goa": 5, "Bangalore": 6,
            "Kochi": 7, "Kolkata": 8
        }
        
        sorted_destinations = sorted(destinations, key=lambda x: region_order.get(x, 999))
        return sorted_destinations + [sorted_destinations[0]]  # Return to start

    def get_travel_logistics(self, route):
        """Get travel logistics for custom routes"""
        logistics = {}
        
        for i in range(len(route) - 1):
            origin = route[i]
            destination = route[i + 1]
            
            # Check if we have data for this route
            if origin in self.city_matrix and destination in self.city_matrix[origin]:
                logistics[f"{origin}-{destination}"] = self.city_matrix[origin][destination]
            else:
                # Estimate for unknown routes
                logistics[f"{origin}-{destination}"] = {
                    "hours": 8,  # Default estimate
                    "km": 500,   # Default estimate
                    "note": "Estimated travel time - please verify"
                }
        
        return logistics

    def get_regional_extensions(self, destinations):
        """Get suggested regional extensions for the given destinations"""
        extensions = {}
        
        for destination in destinations:
            if destination in self.regional_extensions:
                extensions[destination] = self.regional_extensions[destination]
        
        return extensions


# Example usage
if __name__ == "__main__":
    engine = ItinerarySuggestionEngine()
    
    # Test with Golden Triangle
    result = engine.suggest_itinerary("Golden Triangle from Delhi")
    print("Golden Triangle Suggestion:")
    print(f"Circuit: {result['circuit_name']}")
    print(f"Route: {' → '.join(result['suggested_route'])}")
    print(f"Duration options: {[opt['days'] for opt in result['duration_options']]} days")
    if 'regional_extensions' in result:
        print("Regional Extensions Available:")
        for city, extensions in result['regional_extensions'].items():
            for theme, details in extensions.items():
                print(f"  From {city}: {details['theme']} - {', '.join(details['destinations'])}")
    print()
    
    # Test with Kolkata extensions
    result2 = engine.suggest_itinerary("Kolkata Darjeeling")
    print("Kolkata + Extensions:")
    print(f"Route: {' → '.join(result2['suggested_route'])}")
    print(f"Duration options: {[opt['days'] for opt in result2['duration_options']]} days")
    print()
    
    # Test with Goa extensions  
    result3 = engine.suggest_itinerary("Goa Hampi")
    print("Goa + Heritage Extension:")
    print(f"Route: {' → '.join(result3['suggested_route'])}")
    print(f"Duration options: {[opt['days'] for opt in result3['duration_options']]} days")

