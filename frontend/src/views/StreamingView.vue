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
      <div class="mt-8 text-justify" v-html="stream.replace('\n', '<br />')">
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
const result = ref("");

async function infer() {
  stream.value = "";
  lmState.isRunning = true;
  const res = await api.post<InferResponseContract>("/api/llm/inferstream", { "prompt": prompt.value });
  console.log(res.data);
  result.value = res.data.text;
}

onBeforeMount(() => result.value = "")
</script>