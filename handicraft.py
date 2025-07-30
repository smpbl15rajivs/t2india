from flask import Blueprint, jsonify, request
from flask_cors import cross_origin

handicraft_bp = Blueprint('handicraft', __name__)

# Handicraft database
handicrafts = {
    "Jaipur": [
        {
            "id": "jaipur_blue_pottery",
            "name": "Blue Pottery",
            "artisan": "Kripal Singh Shekhawat",
            "description": "A traditional craft of Jaipur, blue pottery is known for its vibrant blue dye and intricate designs. It is a Turko-Persian art form that was brought to India by the Mughals. Master Kripal Singh has been practicing this art for over 30 years and has won numerous awards for his exquisite work.",
            "image": "/images/blue_pottery.jpg",
            "workshops": [
                {"duration": "3 hours", "price": 1500, "type": "Introduction"},
                {"duration": "1 day", "price": 4000, "type": "Hands-on Experience"}
            ],
            "category": "pottery",
            "difficulty": "beginner"
        },
        {
            "id": "jaipur_block_printing",
            "name": "Block Printing",
            "artisan": "Anwar Khatri",
            "description": "A traditional textile art of Rajasthan, block printing involves stamping intricate designs onto fabric using carved wooden blocks. This ancient technique has been passed down through generations and represents the rich textile heritage of Rajasthan.",
            "image": "/images/block_printing.jpg",
            "workshops": [
                {"duration": "2 hours", "price": 1000, "type": "Basic Techniques"},
                {"duration": "4 hours", "price": 1800, "type": "Advanced Patterns"}
            ],
            "category": "textile",
            "difficulty": "beginner"
        },
        {
            "id": "jaipur_jewelry",
            "name": "Jewelry Making",
            "artisan": "Rajesh Soni",
            "description": "Jaipur is famous for its exquisite jewelry, especially Kundan and Meenakari work. Learn the art of crafting intricate jewelry from master artisans who have been perfecting this craft for generations. Experience the traditional techniques of gem setting and enamel work.",
            "image": "/images/jewelry_making.jpg",
            "workshops": [
                {"duration": "4 hours", "price": 2500, "type": "Basic Techniques"},
                {"duration": "2 days", "price": 8000, "type": "Complete Piece Creation"}
            ],
            "category": "jewelry",
            "difficulty": "intermediate"
        },
        {
            "id": "jaipur_miniature",
            "name": "Miniature Painting",
            "artisan": "Shail Choyal",
            "description": "A detailed and intricate art form, miniature paintings are a hallmark of Rajasthani art. Learn the techniques of this beautiful art form from a master who has dedicated his life to preserving this ancient tradition. Create your own masterpiece using traditional pigments and techniques.",
            "image": "/images/miniature_painting.jpg",
            "workshops": [
                {"duration": "5 days", "price": 15000, "type": "Intensive Course"},
                {"duration": "15 days", "price": 40000, "type": "Master Class"}
            ],
            "category": "painting",
            "difficulty": "advanced"
        }
    ],
    "Kashmir": [
        {
            "id": "kashmir_papier_mache",
            "name": "Papier-mâché",
            "artisan": "Abdul Rashid",
            "description": "A unique craft of Kashmir, papier-mâché involves molding paper pulp into beautiful decorative items, which are then hand-painted with intricate designs. This art form has been practiced in Kashmir for centuries and represents the region's rich artistic heritage.",
            "image": "/images/papier_mache.jpg",
            "workshops": [
                {"duration": "3 hours", "price": 1200, "type": "Basic Shaping"},
                {"duration": "1 day", "price": 3500, "type": "Complete Item Creation"}
            ],
            "category": "craft",
            "difficulty": "beginner"
        },
        {
            "id": "kashmir_carpet",
            "name": "Carpet Weaving",
            "artisan": "Mohammad Yusuf",
            "description": "Kashmiri carpets are world-renowned for their intricate designs and fine quality. Learn the art of weaving these beautiful carpets from master weavers who have inherited this skill through generations. Experience the meditative process of creating these masterpieces.",
            "image": "/images/carpet_weaving.jpg",
            "workshops": [
                {"duration": "7 days", "price": 20000, "type": "Basic Weaving"},
                {"duration": "30 days", "price": 75000, "type": "Complete Carpet"}
            ],
            "category": "textile",
            "difficulty": "advanced"
        },
        {
            "id": "kashmir_pashmina",
            "name": "Pashmina Weaving",
            "artisan": "Ghulam Hassan",
            "description": "Learn the art of weaving the world's finest wool, Pashmina, into exquisite shawls and stoles. A truly luxurious and authentic Kashmiri experience. Master Hassan will teach you the traditional techniques used to create these coveted garments.",
            "image": "/images/pashmina_weaving.jpg",
            "workshops": [
                {"duration": "5 days", "price": 18000, "type": "Basic Weaving"},
                {"duration": "10 days", "price": 32000, "type": "Complete Shawl"}
            ],
            "category": "textile",
            "difficulty": "intermediate"
        },
        {
            "id": "kashmir_wood_carving",
            "name": "Wood Carving",
            "artisan": "Nazir Ahmad",
            "description": "Kashmir is known for its intricate wood carvings, especially on walnut wood. Learn the art of carving beautiful designs on wood from master craftsmen who have been practicing this art for decades. Create your own carved masterpiece to take home.",
            "image": "/images/wood_carving.jpg",
            "workshops": [
                {"duration": "3 hours", "price": 1000, "type": "Basic Carving"},
                {"duration": "1 day", "price": 3000, "type": "Detailed Project"}
            ],
            "category": "woodwork",
            "difficulty": "beginner"
        }
    ],
    "Delhi": [
        {
            "id": "delhi_pottery",
            "name": "Traditional Pottery",
            "artisan": "Ram Kumar",
            "description": "Experience the ancient art of pottery making in the heart of Delhi. Learn traditional techniques of wheel throwing and glazing from master potters who have been practicing this craft for generations.",
            "image": "/images/delhi_pottery.jpg",
            "workshops": [
                {"duration": "2 hours", "price": 800, "type": "Wheel Throwing"},
                {"duration": "1 day", "price": 2500, "type": "Complete Pottery"}
            ],
            "category": "pottery",
            "difficulty": "beginner"
        }
    ],
    "Goa": [
        {
            "id": "goa_tile_painting",
            "name": "Azulejo Tile Painting",
            "artisan": "Maria Fernandes",
            "description": "Learn the Portuguese-influenced art of Azulejo tile painting, a beautiful tradition that reflects Goa's colonial heritage. Create your own decorative tiles using traditional techniques and patterns.",
            "image": "/images/goa_tiles.jpg",
            "workshops": [
                {"duration": "3 hours", "price": 1200, "type": "Basic Painting"},
                {"duration": "1 day", "price": 3000, "type": "Complete Tile Set"}
            ],
            "category": "painting",
            "difficulty": "beginner"
        }
    ],
    "Kolkata": [
        {
            "id": "kolkata_terracotta",
            "name": "Terracotta Sculpture",
            "artisan": "Subhash Chandra",
            "description": "Bengal is famous for its terracotta art, especially in temple architecture and Durga Puja idols. Learn the traditional techniques of terracotta sculpture from master artisans in Kolkata.",
            "image": "/images/kolkata_terracotta.jpg",
            "workshops": [
                {"duration": "4 hours", "price": 1500, "type": "Basic Sculpture"},
                {"duration": "2 days", "price": 5000, "type": "Complete Figure"}
            ],
            "category": "sculpture",
            "difficulty": "intermediate"
        }
    ]
}

@handicraft_bp.route('/destinations', methods=['GET'])
@cross_origin()
def get_destinations():
    """Get all destinations with handicraft options"""
    destinations = []
    for destination, crafts in handicrafts.items():
        destinations.append({
            "name": destination,
            "handicraft_count": len(crafts),
            "featured_crafts": [craft["name"] for craft in crafts[:2]]
        })
    return jsonify(destinations)

@handicraft_bp.route('/destination/<destination_name>/handicrafts', methods=['GET'])
@cross_origin()
def get_destination_handicrafts(destination_name):
    """Get handicrafts for a specific destination"""
    if destination_name in handicrafts:
        return jsonify({
            "destination": destination_name,
            "handicrafts": handicrafts[destination_name]
        })
    else:
        return jsonify({"error": "Destination not found"}), 404

@handicraft_bp.route('/handicraft/<handicraft_id>', methods=['GET'])
@cross_origin()
def get_handicraft_details(handicraft_id):
    """Get detailed information about a specific handicraft"""
    for destination, crafts in handicrafts.items():
        for craft in crafts:
            if craft["id"] == handicraft_id:
                return jsonify({
                    "destination": destination,
                    "handicraft": craft
                })
    return jsonify({"error": "Handicraft not found"}), 404

@handicraft_bp.route('/search', methods=['GET'])
@cross_origin()
def search_handicrafts():
    """Search handicrafts by category, difficulty, or keyword"""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    keyword = request.args.get('keyword', '').lower()
    
    results = []
    for destination, crafts in handicrafts.items():
        for craft in crafts:
            # Filter by category
            if category and craft.get("category") != category:
                continue
            
            # Filter by difficulty
            if difficulty and craft.get("difficulty") != difficulty:
                continue
            
            # Filter by keyword
            if keyword and keyword not in craft["name"].lower() and keyword not in craft["description"].lower():
                continue
            
            results.append({
                "destination": destination,
                "handicraft": craft
            })
    
    return jsonify(results)

@handicraft_bp.route('/route-planning', methods=['POST'])
@cross_origin()
def plan_route_with_handicrafts():
    """Plan a route with handicraft integration"""
    data = request.get_json()
    destinations = data.get('destinations', [])
    days = data.get('days', 7)
    interests = data.get('interests', [])
    
    route_plan = []
    for i, dest in enumerate(destinations):
        if dest in handicrafts:
            # Get relevant handicrafts based on interests
            relevant_crafts = []
            for craft in handicrafts[dest]:
                if not interests or any(interest.lower() in craft["category"].lower() or 
                                     interest.lower() in craft["name"].lower() for interest in interests):
                    relevant_crafts.append(craft)
            
            route_plan.append({
                "destination": dest,
                "day": i + 1,
                "suggested_handicrafts": relevant_crafts[:3],  # Top 3 suggestions
                "total_handicrafts": len(handicrafts[dest])
            })
    
    return jsonify({
        "route": route_plan,
        "total_days": days,
        "total_destinations": len(destinations)
    })

