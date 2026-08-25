import React, { useState } from 'react';
import { SamplePattern } from '../../types';
import {
  X,
  Sparkles,
  BookOpen,
  Tag,
  CircleDot,
  Grid,
  Layers,
  Search,
  Check
} from 'lucide-react';

interface SampleGalleryProps {
  isOpen: boolean;
  onClose: () => void;
  samples: SamplePattern[];
  onSelectSample: (sample: SamplePattern) => void;
}

export const SampleGallery: React.FC<SampleGalleryProps> = ({
  isOpen,
  onClose,
  samples,
  onSelectSample
}) => {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');

  if (!isOpen) return null;

  const categories = [
    { id: 'all', label: 'All Patterns' },
    { id: 'amigurumi', label: 'Amigurumi 3D' },
    { id: 'flat_motif', label: 'Granny & Squares' },
    { id: 'mandala', label: 'Mandalas & Doilies' },
    { id: 'row_fabric', label: 'Linear & Scarves' },
    { id: 'flower', label: 'Flowers & Motifs' }
  ];

  const filteredSamples = samples.filter(sample => {
    const matchesCat = selectedCategory === 'all' || sample.category === selectedCategory;
    const matchesSearch =
      searchQuery === '' ||
      sample.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sample.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      sample.tags?.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchesCat && matchesSearch;
  });

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-content gallery-modal" onClick={e => e.stopPropagation()}>
        {/* Modal Header */}
        <div className="modal-header">
          <div className="modal-title-wrap">
            <Sparkles size={20} className="text-primary" />
            <h2>Pattern Preset Library</h2>
          </div>
          <button className="modal-close-btn" onClick={onClose}>
            <X size={18} />
          </button>
        </div>

        {/* Search & Category Filter Bar */}
        <div className="gallery-filter-bar">
          <div className="search-box">
            <Search size={15} />
            <input
              type="text"
              placeholder="Search patterns, tags, techniques..."
              value={searchQuery}
              onChange={e => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="category-pills-row">
            {categories.map(cat => (
              <button
                key={cat.id}
                className={`cat-pill ${selectedCategory === cat.id ? 'active' : ''}`}
                onClick={() => setSelectedCategory(cat.id)}
              >
                {cat.label}
              </button>
            ))}
          </div>
        </div>

        {/* Gallery Grid */}
        <div className="gallery-cards-grid">
          {filteredSamples.length === 0 ? (
            <div className="gallery-empty">
              <BookOpen size={36} />
              <p>No matching patterns found for your search.</p>
            </div>
          ) : (
            filteredSamples.map(sample => (
              <div
                key={sample.id}
                className="pattern-card"
                onClick={() => {
                  onSelectSample(sample);
                  onClose();
                }}
              >
                <div className="pattern-card-header">
                  <span className={`difficulty-badge ${sample.difficulty}`}>
                    {sample.difficulty}
                  </span>
                  <span className="type-badge">
                    {sample.is_circular ? <CircleDot size={11} /> : <Grid size={11} />}
                    {sample.is_circular ? 'Circular' : 'Row-by-Row'}
                  </span>
                </div>

                <h3 className="pattern-title">{sample.title}</h3>
                <p className="pattern-desc">{sample.description}</p>

                <div className="pattern-tags">
                  {sample.tags?.slice(0, 3).map((tag, i) => (
                    <span key={i} className="tag-chip">
                      #{tag}
                    </span>
                  ))}
                </div>

                <div className="pattern-card-footer">
                  <span className="terminology-label">{sample.terminology} Terminology</span>
                  <button className="load-btn">
                    <span>Load Pattern</span>
                    <Check size={14} />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
