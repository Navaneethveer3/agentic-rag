// Model configurations for Atlas Agent
// Grouped by capability: Faster response vs More reasoning but effective
// Labels strictly omit hyphens as requested

export const MODEL_GROUPS = [
  {
    category: "Faster response",
    icon: "⚡",
    description: "Ultra-fast latency and prompt answers",
    models: [
      {
        id: "gemini-3-preview-flash",
        label: "gemini 3 flash",
        tag: "Speed",
      },
      {
        id: "gemini-3.1-flash-lite",
        label: "gemini 3.1 flash lite",
        tag: "Lite",
      },
      {
        id: "gemini-3.5-flash-lite",
        label: "gemini 3.5 flash lite",
        tag: "Lite",
      },
      {
        id: "gemini-2.5-flash-lite",
        label: "gemini 2.5 flash lite",
        tag: "Lite",
      },
    ],
  },
  {
    category: "More reasoning but effective",
    icon: "🧠",
    description: "Deep multi-step reasoning and contextual analysis",
    models: [
      {
        id: "gemini-3.5-flash",
        label: "gemini 3.5 flash",
        tag: "Balanced",
      },
      {
        id: "gemini-3.6-flash",
        label: "gemini 3.6 flash",
        tag: "Reasoning",
      },
      {
        id: "gemini-3.7-flash",
        label: "gemini 3.7 flash",
        tag: "Advanced",
      },
      {
        id: "gemini-3.8-flash",
        label: "gemini 3.8 flash",
        tag: "Flagship",
      },
    ],
  },
];

export const ALL_MODELS = MODEL_GROUPS.flatMap((group) => group.models);

export const DEFAULT_MODEL_ID = "gemini-3-flash-preview";

export function getModelById(id) {
  return ALL_MODELS.find((m) => m.id === id) || ALL_MODELS[0];
}
