**Epic: Manage foundational data entities and lookup tables for the system.**

**Description:**  
• Context: The application requires a centralized and flexible way to store and manage static or semi-static data, such as roles, clients, and seniorities, along with general interview details.  
• Objective: To establish a flexible and extensible data model for core system entities and reference data, ensuring data consistency and reusability.  
• In Scope: CRUD operations for a generic lookup table (Id de dominio, Id del ítem, texto descriptivo) to manage entities like Roles, Clients of Globant, and Seniorities. Storing general interview details including associated analyst, candidate, role, seniority, scheduled date, status, and notes.  
• Out of scope: Complex data migration tools, advanced data warehousing solutions, real-time data synchronization with external master data management systems.  
• Assumptions: The generic lookup table structure is sufficient for all identified reference data types. Data integrity will be maintained through standard database constraints.  
• Dependencies: All other epics will depend on this for foundational and reference data.  
• Tech Note: Relational database design for lookup tables and core entities, generic CRUD API endpoints for data management.

**Title: Implement CRUD operations for candidate entities.**

**Type:** Story

**Description:**  
• Context: Candidates need CRUD operations in the system.  
• Objective: Allow Recruiting Analysts to manage candidate information.  
• In scope: Create, Read, Update, Delete operations for candidates.  
• Out of scope: Candidate self-registration.  
• Assumptions: Candidate entity structure is defined.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Create a new candidate   
Given: The Recruiting Analyst is logged in  
When: The Recruiting Analyst creates a new candidate with valid data  
Then: The candidate is saved in the system

Scenario 2: Read an existing candidate  
Given: The Recruiting Analyst is logged in  
When: The Recruiting Analyst views the details of an existing candidate  
Then: The candidate information is displayed correctly

Scenario 3: Update an existing candidate  
Given: The Recruiting Analyst is logged in  
When: The Recruiting Analyst updates an existing candidate with new data  
Then: The candidate information is updated successfully

**Title: Implement CRUD operations for analyst entities.**

**Type:** Story

**Description:**  
• Context: Analysts need CRUD operations in the system.  
• Objective: Allow administrators to manage analyst information.  
• In scope: Create, Read, Update, Delete operations for analysts.  
• Out of scope: User authentication and authorization.  
• Assumptions: Analyst entity structure is defined.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Create a new analyst  
Given: The administrator is logged in  
When: The administrator creates a new analyst with valid data  
Then: The analyst is saved in the system

Scenario 2: Read an existing analyst  
Given: The administrator is logged in  
When: The administrator views the details of an existing analyst  
Then: The analyst information is displayed correctly

Scenario 3: Update an existing analyst  
Given: The administrator is logged in  
When: The administrator updates an existing analyst with new data  
Then: The analyst information is updated successfully

**Title: Design data structure for the 'Entrevista' entity.**

**Type:** Task

**Description:**  
• Context: 'Entrevista' entity requires data structure design.  
• Objective: Define the 'Entrevista' entity and its attributes.  
• In scope: Defining attributes such as analyst, candidate, role.  
• Out of scope: Implementing API endpoints.  
• Assumptions: Data types for attributes are known.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Data Structure Defined  
Given: Requirements for interview data storage  
When: Data structure implemented  
Then: Entity includes analyst, candidate, role, seniority, CV, Job Description, feedbacks, specific guidelines, scheduled date, state, notes and link

**Title: Create lookup tables for roles, clients, and seniorities.**

**Type:** Story

**Description:**  
• Context: System requires lookup tables to store Roles, Globant Clients, Seniorities.  
• Objective: Enable the storage and management of system lookup data.  
• In scope: Creation of Roles, Client, Seniority lookup tables.  
• Out of scope: Management of user accounts.  
• Assumptions: Data structure for lookup tables is defined.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Create a new role  
Given: The administrator is logged in  
When: The administrator creates a new role with a unique ID and description  
Then: The role is saved to the Roles lookup table

Scenario 2: Create a new client  
Given: The administrator is logged in  
When: The administrator creates a new client with a unique ID and description  
Then: The client is saved to the Clients lookup table

Scenario 3: Create a new seniority  
Given: The administrator is logged in  
When: The administrator creates a new seniority with a unique ID and description  
Then: The seniority is saved to the Seniorities lookup table

**Epic: Provide user interfaces for managing entities and viewing filtered lists.**

**Description:**  
• Context: Users need intuitive interfaces to create, read, update, and delete system entities, as well as to view filtered lists of interviews and candidates.  
• Objective: To enable users to effectively manage system data and monitor interview processes through user-friendly forms and interactive lists.  
• In Scope: Implementation of CRUD (Create, Read, Update, Delete) forms for Analyst, Candidate, Interview, and Lookup Table entities. Development of a filterable list of interviews (by role and client). Development of a filterable list of candidates (by role and name).  
• Out of scope: Advanced search capabilities (e.g., full-text search across all fields), custom report generation, export functionalities (e.g., CSV, PDF) for lists, complex data visualization.  
• Assumptions: Standard web form and table components will be used for the user interface. Basic filtering capabilities are sufficient for the MVP.  
• Dependencies: Core Data Management, User Management, Interview Configuration, Interview Feedback & Reporting (for displaying data).  
• Tech Note: Frontend framework (e.g., React, Angular, Vue) for UI components, backend API endpoints for CRUD operations, pagination and filtering logic for lists.

**Title: Implement CRUD operations for the 'Entrevista' entity.**

**Type:** Story

**Description:**  
• Context: 'Entrevista' entity needs CRUD operations.  
• Objective: Enable CRUD operations for the Interview entity.  
• In scope: CRUD operations for 'Entrevista'.  
• Out of scope: Generating unique interview links.  
• Assumptions: 'Entrevista' data structure is defined.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Create an 'Entrevista'  
Given: An analyst is logged in  
When: The analyst creates a new interview with all necessary data  
Then: The new interview is saved to the database

Scenario 2: Update an 'Entrevista'  
Given: An analyst is logged in  
When: The analyst updates an existing interview with all necessary data  
Then: The interview data is updated successfully

Scenario 3: Delete an 'Entrevista'  
Given: An analyst is logged in  
When: The analyst deletes an existing interview  
Then: The interview is no longer available in the system

**Title: List candidates filterable by role and name.**

**Type:** Story

**Description:**  
• Context: Recruiting analyst need to list candidates.  
• Objective: Provides filtered lists of candidates.  
• In scope: Implement list and filtering by role, name.  
• Out of scope: Complex search functionality.  
• Assumptions: Candidate and Role entities exist.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Filter Candidate List by Role  
Given: The analyst is logged in  
When: The analyst filters the list of candidates by role  
Then: Only candidates with the selected role are displayed

Scenario 2: Filter Candidate List by Name  
Given: The analyst is logged in  
When: The analyst filters the list of candidates by name  
Then: Only candidates matching the provided name are displayed

**Title: Create a list of interviews filterable by role and client.**

**Type:** Story

**Description:**  
• Context: Analyst need a list of interviews filterable by role and client.  
• Objective: Provides a listing of interviews for managing interviews.  
• In scope: Implement list and filtering by role and client.  
• Out of scope: Advanced reporting.  
• Assumptions: 'Entrevista' entity and lookup tables exist.  
• Tech Notes: None

**Acceptance Criteria:** 

Scenario 1: Filter Interview List by Role  
Given: The analyst is logged in  
When: The analyst filters the list of interviews by role  
Then: Only interviews associated with the selected role are displayed

Scenario 2: Filter Interview List by Client  
Given: The analyst is logged in  
When: The analyst filters the list of interviews by client  
Then: Only interviews associated with the selected client are displayed

**Epic: Manage system users and their assigned roles with minimal privileges.**

**Description:**  
• Context: The system requires different levels of access and functionality for Administrators, Recruiting Analysts, and Candidates to perform their respective tasks.  
• Objective: To enable secure access and appropriate permissions for all user types within the application, adhering to the principle of least privilege.  
• In Scope: User registration for Recruiting Analysts (name, surname, email) and Candidates (name, surname, email, ID document). Role assignment for System Administrator, Recruiting Analyst, and Candidate. Basic user profile management.  
• Out of scope: Advanced user authentication methods (e.g., SSO, MFA), complex password policies, detailed audit logs of user actions, user deactivation/archiving.  
• Assumptions: A standard authentication mechanism (e.g., username/password) will be implemented. User roles are static and predefined.  
• Dependencies: Core database infrastructure for user data storage.  
• Tech Note: Standard web application user management patterns and database schema for user and role entities.

**Title: Develop CRUD operations for managing candidate profiles.**

**Type:** Story

**Description:**  
• Context: Candidate information needs to be stored and managed.  
• Objective: Enable the creation, reading, updating, and deletion of candidate profiles.  
• In scope: CRUD operations for candidate data (name, surname, email, ID).  
• Out of scope: Resume parsing or social media integration.  
• Assumptions: Candidate data requirements are clearly defined.  
• Tech Notes: Use RESTful APIs.

**Acceptance Criteria:** 

Scenario 1: Create a candidate profile  
Given: The admin is logged in.  
When: The admin creates a candidate with name, surname, email and ID  
Then: The candidate profile is created successfully.

Scenario 2: Delete a candidate profile  
Given: The admin is logged in.And: A candidate profile exists.  
When: The admin deletes the profile.  
Then: The candidate profile is deleted successfully.

**Title: Develop CRUD operations for managing recruiting analyst profiles.**

**Type:** Story

**Description:**  
• Context: Recruiting analysts need to be managed within the system.  
• Objective: Enable the creation, reading, updating, and deletion of analyst profiles.  
• In scope: CRUD operations for analyst data (name, surname, email).  
• Out of scope: Detailed profiles with history and performance metrics.  
• Assumptions: Analyst data requirements are clearly defined.  
• Tech Notes: Use RESTful APIs.

**Acceptance Criteria:** 

Scenario 1: Create a new analyst profile  
Given: The admin is logged in  
When: The admin creates a new analyst profile with valid information  
Then: The new analyst profile is created successfully

Scenario 2: Update an existing analyst profile  
Given: The admin is logged in  
And: An analyst profile exists  
When: The admin updates the profile's information  
Then: The analyst profile is updated successfully

**Title: Implement user authentication and authorization for system access control.**

**Type:** Story

**Description:**  
• Context: The system requires secure access control based on user roles and permissions.  
• Objective: To ensure secure access and role-based permissions within the system.  
• In scope: User login, role assignment, and permission restrictions.  
• Out of scope: Integration with external authentication providers.  
• Assumptions: User roles and permissions are well-defined.  
• Tech Notes: Use RBAC (Role-Based Access Control).

**Acceptance Criteria:** 

Scenario 1: Admin assigns roles to users  
Given: The admin is logged in  
When: The admin assigns a role to a user  
Then: The user's permissions are updated based on the assigned role

**Title: Implement a lookup table for managing system configurations.**

**Type:** Story

**Description:**  
• Context: System configurations like roles and seniority need to be managed.  
• Objective: To store roles, clients, and seniorities.  
• In scope: CRUD operations for lookup table data (Id de dominio, Id del ítem, text).  
• Out of scope: Complex configurations with dependencies.  
• Assumptions: Lookup table structure is clearly defined.  
• Tech Notes: Use a generic table structure.

**Acceptance Criteria:** 

Scenario 1: Create a lookup entry  
Given: The admin is logged in.  
When: The admin creates a new lookup table entry (e.g., a new role)  
Then: The new lookup entry is created successfully.

Scenario 2: Update a lookup entry  
Given: The admin is logged in  
And: A lookup entry exists  
When: The admin updates the lookup entry's description  
Then: The lookup entry is updated successfully.

**Epic: Enable analysts to configure and schedule technical interviews.**

**Description:**  
• Context: Recruiting Analysts need a dedicated interface to set up interviews by linking candidates to specific Job Descriptions and defining all necessary interview parameters.  
• Objective: To provide a robust and intuitive interface for analysts to efficiently prepare, schedule, and manage interview sessions.  
• In Scope: Associating a candidate with a Job Description, selecting the associated analyst, role, and seniority. Uploading relevant files (CV, JD, previous feedbacks). Defining specific interview guidelines. Setting the scheduled date and time for the interview. Managing the interview's status. Generating and managing a unique, time-sensitive link for the candidate.  
• Out of scope: Automated parsing of Job Descriptions or CVs, integration with external calendar systems, complex scheduling conflict resolution, real-time availability checks for analysts.  
• Assumptions: Job Descriptions and CVs are provided as digital files. Previous feedbacks are available in a structured or file format. The unique link activation window (+/- 5 minutes) is sufficient.  
• Dependencies: User Management (for Analyst and Candidate entities), Core Data Management (for Lookup tables like Roles, Seniorities, Clients).  
• Tech Note: File upload mechanisms, date/time pickers, unique URL generation and validation logic, database schema for interview entity.

**Title: Develop filtered listings for interviews and candidates.**

**Type:** Story

**Description:**  
• Context: Analysts need to find interviews and candidates easily.  
• Objective: Implement filtered listings for interviews (by role and client) and candidates (by role and name).  
• In scope: Filtering functionality in interview and candidate listings.  
• Out of scope: Advanced search features or custom reporting.  
• Assumptions: Filtering criteria are well-defined.  
• Tech Notes: Use efficient database queries.

**Acceptance Criteria:** 

Scenario 1: Filter Interviews by Role  
Given: The analyst is logged in  
When: The analyst applies a filter by Role to the interview list  
Then: The list shows interviews matching the selected role.

Scenario 2: Filter Candidates by Name  
Given: The analyst is logged in.  
When: The analyst applies a filter by Name to the candidates list  
Then: The list shows candidates matching the inserted name.

**Title: Implement unique link generation for accessing scheduled interviews.**

**Type:** Story

**Description:**  
• Context: Candidates need a secure way to access scheduled interviews.  
• Objective: Generate unique, time-limited links for interview access.  
• In scope: Link generation and validation with \+-5 min tolerance.  
• Out of scope: Email notifications or password reset flows.  
• Assumptions: Link generation algorithm is secure and efficient.  
• Tech Notes: Consider URL signing.

**Acceptance Criteria:** Scenario 1: Generate a unique linkGiven: An interview is scheduledWhen: The system generates a link for the interview.Then: A unique link is generated with a limited validity (5 minutes plus or minus the scheduled time).Scenario 2: Access interview using the generated linkGiven: A candidate clicks on the URL link.And: The current is between \-5 or \+5 minutes from start\_date.When: The system validates the linkThen: The candidate is redirect to the interview page.

**Title: Develop CRUD operations for managing interview configurations.**

**Type:** Story

**Description:**  
• Context: Interviews need to be configured and managed properly.  
• Objective: Enable the creation, reading, updating, and deletion of interview configurations.  
• In scope: CRUD for interviews (analyst, candidate, role, seniority, files, etc.).  
• Out of scope: Automated scheduling or calendar integration.  
• Assumptions: Interview configuration data is clearly defined.  
• Tech Notes: Use RESTful APIs.

**Acceptance Criteria:** Scenario 1: Create an interviewGiven: The analyst is logged in.When: The analyst creates a new interview.Then: The interview is created successfully.Scenario 2: Update an interviewGiven: The analyst is logged in and an interview exist.When: The analyst updates the interview.Then: The interview is updated successfully.

**Epic: Implement the AI agent for conducting dynamic technical interviews.**

**Description:**  
• Context: The core functionality of the application is an AI agent that performs verbal, conversational technical interviews based on predefined inputs.  
• Objective: To develop an AI-driven conversational interface that objectively assesses candidates' quantifiable technical skills and experience.  
• In Scope: AI's conversational flow: self-introduction, explanation of client needs, confirmation of candidate aptitude, dynamic technical questioning based on Job Description, CV, previous feedbacks, and specific guidelines. Interview conclusion and thank you message. Saving all interview content to the database.  
• Out of scope: AI model training from scratch, real-time sentiment analysis, evaluation of subjective behavioral criteria, complex natural language generation beyond technical questioning.  
• Assumptions: A pre-trained or configurable conversational AI service will be utilized. The AI will strictly adhere to evaluating quantifiable attributes. Speech-to-text and text-to-speech services are available.  
• Dependencies: Interview Configuration (for all AI inputs), Core Data Management (to save interview transcripts and data).  
• Tech Note: Integration with a conversational AI platform (e.g., OpenAI API, Google Dialogflow), speech-to-text (STT) and text-to-speech (TTS) APIs.

**Title: Limit the scope of the technical interview to quantifiable attributes.**

**Type:** Task

**Description:**  
• Context: Focusing on skills, experience, and knowledge.  
• Objective: To ensure objectivity in technical assessments.  
• In scope: Technical skills and experience.  
• Out of scope: Behavioral and personality assessments.  
• Assumptions: Quantifiable attributes are well-defined.  
• Tech Notes: Data extraction and processing.

**Acceptance Criteria:**   
Scenario 1: Confine interview scope to quantifiable attributes  
Given: The system is configured to conduct a technical interview  
When: The AI asks skill-based or experience-based questions  
Then: The AI does not ask questions related to behavioral competencies

**Title: Develop AI agent to conduct dynamic technical interviews with candidates.**

**Type:** Story

**Description:**  
• Context: The system needs an AI agent to interview candidates.  
• Objective: To automate and standardize the initial technical screening process.  
• In scope: AI agent capable of conversational interviews.  
• Out of scope: Assessing subjective criteria like behavioral traits.  
• Assumptions: Job descriptions are accurately defined.  
• Tech Notes: Use of NLP for understanding and responding.

**Acceptance Criteria:** 

Scenario 1: AI conducts initial technical interview  
Given: The system has a configured interview with a candidate and JD  
When: The candidate starts the interview  
Then: The AI agent conducts a technical interview following the JD

**Title: Configure interviews by associating candidates with job descriptions.**

**Type:** Story

**Description:**  
• Context: Linking candidates to specific job requirements.  
• Objective: To ensure relevant questions are asked during interviews.  
• In scope: Linking candidates and job descriptions.  
• Out of scope: Creating or modifying job descriptions.  
• Assumptions: Job descriptions are pre-existing.  
• Tech Notes: UI components for selection.

**Acceptance Criteria:** 

Scenario 1: Associate a candidate with a job description  
Given:  An analyst is logged in and views a candidate's profile  
When: The analyst selects a job description for the candidate  
Then: The candidate and job description are associated for the interview

**Epic: Generate structured, objective feedback and reports post-interview.**

**Description:**  
• Context: Upon completion of an interview, the system must provide a clear, objective assessment of the candidate's fit for the role.  
• Objective: To deliver comprehensive and actionable feedback that highlights candidate strengths, weaknesses, and overall suitability based on quantifiable attributes.  
• In Scope: Generating general comments on the candidate's overall fit. Providing an overall ranking (1-5). Listing each evaluated skill with a specific ranking (1-5, where 1='Cannot perform' and 5='Can teach others'). Saving all generated feedback to the database.  
• Out of scope: Advanced analytics dashboards, customizable report templates, integration with external HRIS systems for automated feedback sharing, graphical representations of feedback.  
• Assumptions: The AI Interview Execution component will provide all necessary data points for feedback generation. The ranking scales are clearly defined and understood.  
• Dependencies: AI Interview Execution (source of feedback data), Core Data Management (to store structured feedback).  
• Tech Note: Database schema design for structured feedback, reporting generation logic, and data aggregation from interview transcripts.

**Title: Highlight candidate strengths and areas for improvement based on feedback**

**Type:** Task

**Description:**  
• Context: Identifying key areas of strength and gaps.  
• Objective: To offer actionable insights for candidates.  
• In scope: Analysis of interview data and feedback.  
• Out of scope: Providing learning recommendations.  
• Assumptions: Feedback data is accurate.  
• Tech Notes: Algorithm design for evaluation metrics.

**Acceptance Criteria:** 

Scenario 1: Highlight key strengths and improvements for candidate  
Given: Interview feedback generated.  
When: The system analyzes interview feedback.  
Then: The system shows the candidate's strength and improvements

**Title: Provide a ranking structure from 1-5 for general and skill based feedback.**

**Type:** Task

**Description:**  
• Context: Providing candidate ranking for feedback  
• Objective: To give the candidate a comparable ranking to improve their skills  
• In scope: Generate a ranking system for candidate  
• Out of scope: Provide external sources for learning new skills  
• Assumptions: Candidate rankings can be generated without bias.  
• Tech Notes: Ranking framework for skill improvement

**Acceptance Criteria:** 

Scenario 1: Provide a candidate ranking on skill evaluation.  
Given: The system generated the skills ratings.  
When: The system evaluates the candidate's skills.  
Then: The System Provides a 1-5 skill set ranking for the candidate.

**Title: Generate structured feedback with objective candidate-JD fit valuation.**

**Type:** Story

**Description:**  
• Context: Providing objective evaluation of candidate fit.  
• Objective: To provide clear, unbiased insights on candidate fit.  
• In scope: Feedback generation with valuation.  
• Out of scope: Extensive qualitative analysis.  
• Assumptions: Scoring metrics defined and unbiased.  
• Tech Notes: AI feedback generation model.

**Acceptance Criteria:** 

Scenario 1: Generate feedback based on interview results  
Given: The AI technical interview is completed for the candidate  
When: The system generates feedback  
Then: A structured feedback report with objective candidate-JD fit valuation is created

