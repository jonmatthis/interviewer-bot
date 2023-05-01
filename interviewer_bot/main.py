from interviewer_bot.interviewer import Interviewer

interviewer = Interviewer('UI/UX designer', verbose=True)

print(interviewer.last_response)

while True:


    human_input = input("Candidate:")
    response = interviewer.process_message(human_input)

    print(response)