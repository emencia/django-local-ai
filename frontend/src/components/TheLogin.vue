<template>
  <table id="form" class="mt-5">
    <tr>
      <td>Username:</td>
      <td><input type="text" v-model="form.username" /></td>
    </tr>
    <tr>
      <td>Password:</td>
      <td><input type="password" v-model="form.password" /></td>
    </tr>
    <tr>
      <td colspan="2" class="mt-3 text-right">
        <button class="btn primary" @click="login()">Login</button>
      </td>
    </tr>
  </table>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { instant } from "@/ws";
import { user } from "@/state";

const emit = defineEmits(["loggedin"]);

const form = reactive({
  username: "",
  password: "",
});

async function login() {
  await instant.login(form.username, form.password);
  user.isLoggedIn.value = true;
  emit("loggedin");
}
</script>
