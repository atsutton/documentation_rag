import React, { useRef, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import Markdown from 'react-markdown';
import SkeletonLoader from './SkeletonLoader';


function ChatBox({ messages, isAwaitingResponse }) {
  const chatContainerRef = useRef(null);

  // Scroll to the bottom whenever messages change
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  return (
    <Box ref={chatContainerRef} sx={{ 
      p: 2,
      overflowY: 'auto'
    }}>
      {messages.map((msg, index) => (
        <Box
          key={index}
          sx={{
            width: 600,
            marginBottom: 1,
            marginLeft: msg.sender === 'user' ? 'auto' : 0,
            textAlign: msg.sender === 'user' ? 'right' : 'left',
            backgroundColor: msg.sender === 'user' ? '#00fffd45' : 'white'
          }}
        >
          <Typography variant="body1">
            <Markdown>{msg.text}</Markdown>
          </Typography>
        </Box>
      ))}
      {isAwaitingResponse && (
        <SkeletonLoader lines={3} />
      )}
    </Box>
  );
}

export default ChatBox;
