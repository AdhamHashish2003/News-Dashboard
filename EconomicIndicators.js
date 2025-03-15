import React, { useState, useEffect } from 'react';
import { Box, Typography, Grid, Card, CardContent } from '@mui/material';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
import '../styles/EconomicIndicators.css';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// Mock economic indicators data
const mockEconomicData = {
  inflation: {
    dates: [
      '2023-01-15', '2023-02-15', '2023-03-15', 
      '2023-04-15', '2023-05-15', '2023-06-15'
    ],
    values: [6.5, 6.2, 5.9, 5.7, 5.4, 5.1]
  },
  interest_rates: {
    dates: [
      '2023-01-15', '2023-02-15', '2023-03-15', 
      '2023-04-15', '2023-05-15', '2023-06-15'
    ],
    values: [4.25, 4.5, 4.75, 5.0, 5.25, 5.25]
  },
  unemployment: {
    dates: [
      '2023-01-15', '2023-02-15', '2023-03-15', 
      '2023-04-15', '2023-05-15', '2023-06-15'
    ],
    values: [3.6, 3.5, 3.6, 3.7, 3.8, 3.9]
  },
  gdp_growth: {
    dates: [
      '2022-Q2', '2022-Q3', '2022-Q4', 
      '2023-Q1', '2023-Q2'
    ],
    values: [2.1, 2.6, 1.9, 1.3, 0.8]
  },
  debt_to_gdp: {
    dates: [
      '2022-Q2', '2022-Q3', '2022-Q4', 
      '2023-Q1', '2023-Q2'
    ],
    values: [123.4, 124.1, 125.3, 126.5, 127.8]
  }
};

// Mock economic news mentions
const mockEconomicMentions = {
  dates: [
    '2023-05-15', '2023-05-22', '2023-05-29',
    '2023-06-05', '2023-06-12', '2023-06-15'
  ],
  inflation: [25, 28, 30, 32, 35, 38],
  interest_rates: [20, 22, 25, 28, 30, 32],
  unemployment: [15, 14, 16, 18, 17, 15],
  recession: [10, 12, 15, 18, 22, 25],
  gdp: [18, 16, 15, 14, 16, 18]
};

function EconomicIndicators({ filters }) {
  const [economicData, setEconomicData] = useState(null);
  const [mentionsData, setMentionsData] = useState(null);
  
  useEffect(() => {
    // In a real implementation, this would fetch data from an API
    // For now, we'll use mock data
    
    // Prepare economic indicators chart data
    const inflationData = {
      labels: mockEconomicData.inflation.dates.map(date => {
        if (date.includes('Q')) return date; // For quarterly data
        const d = new Date(date);
        return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
      }),
      datasets: [
        {
          label: 'Inflation Rate (%)',
          data: mockEconomicData.inflation.values,
          borderColor: '#f44336',
          backgroundColor: 'rgba(244, 67, 54, 0.1)',
          yAxisID: 'y',
        },
        {
          label: 'Interest Rate (%)',
          data: mockEconomicData.interest_rates.values,
          borderColor: '#2196f3',
          backgroundColor: 'rgba(33, 150, 243, 0.1)',
          yAxisID: 'y',
        },
        {
          label: 'Unemployment Rate (%)',
          data: mockEconomicData.unemployment.values,
          borderColor: '#4caf50',
          backgroundColor: 'rgba(76, 175, 80, 0.1)',
          yAxisID: 'y',
        }
      ]
    };
    
    setEconomicData(inflationData);
    
    // Prepare economic mentions chart data
    const mentionsChartData = {
      labels: mockEconomicMentions.dates.map(date => {
        const d = new Date(date);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: [
        {
          label: 'Inflation',
          data: mockEconomicMentions.inflation,
          backgroundColor: 'rgba(244, 67, 54, 0.7)',
        },
        {
          label: 'Interest Rates',
          data: mockEconomicMentions.interest_rates,
          backgroundColor: 'rgba(33, 150, 243, 0.7)',
        },
        {
          label: 'Unemployment',
          data: mockEconomicMentions.unemployment,
          backgroundColor: 'rgba(76, 175, 80, 0.7)',
        },
        {
          label: 'Recession',
          data: mockEconomicMentions.recession,
          backgroundColor: 'rgba(255, 152, 0, 0.7)',
        },
        {
          label: 'GDP',
          data: mockEconomicMentions.gdp,
          backgroundColor: 'rgba(156, 39, 176, 0.7)',
        }
      ]
    };
    
    setMentionsData(mentionsChartData);
    
  }, [filters]);
  
  const economicOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Key Economic Indicators',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      }
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Percentage (%)'
        }
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    }
  };
  
  const mentionsOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Economic Topic Mentions',
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      }
    },
    scales: {
      y: {
        title: {
          display: true,
          text: 'Number of Mentions'
        },
        beginAtZero: true
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    }
  };
  
  // Current economic indicators
  const currentIndicators = [
    { name: 'Inflation Rate', value: '5.1%', change: '-0.3%', trend: 'down' },
    { name: 'Interest Rate', value: '5.25%', change: '0%', trend: 'flat' },
    { name: 'Unemployment', value: '3.9%', change: '+0.1%', trend: 'up' },
    { name: 'GDP Growth', value: '0.8%', change: '-0.5%', trend: 'down' },
    { name: 'Debt to GDP', value: '127.8%', change: '+1.3%', trend: 'up' }
  ];
  
  const getTrendColor = (trend) => {
    switch (trend) {
      case 'up':
        return trend === 'up' && ['Inflation Rate', 'Unemployment', 'Debt to GDP'].includes(name) ? '#f44336' : '#4caf50';
      case 'down':
        return trend === 'down' && ['Inflation Rate', 'Unemployment', 'Debt to GDP'].includes(name) ? '#4caf50' : '#f44336';
      default:
        return '#ff9800';
    }
  };
  
  return (
    <Box className="economic-indicators-container">
      <Grid container spacing={3}>
        {/* Current Indicators */}
        <Grid item xs={12}>
          <Grid container spacing={2}>
            {currentIndicators.map((indicator, index) => (
              <Grid item xs={6} sm={4} md={2.4} key={index}>
                <Card className="indicator-card">
                  <CardContent>
                    <Typography variant="subtitle2" className="indicator-name">
                      {indicator.name}
                    </Typography>
                    <Typography variant="h5" className="indicator-value">
                      {indicator.value}
                    </Typography>
                    <Typography 
                      variant="body2" 
                      className="indicator-change"
                      style={{ 
                        color: indicator.trend === 'up' ? 
                          (indicator.name === 'GDP Growth' ? '#4caf50' : '#f44336') : 
                          indicator.trend === 'down' ? 
                            (indicator.name === 'GDP Growth' ? '#f44336' : '#4caf50') : 
                            '#ff9800'
                      }}
                    >
                      {indicator.change} 
                      {indicator.trend === 'up' ? '↑' : indicator.trend === 'down' ? '↓' : '→'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Grid>
        
        {/* Economic Indicators Chart */}
        <Grid item xs={12} md={6}>
          <Box className="chart-container">
            {economicData ? (
              <Line data={economicData} options={economicOptions} height={300} />
            ) : (
              <Typography variant="body1" className="loading-text">
                Loading economic data...
              </Typography>
            )}
          </Box>
        </Grid>
        
        {/* Economic Mentions Chart */}
        <Grid item xs={12} md={6}>
          <Box className="chart-container">
            {mentionsData ? (
              <Bar data={mentionsData} options={mentionsOptions} height={300} />
            ) : (
              <Typography variant="body1" className="loading-text">
                Loading mentions data...
              </Typography>
            )}
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}

export default EconomicIndicators;
