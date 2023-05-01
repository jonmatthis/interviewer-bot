from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

prompt=PromptTemplate(
    template='''
    you are playing the role of an interviewer supervisor for {role}. You are speaking to the interviewer conducting the interview.
    
    you need to ensure that the interview gathers sufficient information about different qualifications and skills needed for {role}

    You can make reccomendations to the interviewer based on your assessment.
    
    ''',
    input_variables=["role"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


template="How would you guide given this memory: {memory}"
human_message_prompt = HumanMessagePromptTemplate.from_template(template)

job_skills_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
