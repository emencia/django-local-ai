<template>
  <div class="flex justify-center">
    <div class="flex flex-col">
      <div class="pt-8">
        <span class="p-float-label">
          <Textarea id="prompt" v-model="prompt" rows="5" cols="60" autoResize />
          <label for="prompt">Prompt</label>
        </span>
      </div>
      <div class="pt-5 text-center">
        <button class="w-full btn secondary" @click="infer()" :disabled="isRunning == true">Submit</button>
      </div>
    </div>
  </div>
  <div class="container pt-10 mx-auto">
    <div v-if="isRunning == true">
      <LoadingSpinner class="pt-8 text-6xl txt-lighter" />
    </div>
    <div v-else class="flex justify-center">
      {{ result }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import Textarea from 'primevue/textarea';
import { api } from '@/state';
import LoadingSpinner from '@/widgets/LoadingSpinner.vue';
import { InferResponseContract } from "@/interfaces";


const prompt = ref();
const isRunning = ref(false);
const result = ref("");

async function infer() {
  isRunning.value = true;
  const res = await api.post<InferResponseContract>("/api/llm/inferhttp", { "prompt": prompt.value });
  isRunning.value = false;
  console.log(res.data);
  result.value = res.data.text;
}

onBeforeMount(() => result.value = "")
</script>