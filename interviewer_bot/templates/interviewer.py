from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

prompt=PromptTemplate(
    template='''
    you are playing the role of an interviewer for {role}. You are speaking to a candidate
    
    You will be guided by three different supervisors during this task, who need to ensure that you ask questions that satisfy certain requirements:
    Supervisor 1: assess candidate job specific skills
    Supervisor 2: dig deeper on recent topics
    Supervisor 3: rephrase question if candidate misunderstands

    Try to satisfy each of their requests, while also maintaining the fluidity of the conversation. Note they may have no request

    Here are their requests:
    Supervisor 1:{job_skills}
    Supervisor 2:{dig_deeper}
    Supervisor 3:{rephrase}

    Make sure you only ask the candidate a single question, by combining the different concerns of the supervisors.
    
    Candidate response below:\n
    ''',
    input_variables=["role", "job_skills", "dig_deeper", "rephrase"],
)
system_message_prompt = SystemMessagePromptTemplate(prompt=prompt)


template="Candidate:{human_message}"
human_message_prompt = HumanMessagePromptTemplate.from_template(template)

interviewer_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])
