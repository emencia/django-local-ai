import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue"

const baseTitle = "Django local AI"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    //component: HomeView,
    component: () => import("./views/DemoView.vue"),
    meta: {
      title: "Email commercial"
    }
  },
  {
    path: "/demo",
    component: () => import("./views/DemoView.vue"),
    meta: {
      title: "Email commercial"
    }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.afterEach((to, from) => {
  document.title = `${baseTitle} - ${to.meta?.title}`;
});

export default router
