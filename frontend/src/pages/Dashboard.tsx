import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Mock Types (to be replaced by shared types in Phase 12)
interface ProbabilityPoint {
  lat: number;
  lon: number;
  probability: number;
  confidence: string;
}

interface RiskRegion {
  region_id: string;
  coords: number[][];
  avg_probability: number;
  confidence: string;
}

const VAJRADashboard = () => {
  const [leadTime, setLeadTime] = useState(5);
  const [selectedVariable, setSelectedVariable] = useState('temperature');
  const [points, setPoints] = useState<ProbabilityPoint[]>([]);
  const [regions, setRegions] = useState<RiskRegion[]>([]);
  const [selectedRegion, setSelectedRegion] = useState<ProbabilityPoint | null>(null);

  // Fetch data from Backend API
  useEffect(() => {
    const fetchData = async () => {
      try {
        // In real implementation: fetch(`/api/bust-probability?lead_time=${leadTime}&variable=${selectedVariable}`)
        // For now, simulating the API response
        const mockPoints: ProbabilityPoint[] = [
          { lat: 20.0, lon: 75.0, probability: 0.2, confidence: 'HIGH' },
          { lat: 25.0, lon: 80.0, probability: 0.8, confidence: 'LOW' },
          { lat: 15.0, lon: 70.0, probability: 0.5, confidence: 'MEDIUM' },
        ];
        setPoints(mockPoints);

        const mockRegions: RiskRegion[] = [
          { region_id: 'central_india_1', coords: [[24, 79], [26, 81]], avg_probability: 0.75, confidence: 'LOW' }
        ];
        setRegions(mockRegions);
      } catch (error) {
        console.error('Error fetching VAJRA data:', error);
      }
    };
    fetchData();
  }, [leadTime, selectedVariable]);

  const getColor = (prob: number) => {
    if (prob > 0.7) return '#EF4444'; // Red - Low Confidence
    if (prob > 0.3) return '#F59E0B'; // Amber - Medium Confidence
    return '#10B981'; // Green - High Confidence
  };

  return (
    <div className="min-h-screen bg-[#0A0F1E] text-[#E2E8F0] font-sans">
      {/* Header */}
      <header className="h-16 bg-[#161B2D] border-b border-slate-800 flex items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <h1 className="text-xl font-bold tracking-tight text-cyan-400">VAJRA</h1>
          <span className="text-xs bg-slate-800 px-2 py-1 rounded text-slate-400">Forecast Cycle: 2026-10-02 00Z</span>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 text-xs">
            <div className="w-2 h-2 rounded-full bg-green-500"></div>
            <span className="text-slate-400">Data Status: Syncing</span>
          </div>
        </div>
      </header>

      <div className="flex h-[calc(100vh-64px)]">
        {/* Sidebar Controls */}
        <aside className="w-72 bg-[#161B2D] border-r border-slate-800 p-6 flex flex-col gap-8">
          <div>
            <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Lead Time</label>
            <div className="grid grid-cols-5 gap-2 mt-3">
              {[...Array(10)].map((_, i) => (
                <button
                  key={i}
                  onClick={() => setLeadTime(i + 1)}
                  className={`py-1 text-xs rounded border ${leadTime === i + 1 ? 'bg-cyan-600 border-cyan-500 text-white' : 'bg-slate-800 border-slate-700 text-slate-400 hover:bg-slate-700'}`}
                >
                  D{i + 1}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Variable</label>
            <select
              value={selectedVariable}
              onChange={(e) => setSelectedVariable(e.target.value)}
              className="w-full mt-3 bg-slate-800 border border-slate-700 rounded p-2 text-sm text-slate-200 outline-none"
            >
              <option value="temperature">Temperature</option>
              <option value="precipitation">Precipitation</option>
              <option value="wind">Wind Speed</option>
            </select>
          </div>
        </aside>

        {/* Main Intelligence Map */}
        <main className="flex-1 relative">
          <div className="absolute inset-0 z-0">
             {/* In a real Next.js app, <MapContainer> would go here */}
             <div className="w-full h-full bg-[#0D1224] flex items-center justify-center text-slate-600 italic">
                [Mapbox / Leaflet Integration: Rendering Indian Domain Heatmap]
             </div>
          </div>

          {/* Overlaying simulation of points since MapContainer is not rendered in this text environment */}
          <div className="absolute inset-0 pointer-events-none">
             {points.map((p, i) => (
               <div
                key={i}
                onClick={() => setSelectedRegion(p)}
                className="absolute pointer-events-auto cursor-pointer rounded-full transition-transform hover:scale-125"
                style={{
                    left: `${(p.lon - 68) * 5}%`, // Simple projection for demo
                    top: `${(38 - p.lat) * 5}%`,
                    width: '12px',
                    height: '12px',
                    backgroundColor: getColor(p.probability),
                    boxShadow: `0 0 10px ${getColor(p.probability)}`
                }}
               />
             ))}
          </div>
        </main>
      </div>

      {/* Bottom Intelligence Panel */}
      {selectedRegion && (
        <div className="fixed bottom-0 left-0 right-0 h-64 bg-[#161B2D] border-t border-slate-800 p-6 grid grid-cols-3 gap-8 animate-slide-up">
          <div className="flex flex-col justify-center border-r border-slate-800">
            <span className="text-xs text-slate-500 uppercase">Bust Probability</span>
            <div className="flex items-baseline gap-2">
              <span className="text-4xl font-mono font-bold" style={{ color: getColor(selectedRegion.probability) }}>
                {(selectedRegion.probability * 100).toFixed(0)}%
              </span>
              <span className={`text-sm font-bold px-2 py-0.5 rounded ${
                selectedRegion.confidence === 'LOW' ? 'bg-red-900 text-red-200' :
                selectedRegion.confidence === 'MEDIUM' ? 'bg-amber-900 text-amber-200' : 'bg-green-900 text-green-200'
              }`}>
                {selectedRegion.confidence}
              </span>
            </div>
            <span className="text-sm text-slate-400 mt-1">Lead Time: Day {leadTime}</span>
          </div>

          <div className="border-r border-slate-800">
            <span className="text-xs text-slate-500 uppercase mb-3 block">Explainability (The "Why")</span>
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-slate-300">Ensemble Spread</span>
                <span className="text-red-400 font-mono">High ↑</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-300">Historical Analogue Error</span>
                <span className="text-amber-400 font-mono">Medium →</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-slate-300">Atmospheric Gradient</span>
                <span className="text-green-400 font-mono">Low ↓</span>
              </div>
            </div>
          </div>

          <div>
            <span className="text-xs text-slate-500 uppercase mb-3 block">Historical Analogues</span>
            <div className="space-y-2">
              {[
                { sim: 0.94, out: 'BUST' },
                { sim: 0.88, out: 'NO_BUST' },
                { sim: 0.81, out: 'BUST' },
              ].map((a, i) => (
                <div key={i} className="flex justify-between text-xs p-2 bg-slate-800 rounded">
                  <span className="text-slate-400">Case {i+1} (Sim: {(a.sim * 100).toFixed or 0}%)</span>
                  <span className={`font-bold ${a.out === 'BUST' ? 'text-red-400' : 'text-green-400'}`}>{a.out}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default VAJRADashboard;
