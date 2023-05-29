<template>
  <form-card class="mx-3">
    <div class="hidden text-3xl text-center lg:block">Create an account</div>
    <div class="lg:pt-8">
      <span class="p-float-label">
        <InputText id="name" type="text" v-model="name" />
        <label for="name">Full name</label>
      </span>
      <small v-if="'name' in form.errors" id="name-help" class="p-error" v-html="form.errors.name"></small>
    </div>
    <div>
      <span class="p-float-label">
        <InputText id="email" type="text" v-model="email" />
        <label for="email">Email</label>
      </span>
      <small v-if="'email' in form.errors" id="email-help" class="p-error" v-html="form.errors.email"></small>
    </div>
    <div>
      <span class="p-float-label">
        <Password v-model="password1" />
        <label for="password1">Password</label>
      </span>
      <small v-if="'password1' in form.errors" id="password1-help" class="p-error" v-html="form.errors.password1"></small>
    </div>
    <div>
      <span class="p-float-label">
        <Password v-model="password2" :feedback="false" />
        <label for="password2">Confirm password</label>
      </span>
      <small v-if="'password2' in form.errors" id="password2-help" class="p-error" v-html="form.errors.password2"></small>
    </div>
    <div class="flex flex-col pt-2 text-center">
      <button class="w-full xs:w-96 btn success" @click="post()">Save</button>
      <button class="mt-5 btn txt-light" @click="$router.back()">Cancel</button>
    </div>
  </form-card>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import InputText from 'primevue/inputtext';
import Password from 'primevue/password';
import FormCard from '@/widgets/FormCard.vue';
import { forms } from "@/state";

const emit = defineEmits(["formOk"])

const name = ref("");
const email = ref("");
const password1 = ref("");
const password2 = ref("");

const form = reactive<{ errors: Record<string, string> }>({ errors: {} });

async function post() {
  const payload = {
    name: name.value,
    email: email.value,
    password1: password1.value,
    password2: password2.value,
  }
  const { error, res, errors } = await forms.post("/api/account/register", payload);
  if (!error) {
    emit("formOk");
  } else {
    if (error.type == "validation") {
      form.errors = errors
    } else {
      throw new Error(`Unmanaged error: status code ${res.status}`)
    }
  }
}
</script>