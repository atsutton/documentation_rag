import React from 'react';
import { Box } from '@mui/material';
import './SkeletonLoader.css';

function SkeletonLoader({ lines = 3 }) {
  return (
    <Box className="skeleton-loader-wrapper">
      <Box className="skeleton-loader">
        {Array.from({ length: lines }).map((_, index) => (
          <div
            key={index}
            className={`animated-line-${index % 2 + 1}`} 
          />
        ))}
      </Box>
    </Box>
  );
}

export default SkeletonLoader;
