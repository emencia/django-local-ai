import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue"
import { isStateReady, user } from "./state";

const baseTitle = "Django local AI"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
    //component: () => import("./views/HomeView.vue"),
    meta: {
      title: "Home"
    }
  },
  {
    path: "/demo",
    component: () => import("./views/DemoView.vue"),
    meta: {
      title: "Email commercial"
    }
  },
  {
    path: "/login",
    component: () => import("./views/account/LoginView.vue"),
    name: "login",
    meta: {
      title: "Login"
    }
  },
  {
    path: "/logout",
    component: () => import("./views/account/LogoutView.vue"),
    meta: {
      title: "Logout"
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

router.beforeEach(async (to, from, next) => {
  await isStateReady;
  //sconsole.log("TO", to);
  if (to.name !== 'login' && !user.isLoggedIn.value) {
    next({ name: 'login' })
  }
  else { next() }
})

export default router
