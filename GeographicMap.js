import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { ComposableMap, Geographies, Geography, Marker } from 'react-simple-maps';
import { scaleLinear } from 'd3-scale';
import ReactTooltip from 'react-tooltip';
import '../styles/GeographicMap.css';

// World map topojson
const geoUrl = "https://raw.githubusercontent.com/deldersveld/topojson/master/world-countries.json";

// Mock conflict hotspot data
const mockHotspots = [
  { name: "Ukraine-Russia Border", coordinates: [31.1656, 48.3794], intensity: 90, category: "external_conflict" },
  { name: "Taiwan Strait", coordinates: [121.0, 24.0], intensity: 75, category: "external_conflict" },
  { name: "Israel-Gaza", coordinates: [34.3088, 31.3547], intensity: 85, category: "external_conflict" },
  { name: "Ethiopia-Tigray", coordinates: [39.4699, 13.3135], intensity: 70, category: "internal_conflict" },
  { name: "Myanmar", coordinates: [95.9562, 21.9162], intensity: 65, category: "internal_conflict" },
  { name: "US-Mexico Border", coordinates: [-106.3468, 31.7457], intensity: 60, category: "external_conflict" },
  { name: "South China Sea", coordinates: [114.0994, 16.0797], intensity: 70, category: "external_conflict" },
  { name: "Venezuela", coordinates: [-66.5897, 6.4238], intensity: 55, category: "internal_conflict" },
  { name: "Iran-Saudi Arabia", coordinates: [50.5333, 26.0667], intensity: 65, category: "external_conflict" },
  { name: "North Korea-South Korea", coordinates: [127.0000, 38.0000], intensity: 60, category: "external_conflict" },
  { name: "France Protests", coordinates: [2.3522, 48.8566], intensity: 50, category: "internal_conflict" },
  { name: "US Political Polarization", coordinates: [-98.5795, 39.8283], intensity: 65, category: "internal_conflict" }
];

function GeographicMap({ filters }) {
  const [hotspots, setHotspots] = useState([]);
  const [tooltipContent, setTooltipContent] = useState("");
  
  useEffect(() => {
    // In a real implementation, this would fetch data from an API
    // For now, we'll filter the mock data based on the filters
    
    let filteredHotspots = [...mockHotspots];
    
    // Apply category filter
    if (filters.category && filters.category !== 'all') {
      filteredHotspots = filteredHotspots.filter(hotspot => 
        hotspot.category === filters.category
      );
    }
    
    // Apply region filter
    if (filters.region && filters.region !== 'global') {
      // This is a simplified approach - in a real implementation,
      // we would have more precise region filtering
      const regionCoordinates = {
        'us': [-98.5795, 39.8283],
        'europe': [10.4515, 51.1657],
        'asia': [100.6197, 34.0479],
        'middle_east': [53.4949, 29.3721],
        'latin_america': [-78.6569, -20.7177]
      };
      
      if (regionCoordinates[filters.region]) {
        // Filter hotspots by proximity to region center (simplified)
        const [regionLong, regionLat] = regionCoordinates[filters.region];
        filteredHotspots = filteredHotspots.filter(hotspot => {
          const [hotspotLong, hotspotLat] = hotspot.coordinates;
          const distance = Math.sqrt(
            Math.pow(hotspotLong - regionLong, 2) + 
            Math.pow(hotspotLat - regionLat, 2)
          );
          return distance < 50; // Arbitrary threshold
        });
      }
    }
    
    setHotspots(filteredHotspots);
  }, [filters]);
  
  // Scale for marker size based on intensity
  const markerScale = scaleLinear()
    .domain([0, 100])
    .range([5, 20]);
  
  // Color scale for markers based on category
  const getMarkerColor = (category) => {
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
  
  return (
    <Box className="geographic-map-container">
      <ReactTooltip>{tooltipContent}</ReactTooltip>
      <ComposableMap
        projectionConfig={{
          scale: 147,
          rotation: [-11, 0, 0],
        }}
        width={800}
        height={400}
        style={{ width: "100%", height: "auto" }}
      >
        <Geographies geography={geoUrl}>
          {({ geographies }) =>
            geographies.map((geo) => (
              <Geography
                key={geo.rsmKey}
                geography={geo}
                fill="#EAEAEC"
                stroke="#D6D6DA"
                style={{
                  default: { outline: "none" },
                  hover: { outline: "none", fill: "#F5F5F5" },
                  pressed: { outline: "none" },
                }}
              />
            ))
          }
        </Geographies>
        
        {hotspots.map((hotspot, index) => (
          <Marker 
            key={index} 
            coordinates={hotspot.coordinates}
            data-tip={`${hotspot.name} - Intensity: ${hotspot.intensity}`}
            onMouseEnter={() => {
              setTooltipContent(`${hotspot.name} - Intensity: ${hotspot.intensity}`);
            }}
            onMouseLeave={() => {
              setTooltipContent("");
            }}
          >
            <circle
              r={markerScale(hotspot.intensity)}
              fill={getMarkerColor(hotspot.category)}
              stroke="#FFFFFF"
              strokeWidth={2}
              opacity={0.8}
            />
          </Marker>
        ))}
      </ComposableMap>
      
      <Box className="map-legend">
        <Typography variant="subtitle2">Conflict Intensity</Typography>
        <Box className="legend-items">
          <Box className="legend-item">
            <Box 
              className="legend-marker" 
              style={{ 
                backgroundColor: '#f44336',
                width: markerScale(70),
                height: markerScale(70),
                borderRadius: '50%'
              }} 
            />
            <Typography variant="caption">Internal Conflict</Typography>
          </Box>
          <Box className="legend-item">
            <Box 
              className="legend-marker" 
              style={{ 
                backgroundColor: '#2196f3',
                width: markerScale(70),
                height: markerScale(70),
                borderRadius: '50%'
              }} 
            />
            <Typography variant="caption">External Conflict</Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  );
}

export default GeographicMap;
