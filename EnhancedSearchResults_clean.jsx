import React, { useState, useEffect } from 'react'

const EnhancedSearchResults = ({ query, onClose }) => {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [showContactForm, setShowContactForm] = useState(false)
  const [contactDetails, setContactDetails] = useState({ email: '', phone: '' })
  const [contactSubmitted, setContactSubmitted] = useState(false)

  useEffect(() => {
    analyzeQuery(query)
  }, [query])

  const analyzeQuery = async (query) => {
    setLoading(true)
    try {
      const response = await fetch('https://77h9ikczgqgg.manus.space/api/search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query })
      })

      const data = await response.json()
      
      if (data.success && data.zero_result) {
        setAnalysis(data)
        setShowContactForm(true)
      } else if (data.success) {
        setAnalysis(data.analysis)
      } else {
        console.error('Search failed:', data.error)
      }
    } catch (error) {
      console.error('Error analyzing query:', error)
    } finally {
      setLoading(false)
    }
  }

  const submitContact = async () => {
    if (!contactDetails.email) {
      alert('Email is required')
      return
    }

    try {
      const response = await fetch('https://77h9ikczgqgg.manus.space/api/submit-contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          email: contactDetails.email,
          phone: contactDetails.phone,
          reference_id: analysis?.professional_response?.reference_id
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setContactSubmitted(true)
      } else {
        alert('Error submitting contact details: ' + data.error)
      }
    } catch (error) {
      console.error('Error submitting contact:', error)
      alert('Error submitting contact details')
    }
  }

  if (loading) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto mb-4"></div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">🧠 Analyzing Your Request</h3>
            <p className="text-gray-600">Building your perfect India itinerary...</p>
          </div>
        </div>
      </div>
    )
  }

  if (analysis?.zero_result && showContactForm && !contactSubmitted) {
    const response = analysis.professional_response
    
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
          <div className="flex justify-between items-start mb-6">
            <h2 className="text-2xl font-bold text-gray-800">{response.title}</h2>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
          </div>
          
          <div className="space-y-6">
            <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
              <p className="text-blue-800 font-medium">{response.message}</p>
              <p className="text-blue-600 text-sm mt-2">{response.sub_message}</p>
            </div>
            
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div className="bg-gray-50 p-3 rounded">
                <strong>Reference ID:</strong> {response.reference_id}
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <strong>Response Time:</strong> {response.timeline}
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <strong>Priority:</strong> <span className={`px-2 py-1 rounded text-xs ${
                  response.priority === 'HIGH' ? 'bg-red-100 text-red-800' :
                  response.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-green-100 text-green-800'
                }`}>{response.priority}</span>
              </div>
              <div className="bg-gray-50 p-3 rounded">
                <strong>Your Query:</strong> "{query}"
              </div>
            </div>
            
            <div className="border-t pt-6">
              <h3 className="text-lg font-semibold mb-4">📧 Contact Details for Follow-up</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email Address <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    value={contactDetails.email}
                    onChange={(e) => setContactDetails({...contactDetails, email: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="your.email@example.com"
                    required
                  />
                </div>
                
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number <span className="text-gray-400">(Optional)</span>
                  </label>
                  <input
                    type="tel"
                    value={contactDetails.phone}
                    onChange={(e) => setContactDetails({...contactDetails, phone: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="+91 98765 43210"
                  />
                </div>
                
                <button
                  onClick={submitContact}
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 font-medium"
                >
                  Submit Contact Details
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (contactSubmitted) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
          <div className="text-center">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">✅ Contact Details Submitted!</h3>
            <p className="text-gray-600 mb-4">
              Thank you! Our T2India management team has received your contact details and will reach out within 4 days maximum with your personalized itinerary.
            </p>
            <p className="text-sm text-gray-500 mb-6">
              Reference: {analysis?.professional_response?.reference_id}
            </p>
            <button
              onClick={onClose}
              className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-8 max-w-4xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        <div className="flex justify-between items-start mb-6">
          <h2 className="text-2xl font-bold text-gray-800">🇮🇳 Grand Tour Package of India</h2>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-2xl">&times;</button>
        </div>
        
        <p className="text-gray-600 mb-6">
          Regular search functionality would appear here for queries that match known patterns.
        </p>
        
        <button
          onClick={onClose}
          className="bg-gray-600 text-white py-2 px-6 rounded-md hover:bg-gray-700"
        >
          Close
        </button>
      </div>
    </div>
  )
}

export default EnhancedSearchResults

