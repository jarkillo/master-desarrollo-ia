"""Content routes - Serve educational content from markdown files."""

from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.services.content_reader_service import content_reader_service


router = APIRouter()


class SectionMetadata(BaseModel):
    """Metadata for a content section."""
    index: int
    title: str
    level: int


class SectionContent(BaseModel):
    """Full content for a section."""
    index: int
    title: str
    content: str
    level: int
    total_sections: int


@router.get("/sections", response_model=list[SectionMetadata])
async def get_class_sections(
    module_number: int,
    class_number: int
):
    """
    Get list of section headers for a class.

    Returns section metadata (index, title) for navigation.
    This allows the frontend to show an index or table of contents.
    """
    sections = content_reader_service.get_sections_list(module_number, class_number)

    if not sections:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content not found for Module {module_number}, Class {class_number}"
        )

    return sections


@router.get("/section/{section_index}", response_model=SectionContent)
async def get_section_content(
    module_number: int,
    class_number: int,
    section_index: int
):
    """
    Get specific section content.

    Returns the full markdown content for a single section.
    Frontend can render this with react-markdown.
    """
    section = content_reader_service.get_section_content(
        module_number,
        class_number,
        section_index
    )

    if not section:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Section {section_index} not found for Module {module_number}, Class {class_number}"
        )

    return section


@router.get("/full")
async def get_full_content(
    module_number: int,
    class_number: int
):
    """
    Get full markdown content for a class.

    WARNING: This returns the entire markdown file.
    Only use if you need the complete content.
    Prefer using sections for better UX.
    """
    content = content_reader_service.get_all_content(module_number, class_number)

    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Content not found for Module {module_number}, Class {class_number}"
        )

    return {
        "module_number": module_number,
        "class_number": class_number,
        "content": content
    }
