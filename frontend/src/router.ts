import { createRouter, createWebHistory, RouteRecordRaw } from "vue-router";
import HomeView from "./views/HomeView.vue"

const baseTitle = "App"

const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    component: HomeView,
    meta: {
      title: "Home"
    }
  },
  {
    path: "/http",
    component: () => import("./views/HttpView.vue"),
    meta: {
      title: "Http response"
    }
  },
  {
    path: "/stream",
    component: () => import("./views/StreamingView.vue"),
    meta: {
      title: "Streaming response"
    }
  },
  {
    path: "/template",
    component: () => import("./views/TemplateView.vue"),
    meta: {
      title: "Template"
    }
  },
  {
    path: "/login",
    component: () => import("./views/account/LoginView.vue"),
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
  {
    path: "/account",
    component: () => import("./views/account/CreateAccountView.vue"),
    meta: {
      title: "Create account"
    }
  },
  {
    path: "/activate/:token",
    component: () => import("./views/account/ActivateAccountView.vue"),
    meta: {
      title: "Activate account"
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
