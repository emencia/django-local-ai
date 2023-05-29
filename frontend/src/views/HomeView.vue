<template>
  <div class="flex flex-row justify-center mt-8 space-x-4">
    <button class="btn" @click="$router.push('/http')">Http response</button>
    <button class="btn" @click="$router.push('/stream')">Streaming response</button>
    <button class="btn" @click="$router.push('/template')">Prompt template</button>
  </div>
</template>
