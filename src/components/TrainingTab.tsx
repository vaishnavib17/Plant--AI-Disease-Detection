/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Code2, Terminal, Copy, Check, Play, FileText } from 'lucide-react';

export const TrainingTab: React.FC = () => {
  const [copiedScript, setCopiedScript] = useState<string | null>(null);

  const copyCode = (code: string, name: string) => {
    navigator.clipboard.writeText(code);
    setCopiedScript(name);
    setTimeout(() => setCopiedScript(null), 2000);
  };

  const efficientNetCode = `import tensorflow as tf
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model

base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.4)(x)
predictions = Dense(16, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])`;

  const cnnCode = `import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(16, activation='softmax')
])
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])`;

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
        <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 mb-2 block">Python Deep Learning Pipelines</span>
        <h2 className="text-3xl font-black text-slate-900 mb-3">Model Training & Execution Scripts</h2>
        <p className="text-slate-600 text-sm max-w-3xl leading-relaxed">
          Review the modular Python scripts located in the backend repository for training EfficientNetB0, the Custom CNN baseline, and evaluating model accuracy.
        </p>
      </div>

      {/* Terminal Command Quick Reference */}
      <div className="bg-slate-900 rounded-3xl p-6 text-slate-200 shadow-xl space-y-4">
        <div className="flex items-center space-x-2 text-emerald-400 font-mono text-xs font-bold uppercase tracking-wider">
          <Terminal className="w-4 h-4" />
          <span>Mac Terminal Setup & Training Commands</span>
        </div>
        <div className="bg-slate-950 p-4 rounded-2xl font-mono text-xs space-y-2 border border-slate-800 text-emerald-300 overflow-x-auto">
          <p className="text-slate-400"># 1. Setup virtual environment & dependencies</p>
          <p>cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt</p>
          <p className="text-slate-400 pt-2"># 2. Run EfficientNetB0 Transfer Learning training</p>
          <p>python training/train_efficientnet.py</p>
          <p className="text-slate-400 pt-2"># 3. Run Custom CNN baseline training</p>
          <p>python training/train_cnn.py</p>
          <p className="text-slate-400 pt-2"># 4. Run test evaluation & metrics report</p>
          <p>python training/evaluate.py</p>
        </div>
      </div>

      {/* Code Viewer 1 */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Code2 className="w-5 h-5 text-emerald-600" />
            <h3 className="text-lg font-bold text-slate-900">backend/training/train_efficientnet.py</h3>
          </div>
          <button
            onClick={() => copyCode(efficientNetCode, 'efficientnet')}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition"
          >
            {copiedScript === 'efficientnet' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copiedScript === 'efficientnet' ? 'Copied!' : 'Copy Code'}</span>
          </button>
        </div>
        <pre className="bg-slate-900 text-emerald-400 p-4 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed">
          {efficientNetCode}
        </pre>
      </div>

      {/* Code Viewer 2 */}
      <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Code2 className="w-5 h-5 text-emerald-600" />
            <h3 className="text-lg font-bold text-slate-900">backend/training/train_cnn.py</h3>
          </div>
          <button
            onClick={() => copyCode(cnnCode, 'cnn')}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition"
          >
            {copiedScript === 'cnn' ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copiedScript === 'cnn' ? 'Copied!' : 'Copy Code'}</span>
          </button>
        </div>
        <pre className="bg-slate-900 text-emerald-400 p-4 rounded-2xl text-xs font-mono overflow-x-auto leading-relaxed">
          {cnnCode}
        </pre>
      </div>
    </div>
  );
};
