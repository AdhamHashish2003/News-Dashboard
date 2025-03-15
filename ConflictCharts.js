import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';
import '../styles/ConflictCharts.css';

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

// Mock time series data
const mockTimeSeriesData = {
  dates: [
    '2023-05-15', '2023-05-16', '2023-05-17', '2023-05-18', '2023-05-19',
    '2023-05-20', '2023-05-21', '2023-05-22', '2023-05-23', '2023-05-24',
    '2023-05-25', '2023-05-26', '2023-05-27', '2023-05-28', '2023-05-29',
    '2023-05-30', '2023-05-31', '2023-06-01', '2023-06-02', '2023-06-03',
    '2023-06-04', '2023-06-05', '2023-06-06', '2023-06-07', '2023-06-08',
    '2023-06-09', '2023-06-10', '2023-06-11', '2023-06-12', '2023-06-13',
    '2023-06-14', '2023-06-15'
  ],
  internal_conflict: [
    5, 7, 6, 8, 10, 9, 7, 6, 8, 9,
    11, 13, 12, 10, 9, 8, 10, 12, 14, 15,
    13, 12, 14, 16, 18, 17, 15, 14, 16, 18,
    20, 22
  ],
  external_conflict: [
    8, 9, 10, 11, 10, 9, 8, 10, 12, 14,
    13, 12, 11, 10, 12, 14, 15, 16, 15, 14,
    13, 15, 17, 18, 17, 16, 15, 17, 19, 21,
    20, 19
  ],
  economic_indicators: [
    12, 11, 10, 9, 11, 13, 14, 15, 14, 13,
    12, 14, 16, 17, 16, 15, 14, 16, 18, 19,
    18, 17, 16, 15, 17, 19, 20, 19, 18, 17,
    19, 21
  ]
};

// Mock priority score data
const mockPriorityScoreData = {
  dates: [
    '2023-05-15', '2023-05-22', '2023-05-29',
    '2023-06-05', '2023-06-12', '2023-06-15'
  ],
  internal_conflict: [65, 68, 72, 75, 78, 80],
  external_conflict: [70, 72, 75, 78, 82, 85],
  economic_indicators: [60, 65, 70, 72, 75, 78]
};

function ConflictCharts({ filters }) {
  const [timeSeriesData, setTimeSeriesData] = useState(null);
  const [priorityScoreData, setPriorityScoreData] = useState(null);
  
  useEffect(() => {
    // In a real implementation, this would fetch data from an API
    // For now, we'll use mock data
    
    // Filter data based on category if specified
    let filteredTimeSeries = { ...mockTimeSeriesData };
    let filteredPriorityScores = { ...mockPriorityScoreData };
    
    // Apply date range filter
    let startIndex = 0;
    let endIndex = filteredTimeSeries.dates.length - 1;
    
    if (filters.dateRange === '1d') {
      startIndex = endIndex - 1;
    } else if (filters.dateRange === '7d') {
      startIndex = endIndex - 7;
    } else if (filters.dateRange === '30d') {
      startIndex = endIndex - 30;
    }
    
    // Ensure startIndex is not negative
    startIndex = Math.max(0, startIndex);
    
    // Filter time series data
    filteredTimeSeries = {
      dates: filteredTimeSeries.dates.slice(startIndex, endIndex + 1),
      internal_conflict: filteredTimeSeries.internal_conflict.slice(startIndex, endIndex + 1),
      external_conflict: filteredTimeSeries.external_conflict.slice(startIndex, endIndex + 1),
      economic_indicators: filteredTimeSeries.economic_indicators.slice(startIndex, endIndex + 1)
    };
    
    // Prepare chart data
    const timeSeriesChartData = {
      labels: filteredTimeSeries.dates.map(date => {
        const d = new Date(date);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: []
    };
    
    // Add datasets based on filters
    if (filters.category === 'all' || filters.category === 'internal_conflict') {
      timeSeriesChartData.datasets.push({
        label: 'Internal Conflict',
        data: filteredTimeSeries.internal_conflict,
        borderColor: '#f44336',
        backgroundColor: 'rgba(244, 67, 54, 0.1)',
        tension: 0.4
      });
    }
    
    if (filters.category === 'all' || filters.category === 'external_conflict') {
      timeSeriesChartData.datasets.push({
        label: 'External Conflict',
        data: filteredTimeSeries.external_conflict,
        borderColor: '#2196f3',
        backgroundColor: 'rgba(33, 150, 243, 0.1)',
        tension: 0.4
      });
    }
    
    if (filters.category === 'all' || filters.category === 'economic_indicators') {
      timeSeriesChartData.datasets.push({
        label: 'Economic Indicators',
        data: filteredTimeSeries.economic_indicators,
        borderColor: '#4caf50',
        backgroundColor: 'rgba(76, 175, 80, 0.1)',
        tension: 0.4
      });
    }
    
    setTimeSeriesData(timeSeriesChartData);
    
    // Prepare priority score chart data
    const priorityScoreChartData = {
      labels: filteredPriorityScores.dates.map(date => {
        const d = new Date(date);
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
      }),
      datasets: []
    };
    
    // Add datasets based on filters
    if (filters.category === 'all' || filters.category === 'internal_conflict') {
      priorityScoreChartData.datasets.push({
        label: 'Internal Conflict',
        data: filteredPriorityScores.internal_conflict,
        backgroundColor: 'rgba(244, 67, 54, 0.7)',
      });
    }
    
    if (filters.category === 'all' || filters.category === 'external_conflict') {
      priorityScoreChartData.datasets.push({
        label: 'External Conflict',
        data: filteredPriorityScores.external_conflict,
        backgroundColor: 'rgba(33, 150, 243, 0.7)',
      });
    }
    
    if (filters.category === 'all' || filters.category === 'economic_indicators') {
      priorityScoreChartData.datasets.push({
        label: 'Economic Indicators',
        data: filteredPriorityScores.economic_indicators,
        backgroundColor: 'rgba(76, 175, 80, 0.7)',
      });
    }
    
    setPriorityScoreData(priorityScoreChartData);
    
  }, [filters]);
  
  const timeSeriesOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Conflict Mentions Over Time',
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
          text: 'Number of Articles'
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
  
  const priorityScoreOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Average Priority Scores',
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
          text: 'Priority Score'
        },
        beginAtZero: true,
        max: 100
      },
      x: {
        title: {
          display: true,
          text: 'Date'
        }
      }
    }
  };
  
  return (
    <Box className="conflict-charts-container">
      <Box className="chart-container time-series-chart">
        {timeSeriesData ? (
          <Line data={timeSeriesData} options={timeSeriesOptions} height={300} />
        ) : (
          <Typography variant="body1" className="loading-text">
            Loading time series data...
          </Typography>
        )}
      </Box>
      
      <Box className="chart-container priority-score-chart">
        {priorityScoreData ? (
          <Bar data={priorityScoreData} options={priorityScoreOptions} height={300} />
        ) : (
          <Typography variant="body1" className="loading-text">
            Loading priority score data...
          </Typography>
        )}
      </Box>
    </Box>
  );
}

export default ConflictCharts;
