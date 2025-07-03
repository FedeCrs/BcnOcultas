import React from "react";
import { events, featuredVenues, galleryImages } from "./data";
import { useNavigate } from 'react-router-dom';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col justify-between">
      {/* Fondo */}
      <div className="absolute inset-0 z-0">
        <img
          src="/images/piano.jpg"
          alt="Fondo principal"
          className="w-full h-full object-cover opacity-40"
        />
      </div>

      {/* Contenido */}
      <div className="relative z-10 p-8 space-y-16">
        {/* Cabecera */}
        <div className="text-center">
          <h1 className="text-4xl sm:text-5xl font-bold text-purple-300 mb-4">
            Descubre la escena underground de Barcelona
          </h1>
          <p className="text-lg text-purple-200 mb-6">
            Conciertos alternativos, locales únicos y cultura emergente
          </p>
          <button
            onClick={() => navigate('/chat')}
            className="bg-purple-700 hover:bg-purple-600 text-white font-bold py-2 px-6 rounded-full shadow-lg transition duration-300"
          >
            🤖 Pregúntale a nuestra IA
          </button>
        </div>

        {/* Eventos */}
        <section>
          <h2 className="text-3xl font-semibold text-center text-purple-400 mb-6">
            Próximos eventos
          </h2>
          <div className="space-y-4">
            {events.map((event, index) => (
              <div
                key={index}
                className="bg-gray-800 bg-opacity-60 rounded-lg p-4 text-center"
              >
                <h3 className="text-xl font-bold text-white">{event.title}</h3>
                <p className="text-purple-200">
                  {event.date} – {event.location}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Lugares destacados */}
        <section>
          <h2 className="text-3xl font-semibold text-center text-purple-400 mb-6">
            Lugares destacados
          </h2>
          <div className="space-y-4">
            {featuredVenues.map((venue, index) => (
              <div
                key={index}
                className="bg-gray-800 bg-opacity-70 rounded-lg p-4 text-center"
              >
                <h3 className="text-xl font-bold text-white">{venue.name}</h3>
                <p className="text-purple-200">{venue.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Escena en imágenes */}
        <section className="mb-12">
          <h2 className="text-3xl font-semibold text-center mb-4 text-purple-300">
            Escena en imágenes
          </h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {galleryImages.map((img, index) => (
              <div key={index} className="flex flex-col items-center">
                <img
                  src={img.src}
                  alt={img.caption}
                  className="rounded-lg shadow-md object-cover w-full h-40"
                />
                <p className="text-sm mt-2 text-purple-400 text-center">
                  {img.caption}
                </p>
              </div>
            ))}
          </div>
        </section>
      </div>

      {/* Footer */}
      <footer className="text-center text-purple-500 p-4 text-sm z-10 relative">
        © 2025 BarcelOcultas. Cultura desde las sombras.
      </footer>
    </div>
  );
};

export default LandingPage;
