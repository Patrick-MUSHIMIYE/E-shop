document.addEventListener('DOMContentLoaded', function () {
  var toasts = document.querySelectorAll('.toast');
  toasts.forEach(function (t) {
    setTimeout(function () {
      t.style.transition = 'opacity 0.4s';
      t.style.opacity = '0';
      setTimeout(function () { t.remove(); }, 400);
    }, 3000);
  });
});
