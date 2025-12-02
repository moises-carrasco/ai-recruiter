"""
File handling utilities for CV and Job Description uploads.
"""

import os
import shutil
from datetime import datetime
from typing import Optional, Tuple
from pathlib import Path
from fastapi import UploadFile, HTTPException
from ..core.config import settings


class FileHandler:
    """Handles file operations for interview uploads."""

    # Allowed file types (.txt and .md files)
    ALLOWED_EXTENSIONS = {'.txt', '.md'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def get_upload_dir(cls) -> Path:
        """Get the upload directory path."""
        try:
            # Use absolute path based on project root
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent.parent  # Go up to project root
            upload_dir_name = getattr(settings, 'UPLOAD_DIR', 'uploads')
            upload_dir = project_root / upload_dir_name

            # Ensure directory exists
            upload_dir.mkdir(parents=True, exist_ok=True)
            print(f"DEBUG: Upload directory created/verified at: {upload_dir}")
            return upload_dir
        except Exception as e:
            print(f"ERROR: Failed to create upload directory: {e}")
            # Fallback to current directory
            fallback_dir = Path.cwd() / "uploads"
            fallback_dir.mkdir(parents=True, exist_ok=True)
            print(f"DEBUG: Using fallback upload directory: {fallback_dir}")
            return fallback_dir

    @classmethod
    def validate_file(cls, file: UploadFile) -> None:
        """Validate uploaded file type and size."""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Only .txt and .md files are allowed. Got: {file_ext}"
            )

        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Seek back to beginning

        if file_size > cls.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum allowed size of {cls.MAX_FILE_SIZE / (1024*1024)}MB"
            )

    @classmethod
    def generate_cv_filename(cls, candidate_id: int, interview_id: int, extension: str = '.txt') -> str:
        """Generate CV filename according to naming convention."""
        timestamp = int(datetime.utcnow().timestamp())
        return f"cv_{candidate_id}_int{interview_id}_{timestamp}{extension}"

    @classmethod
    def generate_job_description_filename(cls, interview_id: int, extension: str = '.txt') -> str:
        """Generate job description filename according to naming convention."""
        timestamp = int(datetime.utcnow().timestamp())
        return f"job_description_int{interview_id}_{timestamp}{extension}"

    @classmethod
    async def save_cv_file(cls, file: UploadFile, candidate_id: int, interview_id: int, existing_path: Optional[str] = None) -> str:
        """Save CV file and return relative path. Optionally delete existing file."""
        cls.validate_file(file)

        # Extract original file extension
        original_extension = Path(file.filename).suffix.lower()
        filename = cls.generate_cv_filename(candidate_id, interview_id, original_extension)
        upload_dir = cls.get_upload_dir()
        file_path = upload_dir / filename

        # Delete existing file if provided (handle both relative and absolute paths)
        if existing_path:
            # If it's a relative path, convert to absolute for deletion
            abs_existing_path = existing_path if os.path.isabs(existing_path) else cls.get_absolute_path(existing_path)
            if cls.file_exists(abs_existing_path):
                cls.delete_file(abs_existing_path)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return relative path from project root
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        return str(file_path.relative_to(project_root))

    @classmethod
    async def save_job_description_file(cls, file: UploadFile, interview_id: int, existing_path: Optional[str] = None) -> str:
        """Save job description file and return relative path. Optionally delete existing file."""
        cls.validate_file(file)

        # Extract original file extension
        original_extension = Path(file.filename).suffix.lower()
        filename = cls.generate_job_description_filename(interview_id, original_extension)
        upload_dir = cls.get_upload_dir()
        file_path = upload_dir / filename

        # Delete existing file if provided (handle both relative and absolute paths)
        if existing_path:
            # If it's a relative path, convert to absolute for deletion
            abs_existing_path = existing_path if os.path.isabs(existing_path) else cls.get_absolute_path(existing_path)
            if cls.file_exists(abs_existing_path):
                cls.delete_file(abs_existing_path)

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return relative path from project root
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        return str(file_path.relative_to(project_root))

    @classmethod
    def read_file_content(cls, file_path: str) -> str:
        """Read file content as string."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="File not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

    @classmethod
    def delete_file(cls, file_path: str) -> None:
        """Delete file if it exists."""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            # Log error but don't raise - file deletion failure shouldn't break business logic
            print(f"Warning: Could not delete file {file_path}: {str(e)}")

    @classmethod
    def file_exists(cls, file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path)

    @classmethod
    def get_absolute_path(cls, relative_path: str) -> str:
        """Convert relative path to absolute path based on project root."""
        try:
            # Use absolute path based on project root
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent.parent.parent  # Go up to project root
            absolute_path = project_root / relative_path
            return str(absolute_path)
        except Exception as e:
            print(f"ERROR: Failed to get absolute path for {relative_path}: {e}")
            # Fallback: assume relative_path is already absolute or handle as-is
            return relative_path
