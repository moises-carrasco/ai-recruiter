# User Stories

## Epic 1: Manage basic system data

**Description:**  
Set up the basic data that the system needs to work, like roles, clients, and interview information. This includes creating simple lookup tables and managing candidate and analyst information.

### Story 1.1: Implement CRUD operations for candidate entities
**Type:** Story  
**Description:**  
Allow recruiting analysts to create, view, update, and delete candidate information in the system.

**Acceptance Criteria:**
- **Scenario 1: Create a new candidate**  
  Given: The Recruiting Analyst is logged in  
  When: The Recruiting Analyst creates a new candidate with valid data  
  Then: The candidate is saved in the system

- **Scenario 2: Read an existing candidate**  
  Given: The Recruiting Analyst is logged in  
  When: The Recruiting Analyst views the details of an existing candidate  
  Then: The candidate information is displayed correctly

- **Scenario 3: Update an existing candidate**  
  Given: The Recruiting Analyst is logged in  
  When: The Recruiting Analyst updates an existing candidate with new data  
  Then: The candidate information is updated successfully

### Story 1.2: Implement CRUD operations for analyst entities
**Type:** Story  
**Description:**  
Allow administrators to create, view, update, and delete analyst information in the system.

**Acceptance Criteria:**
- **Scenario 1: Create a new analyst**  
  Given: The administrator is logged in  
  When: The administrator creates a new analyst with valid data  
  Then: The analyst is saved in the system

- **Scenario 2: Read an existing analyst**  
  Given: The administrator is logged in  
  When: The administrator views the details of an existing analyst  
  Then: The analyst information is displayed correctly

- **Scenario 3: Update an existing analyst**  
  Given: The administrator is logged in  
  When: The administrator updates an existing analyst with new data  
  Then: The analyst information is updated successfully

### Story 1.3: Design data structure for the 'Interview' entity
**Type:** Task  
**Description:**  
Define what information an interview needs to store, like which analyst and candidate are involved, what role it's for, and when it's scheduled.

**Acceptance Criteria:**
- **Scenario 1: Data Structure Defined**  
  Given: Requirements for interview data storage  
  When: Data structure implemented  
  Then: Entity includes analyst, candidate, role, seniority, CV, Job Description, feedbacks, specific guidelines, scheduled date, state, notes and link

### Story 1.4: Create lookup tables for roles, clients, and seniorities
**Type:** Story  
**Description:**  
Create simple tables to store and manage roles, clients, and seniority levels that can be used throughout the system.

**Acceptance Criteria:**
- **Scenario 1: Create a new role**  
  Given: The administrator is logged in  
  When: The administrator creates a new role with a unique ID and description  
  Then: The role is saved to the Roles lookup table

- **Scenario 2: Create a new client**  
  Given: The administrator is logged in  
  When: The administrator creates a new client with a unique ID and description  
  Then: The client is saved to the Clients lookup table

- **Scenario 3: Create a new seniority**  
  Given: The administrator is logged in  
  When: The administrator creates a new seniority with a unique ID and description  
  Then: The seniority is saved to the Seniorities lookup table

## Epic 2: Create user interfaces for managing data

**Description:**  
Build easy-to-use screens where users can add, edit, and view information about candidates, interviews, and other system data. Include filtering to help users find what they need quickly.

### Story 2.1: Implement CRUD operations for the 'Interview' entity
**Type:** Story  
**Description:**  
Allow analysts to create, view, update, and delete interview records in the system.

**Acceptance Criteria:**
- **Scenario 1: Create an 'Interview'**  
  Given: An analyst is logged in  
  When: The analyst creates a new interview with all necessary data  
  Then: The new interview is saved to the database

- **Scenario 2: Update an 'Interview'**  
  Given: An analyst is logged in  
  When: The analyst updates an existing interview with all necessary data  
  Then: The interview data is updated successfully

- **Scenario 3: Delete an 'Interview'**  
  Given: An analyst is logged in  
  When: The analyst deletes an existing interview  
  Then: The interview is no longer available in the system

### Story 2.2: List candidates filterable by role and name
**Type:** Story  
**Description:**  
Show a list of candidates that can be filtered by role or name to help analysts find the right people quickly.

**Acceptance Criteria:**
- **Scenario 1: Filter Candidate List by Role**  
  Given: The analyst is logged in  
  When: The analyst filters the list of candidates by role  
  Then: Only candidates with the selected role are displayed

- **Scenario 2: Filter Candidate List by Name**  
  Given: The analyst is logged in  
  When: The analyst filters the list of candidates by name  
  Then: Only candidates matching the provided name are displayed

### Story 2.3: Create a list of interviews filterable by role and client
**Type:** Story  
**Description:**  
Show a list of interviews that can be filtered by role or client to help analysts manage their interviews.

**Acceptance Criteria:**
- **Scenario 1: Filter Interview List by Role**  
  Given: The analyst is logged in  
  When: The analyst filters the list of interviews by role  
  Then: Only interviews associated with the selected role are displayed

- **Scenario 2: Filter Interview List by Client**  
  Given: The analyst is logged in  
  When: The analyst filters the list of interviews by client  
  Then: Only interviews associated with the selected client are displayed

## Epic 3: Manage users and permissions

**Description:**  
Set up user accounts for administrators, recruiting analysts, and candidates. Make sure each type of user can only access what they need to do their job.

### Story 3.1: Develop CRUD operations for managing candidate profiles
**Type:** Story  
**Description:**  
Allow admins to create, view, update, and delete candidate profiles with basic information like name, email, and ID.

**Acceptance Criteria:**
- **Scenario 1: Create a candidate profile**  
  Given: The admin is logged in  
  When: The admin creates a candidate with name, surname, email and ID  
  Then: The candidate profile is created successfully

- **Scenario 2: Delete a candidate profile**  
  Given: The admin is logged in And: A candidate profile exists  
  When: The admin deletes the profile  
  Then: The candidate profile is deleted successfully

### Story 3.2: Develop CRUD operations for managing recruiting analyst profiles
**Type:** Story  
**Description:**  
Allow admins to create, view, update, and delete analyst profiles with basic information like name and email.

**Acceptance Criteria:**
- **Scenario 1: Create a new analyst profile**  
  Given: The admin is logged in  
  When: The admin creates a new analyst profile with valid information  
  Then: The new analyst profile is created successfully

- **Scenario 2: Update an existing analyst profile**  
  Given: The admin is logged in And: An analyst profile exists  
  When: The admin updates the profile's information  
  Then: The analyst profile is updated successfully

### Story 3.3: Implement user authentication and authorization for system access control
**Type:** Story  
**Description:**  
Set up login system and make sure users can only access features appropriate for their role.

**Acceptance Criteria:**
- **Scenario 1: Admin assigns roles to users**  
  Given: The admin is logged in  
  When: The admin assigns a role to a user  
  Then: The user's permissions are updated based on the assigned role

### Story 3.4: Implement a lookup table for managing system configurations
**Type:** Story  
**Description:**  
Create a simple way to manage system settings like roles, clients, and seniority levels.

**Acceptance Criteria:**
- **Scenario 1: Create a lookup entry**  
  Given: The admin is logged in  
  When: The admin creates a new lookup table entry (e.g., a new role)  
  Then: The new lookup entry is created successfully

- **Scenario 2: Update a lookup entry**  
  Given: The admin is logged in And: A lookup entry exists  
  When: The admin updates the lookup entry's description  
  Then: The lookup entry is updated successfully

## Epic 4: Set up and schedule interviews

**Description:**  
Give analysts tools to set up interviews by connecting candidates with job descriptions, uploading files, setting dates, and creating secure links for candidates to access their interviews.

### Story 4.1: Develop filtered listings for interviews and candidates
**Type:** Story  
**Description:**  
Create lists of interviews and candidates that can be filtered to help analysts find what they need quickly.

**Acceptance Criteria:**
- **Scenario 1: Filter Interviews by Role**  
  Given: The analyst is logged in  
  When: The analyst applies a filter by Role to the interview list  
  Then: The list shows interviews matching the selected role

- **Scenario 2: Filter Candidates by Name**  
  Given: The analyst is logged in  
  When: The analyst applies a filter by Name to the candidates list  
  Then: The list shows candidates matching the inserted name

### Story 4.2: Implement unique link generation for accessing scheduled interviews
**Type:** Story  
**Description:**  
Create secure, time-limited links that candidates can use to access their scheduled interviews.

**Acceptance Criteria:**
- **Scenario 1: Generate a unique link**  
  Given: An interview is scheduled  
  When: The system generates a link for the interview  
  Then: A unique link is generated with a limited validity (5 minutes plus or minus the scheduled time)

- **Scenario 2: Access interview using the generated link**  
  Given: A candidate clicks on the URL link And: The current time is between -5 or +5 minutes from start_date  
  When: The system validates the link  
  Then: The candidate is redirected to the interview page

### Story 4.3: Develop CRUD operations for managing interview configurations
**Type:** Story  
**Description:**  
Allow analysts to create, view, update, and delete interview setups including all the necessary details and files.

**Acceptance Criteria:**
- **Scenario 1: Create an interview**  
  Given: The analyst is logged in  
  When: The analyst creates a new interview  
  Then: The interview is created successfully

- **Scenario 2: Update an interview**  
  Given: The analyst is logged in and an interview exists  
  When: The analyst updates the interview  
  Then: The interview is updated successfully

## Epic 5: AI-powered technical interviews

**Description:**  
Build an AI system that can have conversations with candidates to test their technical skills. The AI asks questions based on the job description and candidate's background, then saves everything for review.

### Story 5.1: Limit the scope of the technical interview to quantifiable attributes
**Type:** Task  
**Description:**  
Make sure the AI only asks about technical skills and experience, not personality or behavior.

**Acceptance Criteria:**
- **Scenario 1: Confine interview scope to quantifiable attributes**  
  Given: The system is configured to conduct a technical interview  
  When: The AI asks skill-based or experience-based questions  
  Then: The AI does not ask questions related to behavioral competencies

### Story 5.2: Develop AI agent to conduct dynamic technical interviews with candidates
**Type:** Story  
**Description:**  
Create an AI that can have natural conversations with candidates to test their technical abilities.

**Acceptance Criteria:**
- **Scenario 1: AI conducts initial technical interview**  
  Given: The system has a configured interview with a candidate and JD  
  When: The candidate starts the interview  
  Then: The AI agent conducts a technical interview following the JD

### Story 5.3: Configure interviews by associating candidates with job descriptions
**Type:** Story  
**Description:**  
Connect candidates with specific job descriptions so the AI knows what questions to ask during the interview.

**Acceptance Criteria:**
- **Scenario 1: Associate a candidate with a job description**  
  Given: An analyst is logged in and views a candidate's profile  
  When: The analyst selects a job description for the candidate  
  Then: The candidate and job description are associated for the interview

## Epic 6: Generate feedback and reports

**Description:**  
After interviews are complete, automatically create clear reports that show how well candidates did, what their strengths are, and how they rank on different skills.

### Story 6.1: Highlight candidate strengths and areas for improvement based on feedback
**Type:** Task  
**Description:**  
Analyze interview results to identify what candidates are good at and where they need to improve.

**Acceptance Criteria:**
- **Scenario 1: Highlight key strengths and improvements for candidate**  
  Given: Interview feedback generated  
  When: The system analyzes interview feedback  
  Then: The system shows the candidate's strength and improvements

### Story 6.2: Provide a ranking structure from 1-5 for general and skill based feedback
**Type:** Task  
**Description:**  
Give candidates scores from 1-5 for their overall performance and individual skills to help them understand where they stand.

**Acceptance Criteria:**
- **Scenario 1: Provide a candidate ranking on skill evaluation**  
  Given: The system generated the skills ratings  
  When: The system evaluates the candidate's skills  
  Then: The System Provides a 1-5 skill set ranking for the candidate

### Story 6.3: Generate structured feedback with objective candidate-JD fit valuation
**Type:** Story  
**Description:**  
Create clear, unbiased reports that show how well candidates match the job requirements.

**Acceptance Criteria:**
- **Scenario 1: Generate feedback based on interview results**  
  Given: The AI technical interview is completed for the candidate  
  When: The system generates feedback  
  Then: A structured feedback report with objective candidate-JD fit valuation is created
