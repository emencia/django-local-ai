import { useApi } from "restmix";
import { useScreenSize } from "@snowind/state";
import { User } from "@snowind/state";
import { initNotifyService } from "@/notify";
import { useForms } from "djangoapiforms";

const serverUrl = import.meta.env.DEV ? "http://localhost:8000" : "";

let setStateReady: (value: unknown) => void;
let isStateReady = new Promise((r) => setStateReady = r);

const user = new User();
const api = useApi({
  serverUrl: serverUrl
});
const forms = useForms(api);
const { isMobile, isTablet, isDesktop } = useScreenSize();

async function initState() {
  initNotifyService();
}

async function initUserState() {
  api.setCsrfTokenFromCookie();
  setStateReady(true);
}


export {
  user,
  api,
  forms,
  serverUrl,
  isMobile,
  isTablet,
  isDesktop,
  isStateReady,
  initUserState,
  initState,
}
