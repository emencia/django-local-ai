from typing import cast
from django.conf import settings
from langchain import LLMChain, PromptTemplate  # type: ignore
from instant.producers import publish
from llama_cpp import CompletionChunk
from apps.llm.llama import load_llama_cpp
from apps.llm.langchain import load_langchain

huey = settings.HUEY


@huey.task()
def infer(prompt: str):
    LLM = load_llama_cpp()
    print("Prompt:")
    print(prompt)
    stream = LLM.create_completion(prompt, max_tokens=1024, stream=True)
    running = True
    i = 0
    while running:
        for output in stream:
            output = cast(CompletionChunk, output)
            if i == 0:
                publish("$llm", "#STARTSTREAM#")
            print(output)
            if output["choices"][0]["finish_reason"] == "stop":
                publish("$llm", "#ENDSTREAM#")
                running = False
            else:
                publish("$llm", output["choices"][0]["text"])
            i += 1
    return


@huey.task()
def infertemplate(question: str, template: str):
    LLM = load_langchain(n_ctx=1024)
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=LLM)
    llm_chain.run(question)
    publish("$llm", "#ENDSTREAM#")
    return
