import { useInstant } from "djangoinstant";
import { Message } from "djangoinstant";
import { reactive, ref } from "vue";

const instant = useInstant();
const stream = ref("");
const lmState = reactive({
  isRunning: false,
  isStreaming: false,
})

async function initWs() {
  await instant.init(
    "http://localhost:8000",
    "ws://localhost:8427",
    true)
}

async function connectWs() {
  await instant.onReady;
  console.log("Connecting");
  instant.onMessage((msg: Message) => {
    console.log(msg);
    if (msg.channelName == "$llm") {
      if (msg.msg == "#STARTSTREAM#") {
        lmState.isStreaming = true
      } else if (msg.msg == "#ENDSTREAM#") {
        lmState.isStreaming = false;
        lmState.isRunning = false;
      } else {
        stream.value = stream.value + msg.msg
      }
    }
  });
  await instant.connect();
  console.log("End: connected");
}

export { instant, stream, lmState, initWs, connectWs }