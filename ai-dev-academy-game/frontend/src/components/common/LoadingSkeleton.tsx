/**
 * LoadingSkeleton - Reusable skeleton loading components
 */
import React from 'react';
import './LoadingSkeleton.css';

interface LoadingSkeletonProps {
  type: 'card' | 'text' | 'circle' | 'module' | 'class';
  count?: number;
}

/**
 * LoadingSkeleton component that displays animated placeholders
 * while content is loading.
 */
export const LoadingSkeleton: React.FC<LoadingSkeletonProps> = ({
  type,
  count = 1,
}) => {
  const renderSkeleton = () => {
    switch (type) {
      case 'card':
        return <CardSkeleton />;
      case 'text':
        return <TextSkeleton />;
      case 'circle':
        return <CircleSkeleton />;
      case 'module':
        return <ModuleSkeleton />;
      case 'class':
        return <ClassSkeleton />;
      default:
        return <TextSkeleton />;
    }
  };

  return (
    <div className="skeleton-container">
      {Array.from({ length: count }).map((_, index) => (
        <React.Fragment key={index}>{renderSkeleton()}</React.Fragment>
      ))}
    </div>
  );
};

/**
 * Card skeleton for module cards
 */
const CardSkeleton: React.FC = () => (
  <div className="skeleton skeleton-card">
    <div className="skeleton skeleton-header"></div>
    <div className="skeleton skeleton-text"></div>
    <div className="skeleton skeleton-text skeleton-text-short"></div>
    <div className="skeleton skeleton-progress-bar"></div>
  </div>
);

/**
 * Text skeleton for text lines
 */
const TextSkeleton: React.FC = () => (
  <div className="skeleton skeleton-text"></div>
);

/**
 * Circle skeleton for avatars
 */
const CircleSkeleton: React.FC = () => (
  <div className="skeleton skeleton-circle"></div>
);

/**
 * Module skeleton for module viewer
 */
const ModuleSkeleton: React.FC = () => (
  <div className="skeleton-module-wrapper">
    {/* Header skeleton */}
    <div className="skeleton-module-header">
      <div className="skeleton skeleton-back-btn"></div>
      <div className="skeleton skeleton-title"></div>
      <div className="skeleton skeleton-text"></div>
      <div className="skeleton skeleton-progress-bar"></div>
    </div>

    {/* Classes list skeleton */}
    <div className="skeleton-classes-section">
      <div className="skeleton skeleton-subtitle"></div>
      <div className="skeleton-classes-list">
        {Array.from({ length: 5 }).map((_, index) => (
          <ClassSkeleton key={index} />
        ))}
      </div>
    </div>
  </div>
);

/**
 * Class skeleton for class items in module viewer
 */
const ClassSkeleton: React.FC = () => (
  <div className="skeleton skeleton-class-card">
    <div className="skeleton-class-badge"></div>
    <div className="skeleton-class-content">
      <div className="skeleton skeleton-class-title"></div>
      <div className="skeleton skeleton-class-meta">
        <div className="skeleton skeleton-badge"></div>
        <div className="skeleton skeleton-badge"></div>
        <div className="skeleton skeleton-badge"></div>
      </div>
      <div className="skeleton skeleton-text"></div>
      <div className="skeleton skeleton-text skeleton-text-short"></div>
    </div>
  </div>
);

/**
 * Dashboard skeleton for initial loading
 */
export const DashboardSkeleton: React.FC = () => (
  <div className="skeleton-dashboard">
    {/* Header */}
    <div className="skeleton-dashboard-header">
      <div className="skeleton-player-info">
        <CircleSkeleton />
        <div className="skeleton-player-details">
          <div className="skeleton skeleton-text"></div>
          <div className="skeleton skeleton-text skeleton-text-short"></div>
        </div>
      </div>
    </div>

    {/* Stats grid */}
    <div className="skeleton-stats-grid">
      {Array.from({ length: 4 }).map((_, index) => (
        <div key={index} className="skeleton skeleton-stat-card">
          <div className="skeleton skeleton-circle skeleton-stat-icon"></div>
          <div className="skeleton skeleton-stat-value"></div>
          <div className="skeleton skeleton-text skeleton-text-short"></div>
        </div>
      ))}
    </div>

    {/* XP Progress */}
    <div className="skeleton skeleton-xp-section">
      <div className="skeleton skeleton-progress-bar"></div>
    </div>

    {/* Modules */}
    <div className="skeleton-modules-section">
      <div className="skeleton skeleton-subtitle"></div>
      <div className="skeleton-modules-grid">
        {Array.from({ length: 6 }).map((_, index) => (
          <CardSkeleton key={index} />
        ))}
      </div>
    </div>
  </div>
);

export default LoadingSkeleton;
