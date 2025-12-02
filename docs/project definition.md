# **Project Definition**

The goal of this project is to develop an MVP for a web application that enables an AI agent to conduct technical interviews with Globant workers (Globers) who wish to apply for a specific position within the accounts Globant manages for its clients (Northwind Media, Globex Studios, etc.).

The system must allow each interview to be configured by associating a candidate with a Job Description, which defines the technical and experience requirements for the position. Based on this information, the AI will conduct a verbal interview in a dynamic conversational format with the candidate.

The scope of the technical interview will be limited exclusively to quantifiable attributes such as technical skills, professional background, years of experience, business understanding level, and English proficiency. Subjective behavioral or conduct-related criteria will be excluded.

At the end of the interview, the system must generate **structured feedback**, offering an objective assessment of the candidate’s match level relative to the Job Description, highlighting strengths, gaps, and the degree of fulfillment of the role’s technical requirements.

The system must provide a smooth and standardized interview experience, fully oriented toward evaluating technical competencies objectively and consistently.

---

# **High-Level Requirements**

## **Users and Roles**

The system must support the following user roles:

* System Administrator  
* Recruiting Analyst  
* Candidate

Each user must have an assigned role and be allowed to perform certain actions accordingly. Access control must follow the principle of least privilege.

---

## **Data Entities**

The system must allow registering and maintaining the following data entities:

* **Interviews.** The attributes and details are defined later.  
* **Recruiting Analysts**, with the following attributes:  
  * First Name (text)  
  * Last Name (text)  
  * Email (email)  
* **Candidates** for interviews, with the following attributes:  
  * First Name (text)  
  * Last Name (text)  
  * Email (email)  
  * ID Document (text)  
* For secondary data entities (e.g., roles, clients, seniorities, etc.), the system will manage a general lookup table. This table must contain:  
  * Domain ID (e.g., 001 for roles, 002 for clients, etc.)  
  * Domain Item ID (e.g., for domain 001 Roles: 001 Data Engineer, 002 Python Developer, etc.)  
  * Text (Description of the domain/domain item, used for display in various forms)

---

## Interview

* The system must allow registering interviews with the following attributes:

  * Recruiting Analyst, automatically associated with the logged-in user  
  * Candidate to be evaluated (selection list)  
  * Role applied for (selection list from lookup table)  
  * Estimated seniority (selection list from lookup table)  
  * Candidate’s CV (file upload)  
  * Job Description document from the client (file upload)  
  * Specific interview guidelines (long text)  
  * Scheduled date and time for the interview (datetime)  
  * Interview status (e.g., 01-Registered, 02-Executed, 03-Not Executed)  
  * Unique interview link to be provided to the candidate

* The candidate will use the unique link to access the interview. This link will only be active on the scheduled date and time, with a tolerance of ± 5 minutes.

* The interview will be conducted by the AI assistant, which uses as input all data associated with the interview, such as:  
  * Job Description  
  * Candidate’s CV  
  * Specific interview guidelines  
  * etc.  
* The interview mechanics will proceed as follows:  
  * The AI agent introduces itself and gives brief instructions to the candidate.  
  * It explains the need the client and role are seeking to fulfill.  
  * It asks the candidate to confirm whether they believe they can fulfill the position.  
  * The technical interview begins, based on the technical topics in the Job Description.  
  * After the question round, the agent concludes the interview by thanking the candidate and providing basic next steps, without revealing the results or feedback.  
  * The full interview content will be recorded in the database.  
  * The agent will generate feedback, which will also be stored in the database.  
* The interview feedback provided by the AI agent will consist of three parts:  
  * General comments indicating whether the candidate is a good fit for the position  
  * A general ranking from 1 to 5  
  * A list of each evaluated skill with an assigned ranking from 1 to 5, defined as:  
    * **1** – Cannot perform  
    * **2** – Can perform with supervision  
    * **3** – Can perform with limited supervision  
    * **4** – Can perform with no supervision  
    * **5** – Can teach others  
* The system must provide a form to view interview details, and if the interview has been executed, it must also show the list of candidates interviewed, their interview dates, and the feedback provided by the AI agent.

---

## Forms and Listings

In addition to the CRUD forms for data entities, the system must provide the following listings:

* Interview list with filtering by role and an option to search by client name  
* Candidate list with filtering by role and an option to search by candidate name

# Technical details

## Backend

* Python backend built with FastAPI, SQLAlchemy, and Pydantic.  
* The backend will act as an intermediary between the candidate and the AI Agent, facilitating and orchestrating the interview process.

## Frontend

* Vue 3.0, Vite and Tailwind  
* SPA

## Database

* Sqlite

## Project Structure

```
my_project/  
│  
├── backend/  
│   ├── app/  
│   │   ├── api/  
│   │   │   ├── v1/  
│   │   │   │   ├── routes/  
│   │   │   │   │   ├── users.py  
│   │   │   │   │   ├── auth.py  
│   │   │   │   │   └── interview.py  
│   │   │   │   └── __init__.py  
│   │   │   └── __init__.py  
│   │   ├── core/  
│   │   │   ├── config.py  
│   │   │   ├── security.py  
│   │   │   └── logging_config.py  
│   │   ├── models/  
│   │   │   ├── user.py  
│   │   │   ├── interview.py  
│   │   │   └── base.py  
│   │   ├── schemas/  
│   │   │   ├── user.py  
│   │   │   ├── interview.py  
│   │   │   └── auth.py  
│   │   ├── services/  
│   │   │   ├── user_service.py  
│   │   │   ├── interview_service.py  
│   │   │   └── ai_agent_service.py  
│   │   ├── repositories/  
│   │   │   ├── user_repo.py  
│   │   │   ├── interview_repo.py  
│   │   │   └── base.py  
│   │   ├── db/  
│   │   │   ├── session.py  
│   │   │   └── init_db.py  
│   │   ├── main.py  
│   │   └── __init__.py  
│   ├── tests/  
│   ├── requirements.txt  
│   └── README.md  
│  
└── frontend/  
    ├── src/  
    │   ├── assets/  
    │   ├── components/  
    │   │   ├── InterviewForm.vue  
    │   │   ├── CandidateCard.vue  
    │   │   └── NavigationBar.vue  
    │   ├── views/  
    │   │   ├── HomeView.vue  
    │   │   ├── CandidatesView.vue  
    │   │   └── InterviewView.vue  
    │   ├── router/  
    │   │   └── index.js  
    │   ├── store/  
    │   │   └── interviewStore.js  
    │   ├── utils/  
    │   │   └── api.js   ← Axios config para FastAPI  
    │   ├── App.vue  
    │   └── main.js  
    ├── index.html  
    ├── package.json  
    ├── vite.config.js  
    └── tailwind.config.js
```

