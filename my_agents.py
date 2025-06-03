# this file is for multiple agents

from agents import Agent

def get_agent(model):
    assistant= Agent(
        name="Assistant",
        instructions="You are a helpfull assistant.",
        model=model
    )

    coder= Agent(
        name ="Coder",
        instructions="You are an expert Python programmer.",
        model=model
    )

    teacher= Agent(
        name="Teacher",
        instructions="You explain difficult and complex concept in simple way.",
        model=model
    )

    poet= Agent(
        name="Poet",
        instructions="You create poems amd verses with given words.",
        model=model
    )

    return {
        "assistant":assistant,
        "coder":coder,
        "teacher":teacher,
        "poet":poet
    }
