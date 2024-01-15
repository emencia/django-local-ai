<template>
  <sw-header class="z-10 w-full h-16 lg:h-16 primary fixed"
    :class="$router.currentRoute.value.path == '/' ? 'bg-transparent' : 'primary'"
    @togglemenu="isMenuVisible = !isMenuVisible" breakpoint="lg">
    <template #mobile-back>
      <i-ion-arrow-back-outline class="inline-flex ml-2 text-3xl" v-if="!isHome"></i-ion-arrow-back-outline>
    </template>
    <template #mobile-branding>
      <div class="inline-flex flex-row items-center h-full pt-1 ml-2 text-2xl truncate" @click="$router.push('/')">
        <div v-if="isHome" class="flex flex-row items-center h-full">
          <i-fluent-emoji-high-contrast:llama class="mx-3 text-3xl"></i-fluent-emoji-high-contrast:llama>
          <div class="text-2xl txt-lighter">Django Llm</div>
        </div>
        <div v-else v-html="$router.currentRoute.value.meta?.title"></div>
      </div>
    </template>
    <template #branding>
      <div class="flex flex-row items-center h-full cursor-pointer" @click="$router.push('/')">
        <div class="mx-3">
          <i-fluent-emoji-high-contrast:llama class="text-3xl"></i-fluent-emoji-high-contrast:llama>
        </div>
        <div class="text-2xl txt-lighter">Django Local Language Model</div>
      </div>
    </template>
    <template #menu>
      <div class="flex flex-row items-center justify-end w-full h-full space-x-3"
        v-if="!($router.currentRoute.value.path == '/')">
        <div class="pr-5 text-lg cursor-pointer txt-lighter dark:txt-light" @click="user.toggleDarkMode()">
          <i-fa-solid:moon v-if="!user.isDarkMode.value"></i-fa-solid:moon>
          <i-fa-solid:sun v-else></i-fa-solid:sun>
        </div>
      </div>
    </template>
  </sw-header>
  <sw-mobile-menu class="absolute left-0 z-40 top-16" :is-visible="isMenuVisible" breakpoint="lg">
    <div class="flex flex-col p-3 space-y-3 lighter">
      <div>
        <button class="border-none btn" @click="user.toggleDarkMode(); closeMenu()">
          <template v-if="!user.isDarkMode.value">
            <i-fa-solid:moon></i-fa-solid:moon>&nbsp;Dark mode
          </template>
          <template v-else>
            <i-fa-solid:sun></i-fa-solid:sun> Light mode
          </template>
        </button>
      </div>
    </div>
  </sw-mobile-menu>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import { SwHeader, SwMobileMenu } from "@snowind/header";
import router from '@/router';
import { user } from "@/state";

export default defineComponent({
  components: {
    SwHeader,
    SwMobileMenu,
  },
  setup() {
    const isMenuVisible = ref(false);

    const isHome = computed<boolean>(() => router.currentRoute.value.path == "/");

    function closeMenu() {
      isMenuVisible.value = false;
    }

    return {
      isMenuVisible,
      isHome,
      user,
      closeMenu,
    }
  }
})
</script>