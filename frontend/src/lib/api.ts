export const API_BASE_URL = 'http://127.0.0.1:8000';

export interface GenerateResponse {
  filename: string;
  creative_name: string;
  sound_intent: string;
  explanation: string;
  parallel_logic: boolean;
  devices: string[];
  macro_details: MacroDetail[];
  tips: string[];
}

export interface MacroDetail {
  macro: number;
  name: string;
  description: string;
  target_device?: string;
  target_parameter?: string;
}

export const api = {
  getDevices: async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/devices`);
      if (!res.ok) throw new Error('Failed to fetch devices');
      return await res.json();
    } catch (error) {
      console.error('Error fetching devices:', error);
      return {};
    }
  },

  generateRack: async (prompt: string): Promise<GenerateResponse> => {
    const res = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Generation failed');
    }

    return await res.json();
  },

  downloadRack: (filename: string) => {
    // This assumes the backend serves files from /download/{filename}
    // Or we can direct to the exact URL
    window.location.href = `${API_BASE_URL}/download/${filename}`;
  }
};
