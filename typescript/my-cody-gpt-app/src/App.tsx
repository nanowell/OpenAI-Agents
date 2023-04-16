import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import './App.css';
import * as dotenv from 'dotenv';
dotenv.config();


interface Message {
  role: string;
  content: string;
}

const App = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [message, setMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messageInput = useRef<HTMLInputElement>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (message.trim()) {
      setMessages((prev) => [...prev, { role: 'user', content: message }]);
      setIsLoading(true);
      setMessage('');
      const response = await sendToAPI(message);
      const assistantResponse = response.data.choices[0].message.content.trim();
      setMessages((prev) => [...prev, { role: 'assistant', content: assistantResponse }]);
      setIsLoading(false);
    }
  };

  useEffect(() => {
    if (messageInput.current) {
      messageInput.current.focus();
    }
  }, [messages]);

  const sendToAPI = async (message: string) => {
    const data = {
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: message }],
      temperature: 0.7,
    };

    const config = {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${process.env.API_KEY}`,
      },
    };

    return axios.post('https://api.openai.com/v1/chat/completions', data, config);
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">Chat with GPT-3.5 Turbo</div>
        <div className="chat-messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              {message.content}
            </div>
          ))}
          {isLoading && <div className="loading">Assistant is typing...</div>}
        </div>
        <form className="chat-input" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Type your message"
            ref={messageInput}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
};

export default App;