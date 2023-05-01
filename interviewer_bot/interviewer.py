from dotenv import load_dotenv
load_dotenv()

from langchain.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory
from langchain import OpenAI, LLMChain
from langchain.chains import ConversationChain

from interviewer_bot.templates.interviewer import interviewer_prompt
from interviewer_bot.templates.supervisors.job_skills import job_skills_prompt
from interviewer_bot.templates.supervisors.dig_deeper import dig_deeper_prompt
from interviewer_bot.templates.supervisors.rephrase import rephrase_prompt

dig_deeper_memory = ConversationBufferWindowMemory(k=4)
rephrase_memory = ConversationBufferWindowMemory(k=2)
job_skills_memory = ConversationSummaryMemory(llm = OpenAI(model_name='gpt-3.5-turbo'))

memories = [dig_deeper_memory, rephrase_memory, job_skills_memory]

for memory in memories:
    memory.human_prefix = 'interviewer'
    memory.ai_prefix = 'candidate'


interviewer_memory = ConversationBufferWindowMemory(k=4)

job_skills_memory

interviewer_model = 'gpt-4'
supervisor_model = 'gpt-3.5-turbo'



class Interviewer():
    def __init__(self, role, verbose = False):
        
        self.role = role
        self.verbose = verbose
        self.setup_interviewer()

    def setup_interviewer(self):

        interviewer = LLMChain(llm = OpenAI(model_name=interviewer_model),
                                prompt = interviewer_prompt,
                                memory = interviewer_memory,
                                verbose = self.verbose)

        job_skill_supervisor = LLMChain(llm = OpenAI(model_name=supervisor_model),
                                        prompt = job_skills_prompt,
                                        verbose=self.verbose)
        
        rephrase_supervisor = LLMChain(llm = OpenAI(model_name=supervisor_model),
                                        prompt = rephrase_prompt,
                                        verbose=self.verbose)
        
        dig_deeper_supervisor = LLMChain(llm = OpenAI(model_name=supervisor_model),
                                        prompt = dig_deeper_prompt,
                                        verbose=self.verbose)
        
        self.interviewer = interviewer
        self.job_skill_supervisor = job_skill_supervisor
        self.rephrase_supervisor = rephrase_supervisor
        self.dig_deeper_supervisor = dig_deeper_supervisor

        self.last_response = 'hi!'

        self.supervisor_recommendations = {
            'job_skills' : '',
            'rephrase' : '',
            'dig_deeper' : '',
        }

    def process_message(self, message):

        memories = [job_skills_memory, rephrase_memory, dig_deeper_memory]

        for memory in memories:
            memory.save_context({"input":self.last_response}, {"output":message})



        self.supervisor_recommendations['job_skills'] = self.job_skill_supervisor.predict(role = self.role, memory = job_skills_memory.buffer)
        self.supervisor_recommendations['rephrase'] = self.rephrase_supervisor.predict(role = self.role, memory = hack_memory(rephrase_memory))
        self.supervisor_recommendations['dig_deeper'] = self.dig_deeper_supervisor.predict(role = self.role, memory = hack_memory(dig_deeper_memory))

        rephrase_memory.save_context
        response = self.interviewer.predict(
            human_message = message,
            role = self.role,
            job_skills = self.supervisor_recommendations['job_skills'],
            rephrase = self.supervisor_recommendations['rephrase'],
            dig_deeper = self.supervisor_recommendations['dig_deeper'],
        )

        self.last_response = response

        return response
    
def hack_memory(memory):

    return memory.load_memory_variables({})['history']