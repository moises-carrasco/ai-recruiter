## Summary
This is just a draft of the expected logic for the chat functionality used to conduct interviews.

## Logic
1. Present UI for interview to the candidate.
2. Load interview data and show it in the UI: candidate name, role, etc 
3. Once the chat UI was loaded the frontend sends an internal (not visible to the candidate) message to interview API. Message type = start_interview

In the Backend service
```
conversation_history_list = get_messages_interview(interview_id)
is_new_conversation = len(conversation_history_list) == 0

if message_type == start_interview and is_new_conversation == True:  
  
    interview_data = get_interview_data(interview_id)
  
    # provide the ai assistant a few instructions
    kickoff_msg = """ Hi Interviewer_Expert you are just about to start a new interview with a candidate. Here is the data:"
    candidate = {interview_data.candidate}
    seniority = {interview_data.seniority}
    role = {interview_data.role}
    Job Description = { interview_data.job_description }
    cv = { interview_data.cv }

    This data is just internal information and it represents the parameter that you will be using to conduct the interview. 
    Please remember to start the interview by saying hello to the candidate and introducing yourself
    """

    store_chat_message(interview_id, kickoff_msg, role='system')

filtered_conversation_history_list = filter_messages_only(conversation_history_list, roles = ['candidate', 'assistant'])
send_to_frontend(filtered_conversation_history_list) # send the whole history (excluding system chats to the frontend)
```

4. During the regular conversation, the candidate sends a message to the assistant through the chat tool by clicking the send button.  Message type = candidate_answer 

In the Backend service:
```
if message_type == candidate_answer

    msg = message from the candidate

    store_chat_message(interview_id, msg, role='candidate')

    # this gets all the messages associated to this interview ordered by date and hour
    conversation_history_list = get_messages_interview(interview_id)

    # convert list of messages to json format that will be provided to ai assistant to keep context
    conversation_payload = format_messages_payload_ai(conversation_history_list)

    ai_assistant_answer = ai_service.send(conversation_payload)

    # save to table
    message_from_ia = extract_response_from_ai_payload(ai_assistant_answer)
    store_chat_message(interview_id, message_from_ia, role='assistant')

    # recover the last message
    last_message_from_assistant = get_last_message_from_assistant(interview_id)

    # in this case only sends the last message to the frontend so it can be appended to the chat area
    send_answer_to_frontend([last_message_from_assistant])
```

## The message payload for the AI assistant
The function format_messages_payload_ai should format all the messages from an interview to json format. 
This payload will be send to an AI assistant. The expected format is like this

```
{
  "assistant": "Interviewer_Expert",
  "messages": [
    {
        role: 'assistant'
        content: 'bla bla'
    },
    {
        role: 'user'
        content: 'bla bla'
    }
    # etc
  ],
  "revision": 3,
  "revisionName": "3"
}
```

- The assistant key contains the assistant’s name, with the fixed value Interviewer_Expert.
- The messages key is a list of message records retrieved from the interview_transcripts table. These messages must be ordered sequentially by the started_at column.
- Each item inside the messages list includes a role key. When the role value from the interview_transcripts table is either candidate or system, it must be mapped to 'user'. The 'assistant' role remains unchanged.


## Function `get_messages_interview`

- The function `get_messages_interview` should return all the messages from the `interview_transcripts` table for the given `interview_id` parameter.
- The messages must be sorted by the `started_at` column in ascending order.

## `ai_service.send`

- We need an AI service layer that can send the payload created by the function `format_messages_payload_ai` to an AI assistant.
- The parameters for sending the message are:
    - Method: `POST`
    - URL: `https://api.openai.com/v1/chat/completions`
    - Header: `Authorization: Bearer <AI_API_KEY>`
    - Header: `Content-Type: application/json`
- This request must be sent **synchronously**.

## The response from the AI assistant

- The response sent by the ai assistant follows this format

```
{
	"progress": 100,
	"providerName": "openai",
	"providerResponse": "{\"created\":1764385050,\"usage\":{\"completion_tokens\":725,\"prompt_tokens\":961,\"total_cost\":0.00033805,\"completion_tokens_details\":{\"reasoning_tokens\":640},\"prompt_tokens_details\":{\"cached_tokens\":0},\"total_tokens\":1686,\"currency\":\"USD\",\"completion_cost\":0.00029,\"prompt_cost\":0.00004805},\"model\":\"gpt-5-nano-2025-08-07\",\"service_tier\":\"default\",\"id\":\"chatcmpl-Ch5RKp0kDbveVNa5US09g0vJOMzQO\",\"choices\":[{\"finish_reason\":\"stop\",\"provider_specific_fields\":{},\"index\":0,\"message\":{\"role\":\"assistant\",\"annotations\":[],\"content\":\"Perfecto Juan. ¿Podrías compartir un ejemplo concreto de un proyecto reciente en el que identificaste un riesgo crítico? Describe (1) cómo lo identificaste, (2) cómo evaluaste su probabilidad e impacto, (3) las acciones de mitigación o contingencia que implementaste y (4) los resultados y lecciones aprendidas.\"}}],\"object\":\"chat.completion\"}",
	"requestId": "649e669c-71af-4947-967c-78216178c5cf",
	"status": "succeeded",
	"success": true,
	"text": "Perfecto Juan. ¿Podrías compartir un ejemplo concreto de un proyecto reciente en el que identificaste un riesgo crítico? Describe (1) cómo lo identificaste, (2) cómo evaluaste su probabilidad e impacto, (3) las acciones de mitigación o contingencia que implementaste y (4) los resultados y lecciones aprendidas."
}
```
- From that response we need to recover the following fields
    - status
    - success
    - text
    - requestID

- If the status is not `succeeded`, then you must send an error message to the frontend.
- If the response is successful, the `text` field contains the data that must be stored in the `interview_transcripts` table with `role = 'assistant'`.

