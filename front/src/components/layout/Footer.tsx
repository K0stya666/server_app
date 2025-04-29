import React from 'react';
import { MapPin, Mail, Heart } from 'lucide-react';

const Footer: React.FC = () => {
    return (
        <footer className="bg-gray-800 text-white">
            <div className="container mx-auto px-4 py-8">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    <div>
                        <h3 className="text-xl font-bold mb-4 flex items-center">
                            <MapPin className="h-5 w-5 mr-2" /> TravelPartner
                        </h3>
                        <p className="text-gray-300">
                            Connect with fellow travelers and find your perfect travel companion.
                            Discover new destinations together and create unforgettable memories.
                        </p>
                    </div>

                    <div>
                        <h3 className="text-xl font-bold mb-4">Quick Links</h3>
                        <ul className="space-y-2">
                            <li><a href="/" className="text-gray-300 hover:text-white transition duration-200">Home</a></li>
                            <li><a href="/trips" className="text-gray-300 hover:text-white transition duration-200">Explore Trips</a></li>
                            <li><a href="/about" className="text-gray-300 hover:text-white transition duration-200">About Us</a></li>
                            <li><a href="/contact" className="text-gray-300 hover:text-white transition duration-200">Contact</a></li>
                        </ul>
                    </div>

                    <div>
                        <h3 className="text-xl font-bold mb-4 flex items-center">
                            <Mail className="h-5 w-5 mr-2" /> Stay Connected
                        </h3>
                        <p className="text-gray-300 mb-4">
                            Subscribe to our newsletter for travel tips and updates.
                        </p>
                        <div className="flex">
                            <input
                                type="email"
                                placeholder="Your email"
                                className="px-4 py-2 rounded-l-md focus:outline-none text-gray-800 w-full"
                            />
                            <button className="bg-teal-500 px-4 py-2 rounded-r-md hover:bg-teal-400 transition duration-200">
                                Subscribe
                            </button>
                        </div>
                    </div>
                </div>

                <div className="border-t border-gray-700 mt-8 pt-6 flex flex-col md:flex-row justify-between items-center">
                    <p className="text-gray-400">© 2025 TravelPartner. All rights reserved.</p>
                    <p className="text-gray-400 flex items-center mt-4 md:mt-0">
                        Made with <Heart className="h-4 w-4 mx-1 text-red-400" /> by TravelPartner Team
                    </p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;