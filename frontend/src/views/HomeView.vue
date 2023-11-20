<template>
  <div class="flex justify-center">
    <div class="flex flex-col max-w-[45rem]">
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
      <div class="mt-8 text-justify" v-html="stream">
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, reactive } from 'vue';
import Textarea from 'primevue/textarea';
import { api } from '@/state';
import LoadingSpinner from '@/widgets/LoadingSpinner.vue';


const prompt = ref("<s>[INST] list the planets in the solar system [/INST]");
const result = ref("");
const stream = ref("");
const lmState = reactive({
  isRunning: false,
  isStreaming: false,
})

let i = 0;
const onChunk = (payload: Record<string, any>) => {
  if (i == 0) {
    lmState.isStreaming = true
  }
  if (payload["num"] == 1) {
    lmState.isStreaming = true;
  }
  stream.value += payload
  ++i
};
const abortController = new AbortController();

async function infer() {
  stream.value = "";
  lmState.isRunning = true;
  await api.postSse<Record<string, any>>(
    "/llm/generate/",
    { prompt: prompt.value, params: { max_tokens: 1024 } },
    onChunk,
    abortController,
  )
  lmState.isStreaming = false;
  lmState.isRunning = false;
}

onBeforeMount(() => result.value = "")
</script>