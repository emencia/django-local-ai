<template>
  <div :class="{ dark: user.isDarkMode.value == true }">
    <div class="flex flex-col h-full min-h-screen lightbg">
      <the-header></the-header>
      <div class="flex-grow w-full pb-24">
        <router-view></router-view>
      </div>
    </div>
    <Toast />
    <ConfirmDialog>
      <template #message="slotProps">
        <div class="flex flex-row items-center p-4">
          <div>
            <named-icon :icon="`${slotProps.message.icon}`" class="text-3xl"></named-icon>
          </div>
          <div class="pl-2">{{ slotProps.message.message }}</div>
        </div>
      </template>
    </ConfirmDialog>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted } from 'vue';
import Toast from 'primevue/toast';
import ConfirmDialog from 'primevue/confirmdialog';
import TheHeader from "@/components/TheHeader.vue";
import { initState, initUserState, user } from '@/state';

onBeforeMount(() => initState());
onMounted(() => initUserState());
</script>

<style lang="sass">
.app-form
  & input, .p-dropdown
    @apply w-full xxs:min-w-[22rem] xs:min-w-[24rem]
.p-dialog
  & .p-button.successbtn, .p-button.successbtn:enabled:hover
    @apply success border-none ring-0
  & .p-button.dangerbtn, .p-button.dangerbtn:enabled:hover
    @apply danger border-none ring-0
  & .p-button.warningbtn, .p-button.warningbtn:enabled:hover
    @apply warning border-none ring-0
</style>




