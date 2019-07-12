import state from "./state";

let voices: SpeechSynthesisVoice[] = [];

export function getVoices(): Promise<SpeechSynthesisVoice[]> {
  return new Promise((resolve, reject) => {
    if (voices.length > 0) {
      resolve(voices);
    } else {
      voices = speechSynthesis.getVoices();
      if (voices.length > 0) {
        resolve(voices);
      } else {
        speechSynthesis.onvoiceschanged = () =>
          resolve(speechSynthesis.getVoices());
      }
    }
  });
}

async function speak(text: string) {
  if (state.speech.voice === "silent") {
    return;
  }
  const voices = (await getVoices()).filter(v => v.name === state.speech.voice);
  if (voices.length) {
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voices[0];
    utterance.rate = state.speech.rate;
    utterance.pitch = state.speech.pitch;
    utterance.lang = state.speech.lang;
    speechSynthesis.speak(utterance);
  }
}

export default speak;
