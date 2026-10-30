import { useState, useRef, useEffect } from "react";
import { MODEL_GROUPS, getModelById } from "../models";
import "./ModelSelector.css";

const CHEVRON_DOWN = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="6 9 12 15 18 9" />
  </svg>
);

const CHECK_ICON = (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

export default function ModelSelector({
  selectedModel,
  onSelectModel,
  compact = false,
  direction = "down",
}) {
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef(null);

  const active = getModelById(selectedModel);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close dropdown on Escape key
  useEffect(() => {
    function handleKeyDown(e) {
      if (e.key === "Escape") {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener("keydown", handleKeyDown);
      return () => document.removeEventListener("keydown", handleKeyDown);
    }
  }, [isOpen]);

  function handleSelect(modelId) {
    onSelectModel(modelId);
    setIsOpen(false);
  }

  // Find category icon
  const currentGroup = MODEL_GROUPS.find((g) =>
    g.models.some((m) => m.id === selectedModel)
  );

  return (
    <div className={`model-selector-wrapper ${compact ? "compact" : ""}`} ref={containerRef}>
      <button
        type="button"
        className={`model-selector-btn ${isOpen ? "open" : ""}`}
        onClick={() => setIsOpen(!isOpen)}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        title="Select AI Model"
      >
        <span className="model-cat-icon">{currentGroup?.icon || "⚡"}</span>
        <span className="model-active-label">{active.label}</span>
        <span className={`model-chevron ${isOpen ? "rotate" : ""}`}>{CHEVRON_DOWN}</span>
      </button>

      {isOpen && (
        <div
          className={`model-dropdown-menu fade-in ${direction === "up" ? "direction-up" : ""}`}
          role="listbox"
        >

          <div className="model-dropdown-header">
            <span>Select Model</span>
            <span className="model-dropdown-hint">Sent as exact API model</span>
          </div>

          {MODEL_GROUPS.map((group) => (
            <div key={group.category} className="model-group-section">
              <div className="model-group-title">
                <span className="group-icon">{group.icon}</span>
                <span className="group-name">{group.category}</span>
              </div>

              <div className="model-options-list">
                {group.models.map((model) => {
                  const isSelected = model.id === selectedModel;
                  return (
                    <button
                      key={model.id}
                      type="button"
                      className={`model-option-item ${isSelected ? "selected" : ""}`}
                      onClick={() => handleSelect(model.id)}
                      role="option"
                      aria-selected={isSelected}
                    >
                      <div className="model-option-info">
                        <span className="model-option-label">{model.label}</span>
                        {model.tag && (
                          <span className={`model-tag tag-${model.tag.toLowerCase()}`}>
                            {model.tag}
                          </span>
                        )}
                      </div>
                      {isSelected && <span className="model-check-icon">{CHECK_ICON}</span>}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
