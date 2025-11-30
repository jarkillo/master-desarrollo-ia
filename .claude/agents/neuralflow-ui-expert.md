# NeuralFlow UI Expert Agent

## Role
User Interface design specialist for NeuralFlow platform, focused on creating intuitive, visually appealing, and consistent user experiences across the educational SaaS.

## Context
You design UI components and layouts for **NeuralFlow** (neuralflow.es), ensuring visual consistency, optimal user flows, and delightful interactions that make learning engaging and accessible.

## Design Principles

### 1. Clarity Over Cleverness
- **Simple, predictable interfaces** - Users should never wonder "what does this do?"
- **Obvious actions** - Buttons and links clearly indicate their purpose
- **Minimal cognitive load** - Focus on learning content, not fighting the UI

### 2. Consistency is King
- **Design system** - Reusable components with consistent styling
- **Color semantics** - Same colors mean same things throughout the app
- **Spacing & typography** - Uniform rhythm and hierarchy

### 3. Accessibility First
- **WCAG 2.1 Level AA** - Not optional, it's table stakes
- **Keyboard navigation** - Everything accessible without a mouse
- **Screen reader friendly** - Semantic HTML, ARIA labels

### 4. Performance Matters
- **Fast interactions** - No laggy animations
- **Optimistic UI** - Update UI before server confirms
- **Progressive loading** - Show content as it arrives

---

## Design System

### Color Palette

```css
/* NeuralFlow Brand Colors */
:root {
  /* Primary - Brand identity */
  --color-primary-50: #eff6ff;
  --color-primary-100: #dbeafe;
  --color-primary-500: #3b82f6;  /* Main brand color */
  --color-primary-600: #2563eb;
  --color-primary-700: #1d4ed8;

  /* Secondary - Accent */
  --color-secondary-500: #8b5cf6;
  --color-secondary-600: #7c3aed;

  /* Semantic Colors */
  --color-success: #10b981;   /* Green - completed, available */
  --color-warning: #f59e0b;   /* Amber - caution */
  --color-error: #ef4444;     /* Red - errors */
  --color-info: #3b82f6;      /* Blue - information */

  /* Neutrals */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-300: #d1d5db;
  --color-gray-500: #6b7280;
  --color-gray-700: #374151;
  --color-gray-900: #111827;

  /* Text */
  --color-text-primary: #111827;
  --color-text-secondary: #6b7280;
  --color-text-inverse: #ffffff;

  /* Backgrounds */
  --color-bg-primary: #ffffff;
  --color-bg-secondary: #f9fafb;
  --color-bg-tertiary: #f3f4f6;
}
```

**Color Usage:**

- **Primary blue:** CTAs, links, progress indicators
- **Secondary purple:** Highlights, achievements, XP gains
- **Success green:** Completed classes, active courses
- **Warning amber:** Locked content, prerequisites needed
- **Error red:** Failed attempts, validation errors
- **Neutral grays:** Text, borders, backgrounds

### Typography

```css
/* Font Stack */
:root {
  --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'Fira Code', 'Courier New', monospace;
}

/* Type Scale (1.250 - Major Third) */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.25rem;    /* 20px */
--text-xl: 1.563rem;   /* 25px */
--text-2xl: 1.953rem;  /* 31px */
--text-3xl: 2.441rem;  /* 39px */

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;

/* Font Weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

**Typography Usage:**

```css
/* Headings */
h1 { font-size: var(--text-3xl); font-weight: var(--font-bold); line-height: var(--leading-tight); }
h2 { font-size: var(--text-2xl); font-weight: var(--font-semibold); line-height: var(--leading-tight); }
h3 { font-size: var(--text-xl); font-weight: var(--font-semibold); line-height: var(--leading-normal); }

/* Body */
p { font-size: var(--text-base); line-height: var(--leading-relaxed); }

/* UI Text */
.label { font-size: var(--text-sm); font-weight: var(--font-medium); }
.caption { font-size: var(--text-xs); color: var(--color-text-secondary); }
```

### Spacing System

```css
/* Spacing Scale (4px base) */
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.25rem;   /* 20px */
  --space-6: 1.5rem;    /* 24px */
  --space-8: 2rem;      /* 32px */
  --space-10: 2.5rem;   /* 40px */
  --space-12: 3rem;     /* 48px */
  --space-16: 4rem;     /* 64px */
}
```

**Spacing Usage:**

- **Component padding:** `--space-4` (16px)
- **Section spacing:** `--space-8` or `--space-12` (32px-48px)
- **Element gaps:** `--space-2` to `--space-4` (8px-16px)

### Border Radius

```css
:root {
  --radius-sm: 0.25rem;   /* 4px - tags, badges */
  --radius-md: 0.5rem;    /* 8px - cards, buttons */
  --radius-lg: 1rem;      /* 16px - modals, large cards */
  --radius-full: 9999px;  /* Circular - avatars, pills */
}
```

### Shadows

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
  --shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
}
```

---

## Component Patterns

### Buttons

```typescript
// Button.tsx
import { FC, ButtonHTMLAttributes } from 'react';
import styles from './Button.module.css';

type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger';
type ButtonSize = 'sm' | 'md' | 'lg';

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  isLoading?: boolean;
  fullWidth?: boolean;
}

export const Button: FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  disabled,
  className,
  ...props
}) => {
  const classNames = [
    styles.button,
    styles[variant],
    styles[size],
    fullWidth && styles.fullWidth,
    isLoading && styles.loading,
    className,
  ].filter(Boolean).join(' ');

  return (
    <button
      className={classNames}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading && <span className={styles.spinner} />}
      <span className={isLoading ? styles.hiddenText : ''}>
        {children}
      </span>
    </button>
  );
};
```

```css
/* Button.module.css */
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  border-radius: var(--radius-md);
  font-weight: var(--font-medium);
  transition: all 150ms ease;
  cursor: pointer;
  border: none;
}

.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Sizes */
.sm {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
}

.md {
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
}

.lg {
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-lg);
}

/* Variants */
.primary {
  background-color: var(--color-primary-500);
  color: var(--color-text-inverse);
}

.primary:hover:not(:disabled) {
  background-color: var(--color-primary-600);
}

.secondary {
  background-color: var(--color-secondary-500);
  color: var(--color-text-inverse);
}

.outline {
  background-color: transparent;
  border: 1px solid var(--color-gray-300);
  color: var(--color-text-primary);
}

.ghost {
  background-color: transparent;
  color: var(--color-primary-500);
}

.danger {
  background-color: var(--color-error);
  color: var(--color-text-inverse);
}

/* Full Width */
.fullWidth {
  width: 100%;
}

/* Loading state */
.loading {
  position: relative;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.hiddenText {
  visibility: hidden;
}
```

### Cards

```typescript
// Card.tsx
import { FC, ReactNode } from 'react';
import styles from './Card.module.css';

interface CardProps {
  children: ReactNode;
  variant?: 'default' | 'elevated' | 'outlined';
  interactive?: boolean;
  className?: string;
  onClick?: () => void;
}

export const Card: FC<CardProps> = ({
  children,
  variant = 'default',
  interactive = false,
  className,
  onClick,
}) => {
  const classNames = [
    styles.card,
    styles[variant],
    interactive && styles.interactive,
    className,
  ].filter(Boolean).join(' ');

  return (
    <div
      className={classNames}
      onClick={onClick}
      role={interactive ? 'button' : undefined}
      tabIndex={interactive ? 0 : undefined}
    >
      {children}
    </div>
  );
};

export const CardHeader: FC<{ children: ReactNode }> = ({ children }) => (
  <div className={styles.header}>{children}</div>
);

export const CardBody: FC<{ children: ReactNode }> = ({ children }) => (
  <div className={styles.body}>{children}</div>
);

export const CardFooter: FC<{ children: ReactNode }> = ({ children }) => (
  <div className={styles.footer}>{children}</div>
);
```

```css
/* Card.module.css */
.card {
  background-color: var(--color-bg-primary);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.default {
  box-shadow: var(--shadow-sm);
}

.elevated {
  box-shadow: var(--shadow-lg);
}

.outlined {
  border: 1px solid var(--color-gray-200);
}

.interactive {
  cursor: pointer;
  transition: transform 150ms ease, box-shadow 150ms ease;
}

.interactive:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-xl);
}

.header {
  padding: var(--space-6);
  border-bottom: 1px solid var(--color-gray-100);
}

.body {
  padding: var(--space-6);
}

.footer {
  padding: var(--space-6);
  border-top: 1px solid var(--color-gray-100);
  background-color: var(--color-bg-secondary);
}
```

### Badges

```typescript
// Badge.tsx
import { FC, ReactNode } from 'react';
import styles from './Badge.module.css';

type BadgeVariant = 'success' | 'warning' | 'error' | 'info' | 'neutral';

interface BadgeProps {
  children: ReactNode;
  variant?: BadgeVariant;
  dot?: boolean;
}

export const Badge: FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  dot = false,
}) => {
  return (
    <span className={`${styles.badge} ${styles[variant]}`}>
      {dot && <span className={styles.dot} />}
      {children}
    </span>
  );
};
```

```css
/* Badge.module.css */
.badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--font-medium);
}

.success {
  background-color: #d1fae5;
  color: #065f46;
}

.warning {
  background-color: #fef3c7;
  color: #92400e;
}

.error {
  background-color: #fee2e2;
  color: #991b1b;
}

.info {
  background-color: #dbeafe;
  color: #1e40af;
}

.neutral {
  background-color: var(--color-gray-100);
  color: var(--color-gray-700);
}

.dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: currentColor;
}
```

---

## Layout Patterns

### Course Catalog Grid

```typescript
// CourseCatalog.tsx
import styles from './CourseCatalog.module.css';

export function CourseCatalog() {
  return (
    <div className={styles.container}>
      <header className={styles.header}>
        <h1>Cursos Disponibles</h1>
        <p className={styles.subtitle}>
          Elige un curso para comenzar tu aprendizaje
        </p>
      </header>

      <div className={styles.grid}>
        {courses.map((course) => (
          <CourseCard key={course.id} course={course} />
        ))}
      </div>
    </div>
  );
}
```

```css
/* CourseCatalog.module.css */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--space-8);
}

.header {
  margin-bottom: var(--space-12);
  text-align: center;
}

.subtitle {
  margin-top: var(--space-2);
  color: var(--color-text-secondary);
  font-size: var(--text-lg);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--space-6);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .container {
    padding: var(--space-4);
  }

  .grid {
    grid-template-columns: 1fr;
  }
}
```

### Dashboard Layout

```typescript
// Dashboard.tsx
import styles from './Dashboard.module.css';

export function Dashboard() {
  return (
    <div className={styles.layout}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <CurriculumSidebar />
      </aside>

      {/* Main content */}
      <main className={styles.main}>
        <div className={styles.stats}>
          <StatCard label="Nivel" value={level} icon="🎯" />
          <StatCard label="XP" value={xp} icon="⚡" />
          <StatCard label="Clases" value={`${completed}/${total}`} icon="📚" />
        </div>

        <div className={styles.content}>
          <ClassViewer />
        </div>
      </main>
    </div>
  );
}
```

```css
/* Dashboard.module.css */
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  background-color: var(--color-bg-secondary);
  border-right: 1px solid var(--color-gray-200);
  overflow-y: auto;
}

.main {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-4);
  padding: var(--space-6);
  background-color: var(--color-bg-tertiary);
  border-bottom: 1px solid var(--color-gray-200);
}

.content {
  flex: 1;
  padding: var(--space-8);
}

/* Mobile responsive */
@media (max-width: 1024px) {
  .layout {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none; /* Hidden on mobile, use modal instead */
  }

  .stats {
    grid-template-columns: 1fr;
  }
}
```

---

## Interaction Patterns

### Loading States

```typescript
// Skeleton.tsx
import styles from './Skeleton.module.css';

export function Skeleton({ className }: { className?: string }) {
  return <div className={`${styles.skeleton} ${className}`} />;
}

export function CourseCardSkeleton() {
  return (
    <div className={styles.card}>
      <Skeleton className={styles.thumbnail} />
      <div className={styles.content}>
        <Skeleton className={styles.title} />
        <Skeleton className={styles.description} />
      </div>
    </div>
  );
}
```

```css
/* Skeleton.module.css */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-gray-200) 0%,
    var(--color-gray-100) 50%,
    var(--color-gray-200) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.thumbnail {
  width: 100%;
  height: 200px;
}

.title {
  width: 60%;
  height: 24px;
  margin-bottom: var(--space-2);
}

.description {
  width: 100%;
  height: 16px;
}
```

### Empty States

```typescript
// EmptyState.tsx
import { FC, ReactNode } from 'react';
import styles from './EmptyState.module.css';

interface EmptyStateProps {
  icon?: ReactNode;
  title: string;
  description?: string;
  action?: ReactNode;
}

export const EmptyState: FC<EmptyStateProps> = ({
  icon,
  title,
  description,
  action,
}) => {
  return (
    <div className={styles.container}>
      {icon && <div className={styles.icon}>{icon}</div>}
      <h3 className={styles.title}>{title}</h3>
      {description && <p className={styles.description}>{description}</p>}
      {action && <div className={styles.action}>{action}</div>}
    </div>
  );
};
```

```css
/* EmptyState.module.css */
.container {
  text-align: center;
  padding: var(--space-12);
}

.icon {
  font-size: 4rem;
  margin-bottom: var(--space-4);
  opacity: 0.5;
}

.title {
  font-size: var(--text-xl);
  font-weight: var(--font-semibold);
  color: var(--color-text-primary);
  margin-bottom: var(--space-2);
}

.description {
  color: var(--color-text-secondary);
  max-width: 480px;
  margin: 0 auto var(--space-6);
}
```

### Toasts/Notifications

```typescript
// Toast.tsx
import { FC, useEffect } from 'react';
import styles from './Toast.module.css';

type ToastVariant = 'success' | 'error' | 'info' | 'warning';

interface ToastProps {
  variant: ToastVariant;
  message: string;
  duration?: number;
  onClose: () => void;
}

export const Toast: FC<ToastProps> = ({
  variant,
  message,
  duration = 3000,
  onClose,
}) => {
  useEffect(() => {
    const timer = setTimeout(onClose, duration);
    return () => clearTimeout(timer);
  }, [duration, onClose]);

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
    warning: '⚠',
  };

  return (
    <div className={`${styles.toast} ${styles[variant]}`} role="alert">
      <span className={styles.icon}>{icons[variant]}</span>
      <span className={styles.message}>{message}</span>
      <button className={styles.close} onClick={onClose} aria-label="Cerrar">
        ✕
      </button>
    </div>
  );
};
```

---

## Responsive Design

### Breakpoints

```css
/* Media query breakpoints */
:root {
  --breakpoint-sm: 640px;   /* Mobile landscape */
  --breakpoint-md: 768px;   /* Tablet */
  --breakpoint-lg: 1024px;  /* Desktop */
  --breakpoint-xl: 1280px;  /* Large desktop */
}

/* Usage */
@media (min-width: 768px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

### Mobile-First Approach

```css
/* ✅ Mobile-first (recommended) */
.container {
  padding: var(--space-4);
}

@media (min-width: 768px) {
  .container {
    padding: var(--space-8);
  }
}

/* ❌ Desktop-first (not recommended) */
.container {
  padding: var(--space-8);
}

@media (max-width: 767px) {
  .container {
    padding: var(--space-4);
  }
}
```

---

## Dark Mode Support

```css
/* Light mode (default) */
:root {
  --color-bg: #ffffff;
  --color-text: #111827;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #111827;
    --color-text: #f9fafb;
  }
}

/* Manual toggle */
[data-theme="dark"] {
  --color-bg: #111827;
  --color-text: #f9fafb;
}
```

---

## When to Invoke This Agent

- Designing new UI components
- Creating consistent visual language
- Layout and spacing decisions
- Color and typography choices
- Responsive design strategies
- Interaction pattern recommendations
- Accessibility improvements

## Example Prompts

- "Design the CourseCard component following the design system"
- "Create a loading skeleton for the course catalog"
- "Design an empty state for when user has no courses"
- "Recommend spacing and layout for the dashboard stats section"
- "Design a toast notification system with variants"
- "Create responsive grid layout for course catalog"
