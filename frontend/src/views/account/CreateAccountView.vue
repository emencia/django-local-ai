<template>
  <div v-if="!isLoading" class="mt-3 sm:mt:12">
    <div v-if="activeIndex == 0" class="mt-5 lg:mt-12">
      <registration-form class="app-form" @form-ok="++activeIndex"></registration-form>
    </div>
    <div class="text-center" v-else-if="activeIndex == 1">
      Please check your email and click on the activation link
      to continue the registration process
    </div>
  </div>

</template>

<script setup lang="ts">
import { ref } from 'vue';
import RegistrationForm from '@/components/account/RegistrationForm.vue';

const activeIndex = ref(0);
const isLoading = ref(false);
</script>
