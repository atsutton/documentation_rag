import axios from 'axios';

const checkApi = async () => {
  try {
    const response = await axios.get('http://localhost:5000/check');
    console.log(response.data); // Handle response data here
    return response;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

const sendQuery = async (userInput) => {
  try {
    const response = await axios.post(
      'http://localhost:5000/send-chat',
      { user_input: userInput }
    );
    
    return response.data.message;
    // Example: Display response message in UI
    // document.getElementById('response').innerText = response.data.message;

  } catch (error) {
    console.error('Error posting data:', error);
    
    // Example: Display error message in UI
    // document.getElementById('error').innerText = error.message;
  }
};

export default sendQuery