// Convert the HTML structure to a React component
import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

const Chatbot = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);

    const handleSend = async () => {
        if (!input.trim()) return; // Do not send empty messages

        // Add user message to the conversation
        setMessages(prevMessages => [...prevMessages, { sender: "user", text: input }]);

        try {
            // Send user input to the backend
            const response = await axios.post("http://localhost:8000/chat", {
                message: input,
            });
            const botResponse = response.data.response;

            // Add bot response to the conversation
            setMessages(prevMessages => [...prevMessages, { sender: "bot", text: botResponse }]);
        } catch (error) {
            console.error("Error communicating with the backend:", error);
            setMessages(prevMessages => [...prevMessages, { sender: "bot", text: "Error: Could not reach the backend." }]);
        }

        // Clear the input field
        setInput("");
    };

    // Clear all chat messages
    const handleClearChat = () => {
        setMessages([]);
    };

    // Scroll to the bottom of the chat when new messages are added
    useEffect(() => {
        if (messagesEndRef.current) {
            messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
        }
    }, [messages]);

    return (
        <div className="flex items-center justify-center h-screen bg-gray-100">
            <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-4 border-4 border-gray-800">
                <h2 className="text-2xl font-bold text-center mb-4">AnyBot</h2>
                <div className="h-96 overflow-y-auto p-2 mb-4 border border-gray-300 rounded-lg">
                    {messages.map((msg, index) => (
                        <div
                            key={index}
                            className={`mb-2 p-2 rounded-lg max-w-[70%] w-fit ${
                                msg.sender === "user" ? "bg-gray-800 text-white self-end ml-auto text-right" : "bg-gray-200 text-black self-start mr-auto text-left"
                            }`}
                        >
                            {msg.text}
                        </div>
                    ))}
                    <div ref={messagesEndRef} />
                </div>
                <div className="flex gap-2 mb-4">
                    <input 
                        type="text" 
                        placeholder="Type your message..." 
                        className="w-full p-2 border border-gray-400 rounded-md focus:outline-none focus:ring-2 focus:ring-gray-800"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => {
                            if (e.key === "Enter") handleSend();
                        }}
                    />
                    <button className="bg-gray-800 text-white px-4 py-2 rounded-md hover:bg-black" onClick={handleSend}>Send</button>
                </div>
                <button className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-600 w-full" onClick={handleClearChat}>Clear Chat</button>
            </div>
        </div>
    );
};

export default Chatbot;