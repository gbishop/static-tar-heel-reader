import state from "./state";
import { getVoices } from "./speech";

function initControl(
  selector: string,
  value: string,
  update: (v: string) => void
) {
  const node: HTMLInputElement = document.querySelector(selector);
  if (node) {
    node.value = value;
    node.addEventListener("change", e => {
      update((e.target as HTMLInputElement).value);
      state.persist();
    });
  }
}

async function populateVoiceList() {
  const voices = await getVoices();
  const voiceSelect = document.querySelector("select[name=voices]");

  for (var i = 0; i < voices.length; i++) {
    var option = document.createElement("option");
    option.textContent = voices[i].name + " (" + voices[i].lang + ")";

    if (voices[i].default) {
      option.textContent += " -- DEFAULT";
    }

    option.setAttribute("value", voices[i].name);
    option.setAttribute("data-lang", voices[i].lang);
    option.setAttribute("data-name", voices[i].name);
    voiceSelect.appendChild(option);
  }
}

window.addEventListener("load", () => {
  /* link the controls to the state */
  initControl("input[name=bpp]", "" + state.booksPerPage, v => {
    const newbpp = parseInt(v);
    state.booksPerPage = newbpp;
  });

  initControl("select[name=page]", state.pageColor, v => (state.pageColor = v));
  initControl("select[name=text]", state.textColor, v => (state.textColor = v));
  initControl(
    "select[name=buttons]",
    state.buttonSize,
    v => (state.buttonSize = v)
  );
  /* setup the voices selector */
  populateVoiceList().then(() =>
    initControl(
      "select[name=voices]",
      state.speech.voice,
      v => (state.speech.voice = v)
    )
  );

  /* go back to where we came from */
  document.querySelector("#close").addEventListener("click", () => {
    const backTo = state.mode == "find" ? "find.html" : "choose.html";
    window.location.href = backTo;
  });
});
