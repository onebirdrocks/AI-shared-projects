import React, { useState, useEffect, useRef } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatProps {
  fileName: string;
}

const Chat: React.FC<ChatProps> = ({ fileName }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [ws, setWs] = useState<WebSocket | null>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    setWs(websocket);

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.response) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      }
    };

    return () => {
      websocket.close();
    };
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = () => {
    if (input.trim() && ws) {
      const newMessage: Message = { role: 'user', content: input };
      setMessages(prev => [...prev, newMessage]);
      ws.send(JSON.stringify({ query: input, file_name: fileName, chat_history: messages }));
      setInput('');
    }
  };

  return (
    <div className="flex flex-col h-full bg-gray-100">
      <div className="p-4 bg-gray-100 border-b border-gray-200">
        <h2 className="text-xl font-bold">Chat with PDF</h2>
      </div>
      <div ref={chatContainerRef} className="flex-grow overflow-y-auto p-4">
        {messages.map((message, index) => (
          <div key={index} className={`mb-4 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
            <span className={`inline-block p-2 rounded-lg ${message.role === 'user' ? 'bg-blue-500 text-white' : 'bg-white text-black'}`}>
              {message.content}
            </span>
          </div>
        ))}
      </div>
      <div className="p-4 border-t border-gray-200 bg-gray-100">
        <div className="flex">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            className="flex-grow border border-gray-300 rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="输入您的问题..."
          />
          <button 
            onClick={sendMessage}
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 transition duration-300"
          >
            发送
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;