/**
 * Content API - Fetch educational content from markdown files
 */

import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export interface SectionMetadata {
  index: number;
  title: string;
  level: number;
}

export interface SectionContent {
  index: number;
  title: string;
  content: string;
  level: number;
  total_sections: number;
}

/**
 * Get list of section headers for a class
 */
export const getClassSections = async (
  moduleNumber: number,
  classNumber: number
): Promise<SectionMetadata[]> => {
  const response = await axios.get<SectionMetadata[]>(
    `${API_URL}/content/sections`,
    {
      params: {
        module_number: moduleNumber,
        class_number: classNumber,
      },
    }
  );
  return response.data;
};

/**
 * Get specific section content
 */
export const getSectionContent = async (
  moduleNumber: number,
  classNumber: number,
  sectionIndex: number
): Promise<SectionContent> => {
  const response = await axios.get<SectionContent>(
    `${API_URL}/content/section/${sectionIndex}`,
    {
      params: {
        module_number: moduleNumber,
        class_number: classNumber,
      },
    }
  );
  return response.data;
};

/**
 * Get full markdown content for a class (use sparingly)
 */
export const getFullContent = async (
  moduleNumber: number,
  classNumber: number
): Promise<{ content: string }> => {
  const response = await axios.get(
    `${API_URL}/content/full`,
    {
      params: {
        module_number: moduleNumber,
        class_number: classNumber,
      },
    }
  );
  return response.data;
};
