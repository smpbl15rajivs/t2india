import React, { useState, useEffect } from 'react'

const EnhancedSearchResults = ({ searchQuery, onClose }) => {
  const [analysisData, setAnalysisData] = useState(null)
  const [selectedOptions, setSelectedOptions] = useState({})
  const [itinerary, setItinerary] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    analyzeQuery(searchQuery)
  }, [searchQuery])

  const analyzeQuery = async (query) => {
    setLoading(true)
    try {
      const response = await fetch('https://nghki1clokdo.manus.space/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
      })
      
      const data = await response.json()
      
      if (data.success) {
        setAnalysisData(data.analysis)
        // Set default selections
        const defaults = {}
        data.analysis.components.forEach(component => {
          if (component.ambiguous && component.options) {
            defaults[component.key] = component.suggested || component.options[0].value
          }
        })
        setSelectedOptions(defaults)
        generateItinerary(data.analysis, defaults)
      }
    } catch (error) {
      console.error('Analysis error:', error)
      setLoading(false)
    }
  }

  const generateItinerary = async (analysis, options) => {
    try {
      const response = await fetch('https://nghki1clokdo.manus.space/api/generate-itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          analysis,
          selections: options
        })
      })
      
      const data = await response.json()
      
      if (data.success) {
        setItinerary(data.itinerary)
      }
    } catch (error) {
      console.error('Itinerary generation error:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleOptionChange = (componentKey, value) => {
    const newOptions = { ...selectedOptions, [componentKey]: value }
    setSelectedOptions(newOptions)
    
    // Regenerate itinerary with new selection
    if (analysisData) {
      generateItinerary(analysisData, newOptions)
    }
  }

  const handleCustomInput = (componentKey, value) => {
    handleOptionChange(componentKey, value)
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">🧠 Analyzing Your Request</h3>
            <p className="text-gray-600">Building your perfect India itinerary...</p>
          </div>
        </div>
      </div>
    )
  }

  if (!analysisData) {
    return null
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl max-w-6xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="sticky top-0 bg-white border-b border-gray-200 p-6 rounded-t-2xl">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold text-gray-800">🇮🇳 Grand Tour Package of India</h2>
            <button 
              onClick={onClose}
              className="text-gray-500 hover:text-gray-700 text-2xl"
            >
              ×
            </button>
          </div>
        </div>

        {/* Analysis Section */}
        <div className="p-6 border-b border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">🧠 Building Your Custom Itinerary...</h3>
          <p className="text-gray-600 mb-4">I'm analyzing your request to create the perfect trip. Here's what I've understood:</p>
          
          <div className="overflow-x-auto">
            <table className="w-full border-collapse border border-gray-300">
              <thead>
                <tr className="bg-gray-50">
                  <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Component</th>
                  <th className="border border-gray-300 px-4 py-2 text-left font-semibold">Your Request</th>
                  <th className="border border-gray-300 px-4 py-2 text-left font-semibold">My Understanding & Suggestions</th>
                </tr>
              </thead>
              <tbody>
                {analysisData.components.map((component, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="border border-gray-300 px-4 py-2 font-medium">{component.label}</td>
                    <td className="border border-gray-300 px-4 py-2">"{component.original}"</td>
                    <td className="border border-gray-300 px-4 py-2">
                      {component.ambiguous ? (
                        <div>
                          <p className="mb-3">
                            <strong>Suggested:</strong> {component.suggested_label}
                            <br />
                            <span className="text-sm text-gray-600">Not right? Please select below:</span>
                          </p>
                          
                          <div className="space-y-2">
                            {component.options.map((option, optIndex) => (
                              <label key={optIndex} className="flex items-start space-x-2 cursor-pointer">
                                <input
                                  type="radio"
                                  name={component.key}
                                  value={option.value}
                                  checked={selectedOptions[component.key] === option.value}
                                  onChange={(e) => handleOptionChange(component.key, e.target.value)}
                                  className="mt-1"
                                />
                                <div>
                                  <span className="font-medium">{option.label}</span>
                                  <span className="text-sm text-gray-600 block">{option.description}</span>
                                </div>
                              </label>
                            ))}
                            
                            <label className="flex items-center space-x-2 cursor-pointer">
                              <input
                                type="radio"
                                name={component.key}
                                value="other"
                                checked={selectedOptions[component.key] && !component.options.find(opt => opt.value === selectedOptions[component.key])}
                                onChange={(e) => {
                                  if (e.target.checked) {
                                    const customValue = prompt(`Enter your preferred ${component.label.toLowerCase()}:`);
                                    if (customValue) {
                                      handleCustomInput(component.key, customValue);
                                    }
                                  }
                                }}
                              />
                              <span className="font-medium">Other:</span>
                              <input
                                type="text"
                                placeholder={`e.g., ${component.example || 'Custom option'}`}
                                className="border border-gray-300 rounded px-2 py-1 text-sm"
                                onBlur={(e) => {
                                  if (e.target.value) {
                                    handleCustomInput(component.key, e.target.value);
                                  }
                                }}
                              />
                            </label>
                          </div>
                        </div>
                      ) : (
                        <span className="font-medium">{component.understanding}</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          <div className="mt-4 p-3 bg-green-50 border border-green-200 rounded-lg">
            <p className="text-green-700 font-medium">
              Status: Analysis complete. Generating your detailed itinerary based on selected options...
            </p>
          </div>
        </div>

        {/* Itinerary Section */}
        {itinerary && (
          <div className="p-6">
            <div className="mb-6">
              <h3 className="text-xl font-bold text-gray-800 mb-2">{itinerary.title}</h3>
              <p className="text-gray-600">{itinerary.description}</p>
            </div>

            {/* Flight Information */}
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <h4 className="font-semibold text-blue-800 mb-2">✈️ Important: Please Provide Your Flight Details</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                <div>
                  <strong>Landing City:</strong> _______
                  <br />
                  <strong>Arrival Date/Time:</strong> _______
                </div>
                <div>
                  <strong>Departure City:</strong> _______
                  <br />
                  <strong>Departure Date/Time:</strong> _______
                </div>
              </div>
            </div>

            {/* Destination Photos */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-800 mb-3">📸 Destination Highlights</h4>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {itinerary.photos.map((photo, index) => (
                  <div key={index} className="bg-gray-200 rounded-lg h-32 flex items-center justify-center text-4xl">
                    {photo.emoji}
                  </div>
                ))}
              </div>
            </div>

            {/* Introduction */}
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h4 className="font-semibold text-gray-800 mb-2">🌟 {itinerary.theme_title}</h4>
              <p className="text-gray-700 text-sm leading-relaxed">{itinerary.introduction}</p>
            </div>

            {/* Detailed Itinerary Table */}
            <div className="mb-6">
              <h4 className="font-semibold text-gray-800 mb-3">📋 Detailed Itinerary</h4>
              <div className="overflow-x-auto">
                <table className="w-full border-collapse border border-gray-300">
                  <thead>
                    <tr className="bg-gray-50">
                      <th className="border border-gray-300 px-4 py-2 text-left">Day</th>
                      <th className="border border-gray-300 px-4 py-2 text-left">Destination</th>
                      <th className="border border-gray-300 px-4 py-2 text-left">Hotel</th>
                      <th className="border border-gray-300 px-4 py-2 text-left">Itinerary & Artisan Experiences</th>
                    </tr>
                  </thead>
                  <tbody>
                    {itinerary.days.map((day, index) => (
                      <tr key={index} className="hover:bg-gray-50">
                        <td className="border border-gray-300 px-4 py-2 font-medium">Day {day.day}</td>
                        <td className="border border-gray-300 px-4 py-2">
                          <a href={day.destination_link} className="text-blue-600 hover:underline">
                            {day.destination}
                          </a>
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                          <a href={day.hotel_link} className="text-blue-600 hover:underline">
                            {day.hotel}
                          </a>
                        </td>
                        <td className="border border-gray-300 px-4 py-2">
                          <div className="space-y-2">
                            <div>{day.activities}</div>
                            {day.artisan && (
                              <div className="text-sm bg-orange-50 p-2 rounded border-l-4 border-orange-400">
                                <strong>🎨 Artisan Experience:</strong>{' '}
                                <a href={day.artisan.link} className="text-orange-600 hover:underline">
                                  {day.artisan.name} - {day.artisan.specialty}
                                </a>
                              </div>
                            )}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>

            {/* Package Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                <h4 className="font-semibold text-green-800 mb-2">✅ Package Inclusions</h4>
                <ul className="text-sm space-y-1">
                  {itinerary.inclusions.map((item, index) => (
                    <li key={index}>• {item}</li>
                  ))}
                </ul>
              </div>
              
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <h4 className="font-semibold text-red-800 mb-2">⚠️ Not Included</h4>
                <ul className="text-sm space-y-1">
                  {itinerary.exclusions.map((item, index) => (
                    <li key={index}>• {item}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Pricing */}
            <div className="mt-6 p-4 bg-purple-50 border border-purple-200 rounded-lg">
              <h4 className="font-semibold text-purple-800 mb-2">💰 Package Investment</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div>
                  <strong>Total Cost:</strong> {itinerary.pricing.total}
                </div>
                <div>
                  <strong>Per Person:</strong> {itinerary.pricing.per_person}
                </div>
                <div>
                  <strong>Additional Flights:</strong> {itinerary.pricing.flights}
                </div>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="mt-6 flex flex-wrap gap-4 justify-center">
              <button className="px-6 py-3 bg-orange-500 text-white rounded-lg hover:bg-orange-600 transition-colors">
                📞 Enquire Now
              </button>
              <button className="px-6 py-3 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors">
                📄 Download PDF
              </button>
              <button className="px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors">
                💾 Save Itinerary
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default EnhancedSearchResults

