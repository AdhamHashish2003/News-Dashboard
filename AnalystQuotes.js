import React, { useState, useEffect } from 'react';
import { Box, Typography, List, ListItem, Avatar, Card, CardContent, Divider, Chip } from '@mui/material';
import FormatQuoteIcon from '@mui/icons-material/FormatQuote';
import '../styles/AnalystQuotes.css';

// Mock analyst quotes data
const mockAnalystQuotes = [
  {
    id: 1,
    content: "The current trade tensions represent a fundamental shift in the global economic order. We're seeing the early stages of what could be a prolonged period of deglobalization.",
    analyst_name: "Ray Dalio",
    organization: "Bridgewater Associates",
    date: "2023-06-15T08:30:00Z",
    priority_score: 90.2,
    primary_category: "external_conflict"
  },
  {
    id: 2,
    content: "Rising inflation combined with slowing growth creates a challenging environment for central banks. We may be entering a period of stagflation similar to the 1970s.",
    analyst_name: "Mohamed El-Erian",
    organization: "Allianz",
    date: "2023-06-14T09:45:00Z",
    priority_score: 87.5,
    primary_category: "economic_indicators"
  },
  {
    id: 3,
    content: "The increasing social unrest we're witnessing is a direct consequence of wealth inequality. This internal conflict could have significant implications for political stability.",
    analyst_name: "Nouriel Roubini",
    organization: "Roubini Macro Associates",
    date: "2023-06-13T14:20:00Z",
    priority_score: 82.1,
    primary_category: "internal_conflict"
  },
  {
    id: 4,
    content: "Central banks are losing control of the monetary system. The debt levels we're seeing are unsustainable and will eventually lead to a major restructuring of the global financial system.",
    analyst_name: "Ray Dalio",
    organization: "Bridgewater Associates",
    date: "2023-06-10T10:15:00Z",
    priority_score: 88.7,
    primary_category: "economic_indicators"
  },
  {
    id: 5,
    content: "The geopolitical landscape is shifting dramatically. We're witnessing the rise of a multipolar world where the US-led order is increasingly challenged by emerging powers.",
    analyst_name: "Ian Bremmer",
    organization: "Eurasia Group",
    date: "2023-06-08T16:30:00Z",
    priority_score: 85.3,
    primary_category: "external_conflict"
  },
  {
    id: 6,
    content: "Political polarization has reached dangerous levels in many democracies. The inability to find common ground on basic issues threatens the stability of these systems.",
    analyst_name: "Francis Fukuyama",
    organization: "Stanford University",
    date: "2023-06-07T11:45:00Z",
    priority_score: 79.8,
    primary_category: "internal_conflict"
  },
  {
    id: 7,
    content: "The current debt cycle is approaching its end. We're likely to see a period of deleveraging that will have profound implications for asset prices and economic growth.",
    analyst_name: "Ray Dalio",
    organization: "Bridgewater Associates",
    date: "2023-06-05T09:20:00Z",
    priority_score: 86.4,
    primary_category: "economic_indicators"
  }
];

function AnalystQuotes({ filters, limit = 5 }) {
  const [quotes, setQuotes] = useState([]);
  
  useEffect(() => {
    // In a real implementation, this would fetch data from an API
    // For now, we'll filter the mock data based on the filters
    
    let filteredQuotes = [...mockAnalystQuotes];
    
    // Apply category filter
    if (filters.category && filters.category !== 'all') {
      filteredQuotes = filteredQuotes.filter(quote => 
        quote.primary_category === filters.category
      );
    }
    
    // Apply search query filter
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      filteredQuotes = filteredQuotes.filter(quote => 
        quote.content.toLowerCase().includes(query) || 
        quote.analyst_name.toLowerCase().includes(query) ||
        quote.organization.toLowerCase().includes(query)
      );
    }
    
    // Apply date range filter (simplified for mock data)
    // In a real implementation, this would properly filter by date
    
    // Sort by priority score
    filteredQuotes.sort((a, b) => b.priority_score - a.priority_score);
    
    // Limit the number of results
    filteredQuotes = filteredQuotes.slice(0, limit);
    
    setQuotes(filteredQuotes);
  }, [filters, limit]);
  
  const getCategoryColor = (category) => {
    switch (category) {
      case 'internal_conflict':
        return '#f44336'; // Red
      case 'external_conflict':
        return '#2196f3'; // Blue
      case 'economic_indicators':
        return '#4caf50'; // Green
      default:
        return '#9e9e9e'; // Grey
    }
  };
  
  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      year: 'numeric', 
      month: 'short', 
      day: 'numeric' 
    });
  };
  
  return (
    <Box className="analyst-quotes-container">
      {quotes.length === 0 ? (
        <Typography variant="body1" className="no-results">
          No analyst quotes found matching the current filters.
        </Typography>
      ) : (
        <List className="quotes-list">
          {quotes.map((quote) => (
            <Card key={quote.id} className="quote-card">
              <CardContent>
                <Box className="quote-header">
                  <Avatar className="analyst-avatar">
                    {quote.analyst_name.charAt(0)}
                  </Avatar>
                  <Box className="analyst-info">
                    <Typography variant="subtitle1" className="analyst-name">
                      {quote.analyst_name}
                    </Typography>
                    <Typography variant="caption" className="analyst-org">
                      {quote.organization}
                    </Typography>
                  </Box>
                  <Chip 
                    label={quote.primary_category.replace('_', ' ')} 
                    size="small"
                    className="category-chip"
                    style={{ 
                      backgroundColor: getCategoryColor(quote.primary_category),
                      color: 'white'
                    }}
                  />
                </Box>
                
                <Box className="quote-content">
                  <FormatQuoteIcon className="quote-icon" />
                  <Typography variant="body1">
                    {quote.content}
                  </Typography>
                </Box>
                
                <Box className="quote-footer">
                  <Typography variant="caption" className="quote-date">
                    {formatDate(quote.date)}
                  </Typography>
                  <Typography variant="caption" className="priority-score">
                    Priority: {quote.priority_score.toFixed(1)}
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          ))}
        </List>
      )}
    </Box>
  );
}

export default AnalystQuotes;
