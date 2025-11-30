"""Content Reader Service - Reads educational content from markdown files."""

import re
from pathlib import Path
from typing import Optional
from dataclasses import dataclass


@dataclass
class ContentSection:
    """A section of educational content."""
    index: int
    title: str
    content: str
    level: int  # Header level (2 for ##, 3 for ###, etc.)


class ContentReaderService:
    """Service to read and parse educational content from markdown files."""

    # Mapping from backend class numbers to filesystem class numbers
    # Backend uses 0-based (Class 0, 1, 2...), filesystem uses 1-based (Clase 1, 2, 3...)
    CLASS_NUMBER_OFFSET = 1

    # Base path to module content
    BASE_PATH = Path("/home/jarko/proyectos/master-ia-manu")

    # Module directory names
    MODULE_DIRS = {
        0: "Modulo 0 – IA Development Foundations",
        # Add more modules as needed
    }

    def __init__(self):
        """Initialize the content reader service."""
        pass

    def _get_class_path(self, module_number: int, class_number: int) -> Optional[Path]:
        """
        Get the filesystem path for a class markdown file.

        Args:
            module_number: Backend module number (0-based)
            class_number: Backend class number (0-based)

        Returns:
            Path to the markdown file, or None if not found
        """
        module_dir = self.MODULE_DIRS.get(module_number)
        if not module_dir:
            return None

        # Convert backend class number to filesystem class number
        fs_class_number = class_number + self.CLASS_NUMBER_OFFSET

        # Build path
        module_path = self.BASE_PATH / module_dir

        # Find the class directory (format: "Clase X - Title")
        # We need to glob because the title part varies
        class_dirs = list(module_path.glob(f"Clase {fs_class_number} - *"))

        if not class_dirs:
            return None

        class_dir = class_dirs[0]

        # Find the markdown file inside
        md_files = list(class_dir.glob("*.md"))

        if not md_files:
            return None

        # Return the first (and usually only) .md file
        return md_files[0]

    def _parse_sections(self, content: str) -> list[ContentSection]:
        """
        Parse markdown content into sections based on ## headers.

        Args:
            content: Raw markdown content

        Returns:
            List of ContentSection objects
        """
        sections = []

        # Split by ## headers (level 2 only)
        # Pattern: matches ## Header (but not ### or more)
        pattern = r'^(#{2})\s+(.+)$'

        lines = content.split('\n')
        current_section_title = None
        current_section_content = []
        current_section_level = 0
        section_index = 0

        for line in lines:
            match = re.match(pattern, line)

            if match:
                # Save previous section if exists
                if current_section_title:
                    # Filter out "Índice" section - it's just table of contents
                    if current_section_title.lower() != "índice":
                        sections.append(ContentSection(
                            index=section_index,
                            title=current_section_title,
                            content='\n'.join(current_section_content).strip(),
                            level=current_section_level
                        ))
                        section_index += 1

                # Start new section
                header_level = len(match.group(1))
                current_section_title = match.group(2).strip()
                current_section_level = header_level
                current_section_content = [line]  # Include the header in content
            else:
                # Add line to current section
                current_section_content.append(line)

        # Save last section
        if current_section_title:
            # Filter out "Índice" section
            if current_section_title.lower() != "índice":
                sections.append(ContentSection(
                    index=section_index,
                    title=current_section_title,
                    content='\n'.join(current_section_content).strip(),
                    level=current_section_level
                ))

        return sections

    def get_sections_list(self, module_number: int, class_number: int) -> list[dict]:
        """
        Get list of section headers for a class.

        Args:
            module_number: Module number (0-based)
            class_number: Class number (0-based)

        Returns:
            List of section metadata (index, title)
        """
        file_path = self._get_class_path(module_number, class_number)

        if not file_path or not file_path.exists():
            return []

        content = file_path.read_text(encoding='utf-8')
        sections = self._parse_sections(content)

        return [
            {
                "index": section.index,
                "title": section.title,
                "level": section.level
            }
            for section in sections
        ]

    def get_section_content(
        self,
        module_number: int,
        class_number: int,
        section_index: int
    ) -> Optional[dict]:
        """
        Get specific section content.

        Args:
            module_number: Module number (0-based)
            class_number: Class number (0-based)
            section_index: Section index (0-based)

        Returns:
            Section data with content, or None if not found
        """
        file_path = self._get_class_path(module_number, class_number)

        if not file_path or not file_path.exists():
            return None

        content = file_path.read_text(encoding='utf-8')
        sections = self._parse_sections(content)

        if section_index < 0 or section_index >= len(sections):
            return None

        section = sections[section_index]

        return {
            "index": section.index,
            "title": section.title,
            "content": section.content,
            "level": section.level,
            "total_sections": len(sections)
        }

    def get_all_content(self, module_number: int, class_number: int) -> Optional[str]:
        """
        Get full markdown content for a class.

        Args:
            module_number: Module number (0-based)
            class_number: Class number (0-based)

        Returns:
            Full markdown content, or None if not found
        """
        file_path = self._get_class_path(module_number, class_number)

        if not file_path or not file_path.exists():
            return None

        return file_path.read_text(encoding='utf-8')


# Singleton instance
content_reader_service = ContentReaderService()
