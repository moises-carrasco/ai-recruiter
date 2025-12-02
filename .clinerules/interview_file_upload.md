## Guidelines for interview file uploads

- In the backend side, two variables must be defined to store the file paths for job descriptions and CVs.
- Plain text files are allowed (`.txt` and `.md`) and the paths will be local to the computer.
- File names must follow these naming conventions, preserving the original file extension:
    - **Job Descriptions:** `job_description_int{interview_id}_{timestamp}{original_extension}`
    - **CVs:** `cv_{candidate_id}_int{interview_id}_{timestamp}{original_extension}`
- The paths to these files must be stored in the `interviews` table.
- Once the interview is saved and the CRUD form is opened again, the interface must provide two links that allow downloading these files.
