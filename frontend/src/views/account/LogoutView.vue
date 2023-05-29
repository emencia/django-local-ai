<template></template>

<script setup lang="ts">
import router from '@/router';
import { api, user } from '@/state';
import { onBeforeMount } from 'vue';

async function logout() {
  await api.get("/api/account/logout");
  user.isLoggedIn.value = false;
}

onBeforeMount(() => {
  logout().then(() => {
    router.push("/")
  })
})
</script>