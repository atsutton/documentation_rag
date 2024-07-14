import React, { useState, useRef, useEffect } from 'react';
import ChatBox from "./ChatBox";
import {Box, TextField, IconButton, Paper} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import sendQuery from './apiCaller';
import './Rag.css';

function Rag() {
  const [userInput, setUserInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isAwaitingResponse, setIsAwaitingResponse] = useState('');

  const userInputRef = useRef(null);

  useEffect(() => {
    if (userInputRef.current) {
      userInputRef.current.focus();
    }
  }, []);

  const handleUserInputChange = (event) => {
    setUserInput(event.target.value);
  }

  const handleUserInputKeyDown = (event) => {
    if (event.key === 'Enter' && !event.shiftKey && !event.ctrlKey) {
      handleClickSend();
    }
  }

  const handleClickSend = async (event) => {
    if (!userInput) {
      return;
    }
    const val = userInput.trim();
    appendMessages(val, 'user');
    setUserInput('');
    setIsAwaitingResponse(true);
    const res = await sendQuery(val);
    appendMessages(res, 'bot');
    setIsAwaitingResponse(false);
    userInputRef.current.focus();
  }

  const appendMessages = (msg, sender) => {
    setMessages(prev => [...prev, { text: msg, sender: sender }]);
  }

  return (
    <Box className="Rag">
      <Box className="content-container">
        <Box className="chat-box-container">
          <ChatBox 
            messages={messages} 
            isAwaitingResponse={isAwaitingResponse} 
          />
        </Box>
        <Box class="user-input-container">
          <TextField 
            value={userInput} 
            onChange={handleUserInputChange}
            onKeyDown={handleUserInputKeyDown}
            variant="standard"
            id="user-input"
            inputRef={userInputRef}
          />
          <IconButton onClick={handleClickSend} aria-label="send">
            <SendIcon />
          </IconButton>
        </Box>
      </Box>
    </Box>
  );
}

export default Rag;
