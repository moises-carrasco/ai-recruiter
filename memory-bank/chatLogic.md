## Summary
This is just a draft of the expected logic for the chat functionality used to conduct interviews.

## Logic
1. Present UI for interview to the candidate.
2. Load interview data and show it in the UI: candidate name, role, etc 
3. Once the chat UI was loaded the frontend sends an internal (not visible to the candidate) message to interview API. Message type = start_interview

In the Backend service
```
if message_type == start_interview
  
  interview_data = get_interview_data(interview_id)
  
  msg = """ Hi Interviewer_Expert you are just about to start a new interview with a candidate. Here is the data:"
   candidate = {interview_data.candidate}
   seniority = {interview_data.seniority}
   role = {interview_data.role}
   Job Description = { interview_data.job_description }
   cv = { interview_data.cv }

   This data is just internal information and it represents the parameter that you will be using to conduct the interview. 
   Please remember to start the interview by saying hello to the candidate and introducing yourself
   """

   store_chat_message(interview_id, msg, role='system')

   # this gets all the messages associated to this interview ordered by date and hour
   conversation_payload = get_message_payload_interview(interview_id) 

   ai_assistant_answer = ai_service.send(conversation_payload)

   store_chat_message(interview_id, ai_assistant_answer, role='assistant')

   send_answer_to_frontend
```

4. During the regular conversation, the candidate sends a message to the assistant through the chat tool by clicking the send button.  Message type =candidate_answer 

```
if message_type == candidate_answer

   msg = message from the candidate

   store_chat_message(interview_id, msg, role='candidate')

   # this gets all the messages associated to this interview ordered by date and hour
   conversation_payload = get_message_payload_interview(interview_id)

   ai_assistant_answer = ai_service.send(conversation_payload)

   store_chat_message(interview_id, ai_assistant_answer, role='assistant')

   send_answer_to_frontend
```

## The message payload for the AI assistant
The message payload if the history of the chat for this interview. And it is in json format. This payload will be send to an AI assistant. The expected format is like this

```
{
  "model": "saia:assistant:Interviewer_Expert",
  "messages": [
    {
        role: 'assistant'
        content: 'bla bla'
    },
    {
        role: 'user'
        content: 'bla bla'
    },
    {
        role: 'assistant'
        content: 'bla bla'
    }
    # etc
  ],
  "revision": 3,
  "revisionName": "3"
}
```

The role key could be assistant or user. When the role from the interview_transcript table is either candidate or system then this value should be mapped to 'user'. The 'candidate' value remains the same.
