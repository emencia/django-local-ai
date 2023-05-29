import { confirmSuccess, msg } from "./notify";
import router from "./router";
import { api, user } from "./state";

async function logout() {
  confirmSuccess(
    "Confirmation",
    `Disconnect user ${user.name.value}?`,
    async () => {
      const res = await api.get("/api/account/logout");
      if (res.status == 200) {
        user.isLoggedIn.value = false;
        msg.success("Ok", "User disconnected")
        router.push("/")
      } else {
        throw new Error(`Logout error ${res.status} ${res.data}`)
      }
    },
    "logout"
  );
}

export { logout }
