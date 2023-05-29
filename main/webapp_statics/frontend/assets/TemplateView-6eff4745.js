import{s as m,L as g}from"./LoadingSpinner-0643c70d.js";import{d as b,r as u,o as x,c,a as e,b as d,u as o,g as _,s as p,l as i,e as k,f}from"./index-90d3d32d.js";const T={class:"flex flex-row w-full h-full"},z={class:"flex flex-col w-64 p-5 space-y-3"},A=e("div",{class:"text-lg"},"Examples",-1),V={class:"flex justify-center w-full p-3"},C={class:"flex flex-col max-w-[45rem]"},N={class:"pt-8"},B={class:"p-float-label"},S=e("label",{for:"template"},"Template",-1),j={class:"pt-8"},E={class:"p-float-label"},I=e("label",{for:"prompt"},"Prompt",-1),L={class:"pt-5 text-center"},M=["disabled"],R={key:0},q=["innerHTML"],H=b({__name:"TemplateView",setup($){const s=u(""),n=u(""),l=u("");async function h(){p.value="",i.isRunning=!0;const r=await k.post("/api/llm/inferlc",{prompt:s.value,template:n.value});console.log(r.data),l.value=r.data.text}function v(){l.value="",n.value=`### Instruction: {question}
### Assistant: (answer in json only)`,s.value="List all the planets in the solar system with their diameter in kilometers"}function y(){l.value="",n.value=`### Instruction: If someone asks you to perform a task, your job is to come up with a series of bash commands that will perform the task. There is no need to put "#!/bin/bash" in your answer. Make sure to reason step by step, using this format:

Question: "copy the files in the directory named 'target' into a new directory at the same level as target called 'myNewDirectory'"

I need to take the following actions:
- List all files in the directory
- Create a new directory
- Copy the files from the first directory into the second directory
\`\`\`bash
ls
mkdir myNewDirectory
cp -r target/* myNewDirectory
\`\`\`

Question: {question}

### Assistant: (explain the steps. Answer in markdown)`,s.value='in the directory mydir replace "foo" by "bar" in all the files and rename them with a new_ prefix'}function w(){l.value="",n.value=`Summarize the major key points of this text in a very concise manner, ignore the details:

"{question}"`,s.value=`In 2017, Google wrote a paper, Attention Is All You Need, that introduced Transformer Networks and kicked off a massive revolution in natural language processing. Overnight, machines could suddenly do tasks like translating between languages nearly as good as (sometimes better than) humans. Transformers are highly parallelizable and introduce a mechanism, called “attention”, for the model to efficiently place emphasis on specific parts of the input. Transformers analyze the entire input all at once, in parallel, choosing which parts are most important and influential. Every output token is influenced by every input token.

Transformers are highly parallelizable, efficient to train, and produce astounding results. A downside to transformers is that they have a fixed input and output size – the context window – and computation increases quadratically with the size of this window (in some cases, memory does as well!)

Transformers are not the end of the road, but the vast majority of recent improvements in natural language processing have involved them. There is still abundant active research on various ways of implementing and applying them, such as Amazon’s AlexaTM 20B which outperforms GPT-3 in a number of tasks and is an order of magnitude smaller in its number of parameters.`}return x(()=>l.value=""),(r,t)=>(f(),c("div",T,[e("div",z,[A,e("div",null,[e("button",{class:"text-left btn",onClick:t[0]||(t[0]=a=>v())},"Json response")]),e("div",null,[e("button",{class:"text-left btn",onClick:t[1]||(t[1]=a=>y())},"One shot Bash")]),e("div",null,[e("button",{class:"text-left btn",onClick:t[2]||(t[2]=a=>w())},"Summarize text")])]),e("div",V,[e("div",C,[e("div",N,[e("span",B,[d(o(m),{id:"template",modelValue:n.value,"onUpdate:modelValue":t[3]||(t[3]=a=>n.value=a),rows:"5",cols:"65",autoResize:""},null,8,["modelValue"]),S])]),e("div",j,[e("span",E,[d(o(m),{id:"prompt",modelValue:s.value,"onUpdate:modelValue":t[4]||(t[4]=a=>s.value=a),rows:"5",cols:"65",autoResize:""},null,8,["modelValue"]),I])]),e("div",L,[e("button",{class:"w-full btn secondary",onClick:t[5]||(t[5]=a=>h()),disabled:o(i).isRunning==!0&&s.value.length>0},"Submit",8,M)]),o(i).isRunning==!0&&o(i).isStreaming==!1?(f(),c("div",R,[d(g,{class:"pt-16 text-6xl txt-lighter"})])):_("",!0),e("div",{class:"mt-8 text-justify",innerHTML:o(p).replaceAll(`
`,"<br />").replaceAll("	","  ")},null,8,q)])])]))}});export{H as default};
