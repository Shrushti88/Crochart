import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  RotateCcw,
  Sparkles,
  Zap
} from 'lucide-react';

interface PlaybackControlsProps {
  totalSteps: number;
  currentStep: number;
  onStepChange: React.Dispatch<React.SetStateAction<number>>;
  isPlaying: boolean;
  onTogglePlay: () => void;
  activeRound?: number;
  activeStitchType?: string;
}

export const PlaybackControls: React.FC<PlaybackControlsProps> = ({
  totalSteps,
  currentStep,
  onStepChange,
  isPlaying,
  onTogglePlay,
  activeRound,
  activeStitchType
}) => {
  const [speed, setSpeed] = useState<number>(150); // ms per step
  const timerRef = useRef<number | null>(null);

  useEffect(() => {
    if (isPlaying) {
      timerRef.current = window.setInterval(() => {
        onStepChange(prev => {
          if (prev >= totalSteps - 1) {
            onTogglePlay(); // stop at end
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    } else {
      if (timerRef.current) clearInterval(timerRef.current);
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isPlaying, speed, totalSteps, onStepChange, onTogglePlay]);

  if (totalSteps <= 0) return null;

  const progressPercent = totalSteps > 1 ? Math.min(100, Math.round(((currentStep + 1) / totalSteps) * 100)) : 100;

  return (
    <div className="playback-controls-bar">
      <div className="playback-main">
        {/* Playback action buttons */}
        <div className="playback-btn-group">
          <button
            className="ctrl-btn"
            onClick={() => onStepChange(0)}
            title="Jump to Start"
          >
            <RotateCcw size={14} />
          </button>
          <button
            className="ctrl-btn"
            onClick={() => onStepChange(Math.max(0, currentStep - 1))}
            disabled={currentStep <= 0}
            title="Previous Stitch"
          >
            <SkipBack size={14} />
          </button>
          <button
            className={`ctrl-btn play-toggle-btn ${isPlaying ? 'playing' : ''}`}
            onClick={onTogglePlay}
            title={isPlaying ? 'Pause Animation' : 'Play Stitch Animation'}
          >
            {isPlaying ? <Pause size={16} /> : <Play size={16} />}
          </button>
          <button
            className="ctrl-btn"
            onClick={() => onStepChange(Math.min(totalSteps - 1, currentStep + 1))}
            disabled={currentStep >= totalSteps - 1}
            title="Next Stitch"
          >
            <SkipForward size={14} />
          </button>
        </div>

        {/* Progress Slider */}
        <div className="playback-slider-wrap">
          <div className="playback-info-text">
            <span className="step-count">
              Stitch <strong>{currentStep + 1}</strong> of <strong>{totalSteps}</strong> ({progressPercent}%)
            </span>
            {activeRound && (
              <span className="current-round-badge">
                Round {activeRound} {activeStitchType ? `• ${activeStitchType.toUpperCase()}` : ''}
              </span>
            )}
          </div>
          <input
            type="range"
            min="0"
            max={totalSteps - 1}
            value={currentStep}
            onChange={e => onStepChange(parseInt(e.target.value, 10))}
            className="playback-range-slider"
          />
        </div>

        {/* Speed presets */}
        <div className="playback-speed-group">
          <Zap size={14} className="speed-icon" />
          <button
            className={`speed-pill ${speed === 350 ? 'active' : ''}`}
            onClick={() => setSpeed(350)}
          >
            0.5x
          </button>
          <button
            className={`speed-pill ${speed === 150 ? 'active' : ''}`}
            onClick={() => setSpeed(150)}
          >
            1x
          </button>
          <button
            className={`speed-pill ${speed === 60 ? 'active' : ''}`}
            onClick={() => setSpeed(60)}
          >
            2.5x
          </button>
        </div>
      </div>
    </div>
  );
};
