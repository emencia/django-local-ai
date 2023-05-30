<template>
  <div class="flex flex-row w-full h-full">
    <div class="flex flex-col w-64 p-5 space-y-3">
      <div class="text-lg">Examples</div>
      <div><button class="text-left btn" @click="loadJsonExample()">Json response</button></div>
      <div><button class="text-left btn" @click="loadBashExample()">One shot Bash</button></div>
      <div><button class="text-left btn" @click="loadSumExample()">Summarize text</button></div>
    </div>
    <div class="flex justify-center w-full p-3">
      <div class="flex flex-col max-w-[45rem]">
        <div class="pt-8">
          <span class="p-float-label">
            <Textarea id="template" v-model="template" rows="5" cols="65" autoResize />
            <label for="template">Template</label>
          </span>
        </div>
        <div class="pt-8">
          <span class="p-float-label">
            <Textarea id="prompt" v-model="prompt" rows="5" cols="65" autoResize />
            <label for="prompt">Prompt</label>
          </span>
        </div>
        <div class="pt-5 text-center">
          <button class="w-full btn secondary" @click="infer()"
            :disabled="lmState.isRunning == true && prompt.length > 0">Submit</button>
        </div>
        <div v-if="lmState.isRunning == true && lmState.isStreaming == false">
          <LoadingSpinner class="pt-16 text-6xl txt-lighter" />
        </div>
        <div class="mt-8 text-justify" v-html="stream.replaceAll('\n', '<br />').replaceAll('\t', '&nbsp;&nbsp;')">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount } from 'vue';
import Textarea from 'primevue/textarea';
import { api } from '@/state';
import { stream, lmState } from "@/ws"
import LoadingSpinner from '@/widgets/LoadingSpinner.vue';
import { InferResponseContract } from "@/interfaces";


const prompt = ref("");
const template = ref("");
const result = ref("");

async function infer() {
  stream.value = "";
  lmState.isRunning = true;
  const res = await api.post<InferResponseContract>("/api/llm/inferlc", {
    "prompt": prompt.value,
    "template": template.value
  });
  console.log(res.data);
  result.value = res.data.text;
}

function loadJsonExample() {
  result.value = "";
  template.value = `### Instruction: {question}
### Assistant: (answer in json only)`
  prompt.value = `List all the planets in the solar system with their diameter in kilometers`
}

function loadBashExample() {
  result.value = "";
  template.value = `### Instruction: If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:

Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"

1. I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory

2. Here is the code:
\`\`\`bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
\`\`\`

Question: {question}

### Assistant: (explain the steps. Answer in markdown)`
  prompt.value = `in the directory mydir replace "foo" by "bar" in all the files and rename them with a new_ prefix`
}

function loadSumExample() {
  result.value = "";
  template.value = `Summarize the major key points of this text in a very concise manner, ignore the details:

"{question}"`
  prompt.value = `In 2017, Google wrote a paper, Attention Is All You Need, that introduced Transformer Networks and kicked off a massive revolution in natural language processing. Overnight, machines could suddenly do tasks like translating between languages nearly as good as (sometimes better than) humans. Transformers are highly parallelizable and introduce a mechanism, called “attention”, for the model to efficiently place emphasis on specific parts of the input. Transformers analyze the entire input all at once, in parallel, choosing which parts are most important and influential. Every output token is influenced by every input token.

Transformers are highly parallelizable, efficient to train, and produce astounding results. A downside to transformers is that they have a fixed input and output size – the context window – and computation increases quadratically with the size of this window (in some cases, memory does as well!)

Transformers are not the end of the road, but the vast majority of recent improvements in natural language processing have involved them. There is still abundant active research on various ways of implementing and applying them, such as Amazon’s AlexaTM 20B which outperforms GPT-3 in a number of tasks and is an order of magnitude smaller in its number of parameters.`
}

onBeforeMount(() => result.value = "")
</script>