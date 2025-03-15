import React, { useState, useEffect } from 'react';
import { Box, Typography, FormControl, InputLabel, Select, MenuItem, TextField, Button, Grid } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import SearchIcon from '@mui/icons-material/Search';
import '../styles/SearchFilter.css';

function SearchFilter({ onFilterChange }) {
  const [category, setCategory] = useState('all');
  const [dateRange, setDateRange] = useState('7d');
  const [searchQuery, setSearchQuery] = useState('');
  const [region, setRegion] = useState('global');
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [showCustomDates, setShowCustomDates] = useState(false);

  // Apply filters when they change
  useEffect(() => {
    const filters = {
      category,
      dateRange,
      searchQuery,
      region
    };
    
    // Add custom date range if selected
    if (dateRange === 'custom' && startDate && endDate) {
      filters.startDate = startDate;
      filters.endDate = endDate;
    }
    
    onFilterChange(filters);
  }, [category, dateRange, region, onFilterChange]);

  // Handle search button click
  const handleSearch = () => {
    onFilterChange({
      searchQuery,
      category,
      dateRange,
      region,
      ...(dateRange === 'custom' && startDate && endDate ? { startDate, endDate } : {})
    });
  };

  // Handle date range change
  const handleDateRangeChange = (event) => {
    const value = event.target.value;
    setDateRange(value);
    setShowCustomDates(value === 'custom');
  };

  return (
    <Box className="search-filter-container">
      <Grid container spacing={2} alignItems="center">
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            label="Search Keywords"
            variant="outlined"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
            InputProps={{
              endAdornment: (
                <Button 
                  color="primary" 
                  onClick={handleSearch}
                  startIcon={<SearchIcon />}
                >
                  Search
                </Button>
              ),
            }}
          />
        </Grid>
        
        <Grid item xs={12} md={2}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Category</InputLabel>
            <Select
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              label="Category"
            >
              <MenuItem value="all">All Categories</MenuItem>
              <MenuItem value="internal_conflict">Internal Conflict</MenuItem>
              <MenuItem value="external_conflict">External Conflict</MenuItem>
              <MenuItem value="economic_indicators">Economic Indicators</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Time Period</InputLabel>
            <Select
              value={dateRange}
              onChange={handleDateRangeChange}
              label="Time Period"
            >
              <MenuItem value="1d">Last 24 Hours</MenuItem>
              <MenuItem value="7d">Last 7 Days</MenuItem>
              <MenuItem value="30d">Last 30 Days</MenuItem>
              <MenuItem value="90d">Last 90 Days</MenuItem>
              <MenuItem value="1y">Last Year</MenuItem>
              <MenuItem value="custom">Custom Range</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        <Grid item xs={12} md={2}>
          <FormControl fullWidth variant="outlined">
            <InputLabel>Region</InputLabel>
            <Select
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              label="Region"
            >
              <MenuItem value="global">Global</MenuItem>
              <MenuItem value="us">United States</MenuItem>
              <MenuItem value="europe">Europe</MenuItem>
              <MenuItem value="asia">Asia</MenuItem>
              <MenuItem value="middle_east">Middle East</MenuItem>
              <MenuItem value="latin_america">Latin America</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        
        {showCustomDates && (
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <Grid item xs={12} md={2}>
              <DatePicker
                label="Start Date"
                value={startDate}
                onChange={setStartDate}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Grid>
            <Grid item xs={12} md={2}>
              <DatePicker
                label="End Date"
                value={endDate}
                onChange={setEndDate}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </Grid>
          </LocalizationProvider>
        )}
      </Grid>
    </Box>
  );
}

export default SearchFilter;
