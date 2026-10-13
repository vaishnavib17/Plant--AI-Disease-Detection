/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { WorkspaceTab } from './components/WorkspaceTab';
import { DatasetTab } from './components/DatasetTab';
import { TrainingTab } from './components/TrainingTab';
import { PredictionResult, PredictionHistoryItem } from './types';

export default function App() {
  const [activeTab, setActiveTab] = useState<string>('workspace');
  const [backendHealthy, setBackendHealthy] = useState<boolean>(false);
  const [history, setHistory] = useState<PredictionHistoryItem[]>([]);

  useEffect(() => {
    // Check FastAPI backend health on mount
    fetch('http://localhost:8000/health')
      .then((res) => {
        if (res.ok) setBackendHealthy(true);
      })
      .catch(() => {
        setBackendHealthy(false);
      });
  }, []);

  const handleNewPrediction = (result: PredictionResult, imageUrl: string) => {
    const newItem: PredictionHistoryItem = {
      ...result,
      filename: `leaf_sample_${Date.now().toString().slice(-4)}.jpg`,
      timestamp: new Date().toLocaleString(),
      imageUrl
    };
    setHistory((prev) => [newItem, ...prev]);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans antialiased selection:bg-emerald-500 selection:text-white">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} backendHealthy={backendHealthy} />

      <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'workspace' && <WorkspaceTab onNewPrediction={handleNewPrediction} />}
        {activeTab === 'dataset' && <DatasetTab />}
        {activeTab === 'training' && <TrainingTab />}
      </main>
    </div>
  );
}
