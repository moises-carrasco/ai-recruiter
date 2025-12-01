## Guidelenes for interview file uploads

- In the backend side, two variables must be defined to store the file paths for job descriptions and CVs.
- For now, only plain text (`.txt`) files are allowed and the paths will be local to the computer.
- File names must follow these naming conventions:
    - **Job Descriptions:** `job_description_int{interview_id}_{timestamp}.txt`
    - **CVs:** `cv_{candidate_id}_int{interview_id}_{timestamp}.txt`
- The paths to these files must be stored in the `interviews` table.
- Once the interview is saved and the CRUD form is opened again, the interface must provide two links that allow downloading these files.

