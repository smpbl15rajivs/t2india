import React, { useState, useEffect } from 'react'
import './App.css'
import EnhancedSearchResults from './EnhancedSearchResults'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [showResults, setShowResults] = useState(false)
  const [showEnhancedResults, setShowEnhancedResults] = useState(false)
  const [loading, setLoading] = useState(false)
  const [destinations, setDestinations] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [existingItineraries, setExistingItineraries] = useState([])
  const [searchFocused, setSearchFocused] = useState(false)
  const [showPrompt, setShowPrompt] = useState(false)
  const [promptTimeout, setPromptTimeout] = useState(null)

  // API base URL - using deployed backend
  const API_BASE = 'https://9yhyi3czg65n.manus.space/api'

  // Tour categories with solid colors
  const categories = [
    { id: 'all', name: 'All Tours', color: 'bg-orange-500', icon: '🌟' },
    { id: 'heritage', name: 'Heritage & Culture', color: 'bg-purple-500', icon: '🏛️' },
    { id: 'nature', name: 'Scenic & Nature', color: 'bg-blue-500', icon: '🌿' },
    { id: 'desert', name: 'Desert & Forts', color: 'bg-purple-600', icon: '🏰' },
    { id: 'adventure', name: 'Adventure & Wildlife', color: 'bg-blue-600', icon: '🏔️' },
    { id: 'beach', name: 'Beach & Coastal', color: 'bg-pink-500', icon: '🏖️' },
    { id: 'spiritual', name: 'Spiritual & Temples', color: 'bg-orange-600', icon: '🕉️' },
    { id: 'yoga', name: 'Yoga & Ayurveda', color: 'bg-green-600', icon: '🧘' }
  ]

  // Sample existing itineraries
  const sampleItineraries = [
    {
      id: 1,
      title: 'Classic Golden Triangle',
      duration: '6 Days',
      destinations: ['Delhi', 'Agra', 'Jaipur'],
      price: '₹15,000',
      rating: 4.8,
      bookings: 156,
      image: '🏛️',
      gradient: 'bg-blue-600'
    },
    {
      id: 2,
      title: 'Kerala Backwater Bliss',
      duration: '5 Days',
      destinations: ['Kochi', 'Alappuzha', 'Kumarakom'],
      price: '₹18,000',
      rating: 4.9,
      bookings: 89,
      image: '🌴',
      gradient: 'bg-green-600'
    },
    {
      id: 3,
      title: 'Rajasthan Royal Heritage',
      duration: '8 Days',
      destinations: ['Jodhpur', 'Udaipur', 'Jaisalmer'],
      price: '₹22,000',
      rating: 4.7,
      bookings: 134,
      image: '🏰',
      gradient: 'bg-blue-600'
    },
    {
      id: 4,
      title: 'Kashmir Paradise',
      duration: '7 Days',
      destinations: ['Srinagar', 'Gulmarg', 'Pahalgam'],
      price: '₹25,000',
      rating: 4.9,
      bookings: 67,
      image: '🏔️',
      gradient: 'bg-purple-600'
    }
  ]

  // Load destinations from API on component mount
  useEffect(() => {
    fetchDestinations()
    setExistingItineraries(sampleItineraries)
  }, [])

  const fetchDestinations = async () => {
    try {
      const response = await fetch(`${API_BASE}/destinations`)
      const data = await response.json()
      setDestinations(data.data || [])
    } catch (error) {
      console.error('Error fetching destinations:', error)
      setDestinations([])
    }
  }

  // Generate suggestions with debouncing
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      generateSuggestions(searchQuery)
    }, 300)

    return () => clearTimeout(timeoutId)
  }, [searchQuery])

  const generateSuggestions = async (value) => {
    if (!value || value.length < 2) {
      setSuggestions([])
      setShowSuggestions(false)
      setShowResults(false)
      return
    }

    try {
      const response = await fetch(`${API_BASE}/search/autocomplete?q=${encodeURIComponent(value)}`)
      const data = await response.json()
      
      if (data.success) {
        setSuggestions(data.suggestions || [])
        setShowSuggestions(data.suggestions.length > 0)
      }
    } catch (error) {
      console.error('Autocomplete error:', error)
      setSuggestions([])
      setShowSuggestions(false)
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setSearchQuery(suggestion.text)
    setShowSuggestions(false)
    performSearch(suggestion.text)
  }

  const handleSearchSubmit = () => {
    setShowSuggestions(false)
    if (searchQuery.trim()) {
      performSearch(searchQuery)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      // Always allow Enter key to trigger search
      handleSearchSubmit()
    } else if (e.key === 'Escape') {
      setShowSuggestions(false)
    }
  }

  // Search functionality with 20-second inactivity prompt
  useEffect(() => {
    // Clear existing prompt timeout whenever user types
    if (promptTimeout) {
      clearTimeout(promptTimeout)
      setPromptTimeout(null)
    }
    
    // Hide prompt if user starts typing again
    if (showPrompt) {
      setShowPrompt(false)
    }
    
    // Set up 20-second inactivity prompt if user has typed something
    if (searchQuery.trim() && searchQuery.length > 5) {
      const newPromptTimeout = setTimeout(() => {
        setShowPrompt(true)
      }, 20000) // 20 seconds of NO TYPING
      setPromptTimeout(newPromptTimeout)
    }

    return () => {
      if (promptTimeout) {
        clearTimeout(promptTimeout)
      }
    }
  }, [searchQuery]) // This runs every time user types a character

  const performSearch = async (query = searchQuery) => {
    setLoading(true)
    
    // Check if this is a complex travel query that needs intelligent processing
    const complexQueryPatterns = [
      /\d+\s*days?\s*travel/i,
      /\d+\s*days?\s*in/i,
      /\d+\s*days?\s*and/i,
      /\d+\s*days?\s*for/i,
      /spirituality|spiritual/i,
      /yoga|ayurveda/i,
      /miniature\s*painting/i,
      /learn|workshop|training/i,
      /desert\s*palace/i,
      /golden\s*triangle/i,
      /honeymoon/i,
      /adventure/i,
      /luxury/i,
      /heritage/i,
      /holiday.*days|days.*holiday/i
    ]
    
    const isComplexQuery = complexQueryPatterns.some(pattern => pattern.test(query))
    
    if (isComplexQuery) {
      // Show enhanced search results for complex queries
      setShowEnhancedResults(true)
      setShowResults(false)
      setLoading(false)
      return
    }
    
    // Regular search for simple queries
    try {
      const response = await fetch(`${API_BASE}/search/destinations?q=${encodeURIComponent(query)}`)
      const data = await response.json()
      
      if (data.success) {
        setDestinations(data.data || [])
        setShowResults(true)
        setShowEnhancedResults(false)
      } else {
        setDestinations([])
        setShowResults(true)
        setShowEnhancedResults(false)
      }
    } catch (error) {
      console.error('Search error:', error)
      setDestinations([])
      setShowResults(true)
      setShowEnhancedResults(false)
    } finally {
      setLoading(false)
    }
  }

  const handleCategoryClick = (categoryId) => {
    setSelectedCategory(categoryId)
    if (categoryId === 'all') {
      fetchDestinations()
    } else {
      const filtered = destinations.filter(dest => 
        dest.type.toLowerCase().includes(categoryId.toLowerCase())
      )
      setDestinations(filtered)
    }
  }

  const handleItinerarySelect = (itinerary) => {
    console.log('Selected itinerary:', itinerary)
  }

  const handlePromptSearchNow = () => {
    setShowPrompt(false)
    if (promptTimeout) {
      clearTimeout(promptTimeout)
      setPromptTimeout(null)
    }
    performSearch(searchQuery)
  }

  const handlePromptAddMore = () => {
    setShowPrompt(false)
    if (promptTimeout) {
      clearTimeout(promptTimeout)
      setPromptTimeout(null)
    }
    // Focus back on search input and position cursor at the end
    setTimeout(() => {
      const searchInput = document.querySelector('input[type="text"]')
      if (searchInput) {
        searchInput.focus()
        // Position cursor at the end of the text
        const length = searchInput.value.length
        searchInput.setSelectionRange(length, length)
      }
    }, 100) // Small delay to ensure modal is closed first
  }

  const handleSearchChange = (e) => {
    const value = e.target.value
    
    // Filter out unwanted special characters, allow only letters, numbers, spaces, and basic punctuation
    const filteredValue = value.replace(/[^a-zA-Z0-9\s\-.,()&]/g, '')
    
    setSearchQuery(filteredValue)
  }

  const handleSearchFocus = () => {
    setSearchFocused(true)
  }

  const handleSearchBlur = () => {
    setTimeout(() => {
      setSearchFocused(false)
      setShowSuggestions(false)
    }, 200)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-100 via-pink-50 to-blue-100">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm shadow-sm sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <div className="flex justify-between items-center">
            <div className="flex items-center">
              <img 
                src="/t2india_official_logo.png" 
                alt="T2India Logo" 
                className="h-10 mr-2"
                style={{
                  imageRendering: 'crisp-edges',
                  filter: 'contrast(1.1) brightness(1.05) saturate(1.1)',
                  WebkitFilter: 'contrast(1.1) brightness(1.05) saturate(1.1)'
                }}
                onError={(e) => {
                  e.target.style.display = 'none'
                  e.target.nextSibling.style.display = 'inline-block'
                }}
              />
              <div className="text-xl font-bold text-purple-600 hidden">T2India</div>
            </div>
            <div className="flex space-x-4">
              <button className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                Agent Login
              </button>
              <button className="px-4 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">
                About
              </button>
              <button className="px-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors">
                Contact
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <div className="relative">
        <div className="max-w-5xl mx-auto px-4 py-16 text-center">
          {/* Airplane Icon */}
          <div className="mb-6">
            <div className="text-6xl mb-4">✈️</div>
          </div>

          {/* T2India Logo */}
          <div className="mb-6">
            <img 
              src="/t2india_official_logo.png" 
              alt="T2India Logo" 
              className="h-16 mx-auto mb-4"
              style={{
                imageRendering: 'crisp-edges',
                filter: 'contrast(1.1) brightness(1.05) saturate(1.1)',
                WebkitFilter: 'contrast(1.1) brightness(1.05) saturate(1.1)'
              }}
              onError={(e) => {
                e.target.style.display = 'none'
                e.target.nextSibling.style.display = 'block'
              }}
            />
            <div className="text-3xl font-bold text-purple-600 hidden">
              T2India<span className="text-orange-500">®</span>
              <div className="text-sm text-gray-600 mt-1">Your Gateway To India</div>
            </div>
          </div>

          {/* Tagline */}
          <h1 className="text-2xl md:text-3xl font-light text-gray-700 mb-8">
            Discover Incredible India with Artist, Artisans and Authentic Experience
          </h1>

          {/* Enhanced Search Box - Made Much Larger */}
          <div className="relative max-w-5xl mx-auto mb-8">
            <div className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={handleSearchChange}
                onFocus={handleSearchFocus}
                onBlur={handleSearchBlur}
                onKeyDown={handleKeyDown}
                placeholder="Search destinations, experiences, or regions..."
                className="w-full px-10 py-8 text-xl border-2 border-purple-300 rounded-full shadow-lg focus:outline-none focus:border-purple-500 focus:shadow-xl transition-all duration-300 bg-white/90 backdrop-blur-sm"
                style={{ minHeight: '80px', fontSize: '20px' }}
              />
              <div className="absolute right-6 top-1/2 transform -translate-y-1/2">
                <div 
                  onClick={handleSearchSubmit}
                  className="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center hover:bg-orange-600 transition-colors cursor-pointer"
                >
                  <span className="text-white text-xl">🔍</span>
                </div>
              </div>
            </div>

            {/* Autocomplete Suggestions Dropdown */}
            {showSuggestions && suggestions.length > 0 && (
              <div className="absolute top-full left-0 right-0 mt-2 bg-white rounded-2xl shadow-2xl border border-gray-200 z-50 max-h-96 overflow-y-auto">
                {suggestions.map((suggestion, index) => (
                  <div
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className="flex items-center px-6 py-4 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0 transition-colors"
                  >
                    <div className="flex-shrink-0 mr-4">
                      <div className="w-10 h-10 rounded-full flex items-center justify-center text-white bg-purple-500">
                        📍
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="font-semibold text-gray-800">{suggestion.text}</div>
                      <div className="text-sm text-gray-600">{suggestion.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Dynamic Category Buttons */}
          <div className="flex flex-wrap justify-center gap-3 mb-8">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => handleCategoryClick(category.id)}
                className={`px-6 py-3 rounded-full text-white font-medium transition-all duration-300 transform hover:scale-105 hover:shadow-lg ${
                  selectedCategory === category.id 
                    ? `${category.color} shadow-lg scale-105` 
                    : `${category.color} opacity-80 hover:opacity-100`
                }`}
              >
                <span className="mr-2">{category.icon}</span>
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Existing Itineraries Section */}
      {!showResults && !showEnhancedResults && (
        <div className="max-w-7xl mx-auto px-4 py-12">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
              🎯 Popular Existing Itineraries
            </h2>
            <p className="text-gray-600 text-lg">
              Browse our curated itineraries - ready to book or customize to your needs
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {existingItineraries.map((itinerary) => (
              <div
                key={itinerary.id}
                onClick={() => handleItinerarySelect(itinerary)}
                className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-105 cursor-pointer overflow-hidden border border-gray-100"
              >
                <div className={`h-32 ${itinerary.gradient} flex items-center justify-center text-4xl`}>
                  {itinerary.image}
                </div>
                <div className="p-6">
                  <h3 className="font-bold text-lg text-gray-800 mb-2">{itinerary.title}</h3>
                  <div className="flex items-center text-gray-600 mb-2">
                    <span className="mr-2">📅</span>
                    <span className="text-sm">{itinerary.duration}</span>
                  </div>
                  <div className="flex items-center text-gray-600 mb-3">
                    <span className="mr-2">📍</span>
                    <span className="text-sm">{itinerary.destinations.join(' → ')}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="flex items-center">
                      <span className="text-yellow-500 mr-1">⭐</span>
                      <span className="text-sm font-medium">{itinerary.rating}</span>
                      <span className="text-gray-500 text-xs ml-1">({itinerary.bookings} bookings)</span>
                    </div>
                    <div className="text-lg font-bold text-purple-600">{itinerary.price}</div>
                  </div>
                  <button className="w-full mt-4 py-2 bg-orange-500 text-white rounded-lg hover:bg-orange-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Search Results */}
      {showResults && (
        <div className="max-w-4xl mx-auto px-4 py-8">
          <div className="mb-6">
            <h2 className="text-2xl font-bold text-gray-800">
              About {destinations.length} results for "{searchQuery}"
            </h2>
          </div>
          
          <div className="space-y-6">
            {destinations.map((destination) => (
              <div key={destination.id} className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:scale-102 border border-gray-100 overflow-hidden">
                <div className="p-6">
                  <h3 className="text-2xl font-bold text-gray-800 mb-2">{destination.name}</h3>
                  <div className="flex items-center text-gray-600 mb-2">
                    <span className="mr-2">📍</span>
                    <span>{destination.region}</span>
                    <span className="mx-2">•</span>
                    <span className="mr-2">📅</span>
                    <span>{destination.duration}</span>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <div className="text-2xl font-bold text-purple-600">
                      ₹{destination.price_budget?.toLocaleString() || '15,000'}
                    </div>
                    <button className="px-6 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105 font-medium">
                      Enquire Now →
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Features Section */}
      {!showResults && !showEnhancedResults && (
        <div className="max-w-6xl mx-auto px-4 py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-8 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-100">
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                📍
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Curated Destinations</h3>
              <p className="text-gray-600">Handpicked destinations across India with authentic experiences</p>
            </div>
            
            <div className="text-center p-8 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-green-100">
              <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                👥
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Expert Guides</h3>
              <p className="text-gray-600">Local experts who bring destinations to life with stories</p>
            </div>
            
            <div className="text-center p-8 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-purple-100">
              <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                💜
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-2">Personalized Service</h3>
              <p className="text-gray-600">Tailored itineraries designed just for your preferences</p>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gradient-to-r from-purple-600 via-pink-600 to-blue-600 text-white py-8">
        <div className="max-w-6xl mx-auto px-4 text-center">
          <div className="flex justify-center space-x-8 mb-4">
            <a href="#" className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg hover:bg-white/30 transition-all duration-300">Privacy Policy</a>
            <a href="#" className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg hover:bg-white/30 transition-all duration-300">Terms of Service</a>
            <a href="#" className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg hover:bg-white/30 transition-all duration-300">Support</a>
            <a href="#" className="px-4 py-2 bg-white/20 backdrop-blur-sm rounded-lg hover:bg-white/30 transition-all duration-300">Careers</a>
          </div>
          <p className="text-white/80">© 2024 T2India. Discover Incredible India with authentic experiences.</p>
        </div>
      </footer>

      {/* Enhanced Search Results Modal */}
      {showEnhancedResults && (
        <EnhancedSearchResults 
          searchQuery={searchQuery}
          onClose={() => setShowEnhancedResults(false)}
        />
      )}

      {/* 20-Second Prompt Modal */}
      {showPrompt && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md mx-4 border border-purple-200">
            <div className="text-center">
              <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4 text-2xl">
                ⏰
              </div>
              <h3 className="text-xl font-bold text-gray-800 mb-4">Ready to Search?</h3>
              <p className="text-gray-600 mb-6">
                I noticed you've been composing your search query. Are you ready to search now, or would you like to add more details?
              </p>
              <div className="text-sm text-gray-500 mb-6 p-3 bg-gray-50 rounded-lg">
                <strong>Current query:</strong> "{searchQuery}"
              </div>
              <div className="flex space-x-4">
                <button
                  onClick={handlePromptSearchNow}
                  className="flex-1 px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors font-medium"
                >
                  🔍 Search Now
                </button>
                <button
                  onClick={handlePromptAddMore}
                  className="flex-1 px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
                >
                  ✏️ Add More
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

