/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Database, Layers, CheckCircle2, Sliders, Shield } from 'lucide-react';
import { PLANT_CLASSES } from '../data/plantData';

export const DatasetTab: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
        <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 mb-2 block">PlantVillage Dataset & Methodology</span>
        <h2 className="text-3xl font-black text-slate-900 mb-3">Data Pipeline & Class Distribution</h2>
        <p className="text-slate-600 text-sm max-w-3xl leading-relaxed">
          The system is trained on the benchmark PlantVillage dataset, comprising 54,306 expert-verified images across 16 crop species and disease classes.
        </p>
      </div>

      {/* Dataset Specs */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Total Images</span>
          <span className="text-3xl font-extrabold text-slate-900">54,306</span>
          <p className="text-xs text-emerald-600 mt-2 font-medium">16 Balanced Crop Classes</p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Train / Val / Test Split</span>
          <span className="text-3xl font-extrabold text-slate-900">80 / 10 / 10</span>
          <p className="text-xs text-slate-500 mt-2 font-medium">Stratified Random Sampling</p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Image Resolution</span>
          <span className="text-3xl font-extrabold text-slate-900">224 × 224</span>
          <p className="text-xs text-slate-500 mt-2 font-medium">RGB Normalized [0, 1]</p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1">Data Augmentation</span>
          <span className="text-3xl font-extrabold text-slate-900">Robust</span>
          <p className="text-xs text-emerald-600 mt-2 font-medium">Rotation, Zoom, Shear, Flip</p>
        </div>
      </div>

      {/* Class Directory Table */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm">
        <h3 className="text-lg font-bold text-slate-900 mb-4">Configured Plant Species & Disease Classes</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {PLANT_CLASSES.map((cls) => (
            <div key={cls.id} className="bg-slate-50 p-4 rounded-2xl border border-slate-100 flex items-center justify-between">
              <div>
                <span className="text-xs font-bold text-emerald-700 block">{cls.species}</span>
                <span className="text-sm font-semibold text-slate-900">{cls.condition}</span>
              </div>
              <span className={`text-[10px] px-2 py-0.5 rounded-full font-bold ${
                cls.status === 'Healthy' ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'
              }`}>
                {cls.status}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
