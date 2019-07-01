import state from "./state";

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

window.addEventListener("load", () => {
  /* link the controls to the state */
  initControl("input[name=bpp]", "" + state.booksPerPage, v => {
    const newbpp = parseInt(v);
    state.page = Math.floor((state.page * state.booksPerPage) / newbpp);
    state.booksPerPage = newbpp;
  });

  initControl("select[name=page]", state.pageColor, v => (state.pageColor = v));
  initControl("select[name=text]", state.textColor, v => (state.textColor = v));
  initControl(
    "select[name=buttons]",
    state.buttonSize,
    v => (state.buttonSize = v)
  );

  /* go back to where we came from */
  document.querySelector("#close").addEventListener("click", () => {
    const backTo = state.mode == "find" ? "find.html" : "choose.html";
    window.location.href = backTo;
  });
});
