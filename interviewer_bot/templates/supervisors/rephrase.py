from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

prompt=PromptTemplate(
    template='''
    you are playing the role of an interviewer supervisor for {role}. You are speaking to the interviewer conducting the interview.
    
    you need to ensure that the interviewer rephrases their question if needed (candidate is misunderstanding)

    You can make reccomendations to the interviewer to do so based on your assessment.
    
    ''',
    input_variables=["role"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


template="How would you guide given this memory: {memory}"
human_message_prompt = HumanMessagePromptTemplate.from_template(template)

rephrase_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
