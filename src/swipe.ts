/* Implement simple swipe capability for turning pages */

function swipe(callback: (direction: 'left' | 'right') => void): void {
  let start = [0, 0];
  let end = [0, 0];
  document.addEventListener('touchstart', e => {
    start = [e.changedTouches[0].screenX, e.changedTouches[0].screenY];
  });
  document.addEventListener('touchend', e => {
    end = [e.changedTouches[0].screenX, e.changedTouches[0].screenY];
    const dx = end[0] - start[0];
    const dy = end[1] - start[1];
    const ww = window.innerWidth;
    if (Math.abs(dx) > Math.abs(dy) && Math.abs(dx) > 0.1 * ww) {
      callback(dx < 0 ? 'left' : 'right');
    }
  });
}

export default swipe;
