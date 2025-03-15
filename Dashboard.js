import React, { useState } from 'react';
import { Container, Grid, Paper, Typography, Tabs, Tab, Box, AppBar, Toolbar } from '@mui/material';
import NewsFeed from './NewsFeed';
import ConflictCharts from './ConflictCharts';
import AnalystQuotes from './AnalystQuotes';
import EconomicIndicators from './EconomicIndicators';
import GeographicMap from './GeographicMap';
import SearchFilter from './SearchFilter';
import '../styles/Dashboard.css';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`tabpanel-${index}`}
      aria-labelledby={`tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function Dashboard() {
  const [tabValue, setTabValue] = useState(0);
  const [filters, setFilters] = useState({
    category: 'all',
    dateRange: '7d',
    searchQuery: '',
    region: 'global'
  });

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleFilterChange = (newFilters) => {
    setFilters({ ...filters, ...newFilters });
  };

  return (
    <div className="dashboard-container">
      <AppBar position="static" color="primary">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Ray Dalio's "New World Order" News Dashboard
          </Typography>
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" className="main-container">
        <Grid container spacing={3}>
          {/* Search and Filter Panel */}
          <Grid item xs={12}>
            <Paper elevation={3} className="search-filter-panel">
              <SearchFilter onFilterChange={handleFilterChange} />
            </Paper>
          </Grid>

          {/* Main Content Tabs */}
          <Grid item xs={12}>
            <Paper elevation={3}>
              <Tabs 
                value={tabValue} 
                onChange={handleTabChange} 
                variant="fullWidth"
                indicatorColor="primary"
                textColor="primary"
              >
                <Tab label="Overview" />
                <Tab label="Internal Conflict" />
                <Tab label="External Conflict" />
                <Tab label="Economic Indicators" />
                <Tab label="Analyst Insights" />
              </Tabs>

              {/* Overview Tab */}
              <TabPanel value={tabValue} index={0}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={8}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Conflict Trends
                      </Typography>
                      <ConflictCharts filters={filters} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Top Analyst Quotes
                      </Typography>
                      <AnalystQuotes filters={filters} limit={5} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Priority News Feed
                      </Typography>
                      <NewsFeed filters={filters} limit={10} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Global Conflict Hotspots
                      </Typography>
                      <GeographicMap filters={filters} />
                    </Paper>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Internal Conflict Tab */}
              <TabPanel value={tabValue} index={1}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={8}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Internal Conflict Trends
                      </Typography>
                      <ConflictCharts filters={{...filters, category: 'internal_conflict'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Internal Conflict Indicators
                      </Typography>
                      <EconomicIndicators filters={{...filters, category: 'internal_conflict'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Internal Conflict News
                      </Typography>
                      <NewsFeed filters={{...filters, category: 'internal_conflict'}} limit={15} />
                    </Paper>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* External Conflict Tab */}
              <TabPanel value={tabValue} index={2}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={8}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        External Conflict Trends
                      </Typography>
                      <ConflictCharts filters={{...filters, category: 'external_conflict'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Global Conflict Map
                      </Typography>
                      <GeographicMap filters={{...filters, category: 'external_conflict'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        External Conflict News
                      </Typography>
                      <NewsFeed filters={{...filters, category: 'external_conflict'}} limit={15} />
                    </Paper>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Economic Indicators Tab */}
              <TabPanel value={tabValue} index={3}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={8}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Economic Trends
                      </Typography>
                      <EconomicIndicators filters={{...filters, category: 'economic_indicators'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={4}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Analyst Economic Insights
                      </Typography>
                      <AnalystQuotes filters={{...filters, category: 'economic_indicators'}} limit={5} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Economic News
                      </Typography>
                      <NewsFeed filters={{...filters, category: 'economic_indicators'}} limit={15} />
                    </Paper>
                  </Grid>
                </Grid>
              </TabPanel>

              {/* Analyst Insights Tab */}
              <TabPanel value={tabValue} index={4}>
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Top Analyst Quotes
                      </Typography>
                      <AnalystQuotes filters={filters} limit={10} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Analyst Sentiment Trends
                      </Typography>
                      <ConflictCharts filters={{...filters, dataType: 'analyst'}} />
                    </Paper>
                  </Grid>
                  <Grid item xs={12}>
                    <Paper elevation={2} className="panel">
                      <Typography variant="h6" className="panel-title">
                        Recent Analyst Commentary
                      </Typography>
                      <NewsFeed filters={{...filters, dataType: 'analyst'}} limit={15} />
                    </Paper>
                  </Grid>
                </Grid>
              </TabPanel>
            </Paper>
          </Grid>
        </Grid>
      </Container>
    </div>
  );
}

export default Dashboard;
