/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { ShieldAlert, Github, BookOpen } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 py-12 border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center space-x-2 text-white font-bold text-lg mb-3">
              <span className="w-3 h-3 rounded-full bg-emerald-500"></span>
              <span>PlantCare AI</span>
            </div>
            <p className="text-sm text-slate-400 leading-relaxed">
              Deep Learning-Based Plant Disease Detection System developed for academic research and agricultural intelligence coursework.
            </p>
          </div>
          <div>
            <h4 className="text-white font-semibold text-sm mb-3 uppercase tracking-wider">Model Architecture</h4>
            <ul className="space-y-2 text-sm">
              <li>EfficientNetB0 (Transfer Learning)</li>
              <li>Custom CNN Baseline (Scratch)</li>
              <li>Grad-CAM Visual Explainability</li>
              <li>PlantVillage Dataset (16 Classes)</li>
            </ul>
          </div>
          <div>
            <h4 className="text-white font-semibold text-sm mb-3 uppercase tracking-wider">Academic Notice</h4>
            <div className="flex items-start space-x-2 text-xs bg-slate-800/80 p-3 rounded-lg border border-slate-700 text-slate-300">
              <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
              <p>
                This system is an academic AI prototype. Predictions should be verified by certified agronomists before implementing agricultural chemical controls.
              </p>
            </div>
          </div>
        </div>
        <div className="border-t border-slate-800 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2026 PlantCare AI Academic Project. All rights reserved.</p>
          <div className="flex space-x-6 mt-4 sm:mt-0">
            <span className="hover:text-slate-300 transition cursor-pointer">FastAPI Backend v1.0</span>
            <span className="hover:text-slate-300 transition cursor-pointer">TensorFlow/Keras</span>
            <span className="hover:text-slate-300 transition cursor-pointer">Privacy Policy</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
