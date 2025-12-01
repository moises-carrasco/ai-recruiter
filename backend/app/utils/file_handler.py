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

    # Allowed file types (only .txt as per requirements)
    ALLOWED_EXTENSIONS = {'.txt'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    @classmethod
    def get_upload_dir(cls) -> Path:
        """Get the upload directory path."""
        upload_dir = Path(settings.UPLOAD_DIR) if hasattr(settings, 'UPLOAD_DIR') else Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        return upload_dir

    @classmethod
    def validate_file(cls, file: UploadFile) -> None:
        """Validate uploaded file type and size."""
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in cls.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Only .txt files are allowed. Got: {file_ext}"
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
    def generate_cv_filename(cls, candidate_id: int, interview_id: int) -> str:
        """Generate CV filename according to naming convention."""
        timestamp = int(datetime.utcnow().timestamp())
        return f"cv_{candidate_id}_int{interview_id}_{timestamp}.txt"

    @classmethod
    def generate_job_description_filename(cls, interview_id: int) -> str:
        """Generate job description filename according to naming convention."""
        timestamp = int(datetime.utcnow().timestamp())
        return f"job_description_int{interview_id}_{timestamp}.txt"

    @classmethod
    async def save_cv_file(cls, file: UploadFile, candidate_id: int, interview_id: int) -> str:
        """Save CV file and return relative path."""
        cls.validate_file(file)

        filename = cls.generate_cv_filename(candidate_id, interview_id)
        upload_dir = cls.get_upload_dir()
        file_path = upload_dir / filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return relative path from project root
        return str(file_path.relative_to(Path.cwd()))

    @classmethod
    async def save_job_description_file(cls, file: UploadFile, interview_id: int) -> str:
        """Save job description file and return relative path."""
        cls.validate_file(file)

        filename = cls.generate_job_description_filename(interview_id)
        upload_dir = cls.get_upload_dir()
        file_path = upload_dir / filename

        # Save file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Return relative path from project root
        return str(file_path.relative_to(Path.cwd()))

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
