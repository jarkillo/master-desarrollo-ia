/**
 * ClassContentViewer - Display educational content section by section
 */

import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import remarkEmoji from 'remark-emoji';
import { ChevronLeft, ChevronRight, BookOpen, List } from 'lucide-react';
import { getSectionContent, getClassSections, SectionMetadata, SectionContent } from '../../services/contentApi';

interface ClassContentViewerProps {
  moduleNumber: number;
  classNumber: number;
  onReadingProgress?: (current: number, total: number) => void;
}

const ClassContentViewer: React.FC<ClassContentViewerProps> = ({
  moduleNumber,
  classNumber,
  onReadingProgress,
}) => {
  const [sections, setSections] = useState<SectionMetadata[]>([]);
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [currentSection, setCurrentSection] = useState<SectionContent | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showSectionList, setShowSectionList] = useState(false);
  const [viewedSections, setViewedSections] = useState<Set<number>>(new Set([0]));

  // Load section list on mount and reset viewed sections when class changes
  useEffect(() => {
    const loadSections = async () => {
      try {
        setLoading(true);
        setError(null);

        // Reset viewed sections for new class
        setViewedSections(new Set([0])); // Start with first section viewed

        const sectionList = await getClassSections(moduleNumber, classNumber);
        setSections(sectionList);

        // Load first section by default
        if (sectionList.length > 0) {
          const firstSection = await getSectionContent(moduleNumber, classNumber, 0);
          setCurrentSection(firstSection);
          setCurrentSectionIndex(0);

          // Notify parent of initial progress
          if (onReadingProgress) {
            onReadingProgress(1, sectionList.length);
          }
        }
      } catch (err) {
        console.error('Error loading sections:', err);
        setError('No se pudo cargar el contenido de la clase');
      } finally {
        setLoading(false);
      }
    };

    loadSections();
  }, [moduleNumber, classNumber]);

  // Load specific section
  const loadSection = async (sectionIndex: number) => {
    try {
      setLoading(true);
      const section = await getSectionContent(moduleNumber, classNumber, sectionIndex);
      setCurrentSection(section);
      setCurrentSectionIndex(sectionIndex);
      setShowSectionList(false); // Close section list after selection

      // Track viewed sections
      setViewedSections((prev) => {
        const newSet = new Set(prev);
        newSet.add(sectionIndex);

        // Notify parent of reading progress
        if (onReadingProgress) {
          onReadingProgress(newSet.size, sections.length);
        }

        return newSet;
      });

      // Scroll to top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error('Error loading section:', err);
      setError('No se pudo cargar la sección');
    } finally {
      setLoading(false);
    }
  };

  const goToPreviousSection = () => {
    if (currentSectionIndex > 0) {
      loadSection(currentSectionIndex - 1);
    }
  };

  const goToNextSection = () => {
    if (currentSectionIndex < sections.length - 1) {
      loadSection(currentSectionIndex + 1);
    }
  };

  if (loading && !currentSection) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Cargando contenido...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-500 rounded-lg p-6 text-center">
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  if (!currentSection || sections.length === 0) {
    return (
      <div className="bg-yellow-900/20 border border-yellow-500 rounded-lg p-6 text-center">
        <p className="text-yellow-400">No hay contenido disponible para esta clase</p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Header with section navigation */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-700 rounded-lg p-4 border border-gray-200 dark:border-gray-600">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-3">
            <BookOpen className="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Sección {currentSectionIndex + 1} de {sections.length}
              </p>
              <h3 className="text-gray-900 dark:text-white font-semibold">{currentSection.title}</h3>
            </div>
          </div>

          {/* Section list toggle */}
          <button
            onClick={() => setShowSectionList(!showSectionList)}
            className="flex items-center space-x-2 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors shadow-sm"
          >
            <List className="w-4 h-4" />
            <span className="text-sm">Índice</span>
          </button>
        </div>

        {/* Reading progress bar */}
        <div className="space-y-1">
          <div className="flex items-center justify-between text-xs text-gray-600 dark:text-gray-400">
            <span>Progreso de lectura</span>
            <span className="font-medium">{viewedSections.size} / {sections.length} secciones leídas</span>
          </div>
          <div className="h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 transition-all duration-500"
              style={{ width: `${(viewedSections.size / sections.length) * 100}%` }}
            />
          </div>
        </div>
      </div>

      {/* Section list dropdown */}
      {showSectionList && (
        <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden shadow-lg">
          <div className="p-4 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900">
            <h4 className="font-semibold text-gray-900 dark:text-white">Contenido de la clase</h4>
          </div>
          <div className="max-h-96 overflow-y-auto">
            {sections.map((section, index) => (
              <button
                key={index}
                onClick={() => loadSection(index)}
                className={`w-full text-left px-4 py-3 border-b border-gray-100 dark:border-gray-700 hover:bg-blue-50 dark:hover:bg-gray-700/50 transition-colors ${
                  index === currentSectionIndex ? 'bg-blue-100 dark:bg-blue-900/30 border-l-4 border-l-blue-600' : ''
                }`}
              >
                <div className="flex items-start space-x-3">
                  <span className="text-gray-500 dark:text-gray-400 font-mono text-sm">{index + 1}.</span>
                  <span className={index === currentSectionIndex ? 'text-blue-700 dark:text-blue-400 font-semibold' : 'text-gray-700 dark:text-gray-300'}>
                    {section.title}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Markdown content */}
      <div className="bg-white dark:bg-gray-800/30 rounded-lg p-6 border border-gray-200 dark:border-gray-700">
        <article className="prose dark:prose-invert prose-blue max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm, remarkEmoji]}
            components={{
              // Custom styling for markdown elements
              h1: ({ children }) => (
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-300 dark:border-gray-700 pb-2">
                  {children}
                </h1>
              ),
              h2: ({ children }) => (
                <h2 className="text-2xl font-bold text-blue-600 dark:text-blue-400 mt-6 mb-3">
                  {children}
                </h2>
              ),
              h3: ({ children }) => (
                <h3 className="text-xl font-semibold text-blue-700 dark:text-blue-300 mt-4 mb-2">
                  {children}
                </h3>
              ),
              h4: ({ children }) => (
                <h4 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mt-3 mb-2">
                  {children}
                </h4>
              ),
              p: ({ children }) => (
                <p className="text-gray-700 dark:text-gray-300 leading-relaxed mb-4 whitespace-pre-wrap">
                  {children}
                </p>
              ),
              strong: ({ children }) => (
                <strong className="font-bold text-gray-900 dark:text-white">
                  {children}
                </strong>
              ),
              em: ({ children }) => (
                <em className="italic text-gray-700 dark:text-gray-300">
                  {children}
                </em>
              ),
              ul: ({ children }) => (
                <ul className="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-2 mb-4">
                  {children}
                </ul>
              ),
              ol: ({ children }) => (
                <ol className="list-decimal list-inside text-gray-700 dark:text-gray-300 space-y-2 mb-4">
                  {children}
                </ol>
              ),
              li: ({ children }) => (
                <li className="text-gray-700 dark:text-gray-300 ml-4">
                  {children}
                </li>
              ),
              code: ({ inline, children }: any) =>
                inline ? (
                  <code className="bg-gray-100 dark:bg-gray-900 px-2 py-1 rounded text-blue-600 dark:text-blue-400 font-mono text-sm">
                    {children}
                  </code>
                ) : (
                  <code className="block bg-gray-100 dark:bg-gray-900 p-4 rounded-lg text-green-700 dark:text-green-400 font-mono text-sm overflow-x-auto mb-4">
                    {children}
                  </code>
                ),
              pre: ({ children }) => (
                <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-x-auto mb-4">
                  {children}
                </pre>
              ),
              blockquote: ({ children }) => (
                <blockquote className="border-l-4 border-blue-500 pl-4 italic text-gray-600 dark:text-gray-400 my-4">
                  {children}
                </blockquote>
              ),
              table: ({ children }) => (
                <div className="overflow-x-auto mb-4">
                  <table className="min-w-full border border-gray-300 dark:border-gray-700">
                    {children}
                  </table>
                </div>
              ),
              th: ({ children }) => (
                <th className="border border-gray-300 dark:border-gray-700 px-4 py-2 bg-gray-100 dark:bg-gray-800 text-left text-gray-700 dark:text-gray-300 font-semibold">
                  {children}
                </th>
              ),
              td: ({ children }) => (
                <td className="border border-gray-300 dark:border-gray-700 px-4 py-2 text-gray-700 dark:text-gray-300">
                  {children}
                </td>
              ),
              a: ({ children, href }) => (
                <a
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 underline"
                >
                  {children}
                </a>
              ),
            }}
          >
            {currentSection.content}
          </ReactMarkdown>
        </article>
      </div>

      {/* Navigation buttons */}
      <div className="flex items-center justify-between">
        <button
          onClick={goToPreviousSection}
          disabled={currentSectionIndex === 0}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors shadow-sm ${
            currentSectionIndex === 0
              ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          <ChevronLeft className="w-5 h-5" />
          <span>Anterior</span>
        </button>

        <div className="text-sm text-gray-600 dark:text-gray-400 font-medium">
          Sección {currentSectionIndex + 1} de {sections.length}
        </div>

        <button
          onClick={goToNextSection}
          disabled={currentSectionIndex >= sections.length - 1}
          className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-colors shadow-sm ${
            currentSectionIndex >= sections.length - 1
              ? 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
              : 'bg-blue-600 hover:bg-blue-700 text-white'
          }`}
        >
          <span>Siguiente</span>
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ClassContentViewer;
