import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { FaPaperPlane, FaArrowLeft, FaSun, FaCalendarAlt, FaInfoCircle } from 'react-icons/fa';


function BarcelOCultas() {
  return (
    <>
      Barcelona
      <br />
      Oculta
    </>
  );
}

function ChatPage() {
  console.log("ChatPage montado");
  const [messages, setMessages] = useState([
    { id: 1, text: '¡Hola! ¿Qué te gustaría saber sobre la escena underground de Barcelona hoy?', sender: 'ai' },
    // Sample message history can be added here
  ]);
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim()) {
      const userMessage = { id: Date.now(), text: input, sender: 'user' };
      setMessages((prev) => [...prev, userMessage]);
      setInput('');
      setLoading(true);
  
      try {
        const response = await fetch('/api/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: input }),
        });
        
  
        const data = await response.json();

        console.log("Respuesta de la IA:", data);

        if (response.ok && typeof data.reply === 'string' && data.reply.trim() !== '') {
        setMessages((prev) => [...prev, { id: Date.now() + 1, text: data.reply, sender: 'ai' }]);
        } else {
          setMessages((prev) => [...prev, { id: Date.now() + 1, text: "La IA no respondió correctamente. Intenta nuevamente.", sender: 'ai' }]);
        }
      } catch (error) {
        console.error("Error al contactar el backend:", error);
        setMessages((prev) => [...prev, {
          id: Date.now() + 2,
          text: "Error al contactar la IA. Intenta más tarde.",
          sender: 'ai'
        }]);
      } finally {
        setLoading(false); // Termina la carga pase lo que pase
      }
    }
  };
  
  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) { 
      event.preventDefault(); 
      handleSend();
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-gray-100 overflow-hidden">
      {/* Left Vertical Banner (Reinstated) */}
      <div className="hidden md:flex md:w-1/4 lg:w-1/5 bg-[url('https://images.pexels.com/photos/1763075/pexels-photo-1763075.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1')] bg-cover bg-center relative flex-shrink-0">
        <div className="absolute inset-0 bg-black/60"></div>
        <div className="relative z-10 p-4 flex flex-col justify-end">
          <h2 className="text-2xl font-bold text-white mb-2 shadow-text"><BarcelOCultas></BarcelOCultas></h2>
          <p className="text-sm text-gray-300 shadow-text">Tu IA asistente</p>
        </div>
      </div>

      {/* Main Content Area (Chat + Sidebar together) */}
      <div className="flex flex-1 overflow-hidden p-4 md:p-6 lg:p-8 gap-4 md:gap-6 lg:gap-8"> 
        {/* Chat Box Container - Now individually styled */}
        <main className="flex-1 flex flex-col overflow-hidden bg-gray-800 shadow-xl rounded-lg"> 
          {/* Chat Header - Keep rounded top-left */}
          <header className="bg-black p-4 flex items-center justify-between shadow-md flex-shrink-0 rounded-tl-lg">
            <div className="flex items-center">
              <Link to="/" className="text-purple-400 hover:text-purple-300 mr-4">
                <FaArrowLeft size={20} />
              </Link>
              <h1 className="text-lg font-semibold text-purple-400">Chatea con la IA</h1>
            </div>
          </header>

          {/* Message Display Area */}
          <div className="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 scrollbar-thin scrollbar-thumb-purple-700 scrollbar-track-gray-700/50">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.sender === 'ai' ? 'justify-start' : 'justify-end'}`}>
                <div
                  className={`max-w-[85%] px-4 py-2 rounded-lg shadow ${ 
                    msg.sender === 'ai'
                      ? 'bg-gray-700 text-gray-100 rounded-br-none'
                      : 'bg-purple-600 text-white rounded-bl-none'
                  }`}
                >
                  {/* Simple markdown-like support for newlines if needed in future */}
                  {msg.text.split('\n').map((line, i) => <p key={i} className={i > 0 ? 'mt-1' : ''}>{line}</p>)}
                </div>
              </div>
            ))}
            
            {loading && (
              <div className="flex justify-start">
                <div className="max-w-[85%] px-4 py-2 rounded-lg shadow bg-gray-700 text-gray-400 italic animate-pulse">
                  La IA está escribiendo...
                </div>
              </div>
            )}

            <div ref={messagesEndRef} /> 
          </div>

          {/* Input Area - Keep rounded bottom-left */}
          <div className="bg-gray-900 p-3 md:p-4 flex items-center border-t border-gray-700 flex-shrink-0 rounded-bl-lg space-y-2">
            <div className="flex items-center space-x-3">
              <textarea
                rows={1}
                name="userMessage"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyPress}
                placeholder="Pregunta lo que quieras..."
                disabled={loading}
                className="flex-1 bg-gray-700 border border-gray-600 rounded-md px-4 py-2 focus:outline-none focus:ring-1 focus:ring-purple-500 focus:border-transparent text-gray-100 placeholder-gray-400 resize-none scrollbar-thin scrollbar-thumb-gray-500 scrollbar-track-gray-700 disabled:opacity-50"
                style={{ maxHeight: '80px' }} // Adjusted max height
              />
              <button
                onClick={handleSend}
                aria-label="Enviar mensaje"
                className="bg-purple-600 hover:bg-purple-700 text-white px-5 py-2 rounded-md focus:outline-none focus:ring-1 focus:ring-purple-500 focus:ring-offset-2 focus:ring-offset-gray-900 transition-colors disabled:opacity-50 disabled:cursor-not-allowed h-[42px]"
                disabled={!input.trim() || loading}
              >
                {loading ? (
                  <svg
                    className="animate-spin h-5 w-5 text-white"
                    viewBox="0 0 24 24"
                    fill="none"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
                    />
                  </svg>
                ) : (
                  <FaPaperPlane />
                )}
              </button>
            </div>
          </div>
          </main>

        {/* Right Sidebar (Next to Chat Box) - Now individually styled */}
        <aside className="hidden md:flex flex-col w-64 lg:w-72 bg-gray-800 flex-shrink-0 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-700/50 shadow-xl rounded-lg"> 
          {/* Sidebar Header - Keep rounded top-right */}
          <h2 className="text-lg font-semibold text-purple-400 mb-4 p-4 border-b border-gray-700/50 flex-shrink-0 rounded-tr-lg">Info Rápida</h2>
          
          <div className="space-y-4 p-4 flex-grow">
              {/* Weather Card Placeholder */}
              <div className="bg-gray-700 p-3 rounded-lg shadow">
                <div className="flex items-center mb-2">
                  <FaSun className="text-yellow-400 mr-2 flex-shrink-0" />
                  <h3 className="text-md font-semibold text-gray-200 truncate">Tiempo en BCN</h3>
                </div>
                <p className="text-sm text-gray-400">Soleado, 22°C</p>
                <p className="text-xs text-gray-500 mt-1">Actualizado hace 5 min (simulado)</p>
              </div>

              {/* Featured Event Card Placeholder */}
              <div className="bg-gray-700 p-3 rounded-lg shadow">
                <div className="flex items-center mb-2">
                  <FaCalendarAlt className="text-purple-400 mr-2 flex-shrink-0" />
                  <h3 className="text-md font-semibold text-gray-200 truncate">Evento Destacado</h3>
                </div>
                <p className="text-sm text-gray-300 font-medium">Concierto: Banda X</p>
                <p className="text-sm text-gray-400">Sala Y - Hoy 21:00</p>
                <a href="#" className="text-xs text-purple-400 hover:underline mt-1 block">Más detalles...</a>
              </div>

              {/* Quick Tip Card Placeholder */}
              <div className="bg-gray-700 p-3 rounded-lg shadow">
                <div className="flex items-center mb-2">
                  <FaInfoCircle className="text-blue-400 mr-2 flex-shrink-0" />
                  <h3 className="text-md font-semibold text-gray-200 truncate">Consejo Underground</h3>
                </div>
                <p className="text-sm text-gray-400">Explora las tiendas de discos de segunda mano en Carrer dels Tallers.</p>
              </div>
          </div>
          {/* Ensure bottom-right is rounded if there's no explicit footer inside aside */}
        </aside>
      </div>
    </div>
  );
}


export default ChatPage;

