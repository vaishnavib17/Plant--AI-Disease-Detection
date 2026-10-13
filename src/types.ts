export interface PlantClass {
  id: number;
  name: string;
  species: string;
  condition: string;
  status: 'Healthy' | 'Diseased';
}

export interface Candidate {
  class_name: string;
  species: string;
  condition: string;
  confidence: number;
}

export interface PredictionResult {
  success: boolean;
  predicted_class: string;
  species: string;
  condition: string;
  status: 'Healthy' | 'Diseased';
  confidence: number;
  top_candidates: Candidate[];
  uncertainty_flag: boolean;
  uncertainty_reason?: string;
  inference_time_ms: number;
  model_used: string;
}

export interface PredictionHistoryItem extends PredictionResult {
  filename: string;
  timestamp: string;
  imageUrl?: string;
}

export interface DiseaseInfo {
  species: string;
  condition: string;
  symptoms: string[];
  prevention: string[];
  nextSteps: string[];
  reference: string;
}
