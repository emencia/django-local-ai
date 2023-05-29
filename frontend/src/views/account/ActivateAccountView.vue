<template>
  <div class="flex flex-row justify-center mt-5">Account activation</div>
</template>

<script setup lang="ts">
import { onBeforeMount } from 'vue';
import router from "@/router";
import { api, user } from '@/state';
import { msg } from '@/notify';

async function postRegistrationLink(url: string) {
  const res = await api.get(url);
  if (res.ok) {
    user.isLoggedIn.value = true;
    msg.success("Congratulations", "Registration completed. You can now login")
    router.push("/login")
  } else {
    if (res.status == 401) {
      msg.error("Error", "Account activation refused")
    }
    else {
      msg.error("Error", "An error has occured");
      console.log("ERR", JSON.stringify(res))
    }
  }
}

onBeforeMount(() => {
  const params = router.currentRoute.value.params;
  let url = `/api/account/activate/${params.token}`;
  postRegistrationLink(url)
})
</script>