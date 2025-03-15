import React, { useState, useEffect } from 'react';
import { List, ListItem, ListItemText, Typography, Divider, Chip, Card, CardContent, CardActions, Button, Avatar } from '@mui/material';
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material';
import '../styles/NewsFeed.css';

// Mock data for development
const mockArticles = [
  {
    id: 1,
    title: "Global Trade Tensions Escalate as US and China Impose New Tariffs",
    content: "Trade tensions between the United States and China escalated today as both countries announced new tariffs on each other's goods.",
    source: "Financial Times",
    published_date: "2023-06-15T10:30:00Z",
    url: "https://example.com/article1",
    priority_score: 85.5,
    primary_category: "external_conflict",
    secondary_category: "economic_indicators"
  },
  {
    id: 2,
    title: "Protests Erupt in Major Cities Over Economic Inequality",
    content: "Thousands took to the streets in several major cities today, protesting growing economic inequality and government policies.",
    source: "The New York Times",
    published_date: "2023-06-14T14:45:00Z",
    url: "https://example.com/article2",
    priority_score: 78.2,
    primary_category: "internal_conflict",
    secondary_category: null
  },
  {
    id: 3,
    title: "Central Banks Signal Shift in Monetary Policy Amid Inflation Concerns",
    content: "Several central banks have signaled a potential shift in monetary policy as inflation concerns grow in major economies.",
    source: "Bloomberg",
    published_date: "2023-06-13T09:15:00Z",
    url: "https://example.com/article3",
    priority_score: 72.8,
    primary_category: "economic_indicators",
    secondary_category: null
  },
  {
    id: 4,
    title: "Diplomatic Relations Deteriorate Between European Nations Over Resource Disputes",
    content: "Diplomatic tensions are rising between several European nations as disputes over shared resources intensify.",
    source: "Reuters",
    published_date: "2023-06-12T16:20:00Z",
    url: "https://example.com/article4",
    priority_score: 68.5,
    primary_category: "external_conflict",
    secondary_category: null
  },
  {
    id: 5,
    title: "Political Polarization Reaches New Heights in Legislative Bodies",
    content: "Political analysts report unprecedented levels of polarization in legislative bodies, hampering governance and policy implementation.",
    source: "The Washington Post",
    published_date: "2023-06-11T11:10:00Z",
    url: "https://example.com/article5",
    priority_score: 65.3,
    primary_category: "internal_conflict",
    secondary_category: null
  }
];

// Mock analyst commentary
const mockAnalystCommentary = [
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
  }
];

function NewsFeed({ filters, limit = 10 }) {
  const [articles, setArticles] = useState([]);
  
  useEffect(() => {
    // In a real implementation, this would fetch data from an API
    // For now, we'll filter the mock data based on the filters
    
    let filteredData;
    
    // Determine if we're showing news articles or analyst commentary
    if (filters.dataType === 'analyst') {
      filteredData = [...mockAnalystCommentary];
    } else {
      filteredData = [...mockArticles];
    }
    
    // Apply category filter
    if (filters.category && filters.category !== 'all') {
      filteredData = filteredData.filter(item => 
        item.primary_category === filters.category || 
        item.secondary_category === filters.category
      );
    }
    
    // Apply search query filter
    if (filters.searchQuery) {
      const query = filters.searchQuery.toLowerCase();
      filteredData = filteredData.filter(item => 
        item.title?.toLowerCase().includes(query) || 
        item.content?.toLowerCase().includes(query)
      );
    }
    
    // Apply date range filter (simplified for mock data)
    // In a real implementation, this would properly filter by date
    
    // Sort by priority score
    filteredData.sort((a, b) => b.priority_score - a.priority_score);
    
    // Limit the number of results
    filteredData = filteredData.slice(0, limit);
    
    setArticles(filteredData);
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
  
  const getPriorityIcon = (score) => {
    if (score >= 75) {
      return <TrendingUp style={{ color: '#f44336' }} />;
    } else if (score >= 50) {
      return <TrendingFlat style={{ color: '#ff9800' }} />;
    } else {
      return <TrendingDown style={{ color: '#4caf50' }} />;
    }
  };
  
  return (
    <div className="news-feed-container">
      {articles.length === 0 ? (
        <Typography variant="body1" className="no-results">
          No articles found matching the current filters.
        </Typography>
      ) : (
        <List>
          {articles.map((article) => (
            <Card key={article.id} className="article-card">
              <CardContent>
                <div className="article-header">
                  <Typography variant="h6" className="article-title">
                    {article.title || article.content.substring(0, 60) + '...'}
                  </Typography>
                  <div className="priority-indicator">
                    {getPriorityIcon(article.priority_score)}
                    <Typography variant="body2" className="priority-score">
                      {article.priority_score.toFixed(1)}
                    </Typography>
                  </div>
                </div>
                
                <Typography variant="body2" className="article-content">
                  {article.content}
                </Typography>
                
                <div className="article-meta">
                  <div className="source-date">
                    <Typography variant="caption" className="article-source">
                      {article.source || article.organization}
                    </Typography>
                    <Typography variant="caption" className="article-date">
                      {formatDate(article.published_date || article.date)}
                    </Typography>
                  </div>
                  
                  <div className="article-categories">
                    {article.primary_category && (
                      <Chip 
                        label={article.primary_category.replace('_', ' ')} 
                        size="small"
                        style={{ 
                          backgroundColor: getCategoryColor(article.primary_category),
                          color: 'white'
                        }}
                      />
                    )}
                    {article.secondary_category && (
                      <Chip 
                        label={article.secondary_category.replace('_', ' ')} 
                        size="small"
                        style={{ 
                          backgroundColor: getCategoryColor(article.secondary_category),
                          color: 'white',
                          marginLeft: '8px'
                        }}
                      />
                    )}
                  </div>
                </div>
                
                {article.analyst_name && (
                  <div className="analyst-info">
                    <Avatar className="analyst-avatar">
                      {article.analyst_name.charAt(0)}
                    </Avatar>
                    <div className="analyst-details">
                      <Typography variant="subtitle2" className="analyst-name">
                        {article.analyst_name}
                      </Typography>
                      <Typography variant="caption" className="analyst-org">
                        {article.organization}
                      </Typography>
                    </div>
                  </div>
                )}
              </CardContent>
              <CardActions>
                <Button 
                  size="small" 
                  color="primary"
                  href={article.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  Read More
                </Button>
              </CardActions>
            </Card>
          ))}
        </List>
      )}
    </div>
  );
}

export default NewsFeed;
